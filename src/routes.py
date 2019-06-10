import requests
from flask import request
from src import app
from src.config import transaction_builder


@app.route('/requests', methods=['GET'])
def app_requests():
    URL = 'http://34.66.0.246:8080/api/V1/agents/requests?companyId=1&status=ALL'
    r = requests.get(URL)
    print(dir(r))
    return r.text


@app.route('/iroha_rest/api/v1.0/items', methods=['POST'])
def put_item():
    data = request.get_json()["data"]
    item = data["item"]
    company = data["company"].lower()
    account = data["account"].lower()
    private_key = data["private_key"]
    result, code = transaction_builder.put_item(item=item, company=company, account=account, private_key=private_key)
    return result, code


@app.route('/iroha_rest/api/v1.0/items', methods=['PATCH'])
def claim_item():
    data = request.get_json()["data"]
    item = data["item"]
    company = data["company"].lower()
    account = data["account"].lower()
    private_key = data["private_key"]
    result, code = transaction_builder.claim_item(item=item, company=company, account=account, private_key=private_key)
    return result, code


@app.route('/iroha_rest/api/v1.0/items', methods=['GET'])
def validate_item():
    data = request.get_json()["data"]
    item = data["item"]
    private_key = data["private_key"]
    result = transaction_builder.is_insurable_item(item=item, private_key=private_key)
    if result:
        return "Item is valid to be insured", 200
    else:
        return "Item is invalid to be insured", 226


@app.route('/iroha_rest/api/v1.0/companies', methods=['POST'])
def create_company():
    data = request.get_json()["data"]
    company_name = data["company_name"].lower()
    result, code = transaction_builder.create_company_domain(company_name)
    return result, code


@app.route('/iroha_rest/api/v1.0/agents', methods=['POST'])
def create_agent():
    data = request.get_json()["data"]
    company_name = data["company_name"].lower()
    agent_name = data["agent_name"].lower()
    result, code = transaction_builder.create_agent(company_name=company_name, agent_name=agent_name)
    return result, code
