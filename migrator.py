import logging
from timeit import default_timer as timer

from typedb.client import *

from migrators.mitre_attack.mitre_attack_migrator import MitreMigrator
from schema.initialise import initialise_database

# TODO allow setting via CLI run options
uri = "localhost:1729"
database = "cti"
batch_size = 50
num_threads = 16
logging.basicConfig(level=logging.DEBUG)

start = timer()
initialise_database(uri, database, True)  # TODO don't leave on force = True!!
migrator = MitreMigrator(uri, database, batch_size, num_threads, data_path="data/")
migrator.migrate()
migrator.close()
end = timer()
time_in_sec = end - start
print(f"Elapsed time: {time_in_sec} seconds.")

with TypeDB.core_client(uri) as client:
    with client.session(database, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            print("Total concepts: " + str(tx.query().match_aggregate("match $x isa thing; count;").get().as_int()))
