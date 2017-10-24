"""
Created by: Rimoun Ghaly rghaly@uci.edu
This module contains the Wumpus Game State class.
Made for CS 171.
"""
import random
#from WumpusWorldPythonAI import *

class WumpusGameState():
    
    def __init__(self, rows, columns, Agent):
        """
        Creates the state based on user input. Rows and columns are integers,
        and start_player, top_left_disc, and game_type are strings.
        """
        self._rows = rows
        self._columns = columns
        self.board = [[set() for j in range(self._columns)] for i in range(self._rows)]
        self._wumpus = self._set_rand_obj('Wumpus', 'Stench')        
        self._gold = self._set_rand_obj('Glitter', False)
        self._set_pits()    
        self.board[0][0].add('I')
        self.prev_location = [0, 0]
        self.current_location = [0, 0]
        self.have_gold = False
        self.Agentobj = Agent
        self.facing = 'right'
        self.facing_num = 1
        self.score = 0
        self.game_over = 0
        self.shot_arrow = False
        self.extra_percepts = []
        self.arrows_through = []
        self.percepts = self.board[0][0].copy()
    
    def _set_pits(self):
        """
        Sets pits randomly with breeze around them.
        """
        for i in range(self._rows-1):
            for j in range(self._columns-1):
                if (i == 0 and j == 0) or (i == self._wumpus[0] and j == self._wumpus[1]):
                    continue
                random_num = random.randint(1,6)
                if(random_num == 1):
                    self.board[i][j].add('Pit')
                    breeze_locs = [(i, j - 1),
                           (i, j + 1),
                           (i - 1, j),
                           (i + 1, j)]

                    breeze_locs = [(r,c) for r,c in breeze_locs if 0 <= r < self._rows and 0 <= c < self._columns]

                    for r,c in breeze_locs:
                        self.board[r][c].add('Breeze')
                else:
                    pass                    
    
    def _set_rand_obj(self, obj, around_obj = False):
        """
        Given an object to set and another object to set around
        the first object, sets the object in a random spot and
        surrounds it with the other object. Example: Wumpus
        and Stench
        """
        t_row = int(random.randrange(0, self._rows-1))
        t_col = int(random.randrange(0, self._columns-1))
        while(t_col == 0 and t_row == 0):
            t_row = int(random.randrange(0, self._rows-1))
            t_col = int(random.randrange(0, self._columns-1))

        self.board[t_row][t_col].add(obj)

        if around_obj:
            stinch_locs = [(t_row, t_col - 1),
                           (t_row, t_col + 1),
                           (t_row - 1, t_col),
                           (t_row + 1, t_col)]
            stinch_locs = [(r,c) for r,c in stinch_locs if 0 <= r < self._rows and 0 <= c < self._columns]

            for r,c in stinch_locs:
                self.board[r][c].add(around_obj)
        return (t_row, t_col)
    
    def calculate_scores(self):
        """
        Calculates the current score of the game. Not yet implemented.
        """
        pass
    
    
    def get_rows(self):
        """
        Returns the number of rows on the board.
        """

        return self._rows

    def get_columns(self):
        """
        Returns the number of columns on the board.
        """

        return self._columns

    def _place_piece_as_test(self, row, col, piece_color):
        """
        Allows testing game mechanics by placing items arbitrarily.
        """

        self.board[row-1][col-1] = piece_color        
        
    def _copy_board(self):
        """
        Creates a copy of the game board.
        """
        new_board = []
        for row in range(self._rows):
            new_board.append([])
            for col in range(self._columns):
                new_board[-1].append(self.board[row][col])
        return new_board

    def turn_left(self):
        if(self.facing == 'down'):
            self.facing = 'right'
            self.facing_num = 1
        elif(self.facing == 'right'):
            self.facing = 'up'        
            self.facing_num = 2
        elif(self.facing == 'up'):
            self.facing = 'left'
            self.facing_num = 3
        elif(self.facing == 'left'):
            self.facing = 'down'
            self.facing_num = 0

    def turn_right(self):
        if(self.facing == 'down'):
            self.facing = 'left'
            self.facing_num = 3
        elif(self.facing == 'left'):
            self.facing = 'up'
            self.facing_num = 2
        elif(self.facing == 'up'):
            self.facing = 'right'
            self.facing_num = 1
        elif(self.facing == 'right'):
            self.facing_num = 0
            self.facing = 'down'

    def move_forward(self):
        if(self.facing == 'down'):
            self.current_location[0]+=1
        elif(self.facing == 'left'):
            self.current_location[1]-=1
        elif(self.facing == 'up'):
            self.current_location[0]-=1
        elif(self.facing == 'right'):
            self.current_location[1]+=1
                                
    def make_move(self):
        """
        Asks Agent object to make a move and executes the move, returning the result
        """
        # Get the move
        agent_percepts = self.percepts
        if 'I' in agent_percepts: agent_percepts.remove('I')
        if 'Dead Wumpus' in agent_percepts:
            agent_percepts.remove('Dead Wumpus')
            agent_percepts.add('Stench')
        move = self.Agentobj.get_move(agent_percepts)
        try:
            if move.lower() not in {'grab', 'forward', 'left', 'right', 'shoot'}:
                result = "Agent made an invalid move:", move.lower()
        except:
                result = "Agent made an invalid move:", str(move.lower())            

        # Make the move
        result = ''
        if self.score <= -1000:
            self.game_over = 2
            return "Agent reached -1000 points!"
        
        if str(move).lower() == 'grab':
            self.score -= 1
            grabbed = self.grab_gold()
            if (not(grabbed) and not(self.have_gold)):
                result = "Agent Tried to grab gold but found no gold to grab!"
            elif not(grabbed) and self.have_gold:
                result = "Agent Tried to grab gold, but it already caries it!"
            else:
                result = "Agent grabbed the gold!"
            
        #if str(move).lower() == 'drop':
        #    self.score -= 1
        #    self.drop_gold()
        #    self.game_over = 0
        #    return "Agent dropped the gold!"
        
        
        if(str(move).lower() == 'left'):
            self.score -= 1
            self.turn_left()
            result = 'Agent turned left.'
        
        if(str(move).lower() == 'right'):
            self.score -= 1
            self.turn_right()
            result = 'Agent turned right.'


        if(str(move).lower() == 'climb'):
            self.score -= 1            
            if(self.current_location == [0, 0]):
                result = 'Agent climbed out.\nFinal Score: ' + str(self.score) + '!'
                self.board[0][0].remove('I')
				
                if(self.have_gold):
                    self.score += 1000

                self.game_over = 1
            else:
                result = 'Agent tried to climb out but not at initial spot.'


        if(str(move).lower() == 'shoot'):
            self.score -= 1
            if self.shot_arrow:
                result = "Agent tried to shoot arrow but has no arrow to shoot."
            elif self._handle_shoot():
                self.score -= 10
                result = "Agent killed the Wumpus!"
                self.extra_percepts.append('Scream')
            else:
                self.score -= 10
                result = "Agent shot arrow but did not hit Wumpus."
            self.shot_arrow = True
            

        if(str(move).lower() == 'forward'):
            self.prev_location = self.current_location[:]
            self.score -= 1
            self.move_forward()
            if not(0 <= self.current_location[0] < self._rows and 0 <= self.current_location[1] < self._columns):
                self.current_location = self.prev_location[:]
                self.extra_percepts.append('Bump')
                result = "Agent hit a wall when making the move: {}".format(str(move))
            else:
                result = 'Agent moved forward.'
                self.board[self.prev_location[0]][self.prev_location[1]].remove('I')
                self.board[self.current_location[0]][self.current_location[1]].add('I')
                if 'Wumpus' in self.board[self.current_location[0]][self.current_location[1]]:
                    self.game_over = 2
                    self.score -= 1000
                    result += "The Wumpus got Agent!"
                    
                if 'Pit' in self.board[self.current_location[0]][self.current_location[1]]:
                    self.game_over = 2
                    self.score -= 1000
                    result =  "Agent fell down a pit!"

        self.percepts = self.board[self.current_location[0]][self.current_location[1]].copy()
        for i in self.extra_percepts:
            self.percepts.add(i)
        self.extra_percepts = []
        return result



    def _handle_shoot(self):
        """Called when shooting an arrow to handle shooting action"""
        if self.facing == 'right':
            y = self.current_location[1]
            y += 1
            while(y < self._rows and y >= 0):
                self.arrows_through.append((self.current_location[0], y))
                if 'Wumpus' in self.board[self.current_location[0]][y]:
                    self.board[self.current_location[0]][y].remove('Wumpus')
                    self.board[self.current_location[0]][y].add('Dead Wumpus')
                    self.hit_wumpus = True
                    return True
                y += 1

        if self.facing == 'left':
            y = self.current_location[1]
            y -= 1
            while(y >= 0 and y < self._rows):
                self.arrows_through.append((self.current_location[0], y))
                if 'Wumpus' in self.board[self.current_location[0]][y]:
                    self.hit_wumpus = True
                    self.board[self.current_location[0]][y].remove('Wumpus')
                    self.board[self.current_location[0]][y].add('Dead Wumpus')

                    return True
                y -= 1

        if self.facing == 'up':
            x = self.current_location[0]
            x -=1
            while(x < self._columns and x >= 0):
                self.arrows_through.append((x, self.current_location[1]))
                if 'Wumpus' in self.board[x][self.current_location[1]]:
                    self.board[x][self.current_location[1]].remove('Wumpus')
                    self.board[x][self.current_location[1]].add('Dead Wumpus')

                    self.hit_wumpus = True
                    return True
                x -= 1

        if self.facing == 'down':
            x = self.current_location[0]
            x += 1
            while(x >= 0 and x < self._columns):
                self.arrows_through.append((x, self.current_location[1]))
                if 'Wumpus' in self.board[x][self.current_location[1]]:
                    self.hit_wumpus = True
                    self.board[x][self.current_location[1]].remove('Wumpus')
                    self.board[x][self.current_location[1]].add('Dead Wumpus')
                    return True
                x += 1
        return False
        
    def print_board(self):
        """
        Prints board in Ascii format
        """
        for line in self.board:
            print(line)
        print("\n\n")
        
    def grab_gold(self):
        """
        Let's Agent grab the gold if currently on top of it.
        """
        if 'Glitter' in self.board[self.current_location[0]][self.current_location[1]]:
            self.board[self.current_location[0]][self.current_location[1]].remove('Glitter')
            self.have_gold = True
            return True
        return False

    def drop_gold(self):
        """
        Let's Agent grab the gold if currently on top of it.
        """
        self.board[self.current_location[0]][self.current_location[1]].add('Glitter')
        self.have_gold = False


    def start(self):
        game_file = ''
        while not self.game_over:
            result = self.make_move()
            game_file += result + "\n"
        with open('result_Agent1.txt', 'w') as file:
            file.write(game_file)
            if self.game_over == 1:
                file.write("Result: Agent Climbed Out, Points = "+ str(self.score))
            else:
                file.write("Result: Agent Lost, Points = "+ str(self.score))
        

if __name__ == '__main__':
    import os
    files = sorted([f for f in os.listdir('.') if os.path.isfile(f)])
    files = [AI for AI in files if 'ai' in AI.lower()]
    AIs = [AI[:-3] for AI in files if AI[-3:] == '.py']
    if not AIs:
        print("You have no AIs in the current folder.\n")
    else:
        Agento = __import__(AIs[0])
        size = input("How many rows/columns? ")
        game = WumpusGameState(int(size), int(size), Agento.Agent())
        game.start(AIs[0])


