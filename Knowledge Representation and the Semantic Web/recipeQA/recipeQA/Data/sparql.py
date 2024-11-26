from SPARQLWrapper import SPARQLWrapper, JSON


def queryExecutor(query: str):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql/")
    sparql.setQuery(query)
    try:
        sparql.setReturnFormat(JSON)
        ret = sparql.query()
        response = ret.convert()
        print(response)
        return response['results']['bindings']
    except Exception as e:
        print(e)


def wikiQueryExecutor(query: str):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)
    try:
        sparql.setReturnFormat(JSON)
        ret = sparql.query()
        response = ret.convert()
        print(response)
        return response['results']['bindings']
    except Exception as e:
        print(e)
