def sentenceDeconstruction(sentence: str):
    query_builder = QueryBuilder()
    try:
        subjects = sentence.split(";")
        for i in range(len(subjects)):
            words = subjects[i].split(" ")
            for word in words:
                if word.lower() == "type":
                    query_builder.setType(subjects[i].lower())
                if word.lower() == "ingredients":
                    query_builder.addIngredients(subjects[i].lower())
                if word.lower() == "recipename":
                    query_builder.setRecipeName(subjects[i].lower())
                if word.lower() == "course":
                    query_builder.setCourse(subjects[i].lower())
                if word.lower() == "country":
                    query_builder.setCountry(subjects[i].lower())

        dbPediaQuery = query_builder.createDBPediaQuery()
        wikidataQuery = query_builder.createWikiDataQuery()
        return dbPediaQuery, wikidataQuery
    except Exception as e:
        print(e)
    return "Please enter a valid Question"


class QueryBuilder:
    def __init__(self):
        self.is_type = False
        self.food_type = ""
        self.is_country = False
        self.country = ""
        self.is_course = False
        self.course = ""
        self.ingredients = 0
        self.ingredients_list = []
        self.recipe_name = ""
        self.is_recipe_name = False

    def setType(self, types: str):
        type_array = types.split("type ")[1]
        self.is_type = True
        food_type = str(type_array)
        self.food_type = food_type

    def getIsType(self) -> bool:
        return self.is_type

    def getFoodType(self) -> str:
        return self.food_type

    def setCountry(self, country_str: str):
        self.is_country = True
        country_array = country_str.split("country ")[1]
        country = str(country_array)
        self.country = country

    def getIsCountry(self) -> bool:
        return self.is_country

    def getCountry(self) -> str:
        return self.country

    def setCourse(self, course_str: str):
        self.is_course = True
        course_array = course_str.split("course ")[1]
        course = str(course_array)
        self.course = course

    def getIsCourse(self) -> bool:
        return self.is_course

    def getCourse(self) -> str:
        return self.course

    def addIngredients(self, ingredients_str: str):
        ingredients_array = ingredients_str.split("ingredients ")[1].split(" ")
        self.ingredients = len(ingredients_array)
        ingredients = []
        for i in range(len(ingredients_array)):
            ingredients.append(ingredients_array[i])
        self.ingredients_list = ingredients

    def getIngredientCount(self) -> int:
        return self.ingredients

    def getIngredientList(self) -> list:
        return self.ingredients_list

    def setRecipeName(self, recipe_str: str):
        self.is_recipe_name = True
        recipe_array = recipe_str.split("recipename ")[1]
        recipe_name = str(recipe_array)
        self.recipe_name = recipe_name

    def getIsRecipeName(self) -> bool:
        return self.is_recipe_name

    def getRecipeName(self) -> str:
        return self.recipe_name

    def createDBPediaQuery(self) -> str:
        query = "SELECT DISTINCT ?food, ?recipeName, ?description"
        recipeName = ""
        food_type = ""
        ingredient = ""
        country = ""
        course = ""
        if self.is_recipe_name:
            recipeName = 'FILTER REGEX (?recipeName, "' + self.recipe_name + '", "i").'
        if self.is_type:
            query = query + ", ?type"
            food_type = "?food dbo:type ?typeResource. ?typeResource dbp:name ?type. " + \
                        'FILTER REGEX (?type, "' + self.food_type + '", "i").'
        if self.is_country:
            query = query + ", ?country"
            country = '{?food dbp:country ?countryResource. ?countryResource rdfs:label ?country. ' \
                      'FILTER REGEX(?country, "' + self.country + '", "i" ).} UNION ' \
                                                                  '{?food dbp:country ?country. ' \
                                                                  'FILTER REGEX(?country, "' + self.country + \
                      '", "i" ).} FILTER(LANG(?country)="en").'
        if self.is_course:
            query = query + ", ?course"
            course = "{?food dbp:course ?courseResource. ?courseResource rdfs:label ?course .} UNION " \
                     "{?food dbp:course ?course }. " + 'FILTER REGEX(?course, "' + self.course + '", "i" ). '
        if self.ingredients > 0:
            query = query + ", ?ingredient"
            ingredient = "{?food dbp:mainIngredient ?ingredient. "
            for i in range(self.ingredients):
                ingredient = ingredient + self.ingredientQuery(i)
            ingredient = ingredient + "} UNION {?food dbo:ingredientName ?ingredient. ?ingredientResource rdfs:label " \
                                      "?ingredient. "
            for i in range(self.ingredients):
                ingredient = ingredient + self.ingredientQuery(i)
            ingredient = ingredient + "} UNION {?food dbo:mainIngredient ?ingredient. ?ingredientResource rdfs:label " \
                                      "?ingredient. "
            for i in range(self.ingredients):
                ingredient = ingredient + self.ingredientQuery(i)
            ingredient = ingredient + "}"
        query = query + ' WHERE { ?food a dbo:Food. ?food dbp:name ?recipeName. ?food dbo:abstract ?description. ' \
                        'FILTER(LANG(?description)="en").' + recipeName + food_type + ingredient + country + course + \
                        "} LIMIT 100 "
        print(query)
        return query

    def createWikiDataQuery(self) -> str:
        if not self.is_recipe_name or not self.is_type or not self.is_country:
            query = 'SELECT DISTINCT ?food ?foodLabel ?foodDescription ?countryLabel ?timeLabel ?imageLabel ' \
                    '?inventorLabel ?dishLabel' \
                    ' WHERE {  ' \
                    'SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } { SELECT DISTINCT ?food ' \
                    '?country ?time ?image ?inventor ?dish WHERE { ?food wdt:P527 ?ingredient. ?food wdt:P279 ?dish. ' \
                    '?dish wdt:P31 wd:Q19861951. ?food wdt:P495 ?country. ?food wdt:P18 ?image. ?food wdt:P575 ?time. '
            # ' ?food wdt:P61 ?inventor. '
            recipeName = ""
            food_type = ""
            country = ""
            if self.is_recipe_name:
                recipeName = '?food rdfs:label ?foodLabel. ' \
                             'FILTER REGEX (?foodLabel, "' + self.recipe_name + '", "i"). '
            if self.is_type:
                food_type = "?dish rdfs:label ?dishLabel. " + \
                            'FILTER REGEX (?dishLabel, "' + self.food_type + '", "i"). '
            if self.is_country:
                country = '?country rdfs:label ?countryLabel. ' \
                          'FILTER REGEX(?countryLabel, "' + self.country + '", "i" ). '

            query = query + recipeName + country + food_type + '} LIMIT 100 } }'
            print(query)
        return query

    def ingredientQuery(self, value: int) -> str:
        return 'FILTER REGEX (?ingredient, "' + self.ingredients_list[value] + '", "i").'
