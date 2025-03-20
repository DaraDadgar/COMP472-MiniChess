import math
import copy
import time
import argparse
from xml.etree.ElementTree import tostring

# from selenium.webdriver.common.devtools.v85.runtime import evaluate


class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()
        self.turn_counter = 1 #Variable to keep track of the current turn
        self.turn_with_piece_taken = 1 #Variable to keep track of the last turn a piece was taken.
        self.algorithm = True # True = alpha-beta | false = minimax
        self.heuristic = 0 # controls which heuristic to use
        self.depth = 3 # How deep is your love (CHANGE BEFORE SUBMISSION) | this the depth of how far we checkin lols
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
    def log_move(self, game_state, move, ai_time=0, heuristic_score=0, search_score=0, states_explored=0, depth_stats=None):

        # Dynamically generate the file name
        timeout = 5  # Timeout in seconds (can be parameterized)
        max_turns = 100  # Max number of turns (can be parameterized)
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
        if  game_state["board"][end_row][end_col] != '.':
            self.turn_with_piece_taken = self.turn_counter
        piece = game_state["board"][start_row][start_col]
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece
        # self.log_move(game_state,move) #Logging the move of the player
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

    def evaluate_board(self, game_state):
        #if self.heuristic == 0:     #UNCOMMENT TO ADD OTHER HEURISTICS
            piece_values = {"K": 999, "Q": 9, "B": 3, "N": 3, "p": 1}
            score = 0
            for row in game_state["board"]:
                for square in row:
                    if square != ".":
                        value = piece_values[square[1]]
                        score += value if square[0] == "w" else -value
            return score
        #elif self.heuristic == 1:   #UNCOMMENT TO ADD OTHER HEURISTICS
            #HEURISTIC 1             #UNCOMMENT TO ADD OTHER HEURISTICS
        #else                        #UNCOMMENT TO ADD OTHER HEURISTICS
            #HEURISTIC 2

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

    def simulate_unmake_move(self, game_state, move, captured_piece, original_piece):
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
        board_heuristic = self.evaluate_board(game_state)

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

        if not MoveList:  # No valid moves, return heuristic as is (Case if parent is win/loss condition)
            return (None, board_heuristic)

        if current_depth % 2 == 1:  # Max node (AI's turn)
            current_best_heuristic = alpha
        else:  # Min node (Opponent's turn)
            current_best_heuristic = beta
        current_best_move = None #first move by default
        current_Alpha = alpha
        current_Beta = beta
        # Loop start to evaluate children
        for move in MoveList:
            move = self.parse_input_v2(move)
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
                elif results[1] < current_best_heuristic: # parent is a min node | opponent's turn | we're looking for the minimum
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
                if game_state["board"][end_row][end_col] != ".":
                    value = piece_values[game_state["board"][end_row][end_col][1]]
                    move_heuristic -= value if game_state["board"][end_row][end_col][0] == "w" else -value
                    # Compensate diff for pawn promotion
                    if game_state["board"][end_row][end_col] == "wp" and end_row == 0: move_heuristic += 8
                    if game_state["board"][end_row][end_col] == "bp" and end_row == 5: move_heuristic -= 8
                if move_heuristic > current_best_heuristic:
                    current_best_heuristic = move_heuristic
                    current_best_move = move
                    current_Alpha = current_best_heuristic
            else : # parent is a min node | opponent's turn | we're looking for the minimum
                if game_state["board"][end_row][end_col] != ".":
                    value = piece_values[game_state["board"][end_row][end_col][1]]
                    move_heuristic -= value if game_state["board"][end_row][end_col][0] == "w" else -value
                    # Compensate diff for pawn promotion
                    if game_state["board"][end_row][end_col] == "wp" and end_row==0: move_heuristic += 8
                    if game_state["board"][end_row][end_col] == "bp" and end_row == 5: move_heuristic -= 8

                if move_heuristic < current_best_heuristic:
                    current_best_heuristic = move_heuristic
                    current_best_move = move
                    current_Beta = current_best_heuristic

            if current_Alpha >= current_Beta: break  # PRUNE SIBLINGS
        return current_best_move, current_best_heuristic

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

        # Terminal condition: No moves available or reached maximum depth
        if not MoveList:
            return (None, current_board_value)
        if current_depth == self.depth:
            return (None, current_board_value)

        # Determine if this is a max node (AI's turn) or min node (opponent's turn)
        if current_depth % 2 == 1:  # Max node (AI's turn)
            best_value = -math.inf
            best_move = None
            for move in MoveList:
                # Convert move to internal format
                move = self.parse_input_v2(move)

                # Simulate the move (modifies game_state in place)
                storedPiece, game_state = self.simulate_make_move(game_state, move)

                # Recursively evaluate the resulting board state
                _, child_value = self.minimax(game_state, current_depth + 1)

                # Undo the move to restore the original state
                self.simulate_unmake_move(game_state, move, storedPiece)

                # Update if this move is better than previously seen moves
                if child_value > best_value:
                    best_value = child_value
                    best_move = move

            return (best_move, best_value)
        else:  # Min node (Opponent's turn)
            best_value = math.inf
            best_move = None
            for move in MoveList:
                move = self.parse_input_v2(move)
                storedPiece, game_state = self.simulate_make_move(game_state, move)
                _, child_value = self.minimax(game_state, current_depth + 1)
                self.simulate_unmake_move(game_state, move, storedPiece)

                # Update if this move is lower than previously seen moves
                if child_value < best_value:
                    best_value = child_value
                    best_move = move

            return (best_move, best_value)
        
    def AI_makeMove(self, game_state):
        # start_time = time.perf_counter() 
        if self.algorithm: results = self.alpha_beta(game_state,1,-15000,15000) #UNCOMMENT WHEN MINIMAX IS IMPLEMENTED
        else: results = self.minimax(game_state,1)                            #UNCOMMENT WHEN MINIMAX IS IMPLEMENTED
        # end_time = time.perf_counter()
        # ai_time_taken = end_time - start_time

        # apply the move
        best_move, search_score = results
        # self.make_move(game_state, best_move)
        heuristic_score = self.evaluate_board(self.current_game_state)
        print("This is the Heuristic Score ----------------", heuristic_score)
        print("This is the Search Score ----------------", search_score)
        # self.log_move(game_state, best_move, heuristic_score, search_score, states_explored, depth_stats)
        #     game_state, best_move, ai_time_taken,
        #     self.evaluate_board(game_state), search_score,
        #     states_explored, depth_stats
        # )
        return best_move, search_score


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
            if self.turn_counter>200:
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
            #logging human move, no AI details here
            #if() #if human move then log move
            self.log_move(self.current_game_state, move)
    

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

    def play_AI_Human(self):
        #Printing the initial game information and initial board configuration
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        print("NEW GAME START!\n\nGAME PARAMETERS:\n")
        print("Timeout = 5\nMax Number of Turns = 100\nPlay Mode = AI-H")
        print("\n\nInitial configuration:\n")
        self.display_board(self.current_game_state)
        while True:

            if self.check_draw():
                print("Players draw... ending game")
                exit(1)
            if self.turn_counter>200:
                with open("gameTrace-false-5-10.txt", "a") as file:
                    file.write("\nTurn limit reached at " + str(self.turn_counter - 1) + " turns")
                print("Max turn reached... ending game")
                exit(1)
            print(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if self.current_game_state['turn'] == "white":
                start_time = time.perf_counter()
                move, search_score = self.AI_makeMove(self.current_game_state)
                end_time = time.perf_counter()
                ai_time_taken = end_time - start_time
                heuristic_score = self.evaluate_board(self.current_game_state)
                states_explored = self.total_states_explored  
                depth_stats = self.depth_exploration_stats 
                self.log_move(self.current_game_state, move, ai_time_taken, heuristic_score, search_score, states_explored, depth_stats)
                ##here
                print(self.unparse_input(move))
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
if __name__ == "__main__":
    #Creating an instance of MiniChess
    game = MiniChess()
    #Calling the play() method to initialize the game
    game.play_AI_Human()
    #game.play()