import assets
import random
import copy
from functools import total_ordering
import time


class Player:
    """
    This is a class that represents the witch who the player assumes the role of

    Attributes:
        score (int): the player's score (starts at 0) which increases when they fulfil orders
        location (Location): the player's current location, which they can change by moving
        inventory (Inventory): the player's inventory, which they can fill with items
    """

    def __init__(self, location, inventory):
        """
        The constructor for Player class.

        Parameters:
            location (Location): the player's current location, which they can change by moving
            inventory (Inventory): the player's inventory, which they can fill with items
        """
        self.location = location
        self.inventory = inventory

        # score (int): Player score starts at 0
        self.score = 0

        # completed (list of Item): Record of orders that Player completed during the game
        self.completed = []

    def __str__(self):
        """
        Override the __str__ representation of Player for end game to show the player's name, followed by
        score, followed by their last 10 fulfilled orders.

        Returns:
            A str with the Player's name and their score
        """
        return f"You finished with ${self.score}!"

    def __repr__(self):
        """
        Override the __repr__ representation of Player to point to __str__.

        Returns:
            self.__str__(): The __str__ representation of Player
        """
        return self.__str__()

    def move(self, game, direction):
        """
        Move the player from their current location to a neighboring one.

        Parameters:
            game (Game): the current Game object containing map data
            direction (str): "N", "S", "E", or "W" indicating a direction the Player wants to move
        """
        if direction in self.location.neighbors.keys():
            # index the neighbors dictionary using direction to get the name of the next location
            next_loc = self.location.neighbors[direction]
            # update the player's location with the next Location object from game
            self.location = game.get_location(next_loc)

    def pickup(self, item):
        """
        Add an item to the Player's inventory.

        Parameters:
            item (Item): the Item the Player wants to pick up
        """
        # Make a deepcopy of the item so it isn't removed from it's Location when the player trashes it
        self.inventory.append(copy.deepcopy(item))

    def trash(self, item):
        """
        Remove an item from the Player's inventory.

        Parameters:
            item (Item): the Item the Player wants to pick up
        """
        self.inventory.remove(item)

    @staticmethod
    def mix(recipebook, ingredients):
        """
        Mix together two items to create an entirely new one!

        Parameters:
            recipebook (RecipeBook): a RecipeBook object containing data about item combinations
            ingredients (list of Item): a list of Item objects the player wants to mix

        Returns:
            An Item object if the ingredient combination is valid, None otherwise
        """
        # iterate through all recipes in the RecipeBook for this Game
        for item in recipebook.recipes:
            # if the recipe is None, the item is a Found item and can't be mixed, skip it
            if item.recipe is None:
                continue
            # otherwise sort the ingredient list and the recipe list to see if the items are the same
            elif sorted(ingredients) == sorted(item.recipe):
                return item
        else:
            return None

    def deliver_order(self, game, item, customer):
        """
        Deliver an Item from the Player's inventory to an active customer.

        Parameters:
            game (Game): the current Game object containing map data
            item (Item): the Item object the Player is delivering
            customer (Customer): the Customer object the Player is delivering to
        """
        # remove the Item from the Player's inventory
        self.inventory.remove(item)
        # if the Item matches what the Customer wants
        if item == customer.order:
            # give the Customer's point value to the Player's score
            self.score += customer.give_points()
        # populate a new Customer to replace them
        game.update_customer(customer)


