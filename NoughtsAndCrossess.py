import random
import math

class game():

    def __init__(self):
        
        print("Initializing Game Class")
        self.generateInstance()

    def generateInstance(self):
        
        self.instance = [
                        ["0", "0", "0"],
                        ["0", "0", "0"],
                        ["0", "0", "0"]
                        ]
    
    def renderBoard(self, inputInstance = None): #procedure to print the current position of the board

        if inputInstance == None: 

            inputInstance = self.instance
        
        conversion = {
            
            "0": " ",
            "1": "X",
            "-1": "O",
        }
        print("\n\nCurrent Board Position:\n")
        
        for i in range(3):
            
            sublist = []
            for j in inputInstance[i]:
                sublist.append(conversion[j])

            print("321"[i], " |", sublist[0], "|", sublist[1], "|", sublist[2], "|")

            if i != 2:
                print("   ─────────────")
            else:
                print("\n     a   b   c\n\n")

    def copyState(self, gameInstance=None): #generates a copy of the game instance

        if gameInstance == None: 

            gameInstance = self.instance
        
        self.copiedState = []
        for i in range(3):
            sublist = []
            for j in range(3):
                sublist.append(gameInstance[i][j])
            self.copiedState.append(sublist)

        return self.copiedState
        
    def playMove(self, position, turn, inputInstance = None): #plays a move on the inputted board
        
        if inputInstance == None: 

            inputInstance = self.instance

        inputInstance[int(position[0])][int(position[1])] = turn

        self.updatedBoard = inputInstance
        
        return self.updatedBoard
    
    def checkMoveValidity(self, position, inputInstance = None): #checks a move's validity 

        if inputInstance == None: 

            inputInstance = self.instance

        if inputInstance[int(position[0])][int(position[1])] == "0":

            return True
    
        else:

            return False
        
    def checkEndConditions(self, inputInstance = None): #checks to see if a player have won, or if it is a draw

        if inputInstance == None: 

            inputInstance = self.instance

        conditions = [["00", "01", "02"],["10", "11", "12"], ["20", "21", "22"], 
                        ["00", "10", "20"], ["01", "11", "21"], ["02", "12", "22"],
                        ["00", "11", "22"], ["02", "11", "20"]
                        ]
        
        for c in conditions:

            if inputInstance[int(c[0][0])][int(c[0][1])] == "1" and  inputInstance[int(c[1][0])][int(c[1][1])] == "1" and inputInstance[int(c[2][0])][int(c[2][1])] == "1":

                self.result = "CROSSES"
                return ["CROSSES", "1"]

            if inputInstance[int(c[0][0])][int(c[0][1])] == "-1" and  inputInstance[int(c[1][0])][int(c[1][1])] == "-1" and  inputInstance[int(c[2][0])][int(c[2][1])] == "-1":

                self.result = "NOUGHTS"
                return ["NOUGHTS", "-1"]

        draw = True
        for i in inputInstance:
            for j in i:
                if j == "0":
                    draw = False
        if draw == True:
            self.result = "DRAW"
            return ["DRAW", "0"]

        self.result = "NONE"
        return ["NONE", None]
    
    def getPossibleMoves(self, inputInstance = None): #gets the positions of all remaining empty positions
        
        if inputInstance == None: 

            inputInstance = self.instance

        self.possibleMoves = []
        for i in range(3):
            for j in range(3):
                if inputInstance[i][j] == "0":
                    self.possibleMoves.append(str(i) + str(j))

        return self.possibleMoves

def inverse(turn):

    if turn == "1":

        return "-1"
    
    else:

        return "1"
    
def decodeMove(move): #decodes a user-inputted move
        
        abcvalues = ["a", "b", "c"]
        numvalues = ["3", "2", "1"]

        if move[0].lower() not in abcvalues or move[1] not in numvalues:
            
            return "INVALID"
        
        decodedMove = str(numvalues.index(str(move[1]))) + str(abcvalues.index(move[0].lower()))
        
        return decodedMove    

def getUserMove(turn):
    
    validMove = False 

    while validMove == False:

        validMove = True

        if turn == "1":

            userInput = input("\nCrosses' Turn: ")

        elif turn == "-1":

            userInput = input("\nNoughts' Turn: ")

        if len(userInput) < 2:
            print("\nINVALID\nPlease Type a Valid Coordinate ie: a1")
            validMove = False
            continue

        if (move:=decodeMove(userInput)) == "INVALID":
            validMove = False
            print("\nINVALID\nPlease Type a Valid Coordinate ie: a1")
            continue

        if x.checkMoveValidity(move, x.instance) == False:
            validMove = False
            print("\nINVALID\nThis Coordinate is Already Occupied! Please Choose Another Square")
    
    return move

