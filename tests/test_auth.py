from brokers.dhanhq.auth import DhanClient

client = DhanClient()

dhan = client.get_client()


print(type(dhan))
print(dhan)