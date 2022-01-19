import logging

from migrators.mitre_attack.mitre_attack_migrator import migrate_mitre
from typedb.client import *
from timeit import default_timer as timer
from schema.initialise import initialise_database

# TODO allow setting via CLI run options
uri = "localhost:1729"
database = "cti"
batch_size = 50
num_threads = 8
logging.basicConfig(level=logging.DEBUG)

start = timer()
client = TypeDB.core_client(uri)
initialise_database(client, database, True) # TODO don't leave on force = True!!
migrate_mitre(uri, database, batch_size, num_threads)
end = timer()
time_in_sec = end - start
print(f"Elapsed time: {time_in_sec} seconds.")
