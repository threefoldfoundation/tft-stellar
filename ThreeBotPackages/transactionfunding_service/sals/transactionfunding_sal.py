import hashlib
import gevent
from decimal import Decimal

from jumpscale.loader import j
import gevent
import gevent.queue
import stellar_sdk

gevent_queue = None
funding_greenlet = None
WALLET_NAME = "txfundingwallet"
NUMBER_OF_SLAVES = 30

ASSET_FEES = {
    "TEST": {
        "TFT:GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3": "0.01",
        "TFTA:GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT": "0.01",
        "BTC:GBMDRYGRFNPCGNRYVTHOPFE7F7L566ZLZM7XFQ2UWWIE3NVSO7FA5MFY": "0.0000001",
    },
    "STD": {
        "TFT:GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2": "0.01",
        "TFTA:GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2": "0.01",
        "BTC:GCNSGHUCG5VMGLT5RIYYZSO7VQULQKAJ62QA33DBC5PPBSO57LFWVV6P": "0.0000001",
    },
}


def start_funding_loop():
    global gevent_queue, funding_greenlet
    print("Starting transaction funding service refund loop")
    # create gevent queueu
    gevent_queue = gevent.queue.Queue()
    # start gevent loop at _funding_loop
    funding_greenlet = gevent.spawn(_funding_loop)


def stop_funding_loop():
    print("Halting transaction funding service refund loop")
    funding_greenlet.kill()


def set_wallet_name(wallet_name):
    global WALLET_NAME
    WALLET_NAME = wallet_name


def generate_next_slave_wallet_secret(previous_secret: str) -> str:
    prev_kp = stellar_sdk.Keypair.from_secret(previous_secret)
    next_raw_secret = hashlib.blake2b(prev_kp.raw_secret_key(), digest_size=32).digest()
    next_kp = stellar_sdk.Keypair.from_raw_ed25519_seed(next_raw_secret)
    return next_kp.secret


def slave_wallet_exists(address: str) -> bool:
    main_wallet = j.clients.stellar.get(WALLET_NAME)
    hs = main_wallet._get_horizon_server()
    endpoint = hs.accounts()
    endpoint.account_id(address)
    try:
        endpoint.call()
    except stellar_sdk.exceptions.NotFoundError:
        return False
    return True


def ensure_slavewallets(nr_of_slaves):
    global NUMBER_OF_SLAVES
    NUMBER_OF_SLAVES = nr_of_slaves
    if WALLET_NAME not in j.clients.stellar.list_all():
        return
    main_wallet = j.clients.stellar.get(WALLET_NAME)
    previous_secret = main_wallet.secret

    for slaveindex in range(nr_of_slaves):
        walletname = str(main_wallet.instance_name) + "_" + str(slaveindex)
        if walletname not in j.clients.stellar.list_all():
            secret = generate_next_slave_wallet_secret(previous_secret)
            previous_secret = secret
            slave_wallet = j.clients.stellar.new(walletname, network=main_wallet.network, secret=secret)
            if slave_wallet_exists(slave_wallet.address):
                print(f"slave {walletname} with address {slave_wallet.address} already exists")
                continue
            print(f"activating slave {walletname} with address {slave_wallet.address}")
            main_wallet.activate_account(slave_wallet.address, starting_balance="5")
        else:
            print(f"slave {walletname} already exists")
            previous_secret = j.clients.stellar.get(walletname).secret


def _funding_loop():
    main_wallet = j.clients.stellar.get(WALLET_NAME)
    for walletname in gevent_queue:
        try:
            wallet = j.clients.stellar.get(walletname)
            balances = wallet.get_balance()
            xlmbalance = [b for b in balances.balances if b.is_native][0]
            xlmbalance = Decimal(xlmbalance.balance)
            # if xlmbalance< 3 add 2 from main fundingwallet
            if xlmbalance < Decimal("3"):
                print(f"Refunding {walletname}")
                main_wallet.transfer(wallet.address, "2", asset="XLM", fund_transaction=False)
        except Exception as e:
            print(f"Exception in transaction funding service loop: {e}")


def fund_if_needed(walletname):
    # add walletname to gevent queue
    gevent_queue.put(walletname)

    return None
