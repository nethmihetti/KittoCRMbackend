import base64
from datetime import datetime, date

from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto, primitive_pb2
import binascii
import json

from werkzeug.exceptions import abort

agent_role = "agent"


def get_full_acc(name, domain):
    return name + "@" + domain


def is_expired(date_string):
    date_params = date_string.split("-")
    today = datetime.now()
    expiration_date = datetime(day=int(date_params[0]), month=int(date_params[1]), year=int(date_params[2]))
    if expiration_date >= today:
        return False
    else:
        return True


class TransactionBuilder(object):

    def __init__(self, admin_account, admin_private_key, port):
        self.admin_account = admin_account
        self.admin_private_key = admin_private_key
        self.port = port
        self.iroha = Iroha(self.admin_account)
        self.net = IrohaGrpc(self.port)

    def __send_transaction_and_print_status(self, transaction):
        hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
        print('Transaction hash = {}, creator = {}'.format(
            hex_hash, transaction.payload.reduced_payload.creator_account_id))
        self.net.send_tx(transaction)
        for status in self.net.tx_status_stream(transaction):
            print(status)
        for status in self.net.tx_status_stream(transaction):
            if status == ('COMMITTED', 5, 0):
                return "COMMITTED"

    # item is dictionary. item.id; item.item_type; item.item_desc;
    def put_item(self, item, account, company, private_key):
        if not self.is_valid_item(item=item, private_key=private_key):
            return 'Item is already insured', 409
        item["account"] = account
        item["company"] = company
        commands = [
            self.iroha.command(
                'SetAccountDetail',
                account_id=self.admin_account,
                key=item['item_id'],
                value=base64.urlsafe_b64encode(json.dumps(item).encode()).decode()
            ),
        ]
        transaction = self.iroha.transaction(commands)
        IrohaCrypto.sign_transaction(transaction, private_key)
        if self.__send_transaction_and_print_status(transaction) == "COMMITTED":
            return str(item), 201
        else:
            return 'Internal Error', 500

    def create_company_domain(self, company_name):
        commands = [
            self.iroha.command(
                'CreateDomain',
                domain_id=company_name,
                default_role=agent_role
            ),
        ]
        transaction = self.iroha.transaction(commands)
        IrohaCrypto.sign_transaction(transaction, self.admin_private_key)
        if self.__send_transaction_and_print_status(transaction) == "COMMITTED":
            return company_name, 201
        else:
            return 'Internal Error', 500


    def create_agent(self, company_name, agent_name):
        user_private_key = IrohaCrypto.private_key()
        user_public_key = IrohaCrypto.derive_public_key(user_private_key)
        commands = [
            self.iroha.command('CreateAccount', account_name=agent_name, domain_id=company_name,
                               public_key=user_public_key),
            self.iroha.command('GrantPermission', account_id=get_full_acc(agent_name, company_name),
                               permission=primitive_pb2.can_set_my_account_detail),
            self.iroha.command('AddSignatory', account_id=self.admin_account,
                               public_key = user_public_key)

        ]
        transaction = self.iroha.transaction(commands)
        IrohaCrypto.sign_transaction(transaction, self.admin_private_key)
        self.__send_transaction_and_print_status(transaction)
        if self.__send_transaction_and_print_status(transaction) == "COMMITTED":
            return "Your private key: "+str(user_private_key) + " Your public key: " + str(user_public_key), 201
        else:
            return 'Internal Error', 500

    def is_valid_item(self, item, private_key):
        query = self.iroha.query('GetAccountDetail', account_id=self.admin_account, key=item["item_id"])
        IrohaCrypto.sign_query(query, private_key)
        response = self.net.send_query(query)
        if "reason: NO_ACCOUNT_DETAIL" not in str(response.error_response):
            response_json = json.loads(response.account_detail_response.detail)
            data = json.loads(base64.urlsafe_b64decode(response_json["reg@common"][item["item_id"]].encode()).decode())
            date_string = data['insurance_expiration_date']
            if is_expired(date_string):
                return True
            else:
                return False
        else:
            return True
