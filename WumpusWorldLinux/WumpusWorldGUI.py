"""
This module contains the Wumpus GUI Shell
        Made for UCI CS 171
Created by: Rimoun Ghaly | rghaly@uci.edu
"""
try:
    import pip
except:
    print("You need pip to run this program. Pip usually comes with Python, but \
not in your case. Install it from here: https://pip.pypa.io/en/stable/installing/")

try:
    from PIL import Image, ImageTk #This is the PIL Image library
except:
    if(pip.main(['install', 'Pillow'])):
        from PIL import Image, ImageTk
        print("this program requires Pillow Library. Library has been Installed.\n")
    else:
        print("this program requires Pillow Library. Library was not able to be Installed. Please manually install and try again.\n")
    
import tkinter as tk
import WumpusWorldGameState as wumpus
import tkinter.messagebox
import random
import os


class WumpusShell:
    def __init__(self):
        self.options = WumpusOptionsBox().selected_options
        print("Using agent", self.options[2])
        self.AgentClass = __import__(self.options[2])
        
        self._root_window = tk.Tk()
        self._root_window.bind('<Control-w>', self.start)
        self.images = []
        self._load_images()
        self.start(0)

    def start(self, event: tk.Event):
        Agento = self.AgentClass.Agent()
        game = wumpus.WumpusGameState(self.options[0], self.options[1], Agento)
        WumpusApplication(game, self._root_window, self.images).start()
        
    def _load_images(self):
        """Initializes images for breeze, pit, gold and wumpus for the GUI class"""

        self.rand_num = random.randrange(1,6)
        try:
            self.images.append(Image.open('images\\breeze.jpg'))

            self.images.append(Image.open('images\\pit.jpg'))

            self.images.append(Image.open('images\\gold.jpg'))

            self.images.append(Image.open('images\\w_'+str(self.rand_num)+'.jpg'))

            self.images.append(Image.open('images\\w_up.jpg'))
            
            self.images.append(Image.open('images\\w_down.jpg'))
            
            self.images.append(Image.open('images\\w_left.jpg'))
            
            self.images.append(Image.open('images\\w_right.jpg'))

            self.images.append(Image.open('images\\w_up.jpg')) # INDEX 8

            self.images.append(Image.open('images\\w_down.jpg'))

            self.images.append(Image.open('images\\w_left.jpg'))

            self.images.append(Image.open('images\\w_right.jpg'))

            self.images.append(Image.open('images\\w_look_down.png')) #INDEX 12

            self.images.append(Image.open('images\\w_look_right.png'))

            self.images.append(Image.open('images\\w_look_up.png'))

            self.images.append(Image.open('images\\w_look_left.png'))

            self.images.append(Image.open('images\\bomb.jpg')) #INDEX 16

            self.images.append(Image.open('images\\splash.jpg')) #INDEX 17
            
        except:
            self.images.append(Image.open('images/breeze.jpg'))

            self.images.append(Image.open('images/pit.jpg'))

            self.images.append(Image.open('images/gold.jpg'))

            self.images.append(Image.open('images/w_'+str(self.rand_num)+'.jpg'))

            self.images.append(Image.open('images/w_up.jpg'))
            
            self.images.append(Image.open('images/w_down.jpg'))
            
            self.images.append(Image.open('images/w_left.jpg'))
            
            self.images.append(Image.open('images/w_right.jpg'))

            self.images.append(Image.open('images/w_up.jpg')) # INDEX 8

            self.images.append(Image.open('images/w_down.jpg'))

            self.images.append(Image.open('images/w_left.jpg'))

            self.images.append(Image.open('images/w_right.jpg'))

            self.images.append(Image.open('images/w_look_down.png')) #INDEX 12

            self.images.append(Image.open('images/w_look_right.png'))

            self.images.append(Image.open('images/w_look_up.png'))

            self.images.append(Image.open('images/w_look_left.png'))

            self.images.append(Image.open('images/bomb.jpg')) #INDEX 16

            self.images.append(Image.open('images/splash.jpg')) #INDEX 17

            

