#!!! Hardcode
from src.IrohaHandler.transaction import TransactionBuilder

admin_account = "reg@common"
admin_private_key = "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70"
# !!! change to '127.0.0.1:50051' or your one
iroha_address = '10.90.137.18:50051'

transaction_builder = TransactionBuilder(admin_account, admin_private_key, iroha_address)

