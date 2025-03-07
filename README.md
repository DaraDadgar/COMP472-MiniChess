# Mini Chess Game

## Overview

The purpose of this project is to implement minimax, alpha-beta and develop adversarial heuristics for a Mini Chess game. The game is played on a 5x5 board with a reduced set of pieces. The goal is to capture the opponent's king. The game supports different play modes which are explained further below.

## Features

- **5x5 Chess Board**: The game is played on a smaller board to make it quicker and more accessible.
- **Piece Movement**: Supports standard chess movements for kings, queens, bishops, knights, and pawns.
- **Win Condition**: The game ends when a player captures the opponent's king.
- **Draw Condition**: The game can end in a draw if no pieces are captured for a specified number of turns.
- **Game Logging**: The game logs each move and the state of the board to a text file for further analysis.
- **Adversarial Search**: Implements a minimax algorithm with alpha-beta pruning for AI decision-making.
- **Heuristics**: Includes at least 2 heuristics to evaluate board states and guide the AI's strategy.
- **Play Modes**: Supports human vs. human (H-H), human vs. AI, and AI vs. AI play modes.

## How to Play

1. **Starting the Game**: Run the script to start the game. The initial board configuration will be displayed.
2. **Making Moves**: Players take turns entering moves in the format `B2 B3`, where `B2` is the starting position and `B3` is the destination.
3. **Game End**: The game ends when a player captures the opponent's king or if a draw condition is met.

## Code Structure

- **MiniChess Class**: The main class that handles the game logic, including board initialization, move validation, and game state updates.
  - `init_board()`: Initializes the game board.
  - `display_board(game_state)`: Displays the current state of the board.
  - `is_valid_move(game_state, move)`: Checks if a move is valid.
  - `valid_moves(game_state)`: Returns a list of all valid moves for the current player.
  - `king_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves)`: Updates the list of valid moves with the valid moves for the "King" piece.
  - `knight_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves)`: Updates the list of valid moves with the valid moves for the "Knight" piece.
  - `white_pawn_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves)`: Updates the list of valid moves with the valid moves for the "White Pawn" piece.
  - `black_pawn_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves)`: Updates the list of valid moves with the valid moves for the "Black Pawn" piece.
  - `bishop_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves)`: Updates the list of valid moves with the valid moves for the "Bishop" piece.
  - `queen_valid_moves(self, row_index, col_index, start_row, start_col, game_state, valid_moves)`: Updates the list of valid moves with the valid moves for the "Queen" piece.
  - `number_to_letter(self, number)`: Converts the row numbers into letters for syntax validity
  - `log_move(self, game_state, move)`: Logs the move information to the game file previously generated
  - `parse_input(self, move)`: Parse the input string and modify it into board coordinates
  - `unparse_input(self, move)`: Unparse the input string and modify it into chess terminology.
  - `unparse_input_v2(self, move)`: Unparse the input string and modify it into chess terminology (version 2)
  - `make_move(game_state, move)`: Updates the game state based on the move.
  - `check_win(game_state, move)`: Checks if the move results in a win.
  - `check_draw()`: Checks if the game has reached a draw condition.
  - `play()`: The main game loop that handles player input and game progression.

## Dependencies

- Python 3.x
- Standard Python libraries: `math`, `copy`, `time`, `argparse`, `xml.etree.ElementTree`

## Running the Game

1. Ensure you have Python 3.x installed.
2. Clone the repository or download the script.
3. Run the script using the command:
   ```bash
   python MiniChess.py
   ```
