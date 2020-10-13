import gevent
from decimal import Decimal

from jumpscale.loader import j
import gevent
import gevent.queue

gevent_queue = None
funding_greenlet = None
WALLET_NAME = "txfundingwallet"
NUMBER_OF_SLAVES = 30

_TFT_ISSUERS = {
    "TEST": "GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3",
    "STD": "GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47",
}


_TFTA_ISSUERS = {
    "TEST": "GB55A4RR4G2MIORJTQA4L6FENZU7K4W7ATGY6YOT2CW47M5SZYGYKSCT",
    "STD": "GBUT4GP5GJ6B3XW5PXENHQA7TXJI5GOPW3NF4W3ZIW6OOO4ISY6WNLN2",
}

_FREETFT_ISSUERS = {
    "TEST": "GBLDUINEFYTF7XEE7YNWA3JQS4K2VD37YU7I2YAE7R5AHZDKQXSS2J6R",
    "STD": "GCBGS5TFE2BPPUVY55ZPEMWWGR6CLQ7T6P46SOFGHXEBJ34MSP6HVEUT",
}

ASSET_ISSUERS = {"TFT": _TFT_ISSUERS, "TFTA": _TFTA_ISSUERS, "FreeTFT": _FREETFT_ISSUERS}


def start_funding_loop():
    global gevent_queue, funding_greenlet
    print("Starting transaction funding service refund loop")
    # create gevent queueu
    gevent_queue = gevent.queue.Queue()
    # start gevent loop at _funding_loop
    funding_greenlet = gevent.spawn(_funding_loop)


def stop_funding_loop(self):
    print("Halting transaction funding service refund loop")
    funding_greenlet.kill()


def set_wallet_name(wallet_name):
    global WALLET_NAME
    WALLET_NAME = wallet_name


def ensure_slavewallets(nr_of_slaves):
    global NUMBER_OF_SLAVES
    NUMBER_OF_SLAVES = nr_of_slaves
    main_wallet = j.clients.stellar.get(WALLET_NAME)
    for slaveindex in range(nr_of_slaves):
        walletname = str(main_wallet.instance_name) + "_" + str(slaveindex)
        if walletname not in j.clients.stellar.list_all():
            print(f"activating slave {walletname}")
            slave_wallet = j.clients.stellar.new(walletname, network=main_wallet.network)
            main_wallet.activate_account(slave_wallet.address, starting_balance="5")


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

