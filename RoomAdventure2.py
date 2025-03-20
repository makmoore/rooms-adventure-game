# define room class, blueprint for a room
class Room(object):
    # the constructor
    def __init__(self, name):
        self.name = name
        self.exits = []
        self.exitLocations = []
        self.items = []
        self.itemDescriptions = []
        self.grabbables = []

    # setters and getters
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def exits(self):
        return self._exits

    @exits.setter
    def exits(self, value):
        self._exits = value

    @property
    def exitLocations(self):
        return self._exitLocations

    @exitLocations.setter
    def exitLocations(self, value):
        self._exitLocations = value

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    @property
    def itemDescriptions(self):
        return self._itemDescriptions

    @itemDescriptions.setter
    def itemDescriptions(self, value):
        self._itemDescriptions = value

    @property
    def grabbables(self):
        return self._grabbables

    @grabbables.setter
    def grabbables(self, grabbables):
        self._grabbables = grabbables

    # adds an exit to the room
    # the exit is a string (e.g., north)
    # the room is an instance of a room
    def addExit(self, ex, room):
        # append the exit and room to the appropriate lists
        self._exits.append(ex)
        self._exitLocations.append(room)

    # adds an item to the room
    # the item is a string (e.g., table)
    # the desc is a string that describes the item (e.g., it is made of wood)
    def addItem(self, item, desc):
        # append the item and exit to the appropriate lists
        self._items.append(item)
        self._itemDescriptions.append(desc)
        # adds a grabbable item to the room
        # the item is a string (e.g., key)

    def addGrabbable(self, item):
        # append the item to the list
        self._grabbables.append(item)
        # removes a grabbable item from the room# the item is a string (e.g., key)

    def delGrabbable(self, item):
        # remove the item from the list
        self._grabbables.remove(item)
        # returns a string description of the room

    def __str__(self):
        # first, the room name
        s = "You are in {}.\n".format(self.name)
        # next, the items in the room
        s += "You see: "
        for item in self.items:
            s += item + ", "
        s += "\n"

        # THIS IS TO DISPLAY GRABBABLES IN ROOM
        # s += "You can take: "
        # for t in self.grabbables:
        # [indent] s += t + " "
        # s += "\n"

        # next, the exits from the room
        s += "Exits: "
        for ex in self.exits:
            s += ex + ", "
        return s


#####################################################################
#
# creates the rooms
def createRooms():
    # r1 through r4 are the four rooms in the mansion
    # currentRoom is the room the player is currently in (which can be one of r1 through r4)
    # since it needs to be changed in the main part of the program, it must be global
    global currentRoom

    # create the rooms and give them meaningful names
    r1 = Room("Room 1: Dining Room")
    r2 = Room("Room 2: Living Room")
    r3 = Room("Room 3: Office")
    r4 = Room("Room 4: Bedroom")

    # add exits to room 1
    r1.addExit("east", r2)  # -> to the east of room 1 is room 2
    r1.addExit("south", r3)
    # add grabbables to room 1
    r1.addGrabbable("key")
    # add items to room 1
    r1.addItem("chair", "It is made of plastic. Looks like no one's sat in it in a long time.")
    r1.addItem("table", "It's made of oak. A golden key rests on it.")

    # add exits to room 2
    r2.addExit("west", r1)
    r2.addExit("south", r4)
    # add items to room 2
    r2.addItem("rug", "It is worn and dirty.")
    r2.addItem("fireplace", "It is full of ashes.")

    # add exits to room 3
    r3.addExit("north", r1)
    r3.addExit("east", r4)
    # add grabbables to room 3
    r3.addGrabbable("book")
    r3.addGrabbable("lighter")
    r3.addGrabbable("pen")
    # add items to room 3
    r3.addItem("bookshelf", "The bookshelf has one single book on it. Everything looks dusty and old.")
    r3.addItem("statue", "There's nothing special about it.")
    r3.addItem("desk", "There's a pen on the desk and a lighter in the bottom drawer.")

    # add exits to room 4
    r4.addExit("north", r2)
    r4.addExit("west", r3)
    r4.addExit("south", None)  # DEATH!
    # add grabbables to room 4
    r4.addGrabbable("candle")
    # add items to room 4
    r4.addItem("nightstand", "The nightstand has a candle on it.")
    r4.addItem("bed", "The bed looks like it hasn't been used in years.")

    # set room 1 as the current room at the beginning of the game
    currentRoom = r1


def death():
    print("You died! :(")


####################################################################
#
# START THE GAME!!!
inventory = []  # nothing in inventory yet
createRooms()  # add the rooms to the game

# play forever (well, at least until the player dies or asks to quit)
while True:
    # set the status as variable bellow
    # status = "{}\nYou are carrying: {}\n".format(currentRoom, inventory)     # for storing as variable

    # if the current room is None, then the player is dead & player exits the game
    if currentRoom is None:
        death()
        break

    # display the status (room & inventory info)
    print("======================================================")
    # print(status)   # different method for printing status as one variable
    print(currentRoom)  # same as r1.__str__()
    print()
    print("You are carrying: " + str(inventory))
    print()

    # prompt for player input as <verb> <noun>
    # valid verbs are go, look, and take & valid nouns depend on the verb
    # they used raw_input to treat the input as a string instead of an expression
    action = input("What do you want to do? ")
    # set user's input to lowercase to make it easier to compare verb and noun to known values
    action = action.lower()
    # exit the game if the player wants to leave (supports quit, exit, and bye)
    if action == "quit" or action == "exit" or action == "leave":
        print("Goodbye!")
        break

    # set a default response
    response = "I don't understand. Try verb noun. Valid verbs are go, look, and take"

    # split the user input into words (words are separated by spaces) & store the words in a list
    words = action.split()

    # the game only understands two word inputs
    if (len(words) == 2):
        # isolate the verb and noun
        verb = words[0]
        noun = words[1]
        # the verb is: go
        if (verb == "go"):
            # set a default response
            response = "Invalid exit."

            # check for valid exits in the current room
            for i in range(len(currentRoom.exits)):
                # a valid exit is found
                if (noun == currentRoom.exits[i]):
                    # change the current room to the one that is
                    # associated with the specified exit
                    currentRoom = currentRoom.exitLocations[i]

                    # set the response (success)
                    response = "Room changed."

                    # no need to check any more exits
                    break
        # the verb is: look
        elif (verb == "look"):
            # set a default response
            response = "I don't see that item."

            # check for valid items in the current room
            for i in range(len(currentRoom.items)):
                # a valid item is found
                if (noun == currentRoom.items[i]):
                    # set the response to the item's description
                    response = currentRoom.itemDescriptions[i]

                    # no need to check any more item
                    break

        # the verb is: take
        elif verb == "take" or verb == "grab":
            # set a default response
            response = "I don't see that item."

            # check for valid grabbable items in the current room
            for grabbable in currentRoom.grabbables:
                # a valid grabbable item is found
                if (noun == grabbable):
                    # add the grabbable item to the player's inventory
                    inventory.append(grabbable)

                    # remove the grabbable item from the room
                    currentRoom.delGrabbable(grabbable)

                    # set the response (success)
                    response = "Item grabbed."

                    # no need to check any more grabbable items
                    break
    # display the response
    print(f"\n{response}")
