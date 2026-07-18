from dhanhq import DhanContext, dhanhq
from config.settings import CLIENT_ID, ACCESS_TOKEN


class DhanClient:
    def __init__(self):
        context = DhanContext(
            CLIENT_ID,
            ACCESS_TOKEN
        )

        self.client = dhanhq(context)

    def get_client(self):
        return self.client