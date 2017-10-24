# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 17:10:15 2016

@author: aishasiddiq
"""
import copy

class Agent():
    
    def __init__(self): 
        self.board = {}
        self.frontier = set()
        self.currentCoordinate = (0,0)
        self.directionFacing = "east"
        self.lastMove = "none"
        self.treasure = False
        self.count = 0
        self.stepList = []
        self.recursionBoard = {}
        self.noWumpus = False
        self.arrow = 1
        
    def update_board(self, coordinate, status):
        self.board[coordinate] = status
    
    def forward_currentCoordinate(self):
        if self.directionFacing == "east":
            self.currentCoordinate = (self.currentCoordinate[0]+1, self.currentCoordinate[1])
        elif self.directionFacing == "west":
            self.currentCoordinate = (self.currentCoordinate[0]-1, self.currentCoordinate[1])
        elif self.directionFacing == "north":
            self.currentCoordinate = (self.currentCoordinate[0], self.currentCoordinate[1]-1)
        elif self.directionFacing == "south":
            self.currentCoordinate = (self.currentCoordinate[0], self.currentCoordinate[1]+1)
    
    def undo_currentCoordinate(self):
        if self.directionFacing == "east":
            self.currentCoordinate = (self.currentCoordinate[0]-1, self.currentCoordinate[1])
        elif self.directionFacing == "west":
            self.currentCoordinate = (self.currentCoordinate[0]+1, self.currentCoordinate[1])
        elif self.directionFacing == "north":
            self.currentCoordinate = (self.currentCoordinate[0], self.currentCoordinate[1]+1)
        elif self.directionFacing == "south":
            self.currentCoordinate = (self.currentCoordinate[0], self.currentCoordinate[1]-1)
    
    def update_directionFacing(self):
        if self.lastMove == "right":
            if self.directionFacing == "east":
                self.directionFacing = "south"
            elif self.directionFacing == "south":
                self.directionFacing = "west"
            elif self.directionFacing == "west":
                self.directionFacing = "north"
            elif self.directionFacing == "north":
                self.directionFacing = "east"
        if self.lastMove == "left":
            if self.directionFacing == "east":
                self.directionFacing = "north"
            elif self.directionFacing == "south":
                self.directionFacing = "east"
            elif self.directionFacing == "west":
                self.directionFacing = "south"
            elif self.directionFacing == "north":
                self.directionFacing = "west"

    def update_variables(self, percepts):
        currentPercepts = percepts
        
        if self.lastMove == "right" or self.lastMove == "left":
            self.update_directionFacing()
        if self.lastMove == "forward":
            self.forward_currentCoordinate()            
        
        self.update_board(self.currentCoordinate, currentPercepts)
        
        if "Bump" in currentPercepts and self.lastMove == "forward":
            self.undo_currentCoordinate()            
        
        self.count += 1
    
    def calculate_frontier(self):
        self.frontier = set()
        for x, y in self.board:
            if self.noWumpus:
                if "Stench" in self.board[x,y]:
                    self.board[x,y].remove("Stench")
                if "Scream" in self.board[x,y]:
                    self.board[x,y].remove("Scream")
            if len(self.board[x,y]) == 0:
                if (x+1, y) not in self.board:
                    self.frontier.add((x+1,y))
                if (x, y+1) not in self.board:
                    self.frontier.add((x,y+1))
                if x-1 >= 0 and (x-1, y) not in self.board:
                    self.frontier.add((x-1,y))
                if y-1 >= 0 and (x, y-1) not in self.board:
                    self.frontier.add((x,y-1))
            
    def calculate_next_destination(self):
        if self.treasure or len(self.frontier) == 0:
            self.nextDestination = (0,0)
        else:
            self.nextDestination = sorted(self.frontier, key=(lambda t : abs(t[0] - self.currentCoordinate[0]) + abs(t[1] - self.currentCoordinate[1])))[0]


    def calculate_step_list(self):
        self.stepList = []
        self.recursionBoard = copy.deepcopy(self.board)
        self.recursiveSearch(self.currentCoordinate, "start")
        
    def recursiveSearch(self, current, last):
        self.stepList.append(last)
        if current == self.nextDestination:
            if self.nextDestination == (0,0):
                self.stepList.append("climb")
            return True
        if current not in self.board or "Bump" in self.board[current]:
            self.stepList.pop()
            return False
        if "visit" in self.recursionBoard[current]:
            self.stepList.pop()
            return False        
        self.recursionBoard[current].add("visit")
        
        
        if(self.recursiveSearch((current[0]+1, current[1]), "R")):
            return True
        if(self.recursiveSearch((current[0]-1, current[1]), "L")):
            return True
        if(self.recursiveSearch((current[0], current[1]+1), "D")):
            return True
        if(self.recursiveSearch((current[0], current[1]-1), "U")):
            return True
        self.stepList.pop()
        return False
    
    def print_information(self):
        print()
        print("move #:", self.count)
        print("Direction:", self.directionFacing)
        print("Current Coordinate:", self.currentCoordinate)
        print("Board:", self.board)
        print("Frontier:", self.frontier)
        print("Next Destination:", self.nextDestination)
        print("Step List:", self.stepList)
    
    def calculate_move(self):
        if self.stepList[0] == 'R':
            if "east" == self.directionFacing:
                self.lastMove = "forward" 
            elif "south" == self.directionFacing:
                self.lastMove = "left"
            elif "west" == self.directionFacing:
                self.lastMove = "left"
            elif "north" == self.directionFacing:
                self.lastMove = "right"
        elif self.stepList[0] == 'D':
            if "east" == self.directionFacing:
                self.lastMove = "right" 
            elif "south" == self.directionFacing:
                self.lastMove = "forward"
            elif "west" == self.directionFacing:
                self.lastMove = "left"
            elif "north" == self.directionFacing:
                self.lastMove = "right"
        elif self.stepList[0] == 'L':
            if "east" == self.directionFacing:
                self.lastMove = "left" 
            elif "south" == self.directionFacing:
                self.lastMove = "right"
            elif "west" == self.directionFacing:
                self.lastMove = "forward"
            elif "north" == self.directionFacing:
                self.lastMove = "left"
        elif self.stepList[0] == 'U':
            if "east" == self.directionFacing:
                self.lastMove = "left" 
            elif "south" == self.directionFacing:
                self.lastMove = "left"
            elif "west" == self.directionFacing:
                self.lastMove = "right"
            elif "north" == self.directionFacing:
                self.lastMove = "forward"
        elif self.stepList[0] == 'climb':
                self.lastMove = "climb"
                
    def get_move(self, percepts):
        self.update_variables(percepts)
        
        if "Glitter" in percepts:
            self.treasure = True
            self.lastMove = "grab"
            return self.lastMove
        
        if self.arrow > 0 and "Stench" in percepts:
            self.arrow = 0
            self.lastMove = "shoot"
            return self.lastMove
            
        if "Scream" in percepts:
            self.noWumpus = True
            
        if self.lastMove == "forward":
            self.stepList.pop(0)
            
        if 0 == len(self.stepList):
            self.calculate_frontier()
            self.calculate_next_destination()
            self.calculate_step_list()
            self.stepList.pop(0)
            

        #self.print_information()
        
        self.calculate_move()
        
        return self.lastMove

                    
                    
                        
                        
            
            
            
            
                
                
            
            
            
                
            
            



            
            
            
            
            
                 
                
            
            
        
       
        
        
            
    
    

            