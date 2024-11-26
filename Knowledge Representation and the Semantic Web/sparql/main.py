from SPARQLWrapper import SPARQLWrapper, JSON


def queryExecutor(query: str):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql/")
    sparql.setQuery(query)
    try:
        sparql.setReturnFormat(JSON)
        ret = sparql.query()
        res = ret.convert()
        return res['results']['bindings']
    except Exception as e:
        print(e)


def printResultsWriters(results):
    for i in range(len(results)):
        print("URL: ", results[i]['writer']['value'])
        print("Name: ", results[i]['name']['value'])
        print("Description: ", results[i]['description']['value'])
        print("Nationality: ", results[i]['nationality']['value'])


def printResultsUniversity(results):
    for i in range(len(results)):
        print("URL: ", results[i]['university']['value'])
        print("Name: ", results[i]['name']['value'])
        print("Description: ", results[i]['description']['value'])
        print("Mascot: ", results[i]['mascot']['value'])
        print("Motto: ", results[i]['motto']['value'])


def findWriterByName(name: str) -> str:
    writer_query = "SELECT DISTINCT ?writer, ?name, ?nationality, ?description " \
                   "WHERE { " \
                   "?writer a dbo:Writer; " \
                   "dbp:name ?name; " \
                   'dbp:nationality ?nationality; ' \
                   'dbo:abstract ?description ' \
                   'FILTER(LANG(?name)="en"). ' \
                   'FILTER(LANG(?description)="en"). ' \
                   'FILTER REGEX(?name, "' + name + '", "i").' \
                                                    '} LIMIT 100'
    return writer_query


def findUniversityByMascot(mascot: str) -> str:
    writer_query = "SELECT DISTINCT ?university, ?name, ?mascot, ?motto, ?description " \
                   "WHERE { " \
                   "?university a dbo:University; " \
                   "dbp:type dbr:Private_university; " \
                   "dbp:name ?name; " \
                   'dbo:mascot ?mascot; ' \
                   'dbo:abstract ?description; ' \
                   'dbo:motto ?motto.' \
                   'FILTER(LANG(?name)="en"). ' \
                   'FILTER(LANG(?description)="en"). ' \
                   'FILTER REGEX(?mascot, "' + mascot + '", "i").' \
                                                        '} LIMIT 100'
    return writer_query


if __name__ == "__main__":
    while True:
        print("0: Search by writer name ")
        print("1: Search for University by Mascot")
        print("2: exit")
        user_input = input(">")
        if user_input == "0":
            print("Find Writer by name")
            user_input = input(">")
            query = findWriterByName(user_input)
            response = queryExecutor(query)
            printResultsWriters(response)
        elif user_input == "1":
            print("Enter Mascot name")
            user_input = input(">")
            query = findUniversityByMascot(user_input)
            response = queryExecutor(query)
            printResultsUniversity(response)
        elif user_input == "2":
            exit(0)
