from typedb.client import TransactionType

def write_batch(session, batch):
	with session.transaction(TransactionType.WRITE) as tx:
		for query in batch:
			tx.query().insert(query)
		tx.commit()