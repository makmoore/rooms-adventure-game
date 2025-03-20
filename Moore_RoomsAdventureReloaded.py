###########################################################################################
# Name: Makenzie Moore
# Date: 3/30/24
# Description: This is a simple escape room. There are 4 total rooms. The goal is to unlock the north exit of Room 1:
#  the Bedroom. To do this you do the following: (1.) look at the nightstand in the bedroom to find the note w/ a
#  code on it, (2.) take the note, (3.) go to room 4: the Office (east then south), (4.) look at the safe in the
#  office to use the note in your inventory, (5.) go back to Room 1: Bedroom w/ the key, (6.) go through the north
#  exit to use the key, (7.) and you escaped!
# Additional Notes: I added the option to "use" items in your inventory. There are several items you can pick up in
#  the game that aren't vital to escaping. You can "use" these, though. The safe and final exit are both locked if you
#  don't have the proper items in your inventory. Grabbables aren't displayed to begin with because the player has
#  to discover them through interacting with objects. There's no door between Room 3: Bathroom and Room 4: Office
#  because I wanted the bathroom to only be connected to the bedroom. There is no death option.
###########################################################################################
from tkinter import *


# the room class
class Room(object):
    # the constructor
    def __init__(self, name, image):
        # rooms have a name, an image (the name of a file), exits (e.g., south), exit locations
        # (e.g., to the south is room n), items (e.g., table), item descriptions (for each item),
        # and grabbables (things that can be taken into inventory)
        self.name = name
        self.image = image
        self.exits = {}
        self.items = {}
        self.grabbables = []

    # getters and setters for the instance variables
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def exits(self):
        return self._exits

    @exits.setter
    def exits(self, value):
        self._exits = value

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    @property
    def grabbables(self):
        return self._grabbables

    @grabbables.setter
    def grabbables(self, value):
        self._grabbables = value

    # adds an exit to the room as a string (e.g., north)
    # the room is an instance of a room
    def addExit(self, exit, room):
        # append the exit and room to the appropriate dictionary
        self._exits[exit] = room

    # adds an item to the room as a string (e.g., table)
    # the desc is a string that describes the item (e.g., it is made of wood)
    def addItem(self, item, desc):
        # append the item and description to the appropriate dictionary
        self._items[item] = desc

    # adds a grabbable item to the room as a string (e.g., key)
    def addGrabbable(self, item):
        # append the item to the list
        self._grabbables.append(item)

    # removes a grabbable item from the room - string (e.g., key)
    def delGrabbable(self, item):
        # remove the item from the list
        self._grabbables.remove(item)

    # returns a string description of the room
    def __str__(self):
        # first, the room name
        s = "You are in the {}.\n".format(self.name)

        # next, the items in the room
        s += "You see: "
        for item in self.items.keys():
            s += item + " "
        s += "\n"

        # next, the exits from the room
        s += "Exits: "
        for exit in self.exits.keys():
            s += exit + " "

        return s


