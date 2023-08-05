# dcTrackClient ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/nicfv/dcTrackClient/python-publish.yml?label=publish&logo=pypi) ![PyPI](https://img.shields.io/pypi/v/dcTrackClient) ![PyPI - Downloads](https://img.shields.io/pypi/dm/dcTrackClient)

Sunbird [dcTrack](https://www.sunbirddcim.com/) API client in Python

## Initialize a connection to the dcTrack API

Import the class:

```py
from dcTrackClient import Client
```

Authenticate using a base URL (the same URL to access the GUI) and a username and password:

```py
api = Client('https://dctrack.example.com/', username='user', password='pass')
```

Authenticate using a base URL and an API token:

```py
api = Client('https://dctrack.example.com/', apiToken='asdf')
```

## Usage Example

### Create an item:

- This example shows the minimum attributes required to create an item
- See [the official documentation](#official-dctrack-documentation) for a comprehensive list of attributes
- This function returns the JSON object for the newly created item
- If it fails, the function will return a JSON object containing the error message

```py
api.createItem({'cmbLocation': 'CRT > 2ND > IT', 'tiName': 'NEW-ITEM', 'cmbMake': 'Generic', 'cmbModel': 'Generic^Rackable^01'})
```

### Retrieve item details:

```py
item = api.getItem(1234)
```

Returns:

```json
{
    "item": {
        ... // item attributes in here
    }
}
```

### Modify an existing item:

```py
api.modifyItem(1234, {'tiSerialNumber': 'SN-12345', 'tiAssetTag': 'DEV-12345'})
```

### Delete an existing item:

```py
api.deleteItem(1234)
```

## Official DcTrack Documentation

Visit this link for the official documentation on request bodies and attrribute names.

https://www.sunbirddcim.com/help/dcTrack/v900/API/en/Default.htm
## Documentation
### class Client:
```py
def __init__(self, baseUrl: str, username: str = '', password: str = '', apiToken: str = ''):
```
> Provide either a username and password, or an API token to access the dcTrack database with Python.
```py
def createItem(self, data: dict, returnDetails: bool = True):
```
> Create a new item.
```py
def modifyItem(self, id: int, data: dict, returnDetails: bool = True):
```
> Update an existing item.
```py
def deleteItem(self, id: int):
```
> Delete an item using the item ID.
```py
def getItem(self, id: int):
```
> Get item details using the item ID.
```py
def quicksearch(self, data: dict, pageNumber: int, pageSize: int):
```
> Search for items using criteria JSON object. Search criteria can be any of the fields applicable to items, including custom fields. Specify the fields to be included in the response. This API supports pagination.
```py
def getCabinetItems(self, cabId: int):
```
> Returns a list of Items contained in a Cabinet using the ItemID of the Cabinet. The returned list includes all of the Cabinet's Items including Passive Items.
```py
def manageItemsBulk(self, cabId: int):
```
> Retrieve a list of Items contained in a Cabinet including Passive Items.
```py
def getAllMakes(self):
```
> Retrieve a list of all Makes.
```py
def addMake(self, data: dict):
```
> Add a new Make.
```py
def modifyMake(self, id: int, data: dict):
```
> Modify a Make.
```py
def deleteMake(self, id: int):
```
> Delete a Make.
```py
def getMakesByName(self, name: str, usingSpecialChars: bool = False):
```
> Search for one or more makes using the make name. You also can search using special characters.
```py
def getModel(self, id: int, usedCounts: bool = False):
```
> Get Model fields for the specified Model ID.
```py
def addModel(self, data: dict, returnDetails: bool = True, proceedOnWarning: bool = False):
```
> Add a new Model.
```py
def modifyModel(self, id: int, data: dict, returnDetails: bool = True, proceedOnWarning: bool = False):
```
> Modify an existing Model.
```py
def deleteModel(self, id: int):
```
> Delete a Model using the Model ID.
```py
def searchModels(self, data: dict, pageNumber: int, pageSize: int):
```
> Search for models by user supplied search criteria.
```py
def getConnector(self, id: int, usedCount: bool = False):
```
> Get a Connector record by ID.
```py
def addConnector(self, data: dict):
```
> Add a new Connector.
```py
def updateConnector(self, id: int, data: dict):
```
> Update an existing Connector.
```py
def deleteConnector(self, ids: list[int]):
```
> Delete one or more Connector records.
```py
def searchConnectors(self, data: dict, pageNumber: int, pageSize: int, usedCount: bool):
```
> Retrieve a List of Connectors.
