import time

import assets


class Window:
    """
    This is a class that represents a window in the terminal screen that will display game information.

    Attributes:
        MAX_HEIGHT (int): Class attribute, the maximum height of the terminal screen
        MAX_WIDTH (int): Class attribute, the maximum width of the terminal screen
        height (int): height of the Window
        width (int): width of the Window
        y_start (int): starting y-coordinate of the Window
        x_start (int): starting x-coordinate of the Window
        game (Game): Game object containing data to be displayed in the Window
        screen (curses.WindowObject): WindowObject from the curses library containing display functions
    """

    # MAX_HEIGHT and MAX_WIDTH were determined using curses.WindowObject.getmaxyx() of a manually sized terminal
    MAX_HEIGHT = 52
    MAX_WIDTH = 160

    def __init__(self, height, width, y_start, x_start, game, screen):
        """
        The constructor for Window class.

        Parameters:
            height (int): height of the Window
            width (int): width of the Window
            y_start (int): starting y-coordinate of the Window
            x_start (int): starting x-coordinate of the Window
            game (Game): Game object containing data to be displayed in the Window
            screen (curses.WindowObject): WindowObject from the curses library containing display functions
        """
        self.height = height
        self.width = width
        self.y_start = y_start
        self.x_start = x_start
        self.game = game
        self.screen = screen

    def render(self, header, iterable, height, width, y_start, x_start):
        """
        Takes specified Game data and prints it to the window.

        Parameters:
            header (str): a str representing the header for the data to be displayed
            iterable (list of obj): a list of various objects representing data to be displayed
            height (int): the height of the window
            width (int): the width of the window
            y_start (int): starting y-coordinate of the window
            x_start (int): starting x-coordinate of the window
        """
        # grab the data to be displayed
        info = self.get_info(header, iterable)
        # display the data
        self.print_info(info, y_start, x_start)
        # display a border around the window to distinguish it from other windows
        self.print_borders(y_start, height, x_start, width)

    @staticmethod
    def get_info(header, iterable):
        """
        Takes in a header and a list of objects and converts it to a single list of str

        Parameters:
            header (str): a str representing the header for the data to be displayed
            iterable (list of obj): a list of various objects representing data to be displayed

        Returns:
            A list of str containing str representations of the data to be displayed
        """
        info = [header]
        if iterable is None:
            return info
        for i in iterable:
            info.append(f"{i}")
        return info

    def print_info(self, info, y_start, x_start):
        """
        Writes information to the window screen using curses

        Parameters:
            info (list of str): a list containing str representation of the data
            y_start (int): starting y-coordinate of the window
            x_start (int): starting x-coordinate of the window
        """
        count = 0
        for s in info:
            self.screen.addstr(y_start + count, x_start, s)
            count += 1

    def print_borders(self, y_start, height, x_start, width):
        """
        Writes border lines to the edge of the window screen using curses

        Parameters:
            y_start (int): starting y-coordinate of the window
            height (int): the height of the window
            x_start (int): starting x-coordinate of the window
            width (int): the width of the window
        """
        for line in range(y_start, height-1):
            self.screen.addstr(line, x_start+width-1, f"|")
        for col in range(x_start, x_start+width-1):
            self.screen.addstr(height-1, col, f"-")


class ActiveCustomers(Window):
    """Inherits from Window; displays information about the Game's customers"""

    def __init__(self, game, screen):
        """The constructor for ActiveCustomers class; sets dimensions as a ratio of the maximum terminal size"""
        super().__init__(height=Window.MAX_HEIGHT//4, width=Window.MAX_WIDTH//3,
                         y_start=0, x_start=0, game=game, screen=screen)

    def render_info(self):
        """Calls the parent render() function with this Game's customers data"""
        super().render(f"ACTIVE CUSTOMERS", self.game.customers,
                       self.height, self.width, self.y_start, self.x_start)

    def render_startup(self):
        """Calls the parent render() function with helpful information on what will display in this window"""
        super().render(f"ACTIVE CUSTOMERS", [f"This is where customers will show up with orders.",
                                             f"The number of points you'll receive will show here.",
                                             f"Make sure to visit the Town to deliver their orders!"],
                       self.height, self.width, self.y_start, self.x_start)


