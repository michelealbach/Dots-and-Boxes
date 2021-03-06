import random

def capturedBox(move,p,update):
    foundbox = False
    for c in move:
        if c.islower():
            boxed = True
            for l in lines:
                if c in l and l != move:
                    if lines[l]==0:
                        boxed = False
                        break
            if boxed:
                if update == 'y':
                    boxes[c] = p
                foundbox = True
    return foundbox    

def gameOver():
    for box in boxes.values():
        if box=="empty":
            return False
    return True

def isDead(box):
    lines_around = 0
    for move in lines.keys():
        if box in move:
            if lines[move]==1:
                lines_around = lines_around+1
    if lines_around == 3:
        return True
    return False    

def numDeadBoxes():
    num_dead_boxes = 0
    for box in boxes.keys():
        if isDead(box):
            num_dead_boxes = num_dead_boxes+1
    return num_dead_boxes

def isSafeMove(move):
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
    
def safeMovesLeft():
    for move in lines.keys():
        if lines[move]==0 and isSafeMove(move):
            return True
    return False

def boxesBeside(box):
    boxes_beside = []
    if box.islower() == False:
        return boxes_beside
    for line in lines.keys():
        if box in line and lines[line]==0:
            for c in line:
                if c!=box:
                    boxes_beside.append(c)
    return boxes_beside
        
def returnChains():
    chains = []
    for box in boxes.keys():
#        print(box)
        if any(box in chain for chain in chains):
#            print("skipped!")
            continue
        boxes_beside = boxesBeside(box)
 #       print(boxes_beside)
        if len(boxes_beside)==2:
 #           print("making a chain")
            chain = [boxes_beside[0],box,boxes_beside[1]]
            boxes_beside_l = boxesBeside(boxes_beside[0])
            next_last_box = boxes_beside[0]
            last_box=box
            while len(boxes_beside_l)==2:
  #              print(boxes_beside_l)
                box_1 = boxes_beside_l[0]
                box_2 = boxes_beside_l[1]
                if box_1!=last_box:
                    if box_1 in chain and box_1.islower():
                        chain.insert(0,box_1)
                        break
                    chain.insert(0,box_1)
                    boxes_beside_l = boxesBeside(box_1)
                    last_box = next_last_box
                    next_last_box = box_1
                else:
                    if box_2 in chain and box_2.islower():
                        chain.insert(0,box_2)
                        break
                    chain.insert(0,box_2)
                    boxes_beside_l = boxesBeside(box_2)
                    last_box = next_last_box
                    next_last_box = box_2
            boxes_beside_r = boxesBeside(boxes_beside[1])
            next_last_box = boxes_beside[1]
            last_box = box
            while len(boxes_beside_r)==2:
   #             print(boxes_beside_r)
                box_1 = boxes_beside_r[0]
                box_2 = boxes_beside_r[1]
                if box_1!=last_box:
                    if box_1 in chain and box_1.islower():
                        chain.append(box_1)
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
            chains.append(chain)
    return chains

def returnChain(box):
    chains = returnChains()
    for chain in chains:
        if box in chain:
            return chain
    return []

def numEmptyBoxes():
    left = 0
    for box in boxes.keys():
        if boxes[box] == "empty":
            left = left+1
    return left

def allDeadsAre3():
    for move in lines.keys():
        if lines[move]==0:
            if capturedBox(move,"na",'n'):
                chain=returnChain(move[0])
                if len(chain)!=3:
                    return False
    return True
        
def compPickMove():
    chains = returnChains()
    for move in lines.keys():
        if lines[move] == 0:
            if capturedBox(move,"na",'n'):
                if isDead(move[0]):
                    chain = returnChain(move[0])
                else:
                    chain = returnChain(move[1])
                #print(chain)
                if len(chain)==3 and numDeadBoxes()>1:
                    if allDeadsAre3():
                        return move
                    continue
                only_long_left = True
                for ch in chains:
                    if len(ch)<=4 and ch!=chain:
                        only_long_left = False
                        break
                if len(chain)==3 and numEmptyBoxes()>2 and only_long_left:
                    if chain[0].islower() == False:
                        move = chain[1]+chain[0]
                    elif chain[-1].islower() == False:
                        move = chain[-2]+chain[-1]
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
                #print(move)
                return move
    if safeMovesLeft():
        move = random.choice(list(lines.keys()))
        while lines[move] == 1 or not isSafeMove(move):
            move = random.choice(list(lines.keys()))
        return move
    else:
        smallest = min(chains, key=len)
        if len(smallest) == 4:
            if smallest[1]<smallest[2] and smallest[1].islower():
                move = smallest[1]+smallest[2]
            else:
                move = smallest[2]+smallest[1]
            return move
        move = random.choice(list(lines.keys()))
        good = False
        while not good:
            move = random.choice(list(lines.keys()))
            for c in move:
                if c.islower() and c in smallest and lines[move]==0:
                    good = True
        return move

def printScore():
    comp_score = 0
    your_score = 0
    for box in boxes.values():
        if box == "comp":
            comp_score=comp_score+1
        elif box == "you":
            your_score = your_score+1
    print("Score: Comp "+str(comp_score)+" You "+str(your_score))
    if comp_score>your_score:
        print("Comp Wins!")
    elif comp_score<your_score:
        print("You Win!")
    else:
        print("It's a Tie!")


bs = int(input("what square board size would you like to play? "))
boxes = {}
a = ord('a')
for box in range(bs*bs):
    boxes[chr(a+box)] = "empty"
print(boxes)
lines = {}
for s in range(bs):
    lines[chr(a+s)+'N'] = 0
    for row in range(bs-1):
        lines[chr(a+s+bs*row)+chr(a+s+bs*(row+1))] = 0
    lines[chr(a+s+bs*(bs-1))+'S'] = 0
    lines[chr(a+bs*s)+'W'] = 0
    for col in range(bs-1):
        lines[chr(a+bs*s+col)+chr(a+bs*s+(col+1))] = 0
    lines[chr(a+bs*s+(bs-1))+'E'] = 0
print(lines)
#boxes = {'a':"empty",'b':"empty",'c':"empty",'d':"empty",'e':"empty",'f':"empty",'g':"empty",'h':"empty",'i':"empty"}
#lines = {'aN':1,'bN':1,'cN':0,'ad':0,'be':1,'cf':1,'dg':1,'eh':0,'fi':0,'gS':0,'hS':1,'iS':1,'aW':1,'dW':0,'gW':1,'ab':0,'de':1,'gh':0,'bc':0,'ef':0,'hi':1,'cE':1,'fE':0,'iE':0}
moves = 0
max_moves = 2*bs*(bs+1)
game_over = False
while moves < max_moves and not game_over:
    # you move
    ycont = True
    while ycont and not game_over:
        yplay = input("what move would you like to play? ")
        while yplay not in lines or lines[yplay] == 1:
            if yplay in lines:
                print("There is already a line there")
            else:
                print("Not a valid move")
            yplay = input("what move would you like to play? ")
        lines[yplay] = 1
        moves = moves + 1
        ycont = capturedBox(yplay,"you",'y')
        if ycont:
            print("You captured a box!")
        game_over = gameOver()
    # comp move
    ccont = True
    while ccont and not game_over:
        print("Making my move...")
        cplay = compPickMove()
        lines[cplay] = 1
        moves = moves + 1
        print("I play " + cplay)
        ccont = capturedBox(cplay,"comp",'y')
        if ccont:
            print("Comp captured a box!")
        game_over = gameOver()
printScore()