def gameStructure(gameProcedure):

    def gameWrap(*args, **kwargs):

        turn = "1" #Crosses
        x.renderBoard()
        print("This is the board. To enter a move, type the letter corresponding to the column followed by the number corresponding to the row. ie: b2")

        while x.checkEndConditions()[0] == "NONE":
            
            showRender = gameProcedure(turn, *args, **kwargs)

            if turn == "1":

                turn = "-1"
            else:
                turn = "1"
            
            if showRender[0] == True:

                x.renderBoard()
            
            if showRender[1] != None:

                print("AI played: " + "abc"[int(showRender[1][1])] + "321"[int(showRender[1][0])])

        if showRender[0] == False:

            x.renderBoard()
        
        if x.result == "CROSSES":

            print("\nCrosses Win!")

        elif x.result == "NOUGHTS":

            print("\nNoughts Win!")

        else:
            
            print("\nThe game is a Draw")

    return gameWrap


@gameStructure

def twoPlayerGame(turn):

    move = getUserMove(turn)
    x.playMove(move, turn)
    return [True, None]

@gameStructure

def randomAIGame(turn, player):

    if turn == player:
        
        move = getUserMove(turn)
        x.playMove(move,turn)
        return [False, None]
    
    else:

        move = random.choice(x.getPossibleMoves())
        x.playMove(move,turn)
        return [True, move]

@gameStructure

def defensiveAIGame(turn, player):
    
    if turn == player:
        
        move = getUserMove(turn)
        x.playMove(move,turn)
        return [False, None]
    
    else:

        defensiveOptions = []

        for i in x.getPossibleMoves():

            visualisedResult = x.checkEndConditions(x.playMove(i, inverse(turn), x.copyState()))

            if visualisedResult[1] == player:

                defensiveOptions.append(i) 


        if defensiveOptions:

            x.playMove((move:=random.choice(defensiveOptions)), turn)
            return [True, move]

        x.playMove((move:=random.choice(x.getPossibleMoves())), turn)
        return [True, move]

@gameStructure

def offensiveAIGame(turn, player):

    if turn == player:

        move = getUserMove(turn)
        x.playMove(move,turn)
        return[False, None]
    
    else: 

        offensiveOptions = []

        for i in x.getPossibleMoves():

            visualisedResult = x.checkEndConditions(x.playMove(i, turn, x.copyState()))

            if visualisedResult[1] == inverse(player):

                offensiveOptions.append(i)

        if offensiveOptions:

            x.playMove((move:=random.choice(offensiveOptions)), turn)
            return[True, move]
        
        x.playMove((move:=random.choice(x.getPossibleMoves())),turn)
        return[True, move]

@gameStructure
def offensiveDefensiveAIGame(turn, player):
    
    if turn == player:

            move = getUserMove(turn)
            x.playMove(move,turn)
            return[False, None]
        
    else: 

        offensiveOptions = []
        defensiveOptions = []

        for i in x.getPossibleMoves():

            visualisedDefensiveResult = x.checkEndConditions(x.playMove(i, inverse(turn), x.copyState()))
            visualisedOffensiveResult = x.checkEndConditions(x.playMove(i, turn, x.copyState()))

            if visualisedOffensiveResult[1] == inverse(player):

                offensiveOptions.append(i)

            if visualisedDefensiveResult[1] == player:

                defensiveOptions.append(i)

        if offensiveOptions:

            x.playMove((move:=random.choice(offensiveOptions)), turn)
            return[True, move]
        
        if defensiveOptions:

            x.playMove((move:=random.choice(defensiveOptions)), turn)
            return[True, move]
        
        x.playMove((move:=random.choice(x.getPossibleMoves())),turn)
        return[True, move]
    

@gameStructure

def minimaxAIGame(turn, player):

    if turn == player:

            move = getUserMove(turn)
            x.playMove(move,turn)
            return[False, None]
        
    else: 

        global searchCount
        searchCount = 0

        x.playMove((move:=random.choice(minimax(x.instance, 0, True, player))), turn)

        print("\n" + str(searchCount) + " visualizations made")

        return[True, move]
    
@gameStructure

def minimaxAIGameWithPruning(turn, player):

    if turn == player:

            move = getUserMove(turn)
            x.playMove(move,turn)
            return[False, None]
        
    else: 

        global searchCount
        searchCount = 0

        x.playMove((move:=minimaxWithPruning(x.instance, 0, True, -math.inf, math.inf, player)), turn)

        print("\n" + str(searchCount) + " visualizations made")

        return[True, move]
    

