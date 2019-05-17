# KittoCRMbackend

### Before starting the Iroha container
You should pull fork of Iroha from [github.com/alxndrtarasov/iroha](https://github.com/alxndrtarasov/iroha) to create suitable iroha container with custom genesis block

### Commands to start project on Windows
#### Commands for windows
To create python evironment for project
```python
python -m venv venv
```

To activate venv environment
```
.\venv\Scripts\activate
```

To update pip version
```
python -m pip install --upgrade pip
```

Install Iroha lib from this directory or from pip if exists later version
```
pip install iroha-0.0.4.m-py3-none-any.whl
```

Use genesis.block from IrohaHandler folder as basis block for Iroha

To install dependencies
```
pip install -r requeriments.txt
```

For start application go to directory ./KittoCRMbackend
and run command: 
```
python kittocrmbackend.py
```

After make changes and before commit add all install packages into requirements.txt
```
pip freeze > requeriments.txt
```

For deleting library use:
```
pip unistall <<name_of_library>>
```

For deactivate venv environment

```
deactivate
```

In folder "tests" you can take Postman config to test endpoints
OR
Use iroha_tester.py to write testing scripts