class TimeRemaining(Window):
    """Inherits from Window; displays information about how much time the player has left"""

    def __init__(self, game, screen, totaltime):
        """
        The constructor for TimeRemaining class; sets dimensions as a ratio of the maximum terminal size

        Parameters:
            totaltime (int): the total time in seconds that the game will run for
        """
        # grab the starting time of the game when this window is created
        self.starttime = time.time()
        self.totaltime = totaltime
        super().__init__(height=Window.MAX_HEIGHT//4, width=Window.MAX_WIDTH//3,
                         y_start=0, x_start=Window.MAX_WIDTH//3, game=game, screen=screen)

    def get_remaining_time(self):
        """
        Compute the remaining time in minutes and seconds

        Returns:
            the minutes (int) and seconds (int) remaining
        """
        timeremaining = self.totaltime - (time.time() - self.starttime)
        minutes = int(timeremaining) // 60
        seconds = int(timeremaining) % 60
        return minutes, seconds

    def render_info(self):
        """Calls the parent render() function with this Game's time data"""
        minutes, seconds = self.get_remaining_time()
        super().render(f"TIME REMAINING", [f"{minutes:.0f}:{seconds:02.0f}"],
                       self.height, self.width, self.y_start, self.x_start)

    def render_startup(self):
        """Calls the parent render() function with helpful information on what will display in this window"""
        super().render(f"TIME REMAINING", [f"This is where your remaining time will be shown.",
                                           f"Try and fill as many orders before time runs out!"],
                       self.height, self.width, self.y_start, self.x_start)


class PlayerScore(Window):
    """Inherits from Window; displays information about how much time the player has left"""

    def __init__(self, game, screen):
        """The constructor for PlayerScore class; sets dimensions as a ratio of the maximum terminal size"""
        super().__init__(height=Window.MAX_HEIGHT//4, width=Window.MAX_WIDTH//3,
                         y_start=0, x_start=(2*Window.MAX_WIDTH)//3, game=game, screen=screen)

    def render_info(self):
        """Calls the parent render() function with this Game's player score data"""
        super().render(f"MONEY", [self.game.player.score],
                       self.height, self.width, self.y_start, self.x_start)

    def render_startup(self):
        """Calls the parent render() function with helpful information on what will display in this window"""
        super().render(f"SCORE", [f"This is where your score will be shown.",
                                  f"Fill more orders to get more points!"],
                       self.height, self.width, self.y_start, self.x_start)


class PlayerInventory(Window):
    """Inherits from Window; displays information about what items the player has"""

    def __init__(self, game, screen):
        """The constructor for PlayerInventory class; sets dimensions as a ratio of the maximum terminal size"""
        super().__init__(height=(3*Window.MAX_HEIGHT)//4, width=Window.MAX_WIDTH//3,
                         y_start=Window.MAX_HEIGHT//4, x_start=0, game=game, screen=screen)

    def render_info(self):
        """Calls the parent render() function with this Game's player inventory data"""
        super().render(f"INVENTORY", self.game.player.inventory,
                       self.height, self.width, self.y_start, self.x_start)

    def render_startup(self):
        """Calls the parent render() function with helpful information on what will display in this window"""
        super().render(f"INVENTORY", [f"This is where your inventory  will be shown.",
                                      f"You only have a maximum of 9 slots.",
                                      f"Be sure to trash any items you don't need."],
                       self.height, self.width, self.y_start, self.x_start)

    def render_trash(self):
        """Calls the parent render() function with inventory data and prompts the user to pick an item to trash"""
        iterable = []
        count = 0
        for item in self.game.player.inventory:
            iterable.append(f"{count} - {item}")
            count += 1
        iterable.append(f"Press 9 to undo.")
        super().render(f"What would you like to trash?", iterable,
                       self.height, self.width, self.y_start, self.x_start)

    def render_mix(self, ingredients):
        """
        Calls the parent render() function with inventory data and prompts the user to pick two items to mix

        Parameters:
            ingredients (list): empty list that will contain a maximum of two Item objects
        """
        iterable = []
        count = 0
        for item in self.game.player.inventory:
            iterable.append(f"{count} - {item}")
            count += 1

        if len(ingredients) == 0:
            iterable.append(f"Press 9 to undo.")
            super().render(f"Add your first ingredient to the Cauldron...", iterable,
                           self.height, self.width, self.y_start, self.x_start)
        elif len(ingredients) == 1:
            iterable.append(f"Press 9 to undo.")
            super().render(f"Add your second ingredient to the Cauldron...", iterable,
                           self.height, self.width, self.y_start, self.x_start)

    def render_delivery(self):
        """Calls the parent render() function with inventory data and prompts the user to pick an Item to deliver"""
        iterable = []
        count = 0
        for item in self.game.player.inventory:
            iterable.append(f"{count} - {item}")
            count += 1
        iterable.append(f"Press 9 to undo.")
        super().render(f"What would you like to deliver?", iterable,
                       self.height, self.width, self.y_start, self.x_start)

    def render_delivery_choice(self, delivery):
        """
        Calls the parent render() function with this Game's customers data and prompts the user to select a customer

        Parameters:
            delivery (Item): the Item object the user has selected to deliver
        """
        iterable = []
        count = 0
        for customer in self.game.customers:
            iterable.append(customer)
            count += 1
        iterable.append(f"Press 9 to undo.")
        super().render(f"Who would you like to deliver {delivery} to?", iterable,
                       self.height, self.width, self.y_start, self.x_start)


class InputField(Window):
    """Inherits from Window; displays information about what commands the player can enter"""

    def __init__(self, game, screen):
        """The constructor for InputField class; sets dimensions as a ratio of the maximum terminal size"""
        super().__init__(height=(3*Window.MAX_HEIGHT)//4, width=Window.MAX_WIDTH//3,
                         y_start=Window.MAX_HEIGHT//4, x_start=Window.MAX_WIDTH//3, game=game, screen=screen)

    def render_info(self):
        """Calls the parent render() function with valid commands from assets.py"""
        iterable = [f"-"*52]
        iterable.extend(assets.INPUTS_DISPLAY)
        super().render(f"AVAILABLE COMMANDS", iterable,
                       self.height, self.width, self.y_start, self.x_start)

    def render_startup(self):
        """Calls the parent render() function with helpful information on what will display in this window"""
        super().render(f"AVAILABLE COMMANDS", [f"This is where your available commands will be shown.",
                                               f"Errors will show up at the bottom of this box."],
                       self.height, self.width, self.y_start, self.x_start)

    def render_pickup(self):
        """Calls the parent render() function with location data and prompts the user to pick an Item to pick up"""
        iterable = []
        count = 0
        for item in self.game.player.location.items:
            iterable.append(f"{count} - {item}")
            count += 1
        iterable.append(f"Press 9 to undo.")
        super().render(f"What would you like to pick up?", iterable,
                       self.height, self.width, self.y_start, self.x_start)

    def render_book(self, chapter):
        """Calls the parent render() function with recipe book data and lets the user navigate through chapters"""
        if chapter is None:
            iterable = [f"{k} - {v}" for k, v in assets.CHAPTER_TITLES.items()]
            iterable.append(f"Press 9 to close the book.")
            super().render(f"THE BOOK OF THE BEAST", iterable,
                           self.height, self.width, self.y_start, self.x_start)
        else:
            instructions = assets.RECIPES_BY_CHAPTER[str(chapter)]
            iterable = []
            for entry in instructions:
                item = self.game.get_item(entry)
                ing_1 = item.recipe[0]
                ing_2 = item.recipe[1]
                iterable.append(f"{entry} = {ing_1} + {ing_2}")
            iterable.append(f"Press 8 to go back to the table of contents.")
            iterable.append(f"Press 9 to close the book.")
            super().render(assets.CHAPTER_TITLES[str(chapter)], iterable,
                           self.height, self.width, self.y_start, self.x_start)

    def render_warning(self, warning):
        """Calls the parent render() function with warning data to populate at the bottom of this window"""
        warnings = []
        warnings.append(warning)
        warnings.append(f"Press any other key to continue.")
        count = 0
        for s in warnings:
            self.screen.addstr(self.height-3 + count, self.x_start, s)
            count+=1


class Map(Window):
    """Inherits from Window; displays information about the player's current and neighboring locations"""

    def __init__(self, game, screen):
        """The constructor for InputField class; sets dimensions as a ratio of the maximum terminal size"""
        super().__init__(height = (3*Window.MAX_HEIGHT)//4, width = Window.MAX_WIDTH//3,
                         y_start = Window.MAX_HEIGHT//4, x_start = (2*Window.MAX_WIDTH)//3, game=game, screen=screen)

    def render_startup(self):
        """Calls the parent render() function with helpful information on what will display in this window"""
        super().render(f"MAP", [f"This is where your current location will show.",
                                f"In addition, neighboring locations will show here.",
                                f"Press the arrow keys to move locations.",
                                f"Items for each location will show in this box too."],
                       self.height, self.width, self.y_start, self.x_start)

    def render_info(self):
        """Calls the parent render() function with current and neighboring location information"""
        iterable = [f"-"*52, f"Neighboring Locations", f"-"*52]
        iterable.extend([f"{direction} - {loc}" for direction, loc in self.game.player.location.neighbors.items()])
        pad_neighbors = 4 - len(self.game.player.location.neighbors)
        iterable.extend([f"" for x in range(pad_neighbors)])
        iterable.append(f"-"*52)
        iterable.append(f"{self.game.player.location} Items")
        iterable.append(f"-"*52)
        if self.game.player.location.items is not None:
            item_preview = [item for item in self.game.player.location.items]
            iterable.extend(item_preview)
            pad_items = 5 - len(self.game.player.location.items)
            iterable.extend([f"" for x in range(pad_items)])
        else:
            iterable.extend([f"" for x in range(5)])
        iterable.append(f"-"*52)
        iterable.append(self.game.player.location.spooky())
        super().render(f"CURRENT LOCATION: {self.game.player.location}", iterable,
                       self.height, self.width, self.y_start, self.x_start)
