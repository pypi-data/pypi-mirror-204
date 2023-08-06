# Usage

## Connect

```python
from seven2one import *
client = TechStack(host, user, password)

# More parameters
client = TechStack(host, user, password, copyGraphQLString=True)
```

## Logging

By default the Python lib writes logs to console and to the server the use connects to.

Configure log levels and server endpoint by environment variables if needed:

| Variable       | Description | Default |
| -------------- | ----------- | ------- |
|LOGLEVEL        | Set the log level for console output | 'INFO' |
|LOGLEVEL_SERVER | Set the log level for logs sent to the server (Loki). Log levels are 'ERROR', 'WARNING', 'INFO' and 'DEBUG'. | 'ERROR' |
|LOG_TO_SERVER   | Disable logging to Loki server | 'TRUE' |
|LOG_SERVER      | Overwrite the log server endpoint if e.g. running inside the same cluster | 'https://{host}/logging/loki/api/v1/push' |

## Basic read operations

```python
client.inventories()
client.items('appartments', references=True)
client.inventoryProperties('appartments')
client.propertyList('appartments', references=True, dataTypes=True)
```

## Write operations

### Create inventory

```python
properties = [
   {
        'dataType': 'DATE_TIME_OFFSET',
        'name': 'fieldDATETIMEOFFSET',
        'nullable': True
    },
    {
        'dataType': 'BOOLEAN',
        'name': 'fieldBOOLEAN',
        'nullable': True
    }
]

client.createInventory('testInventory', properties)
```

### Add (basic) items

```python
items =  [
        {
        "fieldSTRING": "bla",
        "fieldDECIMAL": 0,
        "fieldLONG": 0,
        "fieldINT": 0,
        "fieldBOOLEAN": True,
        "fieldDATETIME":  "2021-09-14T00:00:00.000Z",
        "fieldDATETIMEOFFSET": "2021-09-14T00:00:00.000Z"
    }
]

addBasicItems('testInventory', items)

```
