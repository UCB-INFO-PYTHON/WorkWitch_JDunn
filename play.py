import curses
import time

import game as g
from interface import *


class Menu:
    """
    This is a class that will control and manage every aspect of gameplay

    Attributes:
        screen (curses.WindowObject): WindowObject from the curses library containing display functions
        game_over (bool): flag that will let Menu know when the game is over
        game (Game): the Game object for this playthrough
        subwindows (dict of Window): subwindows for the displaying game information at the terminal
    """

    def __init__(self):
        """The constructor for Menu class."""
        # create a WindowObject to work the terminal screen
        self.screen = curses.initscr()
        # noecho() prevents keys from being echoed to the terminal when pressed
        curses.noecho()
        # cbreak() allows the terminal to interpret keys immediately after they're pressed
        curses.cbreak()
        # curs_set(0) turns off the blinking cursor
        curses.curs_set(0)
        # WindowObject.keypad(True) allows for terminal to get curses objects like LEFT_KEY and RESIZE
        self.screen.keypad(True)
        # clear the terminal
        self.screen.clear()

        # start up the game
        self.game_over = False
        self.game = g.Game()
        self.game.setup()
        # start up the subwindows
        self.subwindows = {'customers': ActiveCustomers(self.game, self.screen),
                           'timeremaining': TimeRemaining(self.game, self.screen, totaltime=600),
                           'score': PlayerScore(self.game, self.screen),
                           'inventory': PlayerInventory(self.game, self.screen),
                           'input': InputField(self.game, self.screen),
                           'map': Map(self.game, self.screen)
                           }

    def reset(self):
        """Undo the curses commands that set up the game so the terminal returns to normal"""
        # allows keys to be written to the terminal again
        curses.echo()
        # waits for user to hit enter before the terminal gets keys
        curses.nocbreak()
        # turns the blinking cursor back on
        curses.curs_set(1)
        # turns off curses objects like LEFT_KEY and RESIZE
        self.screen.keypad(False)
        # resets curses getch() to be blocking
        self.screen.nodelay(0)
        # close the WindowObject
        curses.endwin()

    def render(self, exclude=None):
        """
        Update the screen

        Parameters:
            exclude (str): indicates a subwindow that will not render normally because it'll render a prompt
        """
        for name, sw in self.subwindows.items():
            if name != exclude:
                sw.render_info()
            self.screen.refresh()

    def raise_warning(self, warning):
        """
        Display a warning on the screen at the bottom of the InputField window

        Parameters:
            warning (str): the text of the warning to be displayed
        """
        self.screen.clear()
        self.render()
        self.subwindows['input'].render_warning(warning)
        self.screen.refresh()

    def refresh_logic(self):
        """Accomodate curses.nodelay() by refreshing the terminal every second to update the countdown timer"""
        # grab the current time to know when a second has passed
        refreshtime = time.time()

        while True:
            # get a key input from the user, will return -1 otherwise since non-blocking is toggled
            k = self.screen.getch()
            tr = self.subwindows['timeremaining']
            remainingtime = tr.totaltime - (time.time() - tr.starttime)

            # if the total game time has run out, initiate end game sequence
            if remainingtime <= 0:
                self.game_over = True
                break

            # check all customers to see if their waittime has expired
            for customer in self.game.customers:
                if customer.time_remaining() <= 0:
                    self.game.update_customer(customer)

            # if the user has entered a key (anything other than -1) then return it and execute the function
            if k != -1:
                return k

            # if one second has passed, refresh the screen with the updated time
            if time.time() - refreshtime > 1:
                self.subwindows['timeremaining'].render_info()
                self.subwindows['customers'].render_info()
                refreshtime = time.time()

    def startup_screen(self):
        """Start the game by showing the screen with help text displayed"""
        for name, sw in self.subwindows.items():
            sw.render_startup()
        # render_warning adds the "press any key to continue" warning by default
        self.subwindows['input'].render_warning("")
        self.screen.refresh()
        # getch() is blocking as of this moment, prompt user to enter any key to continue
        u = self.screen.getch()
        # nodelay() makes getch() non-blocking
        self.screen.nodelay(1)
        self.screen.clear()
        self.render()

    def play(self):
        """Loop until the game ends or the user quits"""
        while not self.game_over:
            k = self.refresh_logic()
            self.screen.clear()
            self.update(k)
            self.render()
            self.screen.refresh()
        self.end_game()

    def update(self, k):
        """Update the game data depending on what command the user input"""
        # make a dictionary of functions to call depending on what the user inputs
        switch = {ord("p"): self.do_pickup, ord("t"): self.do_trash, ord("h"): self.do_returnhome,
                  ord("b"): self.do_readbook, ord("m"): self.do_mix, ord("d"): self.do_deliver,
                  ord("q"): self.do_quit, curses.KEY_RESIZE: self.do_resize}
        # move function has to be made separate because it takes a direction argument
        directions = {curses.KEY_UP: "N", curses.KEY_DOWN: "S",
                      curses.KEY_LEFT: "W", curses.KEY_RIGHT: "E"}

        if k in switch:
            switch[k]()

        elif k in directions:
            self.do_move(directions[k])

    def do_move(self, direction):
        """
        Move the player based on the direction they want to move

        Parameters:
            direction (str): N, S, E, W representing a direction to move
        """
        self.game.player.move(self.game, direction)

    @staticmethod
    def is_int(k):
        """Check if k can be converted to an int successfully"""
        try:
            int(chr(k))
            return True
        except ValueError:
            return False

    def do_pickup(self):
        """Prompt the player to pick up an item available in their current location"""
        if self.game.player.location.items is None:
            self.raise_warning(f"There are no items to pickup here!")

        elif len(self.game.player.inventory) == 9:
            self.raise_warning(f"Your inventory is full!!")

        else:
            while True:
                # clear the screen and render the pickup prompt in the input field
                self.screen.clear()
                self.render(exclude='input')
                self.subwindows['input'].render_pickup()
                self.screen.refresh()

                # get user input and update inventory accordingly
                k = self.refresh_logic()
                if self.is_int(k):

                    # if the user inputs a valid item position in the location, pick it up
                    if int(chr(k)) in range(len(self.game.player.location.items)):
                        item = self.game.player.location.items[int(chr(k))]
                        self.game.player.pickup(item)
                        self.screen.clear()
                        break

                    # if the user enters 9, cancel the pickup action
                    elif int(chr(k)) == 9:
                        self.screen.clear()
                        break

    def do_trash(self):
        """Prompt the player to trash one of the items in their inventory"""
        if len(self.game.player.inventory) == 0:
            self.raise_warning(f"You have no items to trash!")

        else:
            while True:
                # clear the screen and render the trash prompt in the inventory window
                self.screen.clear()
                self.render(exclude='inventory')
                self.subwindows['inventory'].render_trash()
                self.screen.refresh()

                # get user input and update inventory accordingly
                k = self.refresh_logic()
                if self.is_int(k):
                    # if user inputs a valid item position, trash it
                    if int(chr(k)) in range(len(self.game.player.inventory)):
                        item = self.game.player.inventory[int(chr(k))]
                        self.game.player.trash(item)
                        self.screen.clear()
                        break
                    # if user inputs 9, cancel the trash action
                    elif int(chr(k)) == 9:
                        self.screen.clear()
                        break

    def do_returnhome(self):
        """Move the player back to the Cauldron"""
        if self.game.player.location.name == "Cauldron":
            self.raise_warning(f"You are already here!")

        else:
            self.game.player.location = self.game.get_location("Cauldron")

    def do_readbook(self):
        """Open the recipe book and allow the player to navigate its chapters"""
        # set chapter to None so render_book will first open to the table of contents
        chapter = None
        while True:
            # clear the screen and render the recipe book table of contents
            self.screen.clear()
            self.render(exclude='input')
            self.subwindows['input'].render_book(chapter)
            self.screen.refresh()

            # get user input
            k = self.refresh_logic()
            if self.is_int(k):

                # if user input is a chapter number, turn to that chapter and display recipes
                if int(chr(k)) in range(len(self.game.book.chapters)):
                    chapter = int(chr(k))

                # if user input is 8, return to table of contents
                elif int(chr(k)) == 8:
                    chapter = None

                # if user input is 9, exit the book
                elif int(chr(k)) == 9:
                    self.screen.clear()
                    break

    def do_mix(self):
        """Prompt the player to put two items in the Cauldron and check to see if they produce anything"""
        if len(self.game.player.inventory) == 0:
            self.raise_warning(f"You have no items to mix!")

        elif self.game.player.location.name != "Cauldron":
            self.raise_warning(f"You need to be at the Cauldron to mix!")

        else:
            ingredients = []
            while True:
                # clear the screen and render the mix prompt in the inventory window
                self.screen.clear()
                self.render(exclude='inventory')
                self.subwindows['inventory'].render_mix(ingredients)
                self.screen.refresh()

                # get user input and update inventory accordingly
                k = self.refresh_logic()
                if self.is_int(k):

                    # if user inputs a valid item position, add that item to the ingredients
                    if int(chr(k)) in range(len(self.game.player.inventory)):
                        item = self.game.player.inventory[int(chr(k))]
                        ingredients.append(item)
                        self.game.player.trash(item)

                        # if the player is out of items, break this loop
                        if len(self.game.player.inventory) == 0:
                            break

                        # if the player added 2 ingredients, break this loop
                        elif len(ingredients) == 2:
                            break
                    # if the user inputs 9, quit the mix action
                    elif int(chr(k)) == 9:
                        break

            # if the player entered valid ingredients, create the item!
            reward = self.game.player.mix(self.game.book, ingredients)
            if reward is None:
                self.raise_warning(f"Those ingredients don't make anything! Tough luck!")

            else:
                self.game.player.pickup(reward)
                self.raise_warning(f"Congratulations! You made a {reward}!")

    def do_deliver(self):
        """Prompt the player to deliver one of thier items to one of the active customers"""
        if len(self.game.player.inventory) == 0:
            self.raise_warning(f"You have no items to deliver!")

        elif self.game.player.location.name != "Town":
            self.raise_warning(f"You need to be in Town to deliver!")

        else:
            # set delivery to None so render_delivery will prompt the user to pick an item first
            delivery = None
            while True:
                if delivery is None:
                    # clear the screen and render the delivery prompt in the inventory window
                    self.screen.clear()
                    self.render(exclude='inventory')
                    self.subwindows['inventory'].render_delivery()
                    self.screen.refresh()
                    # get user input and update inventory accordingly
                    k = self.refresh_logic()
                    if self.is_int(k):

                        # if the user inputs a valid item position, make that item the delivery
                        if int(chr(k)) in range(len(self.game.player.inventory)):
                            delivery = self.game.player.inventory[int(chr(k))]
                            self.screen.clear()

                        # if the user inputs 9, quit the deliver action
                        elif int(chr(k)) == 9:
                            self.screen.clear()
                            break

                else:
                    # if the delivery is not None, clear screen and prompt which customer to deliver to
                    self.screen.clear()
                    self.render(exclude='inventory')
                    self.subwindows['inventory'].render_delivery_choice(delivery)
                    self.screen.refresh()

                    # get user input and update customer data accordingly
                    k = self.refresh_logic()
                    if self.is_int(k):

                        # if user enters a valid customer position, give the delivery to that customer
                        if int(chr(k)) in range(len(self.game.customers)):
                            customer = self.game.customers[int(chr(k))]
                            self.game.player.deliver_order(self.game, delivery, customer)
                            self.screen.clear()
                            break

                        # if the user enters 9, quit the delivery action
                        elif int(chr(k)) == 9:
                            self.screen.clear()
                            break

    def do_quit(self):
        """Reset the screen back to normal and quit the program"""
        self.reset()
        quit()

    def do_resize(self):
        """Don't do anything if the user resizes the terminal"""
        pass

    def end_game(self):
        """Show the user that the game is over and then quit the game"""
        self.subwindows['input'].render_warning(f"GAME OVER: {self.game.player}")
        self.screen.refresh()
        self.screen.nodelay(0)
        u = self.screen.getch()
        self.do_quit()


def main():
    m = Menu()
    try:
        m.startup_screen()
        m.play()
    except:
        # if the screen is too small, curses will throw an error and break the terminal
        m.reset()
        print(f"Please ensure the screen is sized to accomodate the game.")


if __name__ == '__main__':
    main()
