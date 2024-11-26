from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint
from string import Template

sparql = SPARQLWrapper("https://dbpedia.org/sparql/")


def queryAthleteName(name):
    query = """
    PREFIX rdf: <http://w3.org/1999/02/22/-rdf-syntax-ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/Athlete/>
    PREFIX rdfs: <http://w3.org/2000/01.rdf-schema#>
    SELECT *
    WHERE
         {
            ?athlete rdfs:label {}@en
         }
    """.format(name)
    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()

    pprint(response)
    # for result in response["results"]["bindings"]:


# def queryAthleteTeam(name):
#     sparql.setQuery("""
#         PREFIX rdf: <http://w3.org/1999/02/22/-rdf-syntax-ns#>
#         PREFIX dbo: <http://dbpedia.org/ontology/SportsClub/>
#         PREFIX rdfs: <http://w3.org/2000/01.rdf-schema#>
#         SELECT *
#         WHERE
#              {
#                 ?club rdfs:label """ + str(name) + str("@en") + """
#              }
#         """)
#
#     sparql.setReturnFormat(JSON)
#     response = sparql.query().convert()
#
#     pprint(response)
#     # for result in response["results"]["bindings"]:


if __name__ == "__main__":
    while True:
        print("0: Search by player")
        print("1: Search by organization")
        print("2: exit")
        user_input = input(">")

        if user_input == "0":
            print("Enter Athletes name")
            user_input = input(">")
            queryAthleteName(user_input)
        elif user_input == "1":
            print("Enter Organization name")
            user_input = input(">")
            queryAthleteTeam(user_input)
        elif user_input == "2":
            exit(0)
