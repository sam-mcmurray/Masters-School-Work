from UI import app
from Controller import question_controller
from Data import sparql
from threading import Thread


def search(DB_query, wiki_Query):
    wiki_Results = sparql.wikiQueryExecutor(wiki_Query)
    db_Results = sparql.queryExecutor(DB_query)
    dbPedia_list = app.setDBPediaResults(db_Results)
    wiki_list = app.setWikiDataResults(wiki_Results)
    combined_list = app.combine_data(dbPedia_list, wiki_list)
    for food in combined_list:
        app.printFood(food)


if __name__ == "__main__":

    while True:
        app.printMenu()
        user_input = input(">>")
        if user_input.lower() == "h":
            app.printHelp()
        if user_input.lower() == "q":
            exit(0)
        elif len(user_input) > 2:
            DBquery, wikiQuery = question_controller.sentenceDeconstruction(user_input)
            thread = Thread(target=search, args=(DBquery, wikiQuery))
            thread.start()
            thread.join()

