# Conductor Python Library

## Installation

```sh
pip install --upgrade conductor-py
```

## Usage

```py
import conductor
conductor.set_api_key("sk_test_...")

# Fetch all invoices for the specified NetSuite account, which previously
# connected to our Conductor account.
invoices = conductor.netsuite.invoice.findMany(connection_id="conn_123...")
```
