
from src import app
from Iroha.IrohaHandler import IrohaHandler


irohaHandler = IrohaHandler()

@app.route('/')
def get_item():
    #code =  irohaHandler.get_item(data)
    if code[0] == '0':
        ans = "Good", 201
    else:
        ans = "Bad", 409
    return ans
