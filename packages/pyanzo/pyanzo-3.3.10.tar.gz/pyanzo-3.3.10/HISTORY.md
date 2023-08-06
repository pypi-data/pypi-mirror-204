# History

## Version 2.0.0

Released November 10, 2020

* Support the anzoclient get endpoint to get the contents of a named graph with `AnzoClient.get`
* Support CONSTRUCT queries where the GRAPH is not specified
* Add the option to indicate named graphs and data layers to target in AnzoClient.query_journal and AnzoClient.query_graphmart
* Support using a cookie to authenticate
* Update `AnzoClient.execute_semantic_service` to take a QuadStore as input. It previously look a list of dictionaries in an Anzo-JSON schema.
* Support update queries against the Anzo system journal
* Add utilities to make QuadStore easier to use

# Version 1.0.0

Released September 28, 2020

* Support the anzoclient call endpoint to execute a semantic service with `AnzoClient.execute_semantic_service`
* Support querying a graphmart
* Support querying the system journal
* Support querying a linked dataset