def minimax(inputInstance, depth, maximize, player):

    global searchCount
    searchCount += 1

    bestMoves = []

    checkGameStatus = x.checkEndConditions(inputInstance)[1]
    
    if checkGameStatus == inverse(player): 

        return 10 - depth
    
    if checkGameStatus == player:

        return depth - 10
    
    if checkGameStatus == "0":

        return 0
    
    if maximize == True: 

        maximumEvaluation = -(math.inf)

        for position in x.getPossibleMoves(inputInstance):

            evaluation = minimax(x.playMove(position, inverse(player), x.copyState(inputInstance)), depth+1, False, player)

            if evaluation > maximumEvaluation:

                maximumEvaluation = evaluation

                if depth == 0:

                    bestMoves = [position]


            elif evaluation == maximumEvaluation and depth == 0:

                bestMoves.append(position)

        if depth == 0:

            return bestMoves
        
        return maximumEvaluation

    else:
        
        minimumEvaluation = (math.inf)

        for position in x.getPossibleMoves(inputInstance):

            evaluation = minimax(x.playMove(position, player, x.copyState(inputInstance)), depth+1, True, player)

            if evaluation < minimumEvaluation:

                minimumEvaluation = evaluation
                
                if depth == 0:

                    bestMoves = [position]

            elif evaluation == minimumEvaluation and depth == 0:

                bestMoves.append(position)

        if depth == 0:

            return bestMoves
        
        return minimumEvaluation
    

def minimaxWithPruning(inputInstance, depth, maximize, alpha, beta, player):

    global searchCount
    searchCount += 1

    bestMoves = []

    checkGameStatus = x.checkEndConditions(inputInstance)[1]
    
    if checkGameStatus == inverse(player): 

        return 10 - depth
    
    if checkGameStatus == player:

        return depth - 10
    
    if checkGameStatus == "0":

        return 0
    
    if maximize == True: 

        maximumEvaluation = -(math.inf)

        for position in x.getPossibleMoves(inputInstance):

            evaluation = minimaxWithPruning(x.playMove(position, inverse(player), x.copyState(inputInstance)), depth+1, False, alpha, beta, player)

            if evaluation > maximumEvaluation:

                maximumEvaluation = evaluation

                if depth == 0:

                    bestMove = position
                
            alpha= max(alpha, evaluation)

            if beta <= alpha:

                break

        if depth == 0:

            return bestMove
        
        return maximumEvaluation

    else:
        
        minimumEvaluation = (math.inf)

        for position in x.getPossibleMoves(inputInstance):

            evaluation = minimaxWithPruning(x.playMove(position, player, x.copyState(inputInstance)), depth+1, True, alpha, beta, player)

            if evaluation < minimumEvaluation:

                minimumEvaluation = evaluation
                
                if depth == 0:

                    bestMove = position

            beta = min(beta, evaluation)

            if beta <= alpha:

                break

        if depth == 0:

            return bestMove
        
        return minimumEvaluation

introduction = "This program run the popular game 'Noughts and Crosses' in a console environment"
mainMenuInstructions = "\n\nPlease Select your gamemode: \n1- 2 Player \n2- AI\n"

def basicMenu(restart):
  

  if restart != True:
    print(introduction)

  else:

    print("Please enter a valid option")
  
  print(mainMenuInstructions)
  userChoice = input("")

  if userChoice == "1":

    print("You have chosen the 2 player mode\n\nTo play a move, type the corresponding letter followed by the corresponding number, ie: (a1), not (1a)\n")
    twoPlayerGame()



  elif userChoice == "2":

    #run AI code

    menuAI(False)

  else:

    #replit.clear
    basicMenu(True)

def pickCharacter(restart):
  if restart == True:
    print("\nPlease Enter A Valid Option")
  print("\nDo you want to play as noughts or as crosses?\n\n1- Crosses \n2- Noughts")
  userChoice = input("\n")

  if userChoice == "1":
    return "1"
  elif userChoice == "2":
    return "-1"
  
def menuAI(restart):
  
  
    aiIntroduction = "You have chosen to take on the AI"

    if restart == True:

        print(aiIntroduction)

    else:

        print("Please enter a valid option")
    

        print("\nSelect your Oppenent:\n \n1- Random\n2- Defensive \n3- Offensive\n4- Offensive Defensive \n5- Minimax \n6- Optimized Minimax")
            
        userChoice = input("\n")

    if userChoice == "1":

        player = pickCharacter(False)
        while not player:
            player = pickCharacter(True)

        randomAIGame(player)


    elif userChoice == "2":

        player = pickCharacter(False)
        while not player:
            player = pickCharacter(True)

        defensiveAIGame(player)

    elif userChoice == "3":

        player = pickCharacter(False)
        while not player:
            player = pickCharacter(True)

        offensiveAIGame(player)

    elif userChoice == "4":

        player = pickCharacter(False)
        while not player:
            player = pickCharacter(True)

        offensiveDefensiveAIGame(player)

    elif userChoice == "5":

        player = pickCharacter(False)
        while not player:
            player = pickCharacter(True)

        minimaxAIGame(player)

    elif userChoice == "6":

        player = pickCharacter(False)
        while not player:
            player = pickCharacter(True)

        minimaxAIGameWithPruning(player)

    else:

        menuAI(restart=True)

running = True
while running == True:

    x = game()

    basicMenu(restart=False)

    valid = False

    while valid == False:

        if again:=input("\nWould you like to play again? Y/N: ").upper() in ["N", "Y"]:
            valid = True
            if again == "N": 
                running = False
