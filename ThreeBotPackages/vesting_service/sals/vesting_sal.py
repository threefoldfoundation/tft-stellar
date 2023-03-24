WALLET = None
UNVESTING_TRANSACTIONS ={}


def set_wallet(wallet):
    global WALLET
    WALLET = wallet


def get_wallet():
    return WALLET


def set_unvesting_transactions(unvesting_transactions):
    global UNVESTING_TRANSACTIONS
    UNVESTING_TRANSACTIONS = unvesting_transactions


def get_unvesting_transactions():
    return UNVESTING_TRANSACTIONS


