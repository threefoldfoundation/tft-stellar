#!/usr/bin/env python
# pylint: disable=no-value-for-parameter

import click
import time, sys
import requests
from tfchaintypes.transactions.Factory import TransactionFactory
from tfchaintypes.IO import CoinOutput, BlockstakeOutput
from tfchaintypes.PrimitiveTypes import Hash, Currency
from tfchaintypes.ConditionTypes import UnlockHash, UnlockHashType

TFCHAIN_EXPLORER = "https://explorer2.threefoldtoken.com"


def unlockhash_get(tfchainaddress: str):
    response = requests.get(TFCHAIN_EXPLORER + "/explorer/hashes/" + tfchainaddress)
    resp = response.json()
    # parse the transactions
    transactions = []
    for etxn in resp["transactions"]:
        # parse the explorer transaction
        transaction = transaction_from_explorer_transaction(etxn, resp=resp)
        # append the transaction to the list of transactions
        transactions.append(transaction)
    # sort the transactions by height
    transactions.sort(key=(lambda txn: sys.maxsize if txn.height < 0 else txn.height), reverse=True)
    return ExplorerUnlockhashResult(unlockhash=UnlockHash.from_json(tfchainaddress), transactions=transactions)


@click.command(help="Get the balances before conversion")
@click.argument("deauthorizationsfile", default="deauthorizations.txt", type=click.File("r"))
@click.argument("output", default="deauthorizedbalances.txt", type=click.File("w"))
def tfchain_balances(deauthorizationsfile, output):
    counter = 0
    blockchaininfo = blockchain_info_get()
    for deauthorization in deauthorizationsfile.read().splitlines():
        counter += 1
        print(f"{counter}")
        splitdeauthorization = deauthorization.split()
        address = splitdeauthorization[1]
        unlockhash = unlockhash_get(address)
        balance = unlockhash.balance(blockchaininfo)

        unlocked_tokens = balance.available.value
        locked_tokens = balance.locked.value
        output.write(f"{address} Free: {unlocked_tokens} Locked: {locked_tokens}\n")
        time.sleep(2)  # give the explorer a break


class ExplorerBlockchainInfo:
    def __init__(self, blockid, height, timestamp):
        self.blockid = blockid
        self.height = height
        self.timestamp = timestamp

    def __repr__(self):
        return "Block {} at height {}, published on {}, is the last known block.".format(
            self.blockid, self.height, self.timestamp
        )


def blockchain_info_get():
    """
        Get the current blockchain info, using the last known block, as reported by an explorer.
        """
    response = requests.get(TFCHAIN_EXPLORER + "/explorer")
    last_height = response.json()["height"]
    response = requests.get(TFCHAIN_EXPLORER + f"/explorer/blocks/{last_height}")
    last_block = response.json()["block"]
    return ExplorerBlockchainInfo(last_block["blockid"], last_height, last_block["rawblock"]["timestamp"])


