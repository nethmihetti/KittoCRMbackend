

from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto
import binascii
import json 

# admin_account = "admin@test"
# admin_private_key = "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70"
# iroha = Iroha(admin_account)
# net = IrohaGrpc('127.0.0.1:8600')

class Transaction(object):
    def __init__(self, admin_account, admin_private_key, port):
        self.admin_account = admin_account
        self.admin_private_key = admin_private_key
        self.port = port
        self.iroha = Iroha(self.admin_account)
        self.net = IrohaGrpc(self.port)

    def send_transaction_and_print_status(self, transaction):
        hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
        print('Transaction hash = {}, creator = {}'.format(
            hex_hash, transaction.payload.reduced_payload.creator_account_id))
        self.net.send_tx(transaction)
        for status in self.net.tx_status_stream(transaction):
            print(status)
    # item is dictionary. item.item_type; item.item_desc
    def put_item(self, item):
        query = self.iroha.query('GetAccountDetail', account_id=self.admin_account)
        IrohaCrypto.sign_query(query, self.admin_private_key)
        response = self.net.send_query(query)
        data = response.account_detail_response
        all_items = {}
        try:
            all_items = json.loads(str(data)[9:-2].replace("\\", ""))[self.admin_account]
        except:
            pass
        if item["item_type"] in all_items.keys():
            return 'Item is already insured', 409
            # abort(409, 'Item is already insured')
        commands = [
            self.iroha.command(
                'SetAccountDetail',
                account_id=self.admin_account, 
                key=item["item_type"], 
                value=item["item_desc"]
            ),
        ]
        transaction = self.iroha.transaction(commands)
        IrohaCrypto.sign_transaction(transaction, self.admin_private_key)
        self.send_transaction_and_print_status(transaction)
        query = self.iroha.query('GetAccountDetail', account_id='admin@test')
        IrohaCrypto.sign_query(query, self.admin_private_key)
        response = self.net.send_query(query)
        data = response.account_detail_response
        result = item["item_type"]+":"+str(json.loads(str(data)[9:-2].replace("\\", ""))[self.admin_account][item["item_type"]])
        return result, 201

    def get_item(self, id):
        pass
