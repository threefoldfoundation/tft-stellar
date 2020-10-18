import click
import os
import sys

from jumpscale.loader import j
from jumpscale.core.base import StoredFactory

current_full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_full_path + "/../models/")
from models import UnlockhashTransaction

unlock_transaction_hash_model = StoredFactory(UnlockhashTransaction)
unlock_transaction_hash_model.always_reload = True


@click.command()
@click.option("--destination", default="/unlockhash_transaction_data", help="Destination to import data from")
def import_unlockhash_transaction_data(destination):

    file_content = j.sals.fs.read_file(destination)
    file_content = file_content.replace("'", "")
    unlockhash_transactions_list = j.data.serializers.json.loads(file_content)
    for unlockhash_transaction_data in unlockhash_transactions_list:
        unlockhash = unlockhash_transaction_data.get("unlockhash")
        transaction_xdr = unlockhash_transaction_data.get("transaction_xdr")
        unlockhash_transaction = unlock_transaction_hash_model.new(unlockhash)

        unlockhash_transaction.unlockhash = unlockhash
        unlockhash_transaction.transaction_xdr = transaction_xdr

        unlockhash_transaction.save()


if __name__ == "__main__":
    import_unlockhash_transaction_data()
