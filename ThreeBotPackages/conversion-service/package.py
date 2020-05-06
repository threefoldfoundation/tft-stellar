from Jumpscale import j
import gevent


class Package(j.baseclasses.threebot_package):
    def start(self):

        conversion_wallet_name = self._package.install_kwargs.get("wallet","converter")
        
        self.conversion_wallet= j.clients.stellar.get(conversion_wallet_name)

        DOMAIN = self._package.install_kwargs.get("domain","testnet.threefoldtoken.io")
        for port in (443, 80):
            website = self.openresty.get_from_port(port)
            website.ssl = port == 443
            website.domain = DOMAIN

            locations = website.locations.get(name=f"conversion_service_{port}_locations")

            include_location = locations.get_location_custom(f"conversion_service_includes_{port}")
            include_location.is_auth = False
            include_location.config = f"""
            location /threefoldfoundation/conversion_service {{
                rewrite /threefoldfoundation/conversion_service/(.*)$ /threefoldfoundation/conversion_service/actors/conversion_service/$1;
            }}"""

            locations.configure()
            website.configure()
        self.activation_pool= gevent.pool.Pool(1)
        self.issuing_pool = gevent.pool.Pool(1)

    def _activate_account(self, address):
        self.conversion_wallet.activate_account(address, starting_balance="3.6")
                
    def activate_account(self, address):
        self.activation_pool.apply(self._activate_account, args=(address,))

    def _transfer(
        self,
        destination_address,
        amount,
        asset: str,
        locked_until=None,
        memo_hash=None,
    ):
        issuer_address = asset.split(':')[1]
        return self.conversion_wallet.transfer(destination_address,amount,asset,locked_until, memo_hash=memo_hash,fund_transaction=False,from_address=issuer_address) 

    def transfer(
        self,
        destination_address,
        amount,
        asset: str,
        locked_until=None,
        memo_hash=None,
    ):
        if locked_until:
            return self._transfer_locked_tokens(destination_address,amount,asset,locked_until,memo_hash)
        else:
            return self.issuing_pool.apply(self._transfer, args=(destination_address,amount,asset,locked_until,memo_hash))
    
    def _transfer_locked_tokens(
        self,
        destination_address,
        amount,
        asset: str,
        locked_until=None,
        memo_hash=None,
     ):
        asset_code =asset.split(':')[0] 
        asset_issuer = asset.split(':')[1] 
        import stellar_sdk
        escrow_kp = stellar_sdk.Keypair.random()

        # delegate to the activation pool
        self.activate_account(escrow_kp.public_key)

        # no problem using the conversion wallet, just use it's code
        self.conversion_wallet.add_trustline(asset_code, asset_issuer, escrow_kp.secret)
        preauth_tx = self.conversion_wallet._create_unlock_transaction(escrow_kp, locked_until)
        preauth_tx_hash = preauth_tx.hash()
        unlock_hash = stellar_sdk.strkey.StrKey.encode_pre_auth_tx(preauth_tx_hash)
        self.conversion_wallet._create_unlockhash_transaction(unlock_hash=unlock_hash, transaction_xdr=preauth_tx.to_xdr())
        self.conversion_wallet._set_escrow_account_signers(escrow_kp.public_key, destination_address, preauth_tx_hash, escrow_kp)
        
        # delegate to the issuing pool
        self.transfer(escrow_kp.public_key, amount, asset, memo_hash=memo_hash)

        return preauth_tx.to_xdr()

    def stop(self):
        if self.activation_pool:
            self.activation_pool = None
        
        if self.issuing_pool:
            self.issuing_pool = None