# Sanity check script to ensure that the VecSpace client can connect
# and is capable of recieving data.
import vecspace
from vecspace.config import Settings

# run in in-memory mode
vecspace_api = vecspace.Client()
print(vecspace_api.heartbeat())
