import math
import copy
import time
import argparse
from xml.etree.ElementTree import tostring


class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()
        self.turn_counter = 1 #Variable to keep track of the current turn
        self.turn_with_piece_taken = 1 #Variable to keep track of the last turn a piece was taken.
        with open("gameTrace-false-5-10.txt", "w") as file:
            file.write("NEW GAME START!\n\nGAME PARAMETERS:\n")
            file.write("Timeout = 5\nMax Number of Turns = 100\nPlay Mode = H-H")
            file.write("\n\nInitial configuration:\n")
            for i, row in enumerate(self.current_game_state["board"], start=1):
                file.write(str(6 - i) + "  " + ' '.join(piece.rjust(3) for piece in row))
                file.write("\n")
    """
    Initialize the board

    Args:
        - None
    Returns:
        - state: A dictionary representing the state of the game
        *Returns two key-value pairs: board config and player turn for the initial configuration of the game*
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
        valid_moves = self.valid_moves(game_state) #Stores the return value of the valid_moves function
        converted_move = self.unparse_input_v2(move) #Unparses the move into chess terminology to make comparision with valid_moves easier
        #Checks if the move is in the valid_moves list
        return converted_move in valid_moves

    """
    Returns a list of valid moves

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
    def valid_moves(self, game_state):
        #Creating a list of all valid moves which will be returned at the end of the funciton
        valid_moves = list()
        
        #Storing the turn value
        turn = game_state["turn"]
        #Looping through each filled coordinate on the board
        for row_index, row in enumerate(game_state["board"]):
            for col_index, square in enumerate(row):
                #Checking if the move's start position is not empty and it corresponds to the correct turn (white/black)
                if (square[0] != '.' and square[0] == turn[0]):
                    piece_type = square[1] #storing the piece type
                    piece_color = square[0] #storing the piece color
                    #Converting the square coordinates to chess terminology
                    start_row = self.number_to_letter(col_index)
                    start_col = str(5-row_index)
                    #Checking the valid moves based on the piece type
                    if (piece_type == "K"):
                       self.king_valid_moves(row_index, col_index, start_row, start_col, game_state, valid_moves)    
                    if (piece_type == "N"):
                        self.knight_valid_moves(row_index, col_index, start_row, start_col, game_state, valid_moves)
                    if (piece_type == "p" and piece_color == "w"):
                        self.white_pawn_valid_moves(row_index, col_index, start_row, start_col, game_state, valid_moves)
                    if (piece_type == "p" and piece_color == "b"):
                        self.black_pawn_valid_moves(row_index, col_index, start_row, start_col, game_state, valid_moves)
                    if (piece_type == "B"):
                        self.bishop_valid_moves(row_index, col_index, start_row, start_col, game_state, valid_moves)
                    if (piece_type == "Q"):
                        self.queen_valid_moves(row_index, col_index, start_row, start_col, game_state, valid_moves)     
        return valid_moves

    """
    Updates the list of valid moves with the valid moves for the "King" piece

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
        return 
    
    """
    Updates the list of valid moves with the valid moves for the "Knight" piece
    
    """
    def knight_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves):
        for i, row in enumerate(game_state["board"]):
            for j, square in enumerate(row):
                if (square == "." or square[0] != game_state["turn"][0]):
                    if (abs(i-row_index) == 2 and abs(j-col_index) == 1) or (abs(i-row_index) == 1 and abs(j-col_index) == 2):
                        end_row = self.number_to_letter(j)
                        end_col = str(5-i)
                        valid_moves.append(((start_row,start_col),(end_row,end_col)))
        return
    
    """
    Updates the list of valid moves with the valid moves for the "White Pawn" piece
    
    """
    def white_pawn_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves):
        for i, row in enumerate(game_state["board"]):
            for j, square in enumerate(row):
                    if (square == "."):
                        if ((i-row_index) == -1 and j == col_index):
                            end_row = self.number_to_letter(j)
                            end_col = str(5-i)
                            valid_moves.append(((start_row,start_col),(end_row,end_col)))
                    elif (square[0] != game_state["turn"][0]):
                        if ((i-row_index) == -1 and abs(j-col_index) == 1):
                            end_row = self.number_to_letter(j)
                            end_col = str(5-i)
                            valid_moves.append(((start_row,start_col),(end_row,end_col)))   
        return 
    
    """
    Updates the list of valid moves with the valid moves for the "Black Pawn" piece
    
    """
    def black_pawn_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves):
        for i, row in enumerate(game_state["board"]):
            for j, square in enumerate(row):
                    if (square == "."):
                        if ((i-row_index) == 1 and j == col_index):
                            end_row = self.number_to_letter(j)
                            end_col = str(5-i)
                            valid_moves.append(((start_row,start_col),(end_row,end_col)))
                    elif (square[0] != game_state["turn"][0]):
                        if ((i-row_index) == 1 and abs(j-col_index) == 1):
                            end_row = self.number_to_letter(j)
                            end_col = str(5-i)
                            valid_moves.append(((start_row,start_col),(end_row,end_col)))   
        return 

    """
    Updates the list of valid moves with the valid moves for the "Bishop" piece
    
    """  
    def bishop_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # top left, top right, bottom left, bottom right
        for d in directions:
            i, j = row_index + d[0], col_index + d[1]
            while 0 <= i < 5 and 0 <= j < 5:
                if game_state["board"][i][j] == ".":
                    end_row = self.number_to_letter(j)
                    end_col = str(5 - i)
                    valid_moves.append(((start_row, start_col), (end_row, end_col)))
                elif game_state["board"][i][j][0] == game_state["turn"][0]:  # same color piece blocks
                    break
                elif game_state["board"][i][j][0] != game_state["turn"][0]:  # capture opponents piece
                    end_row = self.number_to_letter(j)
                    end_col = str(5 - i)
                    valid_moves.append(((start_row, start_col), (end_row, end_col)))
                    break 
                else:
                    break  
                i += d[0]
                j += d[1]
        return 
    
    """
    Updates the list of valid moves with the valid moves for the "Queen" piece
    
    """

    def queen_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1),  # bishop directions
                      (-1, 0), (1, 0), (0, -1), (0, 1)]  # rook directions
        
        for d in directions:
            i, j = row_index + d[0], col_index + d[1]
            while 0 <= i < 5 and 0 <= j < 5:  
                if game_state["board"][i][j] == ".": 
                    end_row = self.number_to_letter(j)
                    end_col = str(5 - i)
                    valid_moves.append(((start_row, start_col), (end_row, end_col)))
                elif game_state["board"][i][j][0] == game_state["turn"][0]: 
                    break
                elif game_state["board"][i][j][0] != game_state["turn"][0]:  
                    end_row = self.number_to_letter(j)
                    end_col = str(5 - i)
                    valid_moves.append(((start_row, start_col), (end_row, end_col)))
                    break  
                else:
                    break 
                i += d[0]
                j += d[1]
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
    Logs the move information to the game file previously generated

    Args:
        - game_state: dict | the current game state dictionary
        - move: tuple | the move as dictionary coordinates
    """
    def log_move(self, game_state, move):
        board_move = self.unparse_input(move)
        start = board_move[0]
        end = board_move[1]
        with open("gameTrace-false-5-10.txt", "a") as file:
            file.write("\nPlayer = " + game_state["turn"] + "\n")
            file.write("Turn #" + str(self.turn_counter) + "\n")
            file.write("Move from " + start + " to " + end + "\n")
            file.write("New configuration:\n")
            for i, row in enumerate(self.current_game_state["board"], start=1):
                file.write(str(6 - i) + "  " + ' '.join(piece.rjust(3) for piece in row))
                file.write("\n")
        return
    
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
        if  game_state["board"][end_row][end_col] != '.':
            self.turn_with_piece_taken = self.turn_counter
        piece = game_state["board"][start_row][start_col]
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece
        self.log_move(game_state,move)
        if piece == "wp" and end_row == 0:
            game_state["board"][end_row][end_col] = "wQ"
        if piece == "bp" and end_row == 4:
            game_state["board"][end_row][end_col] = "bQ"
        if game_state["turn"] == "white":
            game_state["turn"] = "black"
        else:
            game_state["turn"] = "white"
            self.turn_counter += 1
            print(self.turn_counter)

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
    Unparse the input string and modify it into chess terminology

    Args:
        - move: tuples representing a move "((1,2),(0,3))"
    Returns:
        - string representing a move "B2 B3"
    """
    def unparse_input(self, move):
        try:
            start, end = move  # Extract start and end tuples

            # Convert row index back to board notation (e.g., 3 -> "B")
            start_letter = chr(start[1] + ord('A'))
            start_number = str(5 - start[0])

            end_letter = chr(end[1] + ord('A'))
            end_number = str(5 - end[0])

            return (f"{start_letter}{start_number}", f"{end_letter}{end_number}")
        except:
            return None  # Return None if an error occurs

    """
    Unparse the input string and modify it into chess terminology (version 2)

    Args:
        - move: tuples representing a move "((1,2),(0,3))"
    Returns:
        - tuples representing the start and last move in chess terminology
    """
    def unparse_input_v2(self, move):
        try:
            start, end = move  # Extract start and end tuples

            # Convert row index back to board notation (e.g., 3 -> "B")
            start_letter = chr(start[1] + ord('A'))
            start_number = str(5 - start[0])

            end_letter = chr(end[1] + ord('A'))
            end_number = str(5 - end[0])

            return ((start_letter,start_number), (end_letter, end_number))
        except:
            return None  # Return None if an error occurs

    """
    Check if the move to be made is a win condition. This assumes the move is valid

    Args:
        - move: tuple representing a move ((start_row, start_col),(end_row, end_col))
    Returns:
        - String of which side won, if any.
    """
    def check_win(self, game_state, move):
        # Extract the end position from the move tuple
        endPos = move[1]  # Assuming move is a tuple like ((start_row, start_col), (end_row, end_col))

        # Get the board
        board = game_state["board"]

        # Extract the piece at the end position
        end_piece = board[endPos[0]][endPos[1]]

        # Check if the piece is a black king ('bK') or a white king ('wK')
        if end_piece == "bK":
            return "Black King captured! White wins!"
        elif end_piece == "wK":
            return "White King captured! Black wins!"

        # If no king was captured, return None or False
        return None

    """
    Check if the round we have reached is a draw

    Args:
        - none
    Returns:
        - true if the round we have reached is a draw. False otherwise and game continues as normal
    """
    def check_draw(self):
        if self.turn_counter - self.turn_with_piece_taken >= 2: #edit to change number of turns till end of game
            with open("gameTrace-false-5-10.txt", "a") as file:
                file.write("\nMatch ended in a draw after " + str(self.turn_counter - 1) + " turns")
            return True
        else:
            return False

    """
    Game loop
    
    Args:
        - None
    Returns:
        - None
    """
    def play(self):
        #Printing the initial game information and initial board configuration
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        print("NEW GAME START!\n\nGAME PARAMETERS:\n")
        print("Timeout = 5\nMax Number of Turns = 100\nPlay Mode = H-H")
        print("\n\nInitial configuration:\n")
        self.display_board(self.current_game_state)
        while True:

            if self.check_draw():
                print("Players draw... ending game")
                exit(1)
            if self.turn_counter>2:
                with open("gameTrace-false-5-10.txt", "a") as file:
                    file.write("\nTurn limit reached at " + str(self.turn_counter - 1) + " turns")
                print("Max turn reached... ending game")
                exit(1)
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)

            move = self.parse_input(move)
            if not move or not self.is_valid_move(self.current_game_state, move):
                print("Invalid move. Try again.")
                continue

            #Auto checking if it's a valid move from previous statement
            win_condition = self.check_win(self.current_game_state, move)

            #Making the move
            self.make_move(self.current_game_state, move)

            #Printing the move information and the new board configuration
            printable_move = self.unparse_input(move) #unparsing the move to convert it to chess terminology
            print("\nPlayer = " + self.current_game_state["turn"])
            print("Turn #" + str(self.turn_counter))
            print("Move from " + printable_move[0] + " to " + printable_move[1])
            print("New configuration:\n")
            self.display_board(self.current_game_state)

            if win_condition == "White King captured! Black wins!":
                print(win_condition)
                with open("gameTrace-false-5-10.txt", "a") as file:
                    file.write("\nWhite King captured! Black wins after " + str(self.turn_counter - 1) + " turns")
                exit(1)
            elif win_condition == "Black King captured! White wins!":
                print(win_condition)
                with open("gameTrace-false-5-10.txt", "a") as file:
                    file.write("\nBlack King captured! White wins after " + str(self.turn_counter - 1) + " turns")
                exit(1)

if __name__ == "__main__":
    #Creating an instance of MiniChess
    game = MiniChess()
    #Calling the play() method to initialize the game
    game.play()