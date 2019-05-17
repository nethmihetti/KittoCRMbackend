import json
import os
import tempfile

import pytest

from src.IrohaHandler.transaction import TransactionBuilder
import requests
from src.config import transaction_builder

# transaction_builder.create_company_domain('tinkoff')
result, code = transaction_builder.create_agent(company_name="tinkoff", agent_name="nethmi")
print(result, code)


