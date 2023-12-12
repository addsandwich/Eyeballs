
import sys

sys.path.insert(1, '../src')
from Eyeballs import Eyeballs

eyeballs_instance = Eyeballs()#'./servers.yaml')

config_data = eyeballs_instance.get_config()  # Get server configurations
local_setup = eyeballs_instance.get_local_setup()  # Get local setup data

print(config_data)
print(local_setup)