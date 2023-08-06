# PyAnzo

```
*******************************************************************************
 * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
 * All rights reserved.
 * 
 * Contributors:
 *     Cambridge Semantics Incorporated
*******************************************************************************
```

PyAnzo is a python library for interacting with an Anzo server.
PyAnzo faciliates quick iteration and building functionality outside of Anzo as quickly as possible.

The design of this library is centered around an AnzoClient class, with which users can invoke actions on an Anzo server and retrieve information.

For more information, see the documentation.

__Note:__ Developers should also refer to CONTRIBUTING.md.

## Small Examples

### Query a Graphmart

```python
from pyanzo import AnzoClient

# Instantiate the anzo client
anzo_client = AnzoClient(server="10.100.0.26", port="443", username="user", password="password")

query = "SELECT * WHERE { ?s ?p ?o } LIMIT 10",
graphmart = "urn://graphmart_uri"
query_result = anzo_client.query_graphmart(graphmart, query_string=query)

interesting_rows = [r for r in query_result.as_table_results().as_list() if "interesting" in r]
print(interesting_rows)
```

### Query the Anzo Journal

```python
from pyanzo import AnzoClient

anzo_client = AnzoClient(server="10.100.0.26", port="443", username="user", password="password")

jrnl_query = """
PREFIX dc: <http://purl.org/dc/elements/1.1/>
SELECT ?s WHERE {
    ?s dc:title 'Graphmart'
}
LIMIT 10
"""

jrnl_query_result = anzo_client.query_journal(jrnl_query)
print(f"These instances are titled 'Graphmart': {jrnl_query_result.as_table_results().as_list()}")

```

### Query a Linked Dataset

```
from pyanzo import AnzoClient

anzo_client = AnzoClient(server="10.100.0.26", port="443", username="user", password="password")

query = "SELECT * WHERE { ?s ?p ?o } LIMIT 10"
lds_uri = "http://cambridgesemantics.com/LinkedDataset/1234"

lds_query_result = anzo_client.query_lds(lds, query_string=query)
print(lds_query_result.as_table_results())
```

## Setup

```bash
# cd to root of repo

# Install dependencies
pip install -U -r requirements.txt

# Install PyAnzo
pip install -U -e .

# Uninstall
pip uninstall pyanzo
```

Test one of the examples:

```bash
cd examples
python3 query_results_to_pandas.py
```

## Security

By default, PyAnzo uses HTTPS. This means that the anzo client needs to be configured with the HTTPS port, which is typically 443 or 8443 (as opposed to 80 or 8080).

Further, Because Anzo is initially configured with self-signed certs, verification of the host is turned off.
As a result, you'll see a warning printed to the screen: 

```
/Users/anzo/anaconda3/lib/python3.6/site-packages/urllib3/connectionpool.py:847: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
```

This warning is expected and can be suppressed by adding this to your code:

```
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

