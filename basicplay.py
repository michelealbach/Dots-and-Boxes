import random

def capturedBox(move,p,update):
    foundbox = False
    for c in move:
        if c.isdigit():
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
    

def isSafeMove(move):
    for c in move:
        if c.isdigit():
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

def compPickMove():
    for move in lines.keys():
        if lines[move] == 0:
            if capturedBox(move,"na",'n'):
                return move
    if safeMovesLeft():
        move = random.choice(list(lines.keys()))
        while lines[move] == 1 or not isSafeMove(move):
            move = random.choice(list(lines.keys()))
        return move
    else:
        move = random.choice(list(lines.keys()))
        while lines[move]:
            move = random.choice(list(lines.keys()))
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

boxes = {'1':"empty",'2':"empty",'3':"empty",'4':"empty",'5':"empty",'6':"empty",'7':"empty",'8':"empty",'9':"empty"}
lines = {'1n':0,'2n':0,'3n':0,'14':0,'25':0,'36':0,'47':0,'58':0,'69':0,'7s':0,'8s':0,'9s':0,'1w':0,'4w':0,'7w':0,'12':0,'45':0,'78':0,'23':0,'56':0,'89':0,'3e':0,'6e':0,'9e':0}
moves = 0
game_over = False
while moves < 24 and not game_over:
    # you move
    ycont = True
    while ycont and not game_over:
        yplay = input("what move would you like to play? ")
        while lines[yplay] == 1:
            print("There is already a line there")
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
