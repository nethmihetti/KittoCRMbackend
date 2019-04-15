
from src import app
from flask import request
from flask import abort
from src.IrohaHandler.transaction import Transaction


@app.route('/iroha_rest/api/v1.0/items', methods=['POST'])
def get_item():
    data = request.get_json()["data"]

    #!!! Hardcode
    admin_account = "admin@test"
    admin_private_key = "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70"
    #!!! change to '127.0.0.1:50051' or your one
    iroha_address = '127.0.0.1:8600'

    transaction = Transaction(admin_account, admin_private_key, iroha_address)
    return transaction.put_item(data)

