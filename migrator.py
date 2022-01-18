from migrators.mitre_attack.mitre_attack_migrator import migrate_mitre
from typedb.client import *
from timeit import default_timer as timer
from schema.initialise import initialise_database

uri = "localhost:1729"
batch_size = 50
num_threads = 8

start = timer()
client = TypeDB.core_client(uri)
initialise_database(client, "cti", False)
migrate_mitre(uri, batch_size, num_threads)
end = timer()
time_in_sec = end - start
print(f"Elapsed time: {time_in_sec} seconds.")
