from data.security_master import SecurityMasterManager

security = SecurityMasterManager()

print("RELIANCE:", security.get_security_id("RELIANCE"))
print("TCS:", security.get_security_id("TCS"))
print("INFY:", security.get_security_id("INFY"))
print("SBIN:", security.get_security_id("SBIN"))
from data.security_master import SecurityMasterManager
