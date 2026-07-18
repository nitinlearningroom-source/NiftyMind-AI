from data.security_master import SecurityMasterManager

security = SecurityMasterManager()

df = security.load()

print(df.head())
print(df.columns)