class WumpusApplication:

    def __init__(self, wumpus_game: wumpus.WumpusGameState, root_window = 0, images = 0):
        self.restart = False
        self.images = [] if images == 0 else images
        self.imagesTk = []
        if images == 0: self._load_images()

        self._root_window = tk.Tk() if root_window == 0 else root_window
        self._root_window.title('Wumpus World')

        self._canvas = tk.Canvas(
            master=self._root_window, background='black', width=600, height=600)

        self._canvas.grid(
            row=1, column=0, sticky=tk.NSEW)

        self._scores = tk.StringVar(value='Welcome to Wumpus World!')

        self._score_player = tk.Label(
            master=self._root_window, font=('Helvetica', 14), textvariable=self._scores, height=4)

        self._score_player.grid(row=0, column=0, sticky=tk.NSEW)

        self._root_window.columnconfigure(0, weight=1)
        self._root_window.rowconfigure(1, weight=1)

        self._game = wumpus_game
        self._rows = wumpus_game.get_rows()
        self._columns = wumpus_game.get_columns()
        

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._root_window.bind('<space>', self._on_canvas_clicked)
        

        self.direction_numbers = {'up'}
        self._w_loc = self._game._wumpus

        self._click_count = 0
        
    def _get_box_corners(self, canvas_height, canvas_width):
        """
        Accumulates the top left and bottom right pixel coordinates for each board coordinate.
        """

        boxes = []

        row_width = canvas_height/self._rows
        col_width = canvas_width/self._columns

        for r in range(self._rows):
            row_of_boxes = []
            for c in range(self._columns):
                box_coords = [(c*col_width, r*row_width), ((c+1)*col_width, (r+1)*row_width)]
                row_of_boxes.append(box_coords)
            boxes.append(row_of_boxes)

        return boxes


    def start(self):
        """
        Starts the application.
        """
        self._root_window.mainloop()
        


    def _draw_lines(self, canvas_height, canvas_width):
        """
        Draws the lines that separate the game board.
        """

        for i in range(self._rows-1):

            self._canvas.create_line(0, (canvas_height/self._rows) * (i+1), canvas_width-1,
                                     (canvas_height/self._rows) * (i+1), fill='black')

        for i in range(self._columns-1):

            self._canvas.create_line((canvas_width/self._columns) * (i+1), 0, (canvas_width/self._columns) * (i+1)
                                     , canvas_height-1, fill='black')


    def _on_canvas_resized(self, event: tk.Event):
        """
        Re-draws all of the items on the board if the window is resized.
        """

        canvas_height = self._canvas.winfo_height()
        canvas_width = self._canvas.winfo_width()

        self._draw_lines(canvas_height, canvas_width)

        self._draw_pieces(canvas_height, canvas_width, resize = True)



    def _set_score_text(self):
        """
        Sets the correct text for the score label based on the game state.
        """
        self._score_player = tk.Label(
            master=self._root_window, font=('Helvetica', 14), textvariable=self._scores, height=4)
        self._score_player.grid(row=0, column=0, sticky=tk.NSEW)


        
    def _on_canvas_clicked(self, event: tk.Event):
        """
        Makes the next Agent move.
        """

        canvas_height = self._canvas.winfo_height()
        canvas_width = self._canvas.winfo_width()

        self._make_next_move()
        
        self._set_score_text()
        
        self._draw_pieces(canvas_height, canvas_width, resize = False)




    def _convert_to_board(self, x, y):
        """
        Converts a coordinate on the canvas to a board coordinate.
        """

        row_fracs = [0]
        col_fracs = [0]

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        row_frac_width = 1/self._rows
        col_frac_width = 1/self._columns

        for i in range(1, self._rows + 1):
            end_of_row_coord = row_frac_width * i
            row_fracs.append(end_of_row_coord)

        for i in range(1, self._columns + 1):
            end_of_col_coord = col_frac_width * i
            col_fracs.append(end_of_col_coord)

        click_frac_x = x / canvas_width
        click_frac_y = y / canvas_height

        for i in range(len(row_fracs)):
            try:
                if click_frac_y < row_fracs[i+1] and click_frac_y > row_fracs[i]:
                    row_coord = i+1
                else:
                    pass
            except:
                continue

        for i in range(len(col_fracs)):
            try:
                if click_frac_x < col_fracs[i+1] and click_frac_x > col_fracs[i]:
                    col_coord = i+1
                else:
                    pass
            except:
                continue

        try:
            return [row_coord, col_coord]
        except:
            return


    def _make_next_move(self):
        """
        Attempt to place a piece on the game board.
        """
        if(self._game.game_over):
            self._scores = tk.StringVar(value="Game over! Agent Climbed out!\nFinal Score: "+str(self._game.score) if self._game.game_over == 1 else "Game over! Agent Died!\nFinal Score: "+str(self._game.score))
            return
        
        result1 = self._game.make_move()

        result = "Score: " + str(self._game.score) + "\n"
        result += result1
        percepts = self._game.percepts
        if 'I' in percepts: percepts.remove('I')
        if percepts != set():
            result += "\nPercepts: " + ', '.join(percepts)
            result = result.replace('Dead Wumpus', 'Stench')
        else:
            result += "\nPercepts: None"

        self._scores = tk.StringVar(value=result)


    def _draw_pieces(self, canvas_height, canvas_width, resize):
        """
        Draws all of the pieces that have been placed on the game board.
        """
        self._canvas.delete(tk.ALL)
        self._draw_lines(canvas_height, canvas_width)

        boxes = self._get_box_corners(canvas_height, canvas_width)

        """Resize all images"""
        if(resize):
            self.imagesTk = []
            for i in range(18):
                self.imagesTk.append(self.images[i].resize((int(boxes[0][0][1][0]-boxes[0][0][0][0]), int(boxes[0][0][1][1]-boxes[0][0][0][1])), Image.ANTIALIAS))
                self.imagesTk[i] = ImageTk.PhotoImage(self.imagesTk[i])


        """Place all images"""
        for r in range(self._rows):
            for c in range(self._columns):
                try:
                    if 'I' in self._game.board[r][c]:
                        self._canvas.create_image(boxes[r][c][0][0], boxes[r][c][0][1], anchor='nw', image = self.imagesTk[self._game.facing_num + 12])
                        # 12 is for offset of agent images, agents images start at index 12

                    elif 'Glitter' in self._game.board[r][c]:
                        self._canvas.create_image(boxes[r][c][0][0], boxes[r][c][0][1], anchor='nw', image = self.imagesTk[2])
                        
                    elif 'Wumpus' in self._game.board[r][c]:
                        self._canvas.create_image(boxes[r][c][0][0], boxes[r][c][0][1], anchor='nw', image = self.imagesTk[3])

                    elif 'Pit' in self._game.board[r][c]:
                        self._canvas.create_image(boxes[r][c][0][0], boxes[r][c][0][1], anchor='nw', image = self.imagesTk[1])
                        
                    elif 'Stench' in self._game.board[r][c]:
                        wumpus_side = self._which_side('Stench', r, c) + 8 # 8 is for offset of wumpus images, wumpus images start at index 8
                        self._canvas.create_image(boxes[r][c][0][0], boxes[r][c][0][1], anchor='nw', image = self.imagesTk[wumpus_side])

                        
                    elif 'Breeze' in self._game.board[r][c]:
                        self._canvas.create_image(boxes[r][c][0][0], boxes[r][c][0][1], anchor='nw', image = self.imagesTk[0])

                    elif 'Dead Wumpus' in self._game.board[r][c]:
                        self._canvas.create_image(boxes[r][c][0][0], boxes[r][c][0][1], anchor='nw', image = self.imagesTk[17])
                        
                    else:
                        pass
                except: pass

    def _which_side(self, percept, r, c):
        """
        Given a percept and its row and column, returns which
        side of the percept is the location of the object it's
        coming from.
        """
        if percept == 'Breeze':
            surr_locs = [(r, c - 1, 2),
                         (r, c + 1, 3),
                         (r - 1, c, 0),
                         (r + 1, c, 1)]

            surr_locs = [(r,c,z) for r,c,z in surr_locs if 0 <= r < self._rows and 0 <= c < self._columns]
            for loc in surr_locs:
                if 'Pit' in self._game.board[loc[0]][loc[1]]:
                    return loc[2]

        if percept == 'Stench':
            surr_locs = [(r, c - 1, 2),
                         (r, c + 1, 3),
                         (r - 1, c, 0),
                         (r + 1, c, 1)]
            
            surr_locs = [(r,c,z) for r,c,z in surr_locs if 0 <= r < self._rows and 0 <= c < self._columns]
            for loc in surr_locs:
                if 'Wumpus' in self._game.board[loc[0]][loc[1]] or 'Dead Wumpus' in self._game.board[loc[0]][loc[1]]:
                    return loc[2]
        #return -1
        