def transaction_from_explorer_transaction(etxn, resp=None):  # keyword parameters for error handling purposes only
    if resp is None:
        resp = {}
    # parse the transactions
    transaction = TransactionFactory.from_json(etxn["rawtransaction"], etxn["id"])
    # add the parent (coin) outputs
    coininputoutputs = etxn.get("coininputoutputs", None) or []
    if len(transaction.coin_inputs) != len(coininputoutputs):
        raise Exception(
            "amount of coin inputs and parent outputs are not matching: {} != {}".format(
                len(transaction.coin_inputs), len(coininputoutputs)
            )
        )
    for (idx, co) in enumerate(coininputoutputs):
        co = CoinOutput.from_json(obj=co)
        co.id = transaction.coin_inputs[idx].parentid
        transaction.coin_inputs[idx].parent_output = co
    # add the coin output ids
    coinoutputids = etxn.get("coinoutputids", None) or []
    if len(transaction.coin_outputs) != len(coinoutputids):
        raise Exception(
            "amount of coin outputs and output identifiers are not matching: {} != {}".format(
                len(transaction.coin_outputs), len(coinoutputids)
            )
        )
    for (idx, id) in enumerate(coinoutputids):
        transaction.coin_outputs[idx].id = Hash.from_json(obj=id)
    # add the parent (blockstake) outputs
    blockstakeinputoutputs = etxn.get("blockstakeinputoutputs", None) or []
    if len(transaction.blockstake_inputs) != len(blockstakeinputoutputs):
        raise Exception(
            "amount of blockstake inputs and parent outputs are not matching: {} != {}".format(
                len(transaction.blockstake_inputs), len(blockstakeinputoutputs)
            )
        )
    for (idx, bso) in enumerate(blockstakeinputoutputs):
        bso = BlockstakeOutput.from_json(obj=bso)
        bso.id = transaction.blockstake_inputs[idx].parentid
        transaction.blockstake_inputs[idx].parent_output = bso
    # add the blockstake output ids
    blockstakeoutputids = etxn.get("blockstakeoutputids", None) or []
    if len(transaction.blockstake_outputs) != len(blockstakeoutputids):
        raise Exception(
            "amount of blokstake outputs and output identifiers are not matching: {} != {}".format(
                len(transaction.blockstake_inputs), len(blockstakeoutputids)
            )
        )
    for (idx, id) in enumerate(blockstakeoutputids):
        transaction.blockstake_outputs[idx].id = Hash.from_json(obj=id)
    # set the unconfirmed state
    transaction.unconfirmed = etxn.get("unconfirmed", False)
    # set the height of the transaction only if confirmed
    if not transaction.unconfirmed:
        transaction.height = int(etxn.get("height"))
    # return the transaction
    return transaction


class ExplorerUnlockhashResult:
    def __init__(self, unlockhash, transactions):
        """
        All the info found for a given unlock hash, as reported by an explorer.
        """
        self._unlockhash = unlockhash
        self._transactions = transactions

    @property
    def unlockhash(self):
        """
        Unlock hash looked up.
        """
        return self._unlockhash

    @property
    def transactions(self):
        """
        Transactions linked to the looked up unlockhash.
        """
        return self._transactions

    def __repr__(self):
        return "Found {} transaction(s) for {}".format(len(self._transactions), str(self._unlockhash))

    def balance(self, info=None):
        """
        Compute a balance report for the defined unlockhash,
        based on the transactions of this report.
        """
        if self._unlockhash.type == UnlockHashType.MULTI_SIG:
            balance = WalletBalance()  # ignore for now
        else:
            balance = WalletBalance()
            # collect the balance
            address = str(self.unlockhash)
            for txn in self.transactions:
                for ci in txn.coin_inputs:
                    if str(ci.parent_output.condition.unlockhash) == address:
                        balance.output_add(ci.parent_output, confirmed=(not txn.unconfirmed), spent=True)
                for co in txn.coin_outputs:
                    if str(co.condition.unlockhash) == address:
                        balance.output_add(co, confirmed=(not txn.unconfirmed), spent=False)
        # if chain info is supplied, attach it, if not, get the current chain info for it

        if info is None:
            info = blockchain_info_get()
        balance.chain_height = info.height
        balance.chain_time = info.timestamp
        balance.chain_blockid = info.blockid
        return balance


