import numpy as np
import matplotlib.pyplot as plt
import math
import json
import signal
import random

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
            
            0: " ",
            1: "X",
            -1: "O",
            "0": " ",
            "1": "X",
            "-1":"O"
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

class NeuralNetwork:

    def __init__(self, save_name):

        self.save_name = save_name

        with open(f"{self.save_name}.json", "r") as f:

            data = json.load(f)

            self.w1, self.w2, self.w3 = [np.matrix(i) for i in data[0]]
            self.b1, self.b2, self.b3 = [np.matrix(i) for i in data[1]]

        print("\nSUCCESSFULLY LOADED DATA\n")
            

        self.parameter_width = 6

    def _relu(self, x):

        return np.maximum(0,x)

    def _softmax(self,x):

        return(np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())
    
    def predict(self, input_vector):

        self.h1_z = np.dot(input_vector, self.w1) + self.b1
        self.h1_activation = self._relu(self.h1_z)

        self.h2_z = np.dot(self.h1_activation, self.w2) + self.b2
        self.h2_activation = self._relu(self.h2_z)

        self.output_z = np.dot(self.h2_activation, self.w3) + self.b3
        self.output_activation = self._softmax(self.output_z)

        return self.output_activation
    
    def _compute_cross_entropy_loss(self, target_list, prediction_list):
        
        target_list = np.float_(target_list)
        prediction_list = np.float_(prediction_list)
        losses = []
        
        for t,p in zip(target_list, prediction_list):
            loss = -np.sum(t * np.log(p))
            losses.append(loss)
            
        return np.sum(losses)


