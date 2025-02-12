import math
import copy
import time
import argparse

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()

    """
    Initialize the board

    Args:
        - None
    Returns:
        - state: A dictionary representing the state of the game
        *Reteurns two key-value pairs: board config and player turn for the initial configuration of the game*
    """
    def init_board(self):
        state = {
                "board": 
                [['bK', 'bQ', 'bB', 'bN', '.'],
                ['.', '.', 'bp', 'bp', '.'],
                ['.', '.', '.', '.', '.'],
                ['.', 'wp', 'wp', '.', '.'],
                ['.', 'wN', 'wB', 'wQ', 'wK']],
                "turn": 'white',
                }
        return state

    """
    Prints the board
    
    Args:
        - game_state: Dictionary representing the current game state
    Returns:
        - None
    """
    def display_board(self, game_state):
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print()
        print("     A   B   C   D   E")
        print()

    """
    Check if the move is valid    
    
    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move which we check the validity of ((start_row, start_col),(end_row, end_col))
    Returns:
        - boolean representing the validity of the move
    """
    def is_valid_move(self, game_state, move):
        # Check if move is in list of valid moves

        #Stores the return value of the valid_moves function in a variable
        #and checks if the move passed as an argument is in that list of valid moves.
        #valid_moves = self.valid_moves(game_state)
        #if move in valid_moves:
            return True
        #else:
          # return False

    """
    Returns a list of valid moves

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
    def valid_moves(self, game_state):
        # Return a list of all the valid moves.
        # Implement basic move validation
        # Check for out-of-bounds, correct turn, move legality, etc

        #Creating a list of all valid moves which will be returned at the end of the funciton
        valid_moves = list()
        
        #Storing the turn value
        turn = game_state["turn"]
        #Looping through each filled coordinate on the board
        for row_index, row in enumerate(game_state["board"]):
            for col_index, square in enumerate(row):
                if (square[0] != '.' and square[0] == turn[0]):
                    piece = square[1] #storing the piece type
                    start_row = self.number_to_letter(col_index)
                    start_col = str(5-row_index)
                    if (piece == "K"):
                       self.king_valid_moves(row_index, col_index, start_row, start_col, game_state, valid_moves)              
        return

    """
    Updates the list of valid moves with the valid moves for the King piece

    Args:
        - row_index: int | current row position of the square in the dictionary of game_state
        - col_index: int | current column position of the square in the dictionary of game_state
        - start_now: str | current row letter of the square
        - start_col: int | current column number of the square
        - game_state: dict | Dictionary representing the current game state
        - valid_moves: list | A list of nested tuples corresponding to valid moves
    Returns:
        - valid_moves: list | Updated list of nested tuples corresponding to valid moves
    """
    def king_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves):
        for i, row in enumerate(game_state["board"]):
            for j, square in enumerate(row):
                if (square == "." or square[0] != game_state["turn"][0]):
                    if (abs(i-row_index) <= 1 and abs(j-col_index) <= 1):
                        end_row = self.number_to_letter(j)
                        end_col = str(5-i)
                        valid_moves.append(((start_row,start_col),(end_row,end_col)))
        print(valid_moves)
        return 

    """
    Converts the row numbers into letters for syntax validity

    Args:
        - number: int | integer value holding a row number
    Returns:
        - char | returns a single character corresponding to the conversion of the number to a letter
    """
    def number_to_letter(self, number):
        return chr(number + ord("A"))

    """
    Modify the board to make a move

    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state:   dictionary | Dictionary representing the modified game state
    """
    def make_move(self, game_state, move):
        start = move[0]
        end = move[1]
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

        return game_state

    """
    Parse the input string and modify it into board coordinates

    Args:
        - move: string representing a move "B2 B3"
    Returns:
        - (start, end)  tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    """
    def parse_input(self, move):
        try:
            start, end = move.split() #Splits the move (B2 B3) into start=B2 and end=B3
            start = (5-int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5-int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
        except:
            return None

    """
    Game loop

    Args:
        - None
    Returns:
        - None
    """
    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        while True:
            self.display_board(self.current_game_state)
            self.valid_moves(self.current_game_state)
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)

            move = self.parse_input(move)
            if not move or not self.is_valid_move(self.current_game_state, move):
                print("Invalid move. Try again.")
                continue
                    
            self.make_move(self.current_game_state, move)
            


if __name__ == "__main__":
    #Creating an instance of MiniChess
    game = MiniChess()
    #Calling the play() method to initialize the game
    game.play()