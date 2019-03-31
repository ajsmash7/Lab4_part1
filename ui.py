from model import Juggler


# validation to ensure a valid menu option was selected
def display_menu_get_choice(menu):
    """ Displays all of the menu options, checks that the user enters a valid choice and returns the choice.
     :param menu: the menu to display
     :returns: the user's choice """
    while True:
        print(menu)
        choice = input('Enter choice? ')
        if menu.is_valid(choice):
            return choice
        else:
            print('Not a valid choice, try again.')


# display all jugglers, or display no jugglers found if list is empty
def show_jugglers(jugglers):

    if jugglers:
        for juggler in jugglers:
            print(juggler)
    else:
        print('No jugglers to display')


# get the info to add a new juggler
def get_info():

    name = input('Enter Juggler Name: ')
    country = input('Enter Juggler Country: ')
    catches = int(input('Enter total number of catches: '))

    return Juggler(name, country, catches)


# Get the name of the juggler
def name_search():

    search = input('Enter the Juggler Name: ')
    return search


# Get the number of catches to update
def get_catches():

    catches = int(input('Enter the new number of catches for this juggler: '))
    return catches

def message(msg):
    print(msg)
