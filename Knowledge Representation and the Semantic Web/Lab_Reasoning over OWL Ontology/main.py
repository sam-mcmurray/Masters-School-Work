from owlready2 import *
import owlready2

# JAVA Location
owlready2.JAVA_EXE = "C:\\Program Files\\Java\\jdk-16.0.2\\bin\\java.exe"

# get and loads the ontology from the bacteria.owl ontology provided
onto = get_ontology("bacteria.owl").load()

# ontology classes list
classes = list(onto.classes())

# object properties
object_properties = list(onto.object_properties())

# data properties
data_properties = list(onto.data_properties())

# menu list
menu = ["List classes", "Get subclass(s), superclass(s), instances, and definition by name",
        "Get object properties and data properties", "DL Reasoning", "SWRL Reasoning", "Exit"]


def printMenu():
    """printMenu:
        presents a user-friendly menu to handle the search, and reasoning conducted in the program"""
    print("-" * 50)
    print("Ontology Menu:")
    for i in range(len(menu)):
        print(str(i), ":", menu[i])


def handleMenuSelection(value):
    """handleMenuSelection:
        Handles the users menu selection based on the value selected"""
    if value == "0":
        printClasses()
    elif value == "1":
        run = True
        while run:
            print("Enter the value to view subclass(s), superclass(s), instances, and definition "
                  "(note: the definitions will be empty for primitive concepts)")
            user_in = input(">")
            for i in range(len(classes)):
                two_strings = str(classes[i]).split('.')
                classname = two_strings[1]
                if user_in.lower() == classname.lower():
                    printSuperClasses(classes[i], classname)
                    print("-" * 50)
                    printSubclass(classes[i], classname)
                    print("-" * 50)
                    printInstances(classes[i], classname)
                    run = False
                    break
                elif i == len(classes) - 1:
                    print("Please enter proper name of the class. (example: Bacterium)")

    elif value == "2":
        printObjectProperties()
        print("-" * 50)
        printDataProperties()
    elif value == "3":
        dlReasoner()
    elif value == "4":
        swrlReasoning()
    elif value == "5":
        exit(0)


def printClasses():
    """printClasses:
        prints the classes within the ontology, additionally it removes the bacteria.
         to present in a more user-friendly manner."""
    print("Classes: ")
    for i in range(len(classes)):
        two_strings = str(classes[i]).split('.')
        classname = two_strings[1]
        print(str(i), ":", classname)


def printSubclass(the_class, classname):
    """printSubclass:
        Prints the subclasses from the ontology based on the selected class."""
    subClasses = onto.search(subclass_of=the_class, _case_sensitive=False)
    print("Subclasses:", classname)
    if len(subClasses) > 1:
        for j in range(1, len(subClasses)):
            two_strings = str(subClasses[j]).split('.')
            subclass = two_strings[1]
            print(str(j), ":", subclass)
    else:
        print("None")


def printInstances(the_class, classname):
    """printInstances:
        Prints the Instances from the ontology based on the selected class."""
    subClasses = onto.search(type=the_class, _case_sensitive=False)
    print("Instances:", classname)
    if len(subClasses) > 0:
        for j in range(0, len(subClasses)):
            two_strings = str(subClasses[j]).split('.')
            subclass = two_strings[1]
            print(str(j + 1), ":", subclass)

    else:
        print("None")


def printSuperClasses(the_class, classname):
    """printSuperClasses
        Prints the superclasses or parents of based on the selected class"""
    superClasses = the_class.ancestors()
    print("SuperClasses:", classname)
    # iterates over a list of each of the parents or super classes to print
    if len(superClasses) > 0:
        for j in range(0, len(superClasses)):
            two_strings = str(superClasses.pop()).split('.')
            superClass = two_strings[1]
            if superClass.lower() != classname.lower():
                print(str(j), ":", superClass)
    else:
        print("None")


def printObjectProperties():
    """printObjectProperties:
            Prints the object properties that present within the ontology as well as their domain and range"""
    print("Object Property: domain >> range")
    for i in range(len(object_properties)):
        two_strings = str(object_properties[i]).split('.')
        object_property = two_strings[1]
        domain_strings = str(object_properties[i].domain[0]).split('.')
        domain = domain_strings[1]
        range_strings = str(object_properties[i].range[0]).split('.')
        range_str = range_strings[1]
        print(object_property, ":", domain, ">>", range_str)


def printDataProperties():
    """printDataProperties:
        Prints the data properties that present within the ontology as well as their domain and range"""
    print("Data Property: domain >> range")
    for i in range(len(data_properties)):
        two_strings = str(data_properties[i]).split('.')
        data_property = two_strings[1]
        domain_strings = str(data_properties[i].domain[0]).split('.')
        domain = domain_strings[1]
        range_str = str(data_properties[i].range[0])
        print(data_property, ":", domain, ">>", range_str)


def dlReasoner():
    """dlReasoner:
        Handles the reasoning of the ontology for a check on the on satisfiability as well as
        presents the inference of parents and children of the classes."""
    sync_reasoner(debug=2, infer_property_values=True)
    inconsistent_classes = list(default_world.inconsistent_classes())
    print("Reasoning Results:")
    if len(inconsistent_classes) > 0:
        for i in range(len(inconsistent_classes)):
            print("Unsatisfiable due to inconsistent class:", inconsistent_classes[i])
    else:
        print("Satisfiable")

    print("Class inference check")
    for class_ in classes:
        two_strings = str(class_).split('.')
        classname = two_strings[1]
        print(classname, ":")
        print("inferred parent:", onto.get_parents_of(class_))
        print("inferred children:", onto.get_children_of(class_))


def swrlReasoning():
    """swrlReasoning
        Handles the rule check for the unknown bacterium on the rule for Staphylococcus"""
    with onto:
        print("Rule check for unknown instance of unknown_bacterium:", onto.unknown_bacterium.__class__,
              "for Staphylococcus")
        rules = Imp()
        # Rule body
        rules.set_as_rule("""Bacterium(?b), has_grouping(?b, ?InCluster), has_shape(?b, ?Round), 
        gram_positive(?d, ?True) -> Staphylococcus(?b)""")
        # Run Reasoner to handle the changes
        sync_reasoner()
        print(onto.unknown_bacterium.__class__)


if __name__ == "__main__":
    while True:
        printMenu()
        print("Enter value selection from the menu")
        user_input = input(">")
        handleMenuSelection(user_input)
