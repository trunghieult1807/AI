

side0 = ["m1", "m2", "m3", "c1", "c2", "c3"]
side1 = []
boat0 = ["boat"]
boat1 = []

def move(obj, lst0=side0, lst1=side1):
    '''move an object to the other side of the river'''
    if obj in lst0:
        lst1.append(lst0.pop(lst0.index(obj)))
    elif obj in lst1:
        # the object is the boat on side1, so move to side0
        lst0.append(lst1.pop(lst1.index(obj)))
    else:
        print("Cannot move!")

def moveboat():
    move("boat", boat0, boat1)

def turn():
    draw(side0, side1)
    # people on the same side as the boat are "good"
    good_people = []
    if "boat" in boat0:
        good_people = side0
    else:
        good_people = side1
    print("Available to choose from: " + ', '.join(good_people))
    player_move = input("Choose your move: ")
    # check that people on a different side than the boat are not moved
    for i in set(side0) | set(side1):
        if i in player_move:
            if not (i in good_people):
                print("Cannot move " + i + "; the boat is on the wrong side!\n")
    # check that not more than two people are moved
    counter = 0
    for i in set(side0) | set(side1):
        if i in player_move:
            counter += 1
    if counter > 2:
        print("Cannot move more than two!\n")
    # check that when the move is completed, there are not more cannibals
    # than missionaries on each side
    side0temp = side0
    side1temp = side1
    for i in set(side0) | set(side1):
        if i in player_move:
            move(i, side0temp, side1temp)
    for side in [side0temp, side1temp]:
        if any(person.startswith("m") for person in side):
            if sum(person.startswith("c") for person in side) > sum(person.startswith("m") for person in side):
                # cannibals outnumber missionaries; determine on which side that occurs
                if side == side0:
                    print("Cannibals may not outnumber missionaries on top side!")
                else:
                    print("Cannibals may not outnumber missionaries on bottom side!")
                print("DEBUG0")
                return 0
                print("DEBUG1")
    # perform the move for real
    print("DEBUG3")
    for i in good_people:
        if i in player_move:
            move(i, side0, side1)
    moveboat()
    print("DEBUG4")

def draw(top, bottom):
    print("\n" + ' '.join(top))
    if "boat" in top:
        print('''~~B~~~~~~~~~~~~~~
    R i v e r
~~~~~~~~~~~~~~~~~''')
    else:
        print('''~~~~~~~~~~~~~~~~~
    R i v e r
~~B~~~~~~~~~~~~~~''')
    print(' '.join(bottom) + "\n")

turn_number = 0
while len(side1) != 6:
    turn()
    turn_number += 1
print("Congratulations! You won in " + str(turn_number) + " turns. (Minimum 11)")