'''input_vectors = np.array(
        
[[-1, -1, 1, 0, 0, 1, 0, 0, 0], [1, -1, 0, 0, 1, 0, 1, -1, -1], [-1, -1, 0, 1, 1, -1, 1, 0, 0], [0, -1, -1, 1, 0, 0, 1, -1, 1], [0, 1, 1, 0, -1, 0, -1, 1, -1], [1, 0, -1, 1, 0, 1, -1, 0, -1], [1, 0, -1, -1, 1, 0, 1, -1, 0], [1, 0, 0, -1, -1, 1, -1, 0, 1], [0, 1, 1, 0, -1, -1, 1, -1, 0], [1, 0, 1, -1, 0, -1, -1, 1, 0], [0, -1, -1, 1, 0, 1, 1, 0, -1], [-1, 0, -1, 1, 0, 1, -1, 0, 1], [1, 1, -1, 0, 0, -1, 0, -1, 1], [-1, 0, 1, 1, 0, 0, -1, -1, 1], [0, -1, 0, 1, 1, -1, -1, 0, 1], [0, -1, 1, 0, 1, 0, -1, -1, 1], [1, -1, 1, -1, 1, -1, 0, 0, 0], [-1, 1, -1, 0, 1, 1, 1, -1, -1], [0, -1, -1, 1, -1, 0, 1, 1, 0], [1, -1, 0, 0, 1, 0, 0, -1, 0], [-1, 1, 0, 1, 1, -1, 0, 0, -1], [1, 1, -1, -1, 1, 1, -1, -1, 0], [0, 1, 0, -1, 1, 0, 0, 0, -1], [1, 1, 0, -1, 1, -1, 0, 0, -1], [-1, 1, 0, -1, 1, 0, 1, -1, 0], [1, 1, 0, -1, -1, 0, 0, -1, 1], [-1, -1, 1, 0, 1, -1, 0, 0, 1], [-1, 0, 1, -1, 1, -1, 0, 1, 0], [0, 0, -1, 0, 1, 1, -1, 0, 0], [0, -1, 1, 1, 0, -1, 1, -1, 0], [-1, -1, 0, 0, 0, 1, -1, 1, 1], [-1, 1, 1, 0, 0, -1, 1, -1, 0], [-1, 1, 1, 0, 1, 0, -1, 0, -1], [-1, 0, 0, 0, 0, -1, 1, 1, 0], [0, -1, -1, 0, 1, 1, 0, 0, 0], [0, 0, 1, -1, 1, -1, 0, 0, 0], [-1, -1, 1, 1, 0, -1, 1, -1, 1], [0, 0, 0, 0, 1, -1, 0, -1, 1], [0, -1, -1, 1, 1, 0, -1, 1, 0], [0, -1, 1, 0, 1, 1, 0, -1, -1], [1, 1, 0, 0, -1, 1, -1, -1, 0], [-1, -1, 0, -1, 1, 1, 1, 1, -1], [-1, 1, 0, 0, 0, -1, 0, 1, 0], [0, 1, 1, -1, 1, -1, 0, 0, -1], [1, 1, 0, 0, 0, -1, -1, -1, 1], [0, -1, 1, 0, 1, 1, -1, -1, 0], [-1, 0, 1, 0, -1, -1, 1, 1, 0], [0, 0, 1, -1, 0, -1, 1, -1, 1], [0, -1, 1, 0, 0, 0, 0, -1, 1], [1, 0, 1, 1, -1, 0, 0, -1, -1], [-1, 1, -1, 1, 0, 1, -1, 0, 0], [-1, 0, 0, 1, 1, -1, 1, -1, 0], [0, -1, -1, 1, 1, -1, -1, 1, 1], [-1, 0, 1, 1, 0, 0, 1, -1, -1], [1, 0, -1, 1, -1, 1, 0, 0, -1], [0, -1, 0, -1, 0, 0, 0, 1, 1], [0, 0, -1, 0, 1, 1, -1, 1, -1], [1, 0, 1, 0, -1, -1, 1, 0, -1], [-1, 1, 1, -1, 0, 0, 0, 1, -1], [0, 0, -1, 1, 0, -1, 1, 0, 0], [0, 1, 1, -1, 0, 1, -1, -1, 0], [1, 0, 1, 0, -1, 0, 0, 0, -1], [1, -1, 1, 0, -1, 1, -1, 0, 0], [1, 0, 0, -1, 1, 0, -1, 0, 0], [0, 1, 0, -1, 0, -1, 0, 1, 0], [1, 0, 0, -1, 1, -1, 0, 0, 0], [-1, 0, 1, 1, 0, -1, 1, -1, 0], [1, 0, -1, -1, 1, 0, 0, 1, -1], [1, -1, 0, 0, 1, 0, -1, 0, 0], [-1, 1, 1, -1, 0, -1, 1, 0, 0], [-1, 1, 0, -1, 0, -1, 0, 1, 1], [0, 1, 0, 0, -1, 1, -1, -1, 1], [-1, -1, 1, 1, 1, 0, 0, -1, 0], [1, -1, 1, 0, 0, -1, 0, -1, 1], [0, 1, 1, 0, 0, 0, 0, -1, -1], [0, 0, 1, 1, -1, 0, -1, -1, 1], [1, 1, 0, -1, 1, -1, -1, 0, 0], [1, 1, -1, -1, 0, -1, 0, 1, 0], [0, -1, -1, 1, 0, 1, -1, 0, 1], [0, -1, 1, 0, 0, 0, 1, -1, 0], [-1, -1, 0, -1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 0, 1, -1, 0, -1], [-1, 1, 0, -1, 1, 1, 0, 0, -1], [1, 0, -1, 1, 1, 0, -1, 0, -1], [1, -1, 0, -1, 1, -1, 0, 1, 0], [0, 1, -1, 1, 1, -1, -1, -1, 1], [1, 0, 0, 0, 0, -1, 0, -1, 1], [1, 1, 0, -1, 1, 0, 0, -1, -1], [-1, 1, 1, 0, -1, 1, 0, -1, 0], [0, -1, 0, 0, 1, 1, -1, -1, 1], [1, -1, 0, 0, 0, -1, 1, 1, -1], [0, 1, 1, -1, 1, -1, -1, -1, 1], [-1, 0, 0, -1, 1, 0, 1, -1, 1], [0, -1, 0, 0, 1, 1, 0, -1, 0], [1, 0, 1, 0, -1, -1, 0, 1, -1], [1, -1, 0, 1, 0, 0, 0, 0, -1], [-1, 1, 0, 0, 1, 0, 0, 0, -1], [1, 0, 1, -1, 0, -1, 0, -1, 1], [1, -1, 0, 1, 0, 0, 0, -1, 0], [-1, -1, 1, -1, 1, 1, 0, 1, -1], [0, 0, 0, 1, 1, -1, -1, -1, 1], [1, 0, -1, 1, 0, 1, -1, -1, 0], [1, 0, 1, -1, 0, -1, 1, -1, 0], [1, 1, 0, -1, -1, 0, 0, 1, -1], [1, -1, -1, -1, 0, 1, -1, 1, 1], [1, 0, -1, 0, 0, 1, 1, -1, -1], [1, 1, -1, -1, 1, -1, 0, 0, 0], [0, 0, 0, -1, 1, 0, -1, 0, 1], [-1, -1, 1, 1, 1, 0, -1, -1, 1], [0, 0, 0, -1, 1, 1, -1, -1, 1], [0, 0, -1, 1, -1, 0, 1, -1, 1], [-1, 1, 0, 1, 0, -1, 0, 1, -1], [1, 1, -1, 1, 0, 0, 0, -1, -1], [0, 0, 0, -1, 0, -1, 1, 0, 1], [1, -1, 0, 1, 0, 1, -1, -1, 0], [-1, 1, -1, -1, 0, 0, 1, 0, 1], [0, 1, 0, -1, 1, -1, 1, 0, -1], [1, 1, 0, 0, 1, -1, -1, 0, -1], [-1, 0, 0, 0, 0, 1, 0, -1, 1], [-1, -1, 1, -1, 0, 1, 1, 1, -1], [-1, 0, 0, 0, 1, 1, 0, -1, 0], [1, 0, 1, -1, 0, -1, 1, 0, -1], [0, 0, -1, 0, 1, 0, 0, -1, 1], [1, 0, 0, -1, 1, -1, 1, 0, -1], [1, -1, 1, 0, 0, 0, -1, -1, 1], [1, 0, 1, 0, 1, -1, 0, -1, -1], [0, -1, 1, -1, 0, -1, 0, 1, 1], [0, 0, 0, 1, 0, 1, -1, -1, 0], [0, 1, 1, 0, -1, -1, 0, -1, 1], [1, 0, -1, 0, -1, -1, 0, 1, 1], [1, 0, -1, 1, 0, -1, -1, 0, 1], [-1, 1, -1, 0, 1, 1, -1, -1, 1], [0, 0, -1, 0, 0, -1, 1, 0, 1], [1, 0, -1, 0, -1, 1, 1, -1, 0], [-1, 1, 0, 0, 0, 0, 0, 1, -1], [-1, 0, 1, 0, 0, 0, -1, 0, 1], [0, -1, 1, 0, -1, 1, 0, 0, 0], [-1, 0, 0, -1, 0, 0, 1, 1, 0], [-1, -1, 1, -1, 0, 0, 1, 1, 0], [1, 0, -1, -1, 0, -1, 0, 1, 1], [-1, 0, -1, 0, 1, -1, 0, 1, 1], [0, 0, 0, 0, 1, -1, -1, 0, 1], [1, 1, -1, 0, -1, 0, 1, -1, 0], [-1, -1, 1, 1, 0, 1, 1, -1, -1], [1, 0, 0, 0, 0, -1, -1, 0, 1], [-1, 0, 0, 0, 1, -1, 1, -1, 1], [1, -1, 0, -1, -1, 0, 1, 1, 0], [0, 1, 1, 1, -1, -1, 0, 0, -1], [1, 1, -1, 0, 0, -1, 1, -1, 0], [1, 1, 0, 1, -1, 0, -1, -1, 0]]
)

targets = np.array(
    [[0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0]]
)'''
                 