# the game class inherits from the Frame class of tkinter
class Game(Frame):
    # the constructor
    def __init__(self, parent):
        # call the constructor in the superclass
        Frame.__init__(self, parent)

    # creates the rooms
    def createRooms(self):
        # r1 to r4 are the 4 rooms
        # currentRoom is the one the players is currently in
        # create rooms with names and images
        r1 = Room("Bedroom", "images/room1.gif")
        r2 = Room("Kitchen", "images/room2.gif")
        r3 = Room("Bathroom", "images/room3.gif")
        r4 = Room("Office", "images/room4.gif")
        # add exits, grabbables, & items to the rooms

        # room 1: Bedroom
        r1.addExit("east", r2)  # to the east is room 2
        r1.addExit("south", r3)  # south is room 3
        r1.addExit("north", None)  # this is the way out but it's locked
        r1.addItem("bed", "This is the bed you woke up on. It looks like a \nnormal bed.")
        r1.addItem("nightstand", "The nightstand has a note with the numbers 1352 \non it. You should take "
                                 "the note for later. (note)")
        r1.addItem("dresser", "It looks worn and used. There's nothing of note \ninside.")
        r1.addItem("lamp", "The bulb is burnt out so it won't turn on.")
        r1.addGrabbable("note")

        # room 2: Dining Room
        r2.addExit("west", r1)  # west is room 1
        r2.addExit("south", r4)  # south is room 4
        r2.addItem("table", "There are 4 chairs around the table. There's \nnothing on top of it.")
        r2.addItem("fridge", "The only thing in the fridge is a soda. You can \ntake the soda. (soda)")
        r2.addItem("sink", "The sink is completely empty.")
        r2.addGrabbable("soda")

        # room 3: Bathroom
        r3.addExit("north", r1)  # north is room 1
        r3.addItem("toilet", "This is a regular toilet. Nothing to see here.")
        r3.addItem("shower", "There is a normal shower.")
        r3.addItem("sink", "There's an unused bar of soap sitting next to the sink. You can take the soap. (soap)")
        r3.addItem("mirror", "You look into the mirror and your reflection \ngazes back at you.")
        r3.addGrabbable("soap")

        # room 4: Office
        r4.addExit("north", r2)  # north is room 2
        r4.addItem("desk", "The desk looks sturdy and old. The safe is next \nto it.")
        r4.addItem("bookshelf", "There are several old books on the bookshelf. \nYou could take one of the "
                                "books if you want to... \n(book)")
        r4.addItem("safe", "There is a safe next to the desk. It looks like you need to put in a "
                           "4-digit code to unlock it.")
        r4.addItem("window", "The window won't open. It's too high up to escape from anyway.")
        r4.addGrabbable("book")

        # set room 1 as the current room at the beginning of the game
        Game.currentRoom = r1

        # initialize inventory
        Game.inventory = []

    # sets up the GUI
    def setupGUI(self):
        # organize the GUI
        self.pack(fill=BOTH, expand=1)

        # set up the player input at the bottom of the GUI
        # the widget is a Tkinter Entry
        # set its background to white and bind the return key to the
        # function process in the class
        # push it to the bottom of the GUI and let it fill horizontally
        # give it focus so the player doesn't have to click on it
        Game.player_input = Entry(self, bg="white")
        Game.player_input.bind("<Return>", self.process)
        Game.player_input.pack(side=BOTTOM, fill=X)
        Game.player_input.focus()

        # set up the image to the left of the GUI
        # the widget is a Tkinter Label
        # don't let the image control the widget's size
        img = None
        Game.image = Label(self, width=WIDTH, image=img)
        Game.image.image = img
        Game.image.pack(side=LEFT, fill=Y)
        Game.image.pack_propagate(False)

        # set up the text to the right of the GUI
        # first, the frame in which the text will be placed
        text_frame = Frame(self, width=WIDTH / 2)
        # the widget is a Tkinter Text
        # disable it by default
        # don't let the widget control the frame's size
        Game.text = Text(text_frame, bg="lightgrey", state=DISABLED)
        Game.text.pack(fill=Y, expand=1)
        text_frame.pack(side=RIGHT, fill=Y)
        text_frame.pack_propagate(False)

    # sets the current room image
    def setRoomImage(self):
        if Game.currentRoom is None:  # no image for this
            pass
        else:
            # otherwise grab the image for the current room
            Game.img = PhotoImage(file=Game.currentRoom.image)

        # display the image on the left of the GUI
        Game.image.config(image=Game.img)
        Game.image.image = Game.img

    # sets the status displayed on the right of the GUI
    def setStatus(self, status):
        # enable the text widget, clear it, set it, and disabled it
        Game.text.config(state=NORMAL)
        Game.text.delete("1.0", END)
        if Game.currentRoom is None:
            Game.text.insert(END, "You can't get out this way.")
            pass
        else:
            # otherwise, display the appropriate status
            possible_actions = ("\n\n\n\nHints:\nYou can type:\ngo direction \n direction= south, north, east, west"
                                "\nlook object \n object = what's in the room \ntake item \n item = what you found"
                                "\nuse item \n item = anything in your inventory")
            Game.text.insert(END, str(Game.currentRoom) + "\nYou are carrying: " + str(Game.inventory)
                             + "\n\n" + status + "\n\n\n" + possible_actions)
        Game.text.config(state=DISABLED)

    # plays the game
    def play(self):
        # add the rooms to the game
        self.createRooms()
        # configure the GUI
        self.setupGUI()
        # set the current room
        self.setRoomImage()
        # set the current status
        self.setStatus("")

    # processes the player's input
    def process(self, event):
        # grab the player's input from the input at the bottom of the GUI
        action = Game.player_input.get()
        # set the user's input to lowercase to make it easier to
        # compare the verb and noun to known values
        action = action.lower()
        # set a default response
        response = "I don't understand. Try verb noun. Valid verbs are go, look, and use"
        # exit the game if the player wants to leave (supports quit, exit, and bye)
        if action == "quit" or action == "exit" or action == "bye":
            exit(0)
        # the player is dead if he goes/went south from room 4
        if Game.currentRoom == None:
            # clear the player's input
            Game.player_input.delete(0, END)
            return

        # split the user input into words (words are separated by spaces) and store the words in a list
        words = action.split()

        # the game only understands two word inputs
        if len(words) == 2:
            # isolate the verb and noun
            verb = words[0]
            noun = words[1]

            # the verb is: go
            if verb == "go":
                # set a default response
                response = "Invalid exit."
                # check for valid exits in the current room
                if noun in Game.currentRoom.exits:
                    if Game.currentRoom.exits[noun] == None:
                        # the door that leads to the outside is locked
                        response = "This door is locked. You need a key to unlock it."
                        if "key" in Game.inventory:  # checks if the player has the key to unlock the door
                            response += "\n\nThe key is in your inventory!"
                            response += "\n\nYou used your key to unlock the door!"
                            response += "\n\nCongratulations you escaped!!!!!!!!!!!!!!!\n\nType <quit> to exit."
                    else:
                        # if one is found, change the current room to the one that is associated with the specified exit
                        Game.currentRoom = Game.currentRoom.exits[noun]
                        # set the response (success)
                        response = "Room changed."

            # the verb is: look
            elif verb == "look":
                # set a default response
                response = "I don't see that item."
                # check for valid items in the current room
                if noun == "safe":
                    if "note" in Game.inventory and "key" not in Game.inventory:
                        # checks if the player has the note w/ the code to unlock it & hasn't already gotten the key
                        response = ("\n\nYou enter the numbers from the note you found on \nthe nightstand to open "
                                    "the safe.\n\n1-3-5-2")
                        response += "\n\nInside the safe is a key. You take the key."
                        Game.inventory.append("key")
                        response += "\n\nItem grabbed."
                    elif "key" in Game.inventory:  # if player already has key & tries safe again, this message shows
                        response = ("You already unlocked the safe with the code \non the note and took out the key. "
                                    "\n\nThere's nothing left in the safe.")
                    else:  # shows this when the safe is locked
                        response = "\nThe safe is locked. You need a 4-digit code to \nunlock it."
                if noun in Game.currentRoom.items and noun != "safe":
                    # if one is found, set the response to the item's description
                    response = Game.currentRoom.items[noun]

            # if verb is use
            elif verb == "use":
                # set as a default response
                response = "That's not in your inventory"
                if noun in Game.inventory:  # checks for the items in inventory to use them
                    if noun == "soda":
                        response = "\nYou drank the soda. It tasted flat."
                        Game.inventory.remove(noun)
                    elif noun == "note":
                        response = "\nThe numbers 1352 are written on it."
                    elif noun == "book":
                        response = ("\nThe title of the book is 'How to Escape Any \nSituation'. You skim through it "
                                    "but it's \nsurprisingly unhelpful.")
                    elif noun == "soap":
                        response = ("\nYou use the soap to wash your hands. It makes you feel better about this "
                                    "whole situation.")
                        Game.inventory.remove(noun)
                    else:
                        response = "\nGo to the door to use this."

            # the verb is: take
            elif verb == "take":
                # set a default response
                response = "I don't see that item."
                # check for valid grabbable items in the current room
                for grabbable in Game.currentRoom.grabbables:
                    # a valid grabbable item is found
                    if noun == grabbable:
                        # add the grabbable item to the player's inventory
                        Game.inventory.append(grabbable)
                        # remove the grabbable item from the room
                        Game.currentRoom.delGrabbable(grabbable)
                        # set the response (success)
                        response = "Item grabbed."
                        # no need to check any more grabbable items
                        break

        # display the response on the right of the GUI
        # display the room's image on the left of the GUI
        # clear the player's input
        self.setStatus(response)
        self.setRoomImage()
        Game.player_input.delete(0, END)


##########################################################
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# create the window
window = Tk()
window.title("Room Adventure")

# create the GUI as a Tkinter canvas inside the window
g = Game(window)
# play the game
g.play()

# wait for the window to close
window.mainloop()
