# A dots and boxes player, can play up to a 5x5 board.
# Does not use any searching, only strategy

import random
import time
import copy
bs = None # board size
boxes = {} # set of boxes
lines = {} # set of lines

def main():
    # get board size
    bs = input("What square board size would you like to play? (1-5) ")
    # handle invalid input
    while bs.isdigit() == False:
        print("Invalid board size, enter a number from 1 to 5")
        bs = input("What square board size would you like to play? (1-5) ")
    while int(bs)<1 or int(bs)>5:
        print("Invalid board size, enter a number from 1 to 5")
        bs = input("What square board size would you like to play? (1-5) ")
    bs = int(bs)
    # create board (boxes and lines)
    a = ord('a')
    for box in range(bs*bs):
        boxes[chr(a+box)] = "empty"
    #print(boxes)
    for s in range(bs):
        lines[chr(a+s)+'N'] = 0
        for row in range(bs-1):
            lines[chr(a+s+bs*row)+chr(a+s+bs*(row+1))] = 0
        lines[chr(a+s+bs*(bs-1))+'S'] = 0
        lines[chr(a+bs*s)+'W'] = 0
        for col in range(bs-1):
            lines[chr(a+bs*s+col)+chr(a+bs*s+(col+1))] = 0
        lines[chr(a+bs*s+(bs-1))+'E'] = 0
    #print(lines)
    # determine who goes first
    order = input("Would you like to go 1st or 2nd? ")
    # handle invalid input
    while order[0].isdigit() == False:
        print("Invalid input")
        order = input("Would you like to go 1st or 2nd? ")
    order = int(order[0])
    # play game!
    moves = 0 # number of moves played so far
    max_moves = 2*bs*(bs+1) # total possible moves
    game_over = False
    first_loop = True # true if on first loop of game (for playing order)
    while moves < max_moves and not game_over:
        # user takes turn
        if order == 1 or first_loop == False: # skip if first loop and going 2nd
            ycont = True # should user continue their turn (if box is captured)
            while ycont and not game_over:
                # get user move
                yplay = input("What move would you like to play? ")
                yplay = fixMove(yplay)
                # get new move if not valid
                while yplay not in lines or lines[yplay] == 1:
                    if yplay in lines:
                        print("There is already a line there")
                    else:
                        print("Not a valid move")
                    yplay = input("What move would you like to play? ")
                lines[yplay] = 1 # update board
                moves = moves + 1 # increase number of moves done
                # check if move captures box and update board
                ycont = capturedBox(yplay,"you",'y')
                if ycont:
                    print("You captured a box!")
                game_over = gameOver() # check if game is over
        # comp takes their turn
        ccont = True # should comp continue their turn (if box captured)
        while ccont and not game_over:
            print("Making my move...")
            if moves > max_moves/2:
                cplay = fixMove(compSearchMove())
            else:
                cplay = fixMove(compPickMove()) # pick move!
            lines[cplay] = 1 # update board
            moves = moves + 1 # increase number of moves done
            time.sleep(1) # pause for a second to seem more human
            print("I play " + cplay)
            # check if move captures a box and update board
            ccont = capturedBox(cplay,"comp",'y')
            if ccont:
                print("Comp captured a box!")
                time.sleep(0.5) # pause to allow them to read move
            game_over = gameOver() # check if game is over
        first_loop = False
    # print outcome of game
    printScore()

# captureBox: Takes a move, a player who made the move, and a flag for whether
# or not to actually update the board. Returns if a box is captured by that move.
def capturedBox(move,p,update,lines=lines):
    foundbox = False
    # iterate through each box touching the move
    for c in move:
        if c.islower(): # check that c is a box and not a direction
            boxed = True
            # iterate through lines around that box other than the move
            for l in lines:
                if c in l and l != move:
                    # if any line is empty, box would not be captured
                    if lines[l]==0:
                        boxed = False
                        break
            # if a box is captured and flag is yes, update board
            if boxed:
                if update == 'y':
                    boxes[c] = p
                foundbox = True
    return foundbox

# gameOver: returns if all boxes have been captured
def gameOver(boxes = boxes):
    for box in boxes.values():
        if box=="empty":
            return False
    return True

# isDead: takes a box and checks if it is dead (can be captured)
def isDead(box):
    # count the filled in lines around the box
    lines_around = 0
    for move in lines.keys():
        if box in move:
            if lines[move]==1:
                lines_around = lines_around+1
    # if 3 are filled in, box is dead
    if lines_around == 3:
        return True
    return False    

