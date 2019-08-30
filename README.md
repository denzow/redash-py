# redash-py
![version](https://img.shields.io/pypi/v/redash-py) 

redash python api client


## install

```bash
$ pip install redash-py
```

## usage

### create client instance
set environments `REDASH_API_KEY` and `REDASH_SERVICE_URL` (e.g. `https://redash.your.domain`).

```python

from redash_py.client import RedashAPIClient
# call __init__ without Any arguments, use environments.
client = RedashAPIClient()

```

or Explicitly specify.

```python
from redash_py.client import RedashAPIClient
client = RedashAPIClient(
    api_key='your redash admin api key',
    host='https://redash.your.domain)' 
)
```

### create query

Create new query.

```python
res = client.create_query(
    name='query name',
    data_source_name='data source name',
    query='select * from your_table;',
    description='your query description',
    is_publish=True,  # create and publish or draft
)
```

### update or create query

If the QueryId exists, overwrite it. Create Query if not.

```python

res = client.update_or_create_query(
    query_id=1,
    name='query name',
    data_source_name='data source name',
    query='select * from your_table;',
    description='your query description',
    is_publish=True,  # create and publish or draft
)
```