class WalletBalance(object):
    def __init__(self):
        # personal wallet outputs
        self._outputs = {}
        self._outputs_spent = {}
        self._outputs_unconfirmed = {}
        self._outputs_unconfirmed_spent = {}
        # balance chain context
        self._chain_time = 0
        self._chain_height = 0
        self._chain_blockid = Hash()
        # all wallet addresses tracked in this wallet
        self._addresses = set()

    @property
    def addresses(self):
        """
        All (personal wallet) addresses for which an output is tracked in this Balance.
        """
        return list(self._addresses)

    @property
    def chain_blockid(self):
        """
        Blockchain block ID, as defined by the last known block.
        """
        return self._chain_blockid

    @chain_blockid.setter
    def chain_blockid(self, value):
        """
        Set the blockchain block ID, such that applications that which to cache this
        balance object could ensure that the last block is still the same as the
        last known block known by this balance instance.
        """
        if not value:
            self._chain_blockid = Hash()
            return
        if isinstance(value, Hash):
            self._chain_blockid.value = value.value
        else:
            self._chain_blockid.value = value

    @property
    def chain_time(self):
        """
        Blockchain time, as defined by the last known block.
        """
        return self._chain_time

    @chain_time.setter
    def chain_time(self, value):
        """
        Set the blockchain time, such that the balance object can report
        locked/unlocked outputs correctly for outputs that are locked by time.
        """
        if not isinstance(value, int):
            raise Exception("WalletBalance's chain time cannot be of type {} (expected: int)".format(type(value)))
        self._chain_time = int(value)

    @property
    def chain_height(self):
        """
        Blockchain height, as defined by the last known block.
        """
        return self._chain_height

    @chain_height.setter
    def chain_height(self, value):
        """
        Set the blockchain height, such that the balance object can report
        locked/unlocked outputs correctly for outputs that are locked by height.
        """
        if not isinstance(value, int):
            raise Exception("WalletBalance's chain height cannot be of type {} (expected: int)".format(type(value)))
        self._chain_height = int(value)

    @property
    def active(self):
        """
        Returns if this balance is active,
        meaning it has available outputs to spend (confirmed or not).
        """
        return len(self._outputs) > 0 or len(self._outputs_unconfirmed) > 0

    @property
    def outputs_spent(self):
        """
        Spent (coin) outputs.
        """
        return self._outputs_spent

    @property
    def outputs_unconfirmed(self):
        """
        Unconfirmed (coin) outputs, available for spending or locked.
        """
        return self._outputs_unconfirmed

    @property
    def outputs_unconfirmed_available(self):
        """
        Unconfirmed (coin) outputs, available for spending.
        """
        if self.chain_time > 0 and self.chain_height > 0:
            return [
                co
                for co in self._outputs_unconfirmed.values()
                if not co.condition.lock.locked_check(time=self.chain_time, height=self.chain_height)
            ]
        else:
            return list(self._outputs_unconfirmed.values())

    @property
    def outputs_unconfirmed_spent(self):
        """
        Unconfirmed (coin) outputs that have already been spent.
        """
        return self._outputs_unconfirmed_spent

    @property
    def outputs_available(self):
        """
        Total available (coin) outputs.
        """
        if self.chain_time > 0 and self.chain_height > 0:
            return [
                co
                for co in self._outputs.values()
                if not co.condition.lock.locked_check(time=self.chain_time, height=self.chain_height)
            ]
        else:
            return list(self._outputs.values())

    @property
    def available(self):
        """
        Total available coins.
        """
        return sum([co.value for co in self.outputs_available]) or Currency()

    @property
    def locked(self):
        """
        Total available coins that are locked.
        """
        if self.chain_time > 0 and self.chain_height > 0:
            return (
                sum(
                    [
                        co.value
                        for co in self._outputs.values()
                        if co.condition.lock.locked_check(time=self.chain_time, height=self.chain_height)
                    ]
                )
                or Currency()
            )
        else:
            return Currency(value=0)  # impossible to know for sure without a complete context

    @property
    def unconfirmed(self):
        """
        Total unconfirmed coins, available for spending.
        """
        if self.chain_time > 0 and self.chain_height > 0:
            return (
                sum(
                    [
                        co.value
                        for co in self._outputs_unconfirmed.values()
                        if not co.condition.lock.locked_check(time=self.chain_time, height=self.chain_height)
                    ]
                )
                or Currency()
            )
        else:
            return sum([co.value for co in self._outputs_unconfirmed.values()])

    @property
    def unconfirmed_locked(self):
        """
        Total unconfirmed coins that are locked, and thus not available for spending.
        """
        if self.chain_time > 0 and self.chain_height > 0:
            return (
                sum(
                    [
                        co.value
                        for co in self._outputs_unconfirmed.values()
                        if co.condition.lock.locked_check(time=self.chain_time, height=self.chain_height)
                    ]
                )
                or Currency()
            )
        else:
            return Currency(value=0)  # impossible to know for sure without a complete context

    def output_add(self, output, confirmed=True, spent=False):
        """
        Add an output to the Wallet's balance.
        """
        if confirmed:  # confirmed outputs
            if spent:
                self._outputs_spent[output.id] = output
                # delete from other output lists if prior registered
                self._outputs.pop(output.id, None)
                self._outputs_unconfirmed.pop(output.id, None)
                self._outputs_unconfirmed_spent.pop(output.id, None)
            elif output.id not in self._outputs_spent and output.id not in self._outputs_unconfirmed_spent:
                self._outputs[output.id] = output
                # delete from other output lists if prior registered
                self._outputs_unconfirmed.pop(output.id, None)
        elif output.id not in self._outputs_spent:  # unconfirmed outputs
            if spent:
                self._outputs_unconfirmed_spent[output.id] = output
                # delete from other output lists if prior registered
                self._outputs_unconfirmed.pop(output.id, None)
                self._outputs.pop(output.id, None)
            elif output.id not in self._outputs_unconfirmed_spent:
                self._outputs_unconfirmed[output.id] = output
        self._addresses.add(str(output.condition.unlockhash))

    @property
    def _base(self):
        """
        Private helper utility to return this class as a new and pure WalletBalance object
        """
        b = WalletBalance()
        b._outputs = self._outputs
        b._outputs_spent = self._outputs_spent
        b._outputs_unconfirmed = self._outputs_unconfirmed
        b._outputs_unconfirmed_spent = self._outputs_unconfirmed_spent
        b._chain_blockid = self._chain_blockid
        b._chain_height = self._chain_height
        b._chain_time = self._chain_time
        b._addresses = self._addresses
        return b

    def balance_add(self, other):
        """
        Merge the content of the other balance into this balance.
        If other is None, this call results in a no-op.

        Always assign the result, as it could other than self,
        should the class type be changed in order to add all content correctly.
        """
        if other is None:
            return self
        if not isinstance(other, WalletBalance):
            raise Exception("other balance has to be of type wallet balance")
        # another balance is defined, create a new balance that will contain our merge
        # merge the chain info
        if self.chain_height >= other.chain_height:
            if self.chain_time < other.chain_time:
                raise Exception("chain time and chain height of balances do not match")
        else:
            if self.chain_time >= other.chain_time:
                raise Exception("chain time and chain height of balances do not match")
            self.chain_time = other.chain_time
            self.chain_height = other.chain_height
            self.chain_blockid = other.chain_blockid
        # merge the outputs
        for attr in ["_outputs", "_outputs_spent", "_outputs_unconfirmed", "_outputs_unconfirmed_spent"]:
            d = getattr(self, attr, {})
            for id, output in getattr(other, attr, {}).items():
                d[id] = output
        # merge the addresses
        self._addresses |= other._addresses
        # return the modified self
        return self

    def _human_readable_balance(self):
        # report confirmed coins
        result = "{} available and {} locked".format(
            self.available.str(with_unit=True), self.locked.str(with_unit=True)
        )
        # optionally report unconfirmed coins
        unconfirmed = self.unconfirmed
        unconfirmed_locked = self.unconfirmed_locked
        if unconfirmed > 0 or unconfirmed_locked > 0:
            result += "\nUnconfirmed: {} available {} locked".format(
                unconfirmed.str(with_unit=True), unconfirmed_locked.str(with_unit=True)
            )
        unconfirmed_spent = Currency(value=sum([co.value for co in self._outputs_unconfirmed_spent.values()]))
        if unconfirmed_spent > 0:
            result += "\nUnconfirmed Balance Deduction: -{}".format(unconfirmed_spent.str(with_unit=True))
        # return report
        return result

    def __repr__(self):
        return self._human_readable_balance()


if __name__ == "__main__":
    tfchain_balances()