class Customer:
    """
    This is a class that represents a customer who has come to the witch for a request

    Attributes:
        name (str): the Customer's name used to indicate which Customer wants what
        order (Item): the Item the Customer will pay points for
        points (int): the amount of points the Customer will pay for their order
        waittime (float): the maximum amount of time the Customer will wait for their order
        maketime (float): the time the Customer was create to compare against waittime
    """
    def __init__(self, name, order, points, waittime, maketime):
        """
        The constructor for Customer class.

        Parameters:
            name (str): the Customer's name used to indicate which Customer wants what
            order (Item): the Item the Customer will pay points for
            points (int): the amount of points the Customer will pay for their order
            waittime (float): the maximum amount of time the Customer will wait for their order
            maketime (float): the time the Customer was create to compare against waittime
        """
        self.name = name
        self.order = order
        self.points = points
        self.waittime = waittime
        self.maketime = maketime

    def __str__(self):
        """
        Override the __str__ representation of Customer to display their name, order, points, and time remaining.

        Returns:
            A str with the Customer's name, order, points, and time remaining.
        """
        # compute the amount of time remaining in minutes and seconds
        seconds = int(self.time_remaining()) % 60
        minutes = int(self.time_remaining()) // 60
        # pad with spaces between points and time remaining so time remaining is right aligned
        line_length = 52
        customer_str = f"{self.name}: {self.order} ${self.points} (Time Remaining: {minutes}: {seconds:02.0f})"
        # pad the different between the line length and the length of the customer's string representation
        pad = line_length - len(customer_str)
        pad_str = f" " * pad
        return f"{self.name}: {self.order} ${self.points}" + pad_str + f"(Time Remaining: {minutes}: {seconds:02.0f})"

    def __repr__(self):
        """
        Override the __repr__ representation of Customer to point to __str__.

        Returns:
            self.__str__(): The __str__ representation of Customer
        """
        return self.__str__()

    def give_points(self):
        """
        Increase the Player's score by the Customer's points.

        Returns:
            int representing the number of points the Customer's order is worth
        """
        return self.points

    def time_remaining(self):
        """
        Compute the time remaining before the Customer gives up and leaves.

        Returns:
            float representing the difference between time elapsed and maximum time
        """
        return self.waittime - (time.time() - self.maketime)


class Location:
    """
    This is a class that represents a location on the map where the player can visit.

    Attributes:
        name (str): the Location's name
        items (list of Item): the Items that can be found in this Location
        neighbors (dict of str, Location): the amount of points the Customer will pay for their order
    """
    def __init__(self, name):
        """
        The constructor for Location class.

        Parameters:
            name (str): the Location's name
        """
        self.name = name

        # Instantiate items and neighbors as None, these will be populated by Game
        self.items = None
        self.neighbors = None

    def __str__(self):
        """
        Override the __str__ representation of Location to display its name.

        Returns:
            A str with the Location's name
        """
        return self.name

    def __repr__(self):
        """
        Override the __repr__ representation of Location to point to __str__.

        Returns:
            self.__str__(): The __str__ representation of Location
        """
        return self.__str__()

    def spooky(self):
        """
        Select a random flavor text to accompany the Location when a player enters it.

        Returns:
            A str selected from the flavor text asset dict
        """
        return random.choice(assets.LOCATION_FLAVOR[self.name])


class Cauldron(Location):
    """Inherits from Location; represents the witch's home."""
    def __init__(self):
        """The constructor for Cauldron class. Inherits from Location __init__"""
        super().__init__("Cauldron")


class Graveyard(Location):
    """Inherits from Location; represents a graveyard."""
    def __init__(self):
        """The constructor for Graveyard class. Inherits from Location __init__"""
        super().__init__("Graveyard")


class Swamp(Location):
    """Inherits from Location; represents a swamp."""
    def __init__(self):
        """The constructor for Swamp class. Inherits from Location __init__"""
        super().__init__("Swamp")


class Forest(Location):
    """Inherits from Location; represents a forest."""
    def __init__(self):
        """The constructor for Forest class. Inherits from Location __init__"""
        super().__init__("Forest")


class Cave(Location):
    """Inherits from Location; represents a cave."""
    def __init__(self):
        """The constructor for Cave class. Inherits from Location __init__"""
        super().__init__("Cave")


class Town(Location):
    """Inherits from Location; represents the town."""
    def __init__(self):
        """The constructor for Town class. Inherits from Location __init__"""
        super().__init__("Town")


class RecipeBook:
    """
    This is a class that represents the recipe book the witch uses to create items from ingedients.

    Attributes:
        chapters (list of str): a list of str 0 - X indicating chapter numbers
        titles (list of str): a list of str indicating chapter titles
        recipes (dict of Item, list of Item): a dict of Item objects keyed to a list of other Item objects
    """
    def __init__(self, chapters, titles, recipes):
        """
        The constructor for RecipeBook class.

        Parameters:
            chapters (list of str): a list of str 0 - X indicating chapter numbers
            titles (list of str): a list of str indicating chapter titles
            recipes (dict of Item, list of Item): a dict of Item objects keyed to a list of other Item objects
        """
        self.chapters = chapters
        self.titles = titles
        self.recipes = recipes


