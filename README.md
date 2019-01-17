# You Better Work, Witch
**Jimmy Dunn w200 Project 1**

**Fall 2018**

**Email:** jdunn@ischool.berkeley.edu

Title Citation: https://www.youtube.com/watch?v=pt8VYOfr8To

"You Better Work, Witch" (YBWW) is a text-based game where the player takes
on the role of a full-time witch working in a small town somewhere in the
countryside. The goal of the game is to fulfill as many customer orders as
possible (making money along the way) within a 10 minute time limit.

## Playing the Game
To play the game, the player will run `python play.py` at the command line.
Due to a limitation of the `curses` library, the player must ensure their
terminal window is large enough to accommodate the user interface (52 rows
by 160 columns). This should fit on 13.3 in. displays and larger.

On startup, the game will display an intro screen that will show the player
which windows will display what kinds of information. The player will
perform actions by entering the corresponding keys. The game is designed such
that it will respond to the player entering a key immediately, no need to
press enter.

The player will need to fulfill customer orders when they show up to their
cauldron. The player will look through their recipe book to figure out
how to create the items the customers want. The player will have to move
around the map to different locations in order to collect the ingredients
they will need to mix at their cauldron to create orders.

If this wasn't enough, this generation of customers are really impatient and
won't wait forever for the player to create their orders. If their wait time
expires, they will leave and take their money with them. But don't worry,
they will be replaced by a new customer with a new order. thank u, next.


## User Interface
The user interface will populate in the terminal upon running the `play.py`
file and will be subdivided into six sub-windows.

The top left window contains a list of active customers, including their
orders and their current wait times.

The top middle window contains the time remaining for the game, counting
down from 10 minutes.

The top right window contains the player's revenue (or score).

The bottom left window contains the player's inventory, including up to a
maximum of 9 items.

The bottom middle window contains a list of keys a player can input to
perform actions. It also populates warnings at the bottom whenever the
player runs into errors.

The bottom right window contains location information, including the player's
current location, any neighbors, and any items available to be collected.

## Reflections
There are a few user experience design elements I would've liked to get to
if I had more time.

I wanted to develop a more detailed "Game Over" screen that provided an
overview of all the orders the player fulfilled correctly, orders they
messed up, and orders they missed.

In addition, I wanted to play test the customer wait times a bit more to
give different difficulty feelings for different customers.

It would have been fun to flesh out the tech tree for recipes. Due to space
constraints, I could only display two ingredients per order in the recipe
book. It would have been cool to develop 3+ ingredients for some of the
recipes.

In conclusion, this was a huge project. I think I came close to biting off
more than I could chew, especially with learning the nuances of the `curses`
library. However, I'm pretty proud of myself for designing classes and
objects in a way that allowed me to handle the low-level details of curses
separately from designing the high-level game functions.

I hope you enjoy!
