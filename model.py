from dataclasses import dataclass

NO_ID = -1


# create a juggler dataclass
@dataclass
class Juggler:
    """ all jugglers have a name, a country of origin, and a
    recorded number of catches. To reduce redunancy in parameter
    passing, create a Juggler class to pass a single Juggler object"""

    name: str
    country: str
    catches: int
    id: int = NO_ID

    def __str__(self):
        return f'ID: {self.id}, Name: {self.name}, Country: {self.country}, Catches: {self.catches}'