class WumpusOptionsBox:


    def __init__(self):

        self._options_window = tk.Tk()
        self._options_window.title('Wumpus Setup Options')

        self._row_list = tk.Listbox(
            master=self._options_window, width=25, height=10, bd=5, selectmode=tk.SINGLE, exportselection=0)
        self._row_list.grid(row=1, column=0)
        self._row_list.insert(*[i for i in range(2, 101)])

        self._row_label = tk.Label(
            master=self._options_window, font=('Helvetica', 10), text='Rows')
        self._row_label.grid(row=0, column=0)

        self._col_list = tk.Listbox(
            master=self._options_window, width=25, height=10, bd=5, selectmode=tk.SINGLE, exportselection=0)
        self._col_list.grid(row=1, column=1)
        self._col_list.insert(*[i for i in range(2, 101)])

        self._col_label = tk.Label(
            master=self._options_window, font=('Helvetica', 10), text='Columns')
        self._col_label.grid(row=0, column=1)
##
        self._agent_list = tk.Listbox(
            master=self._options_window, width=25, height=10, bd=5, selectmode=tk.SINGLE, exportselection=0)
        self._agent_list.grid(row=1, column=2)

    ##
        self.files = sorted([f for f in os.listdir('.') if os.path.isfile(f)])
        self.files = [AI for AI in self.files if 'ai' in AI.lower()]
        self.AIs = [AI[:-3] for AI in self.files if AI[-3:] == '.py']
        self.AIs.extend([i[:-4] for i in self.files if i[-4:] == '.pyc'])
        for i, AI in enumerate(self.AIs):
            self._agent_list.insert(i, AI)

        self._agent_label = tk.Label(
            master=self._options_window, font=('Helvetica', 10), text='Agents')
        self._agent_label.grid(row=0, column=2)
