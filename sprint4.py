import tkinter as tk
from tkinter import messagebox
import random


class SOSGameGUI:
    def __init__(self, root, board_size, typeOfGame, AIselection):
        self.AIselection = AIselection
        self.typeOfGame = typeOfGame
        self.root = root
        self.root.title("SOS Game")
        self.board_size = board_size
        self.symbols = ['S', 'O']
        self.current_player = 0  # 0 for Player 1, 1 for Player 2
        self.has_made_move = False  # Flag to track if the current player has made a move
        self.flag = True
        self.lists = []
        self.trackMoves = []
        self.trackPlayer1 = 0
        self.trackPlayer2 = 0
        self.trackAIfields = []
        self.btn = None
        self.row = None  # Initialize row attribute
        self.col = None 
        self.create_widgets()


    def create_widgets(self):
        
        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        for row in range(self.board_size):
            for col in range(self.board_size):
                self.btn = tk.Button(self.root, text='', width=4, height=2, command=lambda r=row, c=col: self.make_move(r, c, self.symbol_var.get()))
                print(type(self.btn))
                self.btn.grid(row=row, column=col)
                self.buttons[row][col] = self.btn

        self.symbol_var = tk.StringVar()
        self.symbol_var.set(self.symbols[0])

        symbol_label = tk.Label(self.root, text="Choose your symbol:")
        symbol_label.grid(row=self.board_size, columnspan=self.board_size)

        symbol_menu = tk.OptionMenu(self.root, self.symbol_var, *self.symbols)
        symbol_menu.grid(row=self.board_size + 1, columnspan=self.board_size)

        make_move_button = tk.Button(self.root, text="Make Move", command=self.make_move_button_clicked)
        make_move_button.grid(row=self.board_size + 2, columnspan=self.board_size)

        self.turn_label = tk.Label(self.root, text=f"Player {self.PlayerTrack()}'s turn. Choose symbol and place it on the grid")
        self.turn_label.grid(row=self.board_size + 3, columnspan=self.board_size)

        if  self.AIselection == 1:
            self.perform_ai_move()


    def make_move(self, row, col, symbol):
        if self.AIselection ==4 or (self.AIselection == 1 and self.PlayerTrack() == 2) or (self.AIselection == 2 and self.PlayerTrack() == 1):
            if self.buttons[row][col]["text"] == '':
                self.buttons[row][col]["text"] = symbol
                self.lists.append([row, col, symbol])
                if len(self.lists) == 2:
                    self.buttons[self.lists[0][0]][self.lists[0][1]]["text"] = ''
                    self.lists.pop(0)
    
                self.flag = False
                self.update_turn_label()
                
        else:
            self.perform_ai_move()

    def ai_move(self):

        for self.row in range(self.board_size):
            for self.col in range(self.board_size):
                if self.buttons[self.row][self.col]["text"] == '':
                    self.trackAIfields.append([self.row,self.col])
        print(self.trackAIfields)

        if self.trackAIfields:
            self.row, self.col = random.choice(self.trackAIfields)
            symbol = random.choice(['S', 'O'])
            self.trackAIfields.clear()
            return self.row, self.col, symbol
        return None, None, None 

    def perform_ai_move(self):
        if self.AIselection==1 and self.PlayerTrack() == 1:
            row, col, ai_symbol = self.ai_move()
            if row is not None and col is not None:
                self.buttons[row][col]["text"] = ai_symbol
                self.lists.append([row, col, ai_symbol])
                if len(self.lists) == 2:
                    self.buttons[self.lists[0][0]][self.lists[0][1]]["text"] = ''
                    self.lists.pop(0)

                self.flag = False
                self.update_turn_label()
                self.make_move_button_clicked()


                      
        elif self.AIselection == 2 and self.PlayerTrack() == 2:
        
            row, col, ai_symbol = self.ai_move()
            if row is not None and col is not None:
                self.buttons[row][col]["text"] = ai_symbol
                self.lists.append([row, col, ai_symbol])
                if len(self.lists) == 2:
                    self.buttons[self.lists[0][0]][self.lists[0][1]]["text"] = ''
                    self.lists.pop(0)
                #self.has_made_move = True
                self.flag = False
                self.update_turn_label()
                self.make_move_button_clicked()
                


        elif self.AIselection == 3:
            row, col, ai_symbol = self.ai_move()
            if row is not None and col is not None:
                self.buttons[row][col]["text"] = ai_symbol
                self.lists.append([row, col, ai_symbol])
                if len(self.lists) == 2:
                    self.buttons[self.lists[0][0]][self.lists[0][1]]["text"] = ''
                    self.lists.pop(0)
                self.flag = False
                self.update_turn_label()
                

    def PlayerTrack(self):
        m=0 
        if self.current_player%2==0:
            m=1
        else:
            m=2
        return int(m)

    def make_move_button_clicked(self):
        if self.flag == False:
            self.trackMoves.append(self.lists[-1])
            self.checkGameOver()
            if self.checkGameOver() != 1 and self.checkGameOver()!= 2 and self.AIselection != 3 and self.AIselection != 4:
                self.perform_ai_move()
            
                

    def checkGameOver(self):
        if self.typeOfGame==1:
            return self.simple_game()  
        else:
            return self.general_game() 

    def simple_game(self):
        if self.check_sos1(self.trackMoves):    
            messagebox.showinfo("SOS Game", f"Player {self.PlayerTrack()} formed SOS!")
            #self.track4case = False
            self.trackMoves.clear()
            self.reset_board()
            #self.current_player = 0
            return 1
        if len(self.trackMoves)==self.board_size*self.board_size:
            messagebox.showinfo("SOS Game", f"That's a draw")
            self.trackMoves.clear()
            self.lists.clear()
            self.reset_board()
        else:
            self.lists.clear()
            self.current_player = 1 + self.current_player  # Switch player
            self.turn_label.config(text=f"Player {self.PlayerTrack()}'s turn. Choose symbol and place it on the grid.")
    
    def general_game(self):
        if self.check_sos1(self.trackMoves):
            if self.PlayerTrack()==1:
                self.trackPlayer1=self.trackPlayer1+1
            if self.PlayerTrack()==2:
                self.trackPlayer2=self.trackPlayer2+1
            
        if len(self.trackMoves)==self.board_size*self.board_size:
        
            if self.trackPlayer1>self.trackPlayer2:
                messagebox.showinfo("SOS Game", f"Player 1 won the game. He formed more SOS!")
            if self.trackPlayer1<self.trackPlayer2:
                messagebox.showinfo("SOS Game", f"Player 2 won the game. He formed more SOS!")
            if self.trackPlayer1==self.trackPlayer2:
                messagebox.showinfo("SOS Game", f"That's a draw")
            self.trackMoves.clear()
            self.lists.clear()
            self.reset_board()
            self.trackPlayer1=0
            self.trackPlayer2=0
            return 2
                

        self.lists.clear()
        self.current_player = 1 + self.current_player  # Switch player
        self.turn_label.config(text=f"Player {self.PlayerTrack()}'s turn. Choose symbol and place it on the grid.")

    def check_sos1(self, coordinates):
        if not coordinates:  # Check if coordinates list is empty
            return False
    
        directions = [
            (0, 1),  # Right
            (0, -1),  # Left
            (1, 0),  # Down
            (-1, 0),  # Up
            (1, 1),  # Down-Right
            (-1, -1),  # Up-Left
            (1, -1),  # Down-Left
            (-1, 1)  # Up-Right
        ]

        # Convert list of coordinates to a more efficient search structure
        coord_map = {(x, y): symbol for x, y, symbol in coordinates}

        x, y, symbol = coordinates[-1]  # Get the last element from coordinates
        if symbol == 'S':
            for dx, dy in directions:
                first = (x + dx, y + dy)
                second = (x + 2*dx, y + 2*dy)

                if first in coord_map and second in coord_map:
                    if coord_map[first] == 'O' and coord_map[second] == 'S':
                        return True  # SOS formation found
        elif symbol == 'O':
            for dx, dy in directions:
                sos_pattern1 = (x - dx, y - dy)  # Check the left side of 'O'
                sos_pattern2 = (x + dx, y + dy)  # Check the right side of 'O'
                
                if sos_pattern1 in coord_map and sos_pattern2 in coord_map:
                    if coord_map[sos_pattern1] == 'S' and coord_map[sos_pattern2] == 'S':
                        return True  # SOS formation found
        return False  # No SOS formation found

    def update_turn_label(self):
        self.turn_label.config(text=f"Player {self.PlayerTrack()}'s turn. Press on 'Make Move' button to finalize your selection")
    
    def start_game(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col]["state"] = tk.DISABLED
        self.symbol_var.set(self.symbols[1 - self.current_player])  # Switch symbol for the next player
        self.update_turn_label()

    def reset_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col]["text"] = ''
                self.buttons[row][col]["state"] = tk.NORMAL
        self.current_player = 0
        self.symbol_var.set(self.symbols[0])
        self.update_turn_label()

class getInput:
    def __init__(self):
        self.get_input()

    def get_input(self):
        self.y = int(input('Enter 1 if you want "simple game"\nEnter 2 if you want "General Game": '))
        self.x = int(input("Enter the desired board size"))
        self.z = int(input('Enter 1 if you want first player to be a computer\nEnter 2 if you want second player to be a computer\nEnter 3 if you want both players to be a computer\nEnter 4 if you want both players to be human: '))

        root = tk.Tk()
        game_gui = SOSGameGUI(root, self.x, self.y, self.z)
        root.mainloop()

if __name__ == "__main__":
    input_class = getInput() 