# use total_ordering so we only have to define __eq__ and __lt__ to get full comparison suite
@total_ordering
class Item:
    """
    This is a class that represents an item in the game.

    Attributes:
        name (str): the Item's name
        recipe (list of Item): a list of Items that serve as the ingredients for this Item
    """
    def __init__(self, name, recipe=None):
        """
        The constructor for Item class.

        Parameters:
            name (str): the Item's name
            recipe (list of Item): a list of Items that serve as the ingredients for this Item, None if this Item
                can only be found in a location
        """
        self.name = name
        self.recipe = recipe

    def __str__(self):
        """
        Override the __str__ representation of Item to display its name.

        Returns:
            A str with the Item's name
        """
        return self.name

    def __repr__(self):
        """
        Override the __repr__ representation of Item to point to __str__.

        Returns:
            self.__str__(): The __str__ representation of Item
        """
        return self.__str__()

    def __eq__(self, other):
        """
        Override the __eq__ comparison of Items to compare name attributes.

        Returns:
            True if the Item names are equal, False otherwise
        """
        return self.name == other.name

    def __lt__(self, other):
        """
        Override the __lt__ comparison of Items to compare name attributes.

        Returns:
            True if this Item name is less than the other (a < b, b < c, etc.), False otherwise
        """
        return self.name < other.name