# numDeadBoxes: returns the number of dead boxes on the board
def numDeadBoxes():
    num_dead_boxes = 0
    for box in boxes.keys():
        if isDead(box):
            num_dead_boxes = num_dead_boxes+1
    return num_dead_boxes

# isSafeMove: takes a move and returns if will create a dead box by checking if
# the move is touching a box already surrounded by 2 other lines
def isSafeMove(move, lines = lines):
    for c in move:
        if c.islower():
            lines_around = 0
            for l in lines.keys():
                if c in l and l != move:
                    if lines[l] == 1:
                        lines_around = lines_around+1
            if lines_around == 2:
                return False
    return True

# safeMovesLeft: returns true if there are any safe moves left on the board
def safeMovesLeft():
    for move in lines.keys():
        if lines[move]==0 and isSafeMove(move):
            return True
    return False

# boxesBeside: takes a box and returns a list of the boxes directly touching it # with no filled in lines in between them
def boxesBeside(box):
    boxes_beside = []
    # if box is not actually a box but a direction, return empty
    if box.islower() == False:
        return boxes_beside
    for line in lines.keys():
        if box in line and lines[line]==0:
            for c in line:
                if c!=box:
                    boxes_beside.append(c)
    return boxes_beside

# isLoop: takes a chain and returns if it is a loop
def isLoop(chain):
    if chain[0].islower():
        # checks for any duplicates in the chain
        for i in range(len(chain)):
            if chain[i] in chain[i+1:]:
                return True
    return False

# loopLen: takes a loop and returns its length (without duplicates)
def loopLen(loop):
    # returns the number of boxes in a loop
    return len(set(loop))

# returnChains: returns a list of all the chains in the board
def returnChains():
    chains = []
    # iterate through all boxes, test if the have 2 open boxes beside them, if
    # so, create a chain and add to it until a box with less or more than 2
    # beside it (directions have none beside them so will end the chain)
    for box in boxes.keys():
        # skip box if already in a found chain
        if any(box in chain for chain in chains):
            continue
        boxes_beside = boxesBeside(box)
        # if has 2 open boxes beside it, is part of a chain
        if len(boxes_beside)==2:
            chain = [boxes_beside[0],box,boxes_beside[1]]
            # boxes_beside_l is the 'left' box in the chain so far
            boxes_beside_l = boxesBeside(boxes_beside[0])
            next_last_box = boxes_beside[0]
            last_box=box
            # while the chain continues to the left, add to it
            while len(boxes_beside_l)==2:
                box_1 = boxes_beside_l[0]
                box_2 = boxes_beside_l[1]
                # figure out which box is the new one
                if box_1!=last_box:
                    # end chain if is loop or found direction (end)
                    if box_1 in chain and box_1.islower():
                        chain.insert(0,box_1) # insert at the beginning/left
                        break
                    chain.insert(0,box_1)
                    # get new 'leftmost' box
                    boxes_beside_l = boxesBeside(box_1)
                    last_box = next_last_box
                    next_last_box = box_1
                else:
                    if box_2 in chain and box_2.islower():
                        chain.insert(0,box_2)
                        break
                    chain.insert(0,box_2)
                    # get new 'leftmost' box
                    boxes_beside_l = boxesBeside(box_2)
                    last_box = next_last_box
                    next_last_box = box_2
            # now continue the 'right' side of the chain
            boxes_beside_r = boxesBeside(boxes_beside[1])
            next_last_box = boxes_beside[1]
            last_box = box
            while len(boxes_beside_r)==2:
                box_1 = boxes_beside_r[0]
                box_2 = boxes_beside_r[1]
                if box_1!=last_box:
                    if box_1 in chain and box_1.islower():
                        chain.append(box_1) # append at the end/right
                        break
                    chain.append(box_1)
                    boxes_beside_r = boxesBeside(box_1)
                    last_box = next_last_box
                    next_last_box = box_1
                else:
                    if box_2 in chain and box_2.islower():
                        chain.append(box_2)
                        break
                    chain.append(box_2)
                    boxes_beside_r = boxesBeside(box_2)
                    last_box = next_last_box
                    next_last_box = box_2
            # chain is finished
            chains.append(chain)
    return chains

# returnChain: takes a box and returns the chain that it is in if any
def returnChain(box):
    chains = returnChains()
    for chain in chains:
        if box in chain:
            return chain
    return []

