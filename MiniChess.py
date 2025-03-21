import math
import copy
import time
import argparse
from string import whitespace
from xml.etree.ElementTree import tostring

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()
        self.turn_counter = 1 #Variable to keep track of the current turn
        self.turn_with_piece_taken = 1 #Variable to keep track of the last turn a piece was taken.
        self.algorithm = None # True = alpha-beta | False = minimax
        self.heuristic = 1 # controls which heuristic to use
        self.depth = 1 #this the depth of how far we are exploring in the game tree
        self.invalid_move_counter = 0 #variable used to end the game if a human enters two invalid moves
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
        converted_move = self.unparse_input_v2(move) #Unparses the move into chess terminology to make comparison with valid_moves easier
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
        #Creating a list of all valid moves which will be returned at the end of the function
        valid_moves = list()
        
        #Storing the turn value
        turn = game_state["turn"]
        #Looping through each filled coordinate on the board
        for row_index, row in enumerate(game_state["board"]):
            for col_index, square in enumerate(row):
                # Checking if the move's start position is not empty, and it corresponds to the correct turn (white/black)
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
    def log_move(self, game_state, move, timeout, max_turns, ai_time=0, heuristic_score=0, search_score=0, states_explored=0, depth_stats=None):

        # Dynamically generate the file name
        # timeout = 5  # Timeout in seconds (can be parameterized)
        # max_turns = 100  # Max number of turns (can be parameterized)
        file_name = f"gameTrace-{self.algorithm}-{timeout}-{max_turns}.txt"

        # Open the file in append mode
        with open(file_name, "a") as file:
            # Log the move details
            board_move = self.unparse_input(move)
            start, end = board_move[0], board_move[1]

            file.write("\nPlayer = " + game_state["turn"] + "\n")
            file.write("Turn #" + str(self.turn_counter) + "\n")
            file.write("Move from " + start + " to " + end + "\n")

            # If AI played this move, log additional details
            if game_state["turn"] == "white":  # Assuming white is AI
                file.write("Time for this action: {:.3f} sec\n".format(ai_time))
                file.write("Heuristic score: {}\n".format(heuristic_score))
                file.write("Alpha-Beta search score: {}\n".format(search_score))
                file.write("Minimax search score: {}\n".format(search_score))
                file.write("Cumulative states explored: {}\n".format(states_explored))

                # Log per-depth statistics
                if depth_stats:
                    file.write("Cumulative states explored by depth: {}\n".format(' '.join(["{}={}".format(d, depth_stats[d]) for d in sorted(depth_stats.keys())])
                    ))
                    total_states = sum(depth_stats.values())
                    file.write("Cumulative % states explored by depth: {}\n".format(' '.join(["{}={:.1f}%".format(d, (depth_stats[d] / total_states) * 100) for d in sorted(depth_stats.keys())])
                    ))

                    # Calculate and log average branching factor
                    total_nodes = sum(depth_stats.values()) - depth_stats.get(0, 0)
                    total_branches = sum([d * depth_stats[d] for d in depth_stats if d > 0])
                    avg_branching_factor = total_branches / total_nodes if total_nodes > 0 else 0
                    file.write("Average branching factor: {:.2f}\n".format(avg_branching_factor))

            # Log the new board configuration
            file.write("New configuration:\n")
            for i, row in enumerate(self.current_game_state["board"], start=1):
                file.write(str(6 - i) + "  " + ' '.join(piece.rjust(3) for piece in row))
                file.write("\n")

            file.write("\n")  # Blank line for readability
            
    def make_move(self, game_state, move):
        start = move[0]
        end = move[1]
        start_row, start_col = start
        end_row, end_col = end
        #Update the turn_with_piece_taken if a piece is taken
        if  game_state["board"][end_row][end_col] != '.':
            self.turn_with_piece_taken = self.turn_counter
        #store the piece value in a variable
        piece = game_state["board"][start_row][start_col]
        #Replace the starting position with a '.' and move the piece to the end location
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece
        #Logging the move performed
        # self.log_move(game_state,move) #Logging the move of the player
        #Promoting the pawns if they reach the end row
        if piece == "wp" and end_row == 0:
            game_state["board"][end_row][end_col] = "wQ"
        if piece == "bp" and end_row == 4:
            game_state["board"][end_row][end_col] = "bQ"
        #Switiching the turn once the move is successfuly performed
        if game_state["turn"] == "white":
            game_state["turn"] = "black"
        else:
            game_state["turn"] = "white"
        #Increase the turn counter and print it
            self.turn_counter += 1
            print(self.turn_counter)
        #return the new game state after the move has been performed
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
    Parse a valid_moves string and modify it into board coordinates

    Args:
        - move: string representing a validl move "((B, 2), (B, 3))"
    Returns:
        - (start, end)  tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    """
    def parse_input_v2(self, move):
        try:
            start, end = move  # Unpack the input tuple (e.g., ((B, 2), (B, 3)))

            # Convert the start and end into 0-indexed coordinates
            start = (5 - int(start[1]), ord(start[0].upper()) - ord('A'))  # Row, Column for start
            end = (5 - int(end[1]), ord(end[0].upper()) - ord('A'))  # Row, Column for end

            return (start, end)

        except Exception as e:
            print(f"Error parsing input: {e}")
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
        if self.turn_counter - self.turn_with_piece_taken >= 10: #edit to change number of turns till end of game
            with open("gameTrace-false-5-10.txt", "a") as file:
                file.write("\nMatch ended in a draw after " + str(self.turn_counter - 1) + " turns")
            return True
        else:
            return False

    """
    Evaluates a board state and updates the heuristic score based on the heuristic chosen (3 heuristics available)
    NOTE: White player tries to maximies and Black player tries to minimize in all heuristics

    Args:
        - game_state: dictionary | Dictionary representing the current game state
    Returns:
        - score: integer value representing the heuristic score of the board state passed as a parameter to the function
    """
    def evaluate_board(self, game_state):
        #Heuristic 0
        if self.heuristic == 0:     #UNCOMMENT TO ADD OTHER HEURISTICS
            piece_values = {"K": 999, "Q": 9, "B": 3, "N": 3, "p": 1}
            score = 0
            blackKing = False
            whiteKing = False
            #Assigning values to each piece on the board based on the heuristic function defined
            for row in game_state["board"]:
                for square in row:
                    if square != ".":
                        value = piece_values[square[1]]
                        #Increase the value of score if it is a white piece, otherwise decrease
                        score += value if square[0] == "w" else -value
                    if square == "wK":
                        whiteKing = True
                    if square == "bK":
                        blackKing = True

            if whiteKing == False or blackKing == False: return True,score
            return False,score
        #Heuristic 1
        elif self.heuristic == 1:   #UNCOMMENT TO ADD OTHER HEURISTICS
            piece_values = {"K": 999, "Q": 9, "B": 3, "N": 3, "p": 1}
            score = 0
            blackKing = False
            whiteKing = False
            #Assigning values to each piece on the board based on the heuristic function defined
            for row in game_state["board"]:
                for square in row:
                    if square != ".":
                        value = piece_values[square[1]]
                        #Increase the value of score if it is a white piece, otherwise decrease
                        score += value if square[0] == "w" else -value
                    if square == "wK":
                        whiteKing = True
                    if square == "bK":
                        blackKing = True

            #Adjusting the score value based on the total number of valid_moves for the current game_state
            if (game_state["turn"] == "white"):
                num_white_moves = len(self.valid_moves(game_state)) * 0.1
                game_state["turn"] = "black"
                num_black_moves = len(self.valid_moves(game_state)) * 0.1
                game_state["turn"] = "white"
            else:
                num_black_moves = len(self.valid_moves(game_state)) * 0.1
                game_state["turn"] = "white"
                num_white_moves = len(self.valid_moves(game_state)) * 0.1
                game_state["turn"] = "black"
                
            score += (num_white_moves - num_black_moves)
            # print("New score: " + str(score))

            if whiteKing == False or blackKing == False: return True,score
            return False,score
        #Heuristic 2
        else:      
            return

    """
    Simulates a move on the board. Used by the minimax and alpha-beta algorithms to find the heuristic value of a new board state.

    Args:
        - game_state: dictionary | Dictionary representing the current game state
        - move: tuple representing a move ((start_row, start_col),(end_row, end_col))
    Returns:
        - piece: the type of piece that made the move
        - captured_piece: the piece type that was captured after performing the move
        - game_state: the new modified game_state after the move was performed
    """
    def simulate_make_move(self, game_state, move):
        ## SIMPLIFIED MAKE MOVE FUNCTION

        start, end = move
        # Save the piece at the destination (if any) for undoing later.
        captured_piece = game_state["board"][end[0]][end[1]]

        # Move the piece from the start to the end position.
        piece = game_state["board"][start[0]][start[1]]
        game_state["board"][start[0]][start[1]] = "."
        game_state["board"][end[0]][end[1]] = piece

        # Pawn Promotion
        if piece == "wp" and end[0] == 0:
            game_state["board"][end[0]][end[1]] = "wQ"
        if piece == "bp" and end[0] == 4:
            game_state["board"][end[0]][end[1]] = "bQ"

        # Switch the turn.
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

        return piece,captured_piece, game_state

    """
        Reverts a move on the game_state by restoring the piece's previous position
        and the captured piece (if any).

        Args:
            game_state (dict): The current board state and turn.
            move (tuple): A tuple ((start_row, start_col), (end_row, end_col)).
            captured_piece: The piece that was on the destination square before the move.
            :param game_state:
            :param captured_piece:
            :param original_piece:
    """
    def simulate_unmake_move(self, game_state, move, captured_piece, original_piece):
        start, end = move
        piece = original_piece

        # Restore the moved piece to its original square.
        game_state["board"][start[0]][start[1]] = piece
        # Restore the captured piece (or empty square) at the destination.
        game_state["board"][end[0]][end[1]] = captured_piece

        # Switch the turn back.
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

        return game_state


    def alpha_beta(self, game_state, current_depth, alpha, beta):
        piece_values = {"K": 999, "Q": 9, "B": 3, "N": 3, "p": 1}
        MoveList = self.valid_moves(game_state)
        game_end,board_heuristic = self.evaluate_board(game_state)
        
        if game_end:  # No valid moves, return heuristic as is (Case if parent is win/loss condition)
            return (None, board_heuristic)
                
        #initialize tracking variables for stats
        if not hasattr(self, "total_states_explored"):
            self.total_states_explored = 0  
            self.depth_exploration_stats = {}
        #update the total number of states explored
        self.total_states_explored += 1

        #update the depth exploration stats
        if current_depth not in self.depth_exploration_stats:
            self.depth_exploration_stats[current_depth] = 0
        self.depth_exploration_stats[current_depth] += 1

        if current_depth % 2 == 1:  # Max node (AI's turn)
            current_best_heuristic = alpha
        else:  # Min node (Opponent's turn)
            current_best_heuristic = beta
        current_best_move = None #first move by default
        current_Alpha = alpha
        current_Beta = beta
        # Loop start to evaluate children
        for move in MoveList:
            move = self.parse_input_v2(move) # ((A,2),(B,2)) => ((3,0),(
            # Will do recursion to go to children for internal nodes
            if current_depth < self.depth:  # If we're not at the max depth then go one layer down by simulating the move
                original_piece,captured_piece, game_state = self.simulate_make_move(game_state, move)
                results = self.alpha_beta(game_state, current_depth + 1, current_Alpha, current_Beta)
                if (current_depth % 2) == 1 and results[1] > current_best_heuristic: # parent is a max node | AI's turn | we're looking for the max
                    current_best_heuristic = results[1]
                    current_best_move = move
                    current_Alpha = results[1]
                    game_state = self.simulate_unmake_move(game_state, move, captured_piece, original_piece) # Restore board history
                    if current_Alpha >= current_Beta: break  # PRUNE SIBLINGS
                    continue # Evaluate next move
                elif (current_depth % 2) == 0 and results[1] < current_best_heuristic: # parent is a min node | opponent's turn | we're looking for the minimum
                    current_best_heuristic = results[1]
                    current_best_move = move
                    current_Beta = results[1]
                    game_state = self.simulate_unmake_move(game_state, move, captured_piece, original_piece) # Restore board history
                    if current_Alpha >= current_Beta: break  # PRUNE SIBLINGS
                    continue # Evaluate next move
                game_state = self.simulate_unmake_move(game_state, move, captured_piece, original_piece)  # Restore board history
                continue

            ##START OF EVALUATING EXTERNAL NODES
            move_heuristic = board_heuristic
            end_row, end_col = move[1]
            if (current_depth % 2) == 1 : # parent is a max node | AI's turn | we're looking for the max
                original_piece, captured_piece, game_state = self.simulate_make_move(game_state, move)
                ignore, move_heuristic = self.evaluate_board(game_state)
                game_state = self.simulate_unmake_move(game_state, move, captured_piece, original_piece)  # Restore board history
                # if game_state["board"][end_row][end_col] != ".":
                #     value = piece_values[game_state["board"][end_row][end_col][1]]
                #     move_heuristic -= value if game_state["board"][end_row][end_col][0] == "w" else -value
                #     # Compensate diff for pawn promotion
                #     if game_state["board"][end_row][end_col] == "wp" and end_row == 0: move_heuristic += 8
                #     if game_state["board"][end_row][end_col] == "bp" and end_row == 5: move_heuristic -= 8

                if move_heuristic > current_best_heuristic:
                    current_best_heuristic = move_heuristic
                    current_best_move = move
                    current_Alpha = current_best_heuristic
            else : # parent is a min node | opponent's turn | we're looking for the minimum
                original_piece, captured_piece, game_state = self.simulate_make_move(game_state, move)
                ignore, move_heuristic = self.evaluate_board(game_state)
                game_state = self.simulate_unmake_move(game_state, move, captured_piece, original_piece)  # Restore board history

                # if game_state["board"][end_row][end_col] != ".":
                #     value = piece_values[game_state["board"][end_row][end_col][1]]
                #     move_heuristic -= value if game_state["board"][end_row][end_col][0] == "w" else -value
                #     # Compensate diff for pawn promotion
                #     if game_state["board"][end_row][end_col] == "wp" and end_row==0: move_heuristic += 8
                #     if game_state["board"][end_row][end_col] == "bp" and end_row == 5: move_heuristic -= 8

                if move_heuristic < current_best_heuristic:
                    current_best_heuristic = move_heuristic
                    current_best_move = move
                    current_Beta = current_best_heuristic

            if current_Alpha >= current_Beta: break  # PRUNE SIBLINGS
        return current_best_move, current_best_heuristic

    """
    AI minimax function. Recursively expands the game tree from the given current_depth 
    and finds the best move to be performed by the AI.

    Args:
        - game_state: dictionary | Dictionary representing the current game state
        - current_depth: integer value representing the current depth of the game tree being explored
    Returns:
        - best_move: the best move from the current board state after developing the full game tree
        - best_value: the heuristic value of the best move to be taken 
    """
    def minimax(self, game_state, current_depth):
        # Initialize tracking variables for stats
        if not hasattr(self, "total_states_explored"):
            self.total_states_explored = 0
            self.depth_exploration_stats = {}

        # Update the total number of states explored
        self.total_states_explored += 1

        # Update the depth exploration stats
        if current_depth not in self.depth_exploration_stats:
            self.depth_exploration_stats[current_depth] = 0
        self.depth_exploration_stats[current_depth] += 1

        # Get the list of valid moves and evaluate the current board
        MoveList = self.valid_moves(game_state)
        current_board_value = self.evaluate_board(game_state)

        # Terminal condition: No moves available(win, loss or draw) or reached maximum depth
        #TODO: make sure the valid_moves is empty after a draw, win or loss??
        if not MoveList:
            return (None, current_board_value)
        if current_depth == self.depth:
            return (None, current_board_value)

        # Determine if this is a max node/white's turn or a min node/black's turn
        if current_depth % 2 == 1:  # Max node (turn = white)
            best_value = -math.inf
            best_move = None
            for move in MoveList:
                # Convert move to internal format
                move = self.parse_input_v2(move)

                # Simulate the move (modifies game_state in place)
                original_piece, captured_piece, game_state = self.simulate_make_move(game_state, move)

                # Recursively evaluate the resulting board state
                _, child_value = self.minimax(game_state, current_depth + 1)

                # Undo the move to restore the original state
                self.simulate_unmake_move(game_state, move, captured_piece, original_piece)

                # Update if this move is better than previously seen moves
                if child_value > best_value:
                    best_value = child_value
                    best_move = move

            return (best_move, best_value)
        else:  # Min node (black = turn)
            best_value = math.inf
            best_move = None
            for move in MoveList:
                move = self.parse_input_v2(move)
                original_piece, captured_piece, game_state = self.simulate_make_move(game_state, move)
                _, child_value = self.minimax(game_state, current_depth + 1)
                self.simulate_unmake_move(game_state, move, captured_piece, original_piece)

                # Update if this move is lower than previously seen moves
                if child_value < best_value:
                    best_value = child_value
                    best_move = move

            return (best_move, best_value)

    """
    Return the best move to be performed by the AI after running either minimax or alpha-beta algorithms.
    It runs the AI algorithm starting from 

    Args:
        - game_state: dictionary | Dictionary representing the current game state
    Returns:
        - best_move: the best move to be performed by the AI from the current board state after developing the full game tree
        - eval_time: the time taken to find the best move using the algorithm chosen
    """
    def AI_makeMove(self, game_state, turn):
        #Determine the starting depth based on the AI's turn
        revertDepth = False
        if turn == "white":
            start_depth = 1
        else:
            start_depth = 2
            self.depth += 1
            revertDepth = True
        
        if self.algorithm: 
            start = time.time() #starting a timer before the algorithm method is called
            results = self.alpha_beta(game_state,start_depth,-15000,15000)
            end = time.time() #ending the timer once the algorithm finishes execution
        else:
            start = time.time()
            results = self.minimax(game_state,start_depth) 
            end = time.time()

        if revertDepth:
            self.depth -= 1
            revertDepth = False
        #Computing the evalutation time to find the best move
        eval_time = round(end - start, 7)
        #Storing the best move found by the algorithm chosen
        best_move = results[0]    
        heuristic_score = results[1]
        #returns the best move found using either alpha-beta or minimax algorithm and the time taken to find that move
        result_info = best_move, eval_time, heuristic_score
        return result_info

    """
    Main game loop which inputs the user to choose their prefered game mode and game parameters
    and launches that game mode
    
    Args:
        - None
    Returns:
        - None
    """
    def play(self):
        #Printing the initial game information and initial board configuration
        print("Welcome to Mini Chess!\n")
        print("1- Human vs Human\n2- AI vs Human\n3- Human vs AI\n4- AI vs AI\n")
        #Registering the user's game mode selection
        game_mode = input("Please Select a Game Mode(ex: 1 for \"Human vs Human\"): ")
        while(1): 
            #Launching the appropriate game based on the user's selection
            if game_mode == "1":
                max_turns = input("Enter the maximum number of turns before the end of the game: ")
                self.h_vs_h(max_turns)
            elif game_mode == "2":
                timeout = input("Enter the maximum time (in seconds) allocated for the AI to make a move: ")
                max_turns = input("Enter the maximum number of turns before the end of the game: ")
                algorithm = input("Enter the algorithm you want to use for the AI(m for minimax and a for alpha-beta): ")
                while(1):
                    if (algorithm == "m"):
                        self.algorithm = False
                        self.ai_vs_h(timeout, max_turns)
                    elif (algorithm == "a"):
                        self.algorithm = True
                        self.ai_vs_h(timeout, max_turns)
                    else:
                        algorithm = input("Incorrect input! Please try again: ")   
                        continue 
                exit(1)
            elif game_mode == "3":
                timeout = input("Enter the maximum time (in seconds) allocated for the AI to make a move: ")
                max_turns = input("Enter the maximum number of turns before the end of the game: ")
                algorithm = input("Enter the algorithm you want to use for the AI(m for minimax and a for alpha-beta): ")
                while(1):
                    if (algorithm == "m"):
                        self.algorithm = False
                        self.h_vs_ai(timeout, max_turns)
                    elif (algorithm == "a"):
                        self.algorithm = True
                        self.h_vs_ai(timeout, max_turns)
                    else:
                        algorithm = input("Incorrect input! Please try again: ")   
                        continue 
                exit(1)
            elif game_mode == "4":
                timeout = input("Enter the maximum time (in seconds) allocated for the AI to make a move: ")
                max_turns = input("Enter the maximum number of turns before the end of the game: ")
                heuristic_white_AI = input("Enter the heuristic you'd like white AI to use (0,1,2): ")
                heuristic_black_AI = input("Enter the heuristic you'd like black AI to use (0,1,2): ")
                algorithm = input("Enter the algorithm you want to use for the AI(m for minimax and a for alpha-beta): ")
                while True:
                    if algorithm == "m":
                        self.algorithm = False
                        self.ai_vs_ai(timeout, max_turns, int(heuristic_white_AI), int(heuristic_black_AI))
                    elif algorithm == "a":
                        self.algorithm = True
                        self.ai_vs_ai(timeout, max_turns, int(heuristic_white_AI), int(heuristic_black_AI))
                    else:
                        algorithm = input("Incorrect input! Please try again: ")   
                        continue 
                exit(1)
            else:
                game_mode = input("Invalid Input! Please try again: ")
        exit(1)

    """
    Human vs Human game mode
    
    Args:
        - max_turns: a string indicating the maximum number of turns before the game ends
    Returns:
        - None
    """
    def h_vs_h(self, max_turns):
        #Printing the initial game information and initial board configuration
        print()
        print("-------------------------------------------------------------------")
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        print("NEW GAME START!\n\nGAME PARAMETERS:\n")
        print("Timeout = 5\nMax Number of Turns = " + max_turns + "\nPlay Mode = H-H")
        print("\n\nInitial configuration:\n")
        self.display_board(self.current_game_state)
        while True:

            if self.check_draw():
                print("Players draw... ending game")
                exit(1)
            if self.turn_counter>int(max_turns):
                with open("gameTrace-false-5-10.txt", "a") as file:
                    file.write("\nTurn limit reached at " + str(self.turn_counter - 1) + " turns")
                print("Max turn reached... ending game")
                exit(1)
            #Asking the user for their move input
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)

            move = self.parse_input(move)
            if not move or not self.is_valid_move(self.current_game_state, move):
              if (self.invalid_move_counter < 2):
                  self.invalid_move_counter += 1 #incrementing the count of invalid moves
                  #Ending the game if two invalid moves are entered
                  if(self.invalid_move_counter == 2):
                    print("You entered two invalid moves in a row!")
                    if (self.current_game_state["turn"] == "white"):
                        print("Black wins!")
                        exit(1)
                    else:
                        print("White wins!")   
                        exit(1)
                  #Otherwise, we alert the user for thier invalid move and continue the loop
                  else:
                    print("Invalid move. Try again.")
                    continue
            
            #Reseting the invalid_move_counter for reuse in next turns
            self.invalid_move_counter = 0
            
            #Auto checking if it's a valid move from previous statement
            win_condition = self.check_win(self.current_game_state, move)

            #Making the move
            self.make_move(self.current_game_state, move)
            #logging human move, no AI details here
            #if() #if human move then log move
            self.log_move(self.current_game_state, move, max_turns=max_turns, timeout=None)


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

    """
    AI vs Human game mode
    
    Args:
        - timeout: string indicating the maximum time allowed for the AI to return the best move
        - max_turns: a string indicating the maximum number of turns before the game ends
    Returns:
        - None
    """
    def ai_vs_h(self, timeout, max_turns):
        #Checking the algorithm chosen by the user
        if self.algorithm: alg = "Alpha-Beta" 
        else: alg = "Minimax"
        #Printing the initial game information and initial board configuration
        print()
        print("-------------------------------------------------------------------")
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        print("NEW GAME START!\n\nGAME PARAMETERS:\n")
        print("Timeout = " + timeout + " s\nMax Number of Turns = " + max_turns + "\nPlay Mode = AI-H\nAI Algorithm = " + alg)
        print("\n\nInitial configuration:\n")
        self.display_board(self.current_game_state)
        while True:

            if self.check_draw():
                print("Players draw... ending game")
                exit(1)
            if self.turn_counter>int(max_turns):
                with open("gameTrace-false-5-10.txt", "a") as file:
                    file.write("\nTurn limit reached at " + str(self.turn_counter - 1) + " turns")
                print("Max turn reached... ending game")
                exit(1)
            print(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if self.current_game_state['turn'] == "white":
                turn = "white"
                start_time = time.perf_counter()
                move_info = self.AI_makeMove(self.current_game_state, turn)
                search_score = move_info[2]
                #Unloading the first element of the tuple (best_move) into a move variable
                move = move_info[0]
                #Make the AI lose if the best move found is not the current list of valid moves
                if not self.is_valid_move(self.current_game_state, move):
                    print("Invalid move entered by the AI! The Human wins.")
                    exit(1)
                end_time = time.perf_counter()
                ai_time_taken = end_time - start_time
                heuristic_score = self.evaluate_board(self.current_game_state)
                states_explored = self.total_states_explored  
                depth_stats = self.depth_exploration_stats 
                self.log_move(self.current_game_state, move, timeout, max_turns, ai_time_taken, heuristic_score, search_score, states_explored, depth_stats)
                ##here
                print(self.unparse_input(move))
                print("Time taken to find the move: " + str(move_info[1]) + " seconds")
                #Ending the game if the AI takes longer than the timeout value to find the best move
                if move_info[1] > float(timeout):
                    print("Timeout value reached! Black wins!")
                    exit(1)
            else:
                move = input()
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

    """
    Human vs AI game mode
    
    Args:
        - timeout: string indicating the maximum time allowed for the AI to return the best move
        - max_turns: a string indicating the maximum number of turns before the game ends
    Returns:
        - None
    """
    def h_vs_ai(self, timeout, max_turns):
        #Checking the algorithm chosen by the user
        if self.algorithm: alg = "Alpha-Beta" 
        else: alg = "Minimax"
        #Printing the initial game information and initial board configuration
        print()
        print("-------------------------------------------------------------------")
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        print("NEW GAME START!\n\nGAME PARAMETERS:\n")
        print("Timeout = " + timeout + " s\nMax Number of Turns = " + max_turns + "\nPlay Mode = H-AI\nAI Algorithm = " + alg)
        print("\n\nInitial configuration:\n")
        self.display_board(self.current_game_state)
        while True:

            if self.check_draw():
                print("Players draw... ending game")
                exit(1)
            if self.turn_counter>int(max_turns):
                with open("gameTrace-false-5-10.txt", "a") as file:
                    file.write("\nTurn limit reached at " + str(self.turn_counter - 1) + " turns")
                print("Max turn reached... ending game")
                exit(1)
            print(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if self.current_game_state['turn'] == "black":
                turn = "black"
                move_info = self.AI_makeMove(self.current_game_state, turn)
                #Unloading the first element of the tuple (best_move) into a move variable
                move = move_info[0]
                #Make the AI lose if the best move found is not the current list of valid moves
                if not self.is_valid_move(self.current_game_state, move):
                    print("Invalid move entered by the AI! The Human wins.")
                    exit(1)
                print(self.unparse_input(move))
                print("Time taken to find the move: " + str(move_info[1]) + " seconds")
                #Ending the game if the AI takes longer than the timeout value to find the best move
                if move_info[1] > float(timeout):
                    print("Timeout value reached! White wins!")
                    exit(1)
            else:
                move = input()
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

    
    """
    AI vs AI game mode
    
    Args:
        - timeout: string indicating the maximum time allowed for the AI to return the best move
        - max_turns: a string indicating the maximum number of turns before the game ends
    Returns:
        - None
    """
    def ai_vs_ai(self, timeout, max_turns, white_heuristic, black_heuristic):
        #Checking the algorithm chosen by the user
        if self.algorithm: alg = "Alpha-Beta" 
        else: alg = "Minimax"
        #Printing the initial game information and initial board configuration
        print()
        print("-------------------------------------------------------------------")
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        print("NEW GAME START!\n\nGAME PARAMETERS:\n")
        print("Timeout = " + timeout + " s\nMax Number of Turns = " + max_turns + "\nPlay Mode = AI-AI\nAI Algorithm = " + alg)
        print("\n\nInitial configuration:\n")
        self.display_board(self.current_game_state)
        while True:

            if self.check_draw():
                print("Players draw... ending game")
                exit(1)
            if self.turn_counter>int(max_turns):
                with open("gameTrace-false-5-10.txt", "a") as file:
                    file.write("\nTurn limit reached at " + str(self.turn_counter - 1) + " turns")
                print("Max turn reached... ending game")
                exit(1)
            print(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if self.current_game_state['turn'] == "white":
                turn = "white"
                self.heuristic = white_heuristic
                move_info = self.AI_makeMove(self.current_game_state, turn)
                #Unloading the first element of the tuple (best_move) into a move variable
                move = move_info[0]
                #Make the AI lose if the best move found is not the current list of valid moves
                if not self.is_valid_move(self.current_game_state, move):
                    print("Invalid move entered by the AI! Black wins.")
                    exit(1)
                print(self.unparse_input(move))
                print("Time taken to find the move: " + str(move_info[1]) + " seconds")
                #Ending the game if the AI takes longer than the timeout value to find the best move
                if move_info[1] > float(timeout):
                    print("Timeout value reached! Black wins!")
                    exit(1)
            else:
                turn = "black"
                self.heuristic = black_heuristic
                move_info = self.AI_makeMove(self.current_game_state, turn)
                #Unloading the first element of the tuple (best_move) into a move variable
                move = move_info[0]
                #Make the AI lose if the best move found is not the current list of valid moves
                if not self.is_valid_move(self.current_game_state, move):
                    print("Invalid move entered by the AI! White wins.")
                    exit(1)
                print(self.unparse_input(move))
                print("Time taken to find the move: " + str(move_info[1]) + " seconds")
                #Ending the game if the AI takes longer than the timeout value to find the best move
                if move_info[1] > float(timeout):
                    print("Timeout value reached! White wins!")
                    exit(1)


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