class Game:
    """
    This is a class that represents the game itself from a high level. Manages all the smaller components.

    Attributes:
        player (Player): the Player object created for this game
        locations (list of Location): the Location objects created for this game
        book (RecipeBook): the RecipeBook object created for this game
        customers (Customer): the initial Customer objects created for this game
    """
    def __init__(self):
        """The constructor for Game class."""
        # instantiate all attributes as None to be replaced with generated objects in later functions
        self.player = None
        self.locations = None
        self.book = None
        self.customers = []

    def setup(self):
        """Generate Game attributes for this game."""
        # randomly assign Items to other Item's recipe lists and create a RecipeBook object
        self.create_book()
        # create a map with all Location objects according to their neighbors and randomly assign found Items
        self.create_map()
        # create a Player
        self.create_player()
        # create 4 Customers with random orders and point values
        self.create_customers(4)

    def create_map(self):
        """Generate the locations attribute of Game using assets.py"""
        # create one of each Location object
        self.locations = [Cauldron(), Swamp(), Forest(), Town(), Cave(), Graveyard()]
        
        # distribute the found Items equally across locations except the Cauldron
        # get all Items in RecipeBook that can only be found and not made
        found_items = [x for x in self.book.recipes if x.recipe is None]
        # compute how many Items per area are required to be distributed evenly
        items_per_loc = len(found_items) // (len(self.locations) - 1)
        # compute how many leftover Items will need to be distributed randomly after reaching items_per_loc
        leftover_items = len(found_items) % (len(self.locations) - 1)

        # iterate through each Location
        for loc in self.locations:
            # get the Location's neighbors from assets.py
            loc.neighbors = assets.MAP_SETUP[loc.name]
            # skip the Cauldron because it doesn't get found Items
            if loc.name == "Cauldron":
                continue
            else:
                # instantiate this Location's items as an empty list
                loc.items = []
                # iterate through a range of the number of Items per Location computed earlier
                for i in range(items_per_loc):
                    # use random.choice to grab a random Item
                    selected_item = random.choice(found_items)
                    # remove that Item from found_items so it won't be duplicated in another Location
                    found_items.remove(selected_item)
                    # append that Item to this Location's items
                    loc.items.append(selected_item)

        # distribute remaining found Items
        # iterate through a range of the number of Items that are leftover computed earlier
        for i in range(leftover_items):
            # use random.choice to grab a random Location
            selected_loc = random.choice(self.locations)
            # ensure the Cauldron can't get Items
            while selected_loc.name == "Cauldron":
                selected_loc = random.choice(self.locations)
            # use random.choice to grab a random Item
            selected_item = random.choice(found_items)
            # append the Item to the selected Location's items
            selected_loc.items.append(selected_item)
            # remove the Item so it won't be duplicated in another Location
            found_items.remove(selected_item)

    def create_player(self):
        """Create a player attribute for this Game"""
        # make a character creation screen that asks for name and other fun bits
        self.player = Player(location=self.get_location("Cauldron"), inventory=[])

    def create_book(self):
        """Create a book attribute for this Game"""
        # get the chapter numbers from assets.py
        chapters = [chapter for chapter in assets.CHAPTER_TITLES]
        # get the chapter titles from assets.py
        titles = [assets.CHAPTER_TITLES[chapter] for chapter in assets.CHAPTER_TITLES]

        # populate the RecipeBook with Items
        # instantiate recipes as an empty list
        recipes = []
        # instantiate used Items as an empty list
        used = []
        # iterate through the ITEMS_BY_INGREDIENTS dict in assets.py
        for level, item in assets.ITEMS_BY_INGREDIENTS.items():
            # FOUND indicates the Item can only be found in a Location and can't be made
            if level == "FOUND":
                [recipes.append(Item(name)) for name in item]
            else:
                # iterate through each Item name in a given level
                for name in item:
                    ingredients = []
                    # randomly select two other Items to list in this Item's recipe
                    for i in range(2):
                        # use random.choice to get a random Item already in recipes
                        # this way we can tier ingredients by adding FOUND first, BASIC next, etc.
                        draw = random.choice(recipes)
                        # ensure there are no duplicate Item's in recipes
                        while draw in used:
                            draw = random.choice(recipes)
                        # append the Item to the ingredients list
                        ingredients.append(draw)
                        # append this Item to used so we can check if it's been used already in the future
                        used.append(draw)
                    # append the Item with it's ingredients to the RecipeBook's recipes
                    recipes.append(Item(name, ingredients))
        # create this Game's RecipeBook
        self.book = RecipeBook(chapters, titles, recipes)

    def create_customers(self, number):
        """
        Create a certain number of starting Customers for this Game.

        Parameters:
            number (int): the number of starting Customers to create
        """
        # iterate through a range of the number of starting Customers
        for i in range(number):
            # set name equal to the current iteration
            name = i
            # grab all possible Items that can be made and not found
            possible_orders = [item for item in self.book.recipes if item.recipe is not None]
            # use random.choice to grab a random order
            order = random.choice(possible_orders)
            # assign points and waittime based on how difficult it is to make the order
            if order.name in assets.ITEMS_BY_INGREDIENTS['BASIC']:
                points = random.randint(5, 10)
                waittime = random.randrange(45, 75, 5)
            elif order.name in assets.ITEMS_BY_INGREDIENTS['INTERMEDIATE']:
                points = random.randint(10, 30)
                waittime = random.randrange(60, 120, 5)
            elif order.name in assets.ITEMS_BY_INGREDIENTS['ADVANCED']:
                points = random.randint(30, 75)
                waittime = random.randrange(120, 180, 10)
            # add this Customer to this Game's customers
            self.customers.append(Customer(name, order, points, waittime, maketime=time.time()))

    def update_customer(self, customer):
        """
        Replace a current Customer with a new one when an order is fulfilled or when they run out of patience.

        Parameters:
            customer (Customer): the Customer object to be replaced
        """
        # set the next Customer's name equal to the current Customer's name
        name = customer.name
        # populate the next Customer's attributes in a similar fashion to create_customers()
        possible_orders = [item for item in self.book.recipes if item.recipe is not None]
        order = random.choice(possible_orders)
        if order.name in assets.ITEMS_BY_INGREDIENTS['BASIC']:
            points = random.randint(5, 10)
            waittime = random.randrange(45, 75, 5)
        elif order.name in assets.ITEMS_BY_INGREDIENTS['INTERMEDIATE']:
            points = random.randint(10, 30)
            waittime = random.randrange(60, 120, 5)
        elif order.name in assets.ITEMS_BY_INGREDIENTS['ADVANCED']:
            points = random.randint(30, 75)
            waittime = random.randrange(120, 180, 10)
        # replace the current Customer with this new one
        self.customers[int(customer.name)] = Customer(name, order, points, waittime, maketime=time.time())

    def get_location(self, next_loc):
        """
        Get a Location object by its name.

        Parameters:
            next_loc (str): the name of the next Location

        Returns:
            A Location object matching the next_loc name
        """
        return [l for l in self.locations if l.name == next_loc].pop()

    def get_item(self, item_name):
        """
        Get a Item object by its name.

        Parameters:
            item_name (str): the name of the Item

        Returns:
            An Item object matching the item_name
        """
        return [i for i in self.book.recipes if i.name == item_name].pop()