save_name = "trainedAIWeights"


neural_network = NeuralNetwork(save_name)

x = game()

'''for instance in range(len(input_vectors)):

    if np.argmax(neural_network.predict(input_vectors[instance])) != np.argmax(targets[instance]):

        x.renderBoard([input_vectors[instance][:3], input_vectors[instance][3:6], input_vectors[instance][6:]])

print(f"\nACCURACY: {100 * sum([not (np.argmax(targets[x]) ^ np.argmax(neural_network.predict(input_vectors[x]))).tolist() for x in range(len(input_vectors))]) / len(input_vectors)}")'''

@gameStructure

def AIGame(turn, player):
    
    if turn == player:
        
        move = getUserMove(turn)
        print(move)
        x.playMove(move,turn)
    
        return [False, None]
    
    else:

        instance = x.instance[0] + x.instance[1] + x.instance[2]
        instance = [int(i) for i in instance]
        
        rawPrediction = np.argmax(neural_network.predict(instance))

        row, column = rawPrediction // 3, rawPrediction % 3

        if x.checkMoveValidity([row,column]) == True:
            move = [row, column]
            x.playMove(move, turn)

        else:

            print("AI made a mistake: Playing Random Move")
            move = random.choice(x.getPossibleMoves())
            x.playMove(move,turn)

        return [True, move]


global playerSide
global aiSide
playerSide = "-1"
aiSide = inverse(playerSide)

AIGame(playerSide)
