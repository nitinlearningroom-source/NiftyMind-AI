from brokers.dhanhq.auth import DhanClient

client = DhanClient().get_client()

print(client)