# numEmptyBoxes: returns the number of non-captured boxes
def numEmptyBoxes():
    left = 0
    for box in boxes.keys():
        if boxes[box] == "empty":
            left = left+1
    return left

# bothEndsDead: takes a chain and returns if it enclosed from both ends, aka
# the end boxes in the chain are both dead (so it can't be doube-crossed normally)
def bothEndsDead(chain):
    for box in chain:
        if box.islower() == False:
            return False
    return isDead(chain[0]) and isDead(chain[-1])

# allDeadsAre3: returns true if all dead boxes are in chains of length 3
def allDeadsAre3():
    for move in lines.keys():
        if lines[move]==0:
            if capturedBox(move,"na",'n'):
                chain=returnChain(move[0])
                if len(chain)!=3:
                    return False
    return True

# doublecross: takes a chain (of length 3) and returns a move to double-cross it
def doublecross(chain):
    if len(chain)!=3:
        return "Error"
    # if the chain opens to a direction, just fill in the end touching the
    # direction
    if chain[0].islower() == False:
        move = chain[1]+chain[0]
    elif chain[-1].islower() == False:
        move = chain[-2]+chain[-1]
    # else, find which end is dead and return the other side
    else:
        if isDead(chain[0]):
            if chain[-2]<chain[-1]:
                move = chain[-2]+chain[-1]
            else:
                move = chain[-1]+chain[-2]                      
        else:
            if chain[0]<chain[1]:
                move = chain[0]+chain[1]
            else:
                move = chain[1]+chain[0]
    return move

# fixMove: takes a move and fixes the order of boxes to convention
def fixMove(move):
    # if either part of the move is a direction, list it last
    if move[0].islower()==False:
        return move[1]+move[0]
    if move[1].islower()==False:
        return move[0]+move[1]
    # else put in alphabetical order
    if move[1]<move[0]:
        return move[1]+move[0]
    return move

# avoidLoops: looks for corners that have been created and returns a move to
# attempt to limit that corner from becoming a loop
def avoidLoops():
    # finds boxes with 2 lines filled in around them that are toucing at a corner
    for box in boxes:
        beside = boxesBeside(box)
        if len(beside)==2 and beside[0].islower() and beside[1].islower():
            for b in boxes:
                if fixMove(beside[0]+b) in lines and fixMove(beside[1]+b) in lines and b!=box:
                    move1 = fixMove(beside[0]+b)
                    move2 = fixMove(beside[1]+b)
                    # if it is free and safe, return a move to block the loop
                    if lines[move1] == 0:
                        if isSafeMove(move1):
                            return move1
                    if lines[move2] == 0:
                        if isSafeMove(move2):
                            return move2
                        break
    return False

def compScore(s_boxes):
    cs = 0
    for box in s_boxes.values():
        if box == "comp":
            cs = cs+1
    return cs

def fillInBoxes(s_boxes, s_lines, p):
    for box in s_boxes:
        fillin = True
        for line in s_lines:
            if box in line and s_lines[line] == 0:
                fillin = False
                break
        if fillin and s_boxes[box] == "empty":
            s_boxes[box] = p
    return s_boxes

def search(s_lines,s_boxes):
    s_lines = copy.deepcopy(s_lines)
    s_boxes = copy.deepcopy(s_boxes)
    if gameOver(s_boxes):
        print("found leaf")
        return compScore(s_boxes), None
    best_score = 0
    best_move = random.choice(list(lines.keys()))
    while s_lines[best_move] == 1:# or not isSafeMove(move):
        best_move = random.choice(list(lines.keys()))
    s_lines_copy_1 = copy.deepcopy(s_lines)
    s_boxes_copy_1 = copy.deepcopy(s_boxes)
    for cmove in s_lines:
        s_lines = copy.deepcopy(s_lines_copy_1)
        s_boxes = copy.deepcopy(s_boxes_copy_1)
        if s_lines[cmove] == 1:
            continue
        print("at cmoves")
        s_lines[cmove] = 1
        s_boxes = fillInBoxes(s_boxes, s_lines, "comp")
        scores = ()
        s_lines_copy_2 = copy.deepcopy(s_lines)
        s_boxes_copy_2 = copy.deepcopy(s_boxes)
        for ymove in s_lines:
            s_lines = copy.deepcopy(s_lines_copy_2)
            s_boxes = copy.deepcopy(s_boxes_copy_2)
            if s_lines[ymove] == 1:
                continue
            print("at ymoves")
            s_lines[ymove] = 1
            s_boxes = fillInBoxes(s_boxes, s_lines, "you")
            scores= scores +(search(s_lines,s_boxes)[0],)
            print(scores)
        if min(scores, default=0)>best_score:
            best_score = min(scores)
            best_move = cmove
    return best_score, best_move

