# bigbucket-python

Python3 client for the [Bigbucket](https://github.com/adrianchifor/Bigbucket) database.

## Install

```
pip3 install bigbucket
```

## Usage

```python
import bigbucket

client = bigbucket.Client()

# --------------------------
#        Show tables
# --------------------------
tables = client.get_tables()
print(tables)
# ['table1', 'table2']

# --------------------------
#         Use table
# --------------------------
tbl = client.table("table1")

# --------------------------
#        List columns
# --------------------------
columns = tbl.list_columns()
print(columns)
# ['col1', 'col2', 'col3', 'col4']

# --------------------------
#        Count rows
# --------------------------
rows = tbl.count_rows()
print(rows)
# 10

# --------------------------
#      Read single row
# --------------------------
row = tbl.read_row("key1", columns=["col1", "col2"])
print(row)
# {'col1': 'a value', 'col2': 'another value'}

# --------------------------
#       Read all rows
# --------------------------
rows = tbl.read_rows()
print(rows)
# {
#   'key0': {'col1': '<value>', 'col2': '<value>', 'col3': '<value>', 'col4': '<value>'},
#   'key1': {'col1': '<value>', 'col2': '<value>', 'col3': '<value>', 'col4': '<value>'},
#   ...
# }

# --------------------------
#   Read rows with prefix
# --------------------------
rows = tbl.read_rows("key", columns=["col3"], limit=3)
print(rows)
# {
#   'key0': {'col3': '<value>'},
#   'key1': {'col3': '<value>'},
#   'key2': {'col3': '<value>'}
# }

# --------------------------
#          Set row
# --------------------------
updates = {
    "col1": "new value",
    "col4": "new value"
}
tbl.set_row("key1", updates)

print(tbl.read_row("key1"))
# {'col1': 'new value', 'col2': '..', 'col3': '..', 'col4': 'new value'}

# --------------------------
#     Delete single row
# --------------------------
tbl.delete_row("key1")

# --------------------------
#   Delete rows with prefix
# --------------------------
tbl.delete_rows("key")

# --------------------------
#   Delete column (async)
# --------------------------
tbl.delete_column("col1")

# --------------------------
#   Delete table (async)
# --------------------------
tbl.delete_table()
```

## Client configuration

Defaults

```python
client = bigbucket.Client(address="http://localhost:8080", timeout=30.0, gcp_auth=False)
```

```
address  - The Bigbucket API endpoint
           e.g. port 80      > http://endpoint
                port 443 TLS > https://endpoint
                custom port  > http://endpoint:port

timeout  - Requests timeout (seconds, float)

gcp_auth - If True it generates GCP JWT tokens for address and adds 'Authorization' header to requests.
           Useful when running clients in GCP and need to authenticate against private Cloud Run services.
           (docs -> https://cloud.google.com/run/docs/authenticating/service-to-service)
```

## Exceptions

From `bigbucket.errors` module.

**ConnectionError** - Connection refused to Bigbucket API

**Timeout** - Request to Bigbucket API timed out

**TooManyRedirects** - Request to Bigbucket API was redirected too many times

**NotFound** - Request to Bigbucket API returned 404 HTTP status code

**RequestError** - Generic request error (all inherit from this) or Bigbucket API returned 5xx HTTP status code

## Running Bigbucket

See https://github.com/adrianchifor/Bigbucket#running