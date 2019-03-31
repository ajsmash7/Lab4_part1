# Author: Ashley Johnson
# Program: Simple Sqlite Chainsaw Jugglers Program


''' This main module executes action methods based on
user input.
it imports the database module to send the user interaction
data to the database for CRUD processing.

For user interaction ease, I borrowed Clara's menu module and
modified it to reflect the flow and use of this program. as well
as the ask question and message methods, because they are a brilliant idea
Hope you don't mind. '''


from menu import Menu
from chain_db import Database
import ui


# declare a menu loop terminator
QUIT = 'Q'

# declare an instance of the database to write to
db = Database()


def main():

    menu = create_menu()

    while True:
        choice = ui.display_menu_get_choice(menu)
        action = menu.get_action(choice)
        action()
        if choice == QUIT:
            break

# menu creation to add menu options for user interaction
def create_menu():
    menu = Menu()
    menu.add_option('1', 'Add New Juggler', add_new_juggler)
    menu.add_option('2', 'Show All Jugglers', show_table)
    menu.add_option('3', 'Search by Juggler Name', search_by_name)
    menu.add_option('4', 'Update Catches for Juggler', update_juggler_catches)
    menu.add_option('5', 'Delete a Juggler', delete_by_name)
    menu.add_option(QUIT, 'Quit', quit_program)

    return menu


# add juggler method
# calls the interface to gather the information from the user, and package in a Juggler object
# then passes it to the database to add the new record
def add_new_juggler():
    new_record = ui.get_info()
    db.add_record(new_record)


# calls the database to return all juggler records
# p passes to the interface to display
def show_table():
    display_records = db.get_jugglers()
    ui.show_jugglers(display_records)


# interface requests the name from the user
# passes the name to the database
# passes the matches back to the interface for dislay
def search_by_name():
    search = ui.name_search()
    matches = db.search_records(search)
    ui.show_jugglers(matches)


# gets the Juggler's name from the interface
# gets the number of catches from the interface
# passes to the database for updating
def update_juggler_catches():
    catcher_name = ui.name_search()
    catches = ui.get_catches()
    db.update_catches(catcher_name, catches)


# get juggler name from interface
# passes to the database for deleting
def delete_by_name():
    juggler_name = ui.name_search()
    db.delete_juggler(juggler_name)


def quit_program():
    ui.message('Good bye!')


if __name__ == '__main__':
    main()