def compSearchMove():
    s_lines = copy.deepcopy(lines)
    s_boxes = copy.deepcopy(boxes)
    return search(s_lines,s_boxes)[1]

# compPickMove: picks a move
def compPickMove():
    chains = returnChains()
    NE = numEmptyBoxes()
    # find if any boxes can be captured
    for move in lines.keys():
        if lines[move] == 0:
            if capturedBox(move,"na",'n'):
                # if yes, get the chain that that box is a part of
                if isDead(move[0]):
                    chain = returnChain(move[0])
                else:
                    chain = returnChain(move[1])
                # if the chain is of length 3 and there are other boxes that
                # can be captured, move on to capture the other boxes first
                if len(chain)==3 and numDeadBoxes()>1:
                    # UNLESS all capturable chains are of length 3
                    if allDeadsAre3():
                        return move
                    continue
                # should comp double-cross?
                should_doublecross = True
                # if all boxes can be captured, then no
                if NE<=2 or len(chains)==1:
                    should_doublecross = False
                # count the number of chains that cannot be double-crossed (to
                # short) as well as the loops
                num_no_dc = 0
                num_loops = 0
                for ch in chains:
                    if len(ch)<=4 and ch!=chain:
                        num_no_dc = num_no_dc+1
                    if isLoop(ch) and ch!=chain:
                        num_loops = num_loops+1
                # if there is an odd number of chains that cannot be
                # double-crossed, then dont double-cross
                if num_no_dc%2 == 1:
                    should_doublecross = False
                # double chains of length 3 if we should (if longer than 3,
                # capture some of it first, if shorter, cannot double-cross)
                if len(chain)==3 and should_doublecross:
                    move = doublecross(chain)
                # next, check for loop double-crossing
                # Have to give up 4 boxes, so don't do it if can't gain more
                # than 4 boxes
                if NE-4-(len(chains)-2)*2-num_loops*2<=4:
                    should_doublecross = False
                # capture boxes until a chain of length 4 with dead ends is
                # created, then double-cross it if should
                if len(chain)==4 and bothEndsDead(chain) and should_doublecross:
                    if chain[1]<chain[2]:
                        move = chain[1]+chain[2]
                    else:
                        move = chain[2]+chain[1]
                return move
    # if no boxes can be captured, try to find a safe move
    if safeMovesLeft():
        # play to avoid loops somtimes
        loop_avoidance = 0.5
        if random.uniform(0,1)>loop_avoidance:
            move = avoidLoops()
            if move:
                return move
        # else find a random allowed and safe move
        move = random.choice(list(lines.keys()))
        while lines[move] == 1 or not isSafeMove(move):
            move = random.choice(list(lines.keys()))
        return move
    # if no safe moves are left, give up a chain as small as possible
    else:
        # find the smallest length chain or loop
        smallest = min(chains, key=len)
        for chain in chains:
            if isLoop(chain) and loopLen(chain)<len(smallest):
                smallest = chain
        # if chain is length 4 (meaning length 2 without the ends), return the
        # move in the middle to prevent double-crossing
        if len(smallest) == 4:
            if smallest[1]<smallest[2] and smallest[1].islower():
                move = smallest[1]+smallest[2]
            else:
                move = smallest[2]+smallest[1]
            return move
        # else, randomly choose a valid move within the smallest chain
        move = random.choice(list(lines.keys()))
        good = False
        while not good:
            move = random.choice(list(lines.keys()))
            for c in move:
                if c.islower() and c in smallest and lines[move]==0:
                    good = True
        return move

# printScore: prints the end of the game score onto the screen
def printScore():
    comp_score = 0
    your_score = 0
    # count each player's total
    for box in boxes.values():
        if box == "comp":
            comp_score=comp_score+1
        elif box == "you":
            your_score = your_score+1
    print("Score: Comp "+str(comp_score)+" You "+str(your_score))
    # print the winner
    if comp_score>your_score:
        print("Comp Wins!")
    elif comp_score<your_score:
        print("You Win!")
    else:
        print("It's a Tie!")

main()
