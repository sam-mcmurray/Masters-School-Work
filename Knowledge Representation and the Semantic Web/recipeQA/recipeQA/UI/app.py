from pprint import pprint


class Food:
    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.ingredients = ""
        self.country = ""
        self.course = ""
        self.type = ""
        self.url = url
        self.image = ""
        self.inventor = ""
        self.discovery = ""

    def setCountry(self, country: str):
        self.country = country

    def setImage(self, image: str):
        self.image = image

    def getImage(self) -> str:
        return self.image

    def setInventor(self, inventor: str):
        self.inventor = inventor

    def getInventor(self) -> str:
        return self.inventor

    def setDiscovery(self, discovery: str):
        self.discovery = discovery

    def getDiscovery(self) -> str:
        return self.discovery

    def getCountry(self) -> str:
        return self.country

    def setCourse(self, course: str):
        self.course = course

    def getCourse(self) -> str:
        return self.course

    def setType(self, food_type: str):
        self.type = food_type

    def getType(self) -> str:
        return self.type

    def getDescription(self) -> str:
        return self.description

    def getName(self) -> str:
        return self.name

    def getUrl(self) -> str:
        return self.url

    def getIngredients(self) -> str:
        return self.ingredients

    def setIngredients(self, ingredients: str):
        self.ingredients = ingredients


menu = ["h: Help", "q: Exit"]


def printMenu():
    print("Welcome to RecipeQAS")
    print("*" * 50)
    for i in range(len(menu)):
        print(menu[i])
    print("Ask Question")


def printHelp():
    print("Help:")
    print("> To find a recipe by name")
    print("ex.(recipeName chicken curry;)")
    print("> To find a recipe by type")
    print("ex.(type curry;)")
    print("> To find a recipe by country")
    print("ex.(country indian subcontinent;)")
    print("> To find a recipe by course")
    print("ex.(course main course;)")
    print("> To find a recipe by ingredients")
    print(">ex.(ingredients chicken onions garlic chili peppers;")
    print("> A search can be preformed with any combination of features")
    print("ex.(recipe name chicken curry; type curry;country indian subcontinent;)")
    print("> Please note not every recipe has all information available...")
    print("> The more complex a question the more likely it is to return nothing")


def printFood(food: Food):
    print("Name: ", food.getName())
    descr = "Description: " + food.getDescription()
    pprint(descr)
    print("URL: ", food.getUrl())
    if food.getType() != "":
        print("Type: ", food.getType())
    if food.getIngredients() != "":
        print("Ingredients: ", food.getIngredients())
    if food.getCountry() != "":
        print("Country: ", food.getCountry())
    if food.getCourse() != "":
        print("Course: ", food.getCourse())
    if food.getInventor() != "":
        print("Inventor: ", food.getInventor())
    if food.getDiscovery() != "":
        print("Discovery Year: ", food.getDiscovery())
    if food.getImage() != "":
        print("Image: ", food.getImage())


def setDBPediaResults(results):
    food_list = []
    try:
        for i in range(len(results)):
            food = Food(results[i]['recipeName']['value'], results[i]['description']['value'], results[i]['food']['value'])
            try:
                food.setCountry(results[i]['country']['value'])
            except Exception:
                food.setCountry("")
            try:
                food.setCourse(results[i]['course']['value'])
            except Exception:
                food.setCourse("")
            try:
                food.setType(results[i]['course']['value'])
            except Exception:
                food.setType("")
            try:
                food.setIngredients(results[i]['ingredient']['value'])
            except Exception:
                food.setIngredients("")

            food_list.append(food)
    except Exception as e:
        print(e)

    return food_list


def setWikiDataResults(results):
    food_list = []
    try:
        for i in range(len(results)):
            food = Food(results[i]['foodLabel']['value'], results[i]['foodDescription']['value'],
                        "https://www.wikidata.org/wiki/" + results[i]['food']['value'])
            try:
                food.setCountry(results[i]['countryLabel']['value'])
            except Exception:
                food.setCountry("")
            try:
                food.setImage(results[i]['imageLabel']['value'])
            except Exception:
                food.setImage("")
            try:
                food.setType(results[i]['dishLabel']['value'])
            except Exception:
                food.setType("")
            try:
                food.setDiscovery(results[i]['timeLabel']['value'].split("-")[0])
            except Exception:
                food.setDiscovery("")
            try:
                food.setInventor(results[i]['inventorLabel']['value'])
            except Exception:
                food.setInventor("")

            food_list.append(food)
    except Exception as e:
        print(e)

    return food_list


def combine_data(db_List, wiki_List):
    combine_list = []
    remove_db = []
    remove_wiki = []
    for i in range(len(db_List)):
        item1 = db_List[i]
        for j in range(len(wiki_List)):
            item2 = wiki_List[j]
            if item1.getName().lower() == item2.getName().lower():
                remove_db.append(item1)
                remove_wiki.append(item2)
                food = Food(item1.getName(), item1.getDescription(), item1.getUrl())
                food.setCountry(item1.getCountry() + "/" + item2.getCountry())
                food.setImage(item2.getImage())
                food.setIngredients(item1.getIngredients())
                food.setCourse(item1.getCourse())
                food.setType(item1.getType() + "/" + item2.getType())
                food.setInventor(item2.getInventor())
                food.setDiscovery(item2.getDiscovery())
                combine_list.append(food)
    try:
        for i in remove_db:
            db_List.remove(i)
    except Exception as e:
        print(e)
    try:
        for i in remove_wiki:
            wiki_List.remove(i)
    except Exception as e:
        print(e)
    try:
        for food in db_List:
            combine_list.append(food)
        for food in wiki_List:
            combine_list.append(food)
    except Exception as e:
        print(e)

    return combine_list
