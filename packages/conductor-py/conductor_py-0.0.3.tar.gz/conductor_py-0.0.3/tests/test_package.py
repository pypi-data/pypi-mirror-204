import os

from dotenv import load_dotenv

import conductor

load_dotenv()
conductor.set_api_key(os.environ["CONDUCTOR__TEST_API_KEY"])
integration_connection_id = os.environ["CONDUCTOR__TEST_CONNECTION_ID"]

invoices = conductor.netsuite.invoice.find_many(integration_connection_id)
print(invoices)
