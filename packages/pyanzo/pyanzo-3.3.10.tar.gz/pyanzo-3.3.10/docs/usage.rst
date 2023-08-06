=====
Usage
=====

To use PyAnzo in a project::

	from pyanzo import AnzoClient
	
	# Instantiate the anzo client
	anzo_client = AnzoClient(server="10.100.0.26", port="443", username="user", password="password")
	
	# Query a graphmart
	query = "SELECT * WHERE { ?s ?p ?o } LIMIT 10",
	graphmart = "urn://graphmart_uri"
	query_result = anzo_client.query_graphmart(graphmart, query_string=query)
	
	interesting_rows = [r for r in query_result.as_table_results().as_list() if "interesting" in r]
	print(interesting_rows)
	
	# Query the Anzo Journal
	jrnl_query = """
	PREFIX dc: <http://purl.org/dc/elements/1.1/>
	SELECT ?s WHERE {
	    ?s dc:title 'Graphmart'
	}
	LIMIT 10
	"""
	
	jrnl_query_result = anzo_client.query_journal(jrnl_query)
	print(f"These instances are titled 'Graphmart': {jrnl_query_result.as_table_results().as_list()}")
	
	
	# Query a Linked Dataset
	lds_query = "SELECT * WHERE { ?s ?p ?o } LIMIT 10"
	lds_uri = "http://cambridgesemantics.com/LinkedDataset/1234"
	
	lds_query_result = anzo_client.query_lds(lds, query_string=lds_query)
	print(lds_query_result.as_table_results())