##
        
        self._button_frame = tk.Frame(master=self._options_window)
        self._button_frame.grid(row=2, column=0, columnspan=6)

        self._description = tk.Label(
            master=self._button_frame, font=('Helvetica', 10), text='Choose your options and press Okay to start!\n Press Okay will default to 4x4.')
        self._description.grid(row=0, column=2)

        self._okay = tk.Button(
            master=self._button_frame, width=20, height=3, text='Okay', font=(40,), command=self._on_button_clicked,
            bg='grey')
        self._okay.grid(row=1, column=2)

        self._options_window.rowconfigure(0, weight=1)
        self._options_window.rowconfigure(1, weight=1)
        self._options_window.columnconfigure(0, weight=1)
        self._options_window.columnconfigure(1, weight=1)
        self._options_window.columnconfigure(2, weight=1)
        self._options_window.columnconfigure(3, weight=1)
        self._options_window.columnconfigure(4, weight=1)
        self._options_window.columnconfigure(5, weight=1)

        self._button_frame.rowconfigure(0, weight=1)
        self._button_frame.columnconfigure(2, weight=1)

        self.selected_options = [4, 4, self.AIs[0]]

        self._options_window.mainloop()



    def _on_button_clicked(self):
        """
        Gathers the information from the listboxes, closes the options box, and returns the information.
        """
        try:
            rows_select = self._row_list.curselection()
            rows = self._row_list.get(rows_select)

            cols_select = self._col_list.curselection()
            cols = self._col_list.get(cols_select)

            agent_select = self._agent_list.curselection()
            agent = self._agent_list.get(agent_select)
            self.selected_options = [rows, cols, agent]
            
            self._options_window.destroy()

        except:
            try:
                agent_select = self._agent_list.curselection()
                agent = self._agent_list.get(agent_select)
                self.selected_options = [4, 4, agent]
                self._options_window.destroy()
            except:
                tk.messagebox.showwarning("No Agent selected", "Please select an Agent.\nIf there are none available make sure your agent's \
                                          file has 'AI' in it and the class is called Agent.")


if __name__ == '__main__':
    WumpusShell()


