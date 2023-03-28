import { default as StellarSdk, FeeBumpTransaction, Memo, Operation, Transaction, type MemoType } from 'stellar-sdk';
import { Buffer } from 'buffer';

const server = new StellarSdk.Server(window.config.STELLAR_HORIZON_URL);

class Stellar{
  async init(secret: string) {
    const walletKeypair = StellarSdk.Keypair.fromSecret(secret);
    const walletPublicKey = walletKeypair.publicKey();
    await server.loadAccount(walletPublicKey);
    return walletPublicKey;
  }

  async sign(secret: string, content: string) {
    const walletKeypair = StellarSdk.Keypair.fromSecret(secret);
    const signed_content = walletKeypair.sign(content);
    return Buffer.from(signed_content).toString('hex');
  }

  async submitTransaction(transaction: Transaction<Memo<MemoType>, Operation[]> | FeeBumpTransaction){
    return await server.submitTransaction(transaction);
  }
}

export { Stellar as Stellar };
