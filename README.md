# Mini Chess Game

## Overview

The purpose of this project is to implement minimax, alpha-beta and develop adversarial heuristics for a Mini Chess game. The game is played on a 5x5 board with a reduced set of pieces. The goal is to capture the opponent's king. The game supports different play modes which are explained further below.

## Features

- **5x5 Chess Board**: The game is played on a smaller board to make it quicker and more accessible.
- **Piece Movement**: Supports standard chess movements for kings, queens, bishops, knights, and pawns.
- **Win Condition**: The game ends when a player captures the opponent's king.
- **Draw Condition**: The game can end in a draw if no pieces are captured for a specified number of turns.
- **Game Logging**: The game logs each move and the state of the board to a text file for further analysis.
- **Adversarial Search**: Implements a minimax and an alpha-beta pruning algorithms for AI decision-making.
- **Heuristics**: Includes 3 heuristics to evaluate board states and guide the AI's strategy. The user chooses the heuristic used by the AI.
- **Play Modes**: Supports human vs. human, AI vs. human, human vs. AI and AI vs. AI play modes.

## How to Play

1. **Starting the Game**: Run the script to start the game.
2. **Select a Game Mode**: Select your preferred game mode out of the 4 game modes displayed (HvsH, AIvsH, HvsAI, AIvsAI).
3. **Add the Game Parameters**: Based on the game mode selection, enter the requested parameters such as timeout, maximum number of turns and AI algorithm to use.
4. **Making a Move**: When it is your turn, the game asks you to enter a move. You can enter a move by simply writing the starting and end positions of your move (E1 E2).
5. **Game End**: The game ends when a player captures the opponent's king or if a draw condition is met.

## Code Structure

The **MiniChess** project implements a simplified chess game with AI-powered decision-making. The code is structured as follows:

### 1. Initialization and Game Setup
- `__init__(self)`: Initializes the game state, turn counters, AI settings, and other parameters.
- `init_board(self)`: Sets up the initial board configuration.
- `display_board(self, game_state)`: Prints the current board state to the console.

### 2. Game Mechanics
- `parse_input(self, move)`: Converts user input (e.g., `"B2 B3"`) into board coordinates.
- `parse_input_v2(self, move)`: Converts valid moves into board coordinates.
- `unparse_input(self, move)`: Converts board coordinates back to chess notation.
- `is_valid_move(self, game_state, move)`: Checks if a move is valid.
- `valid_moves(self, game_state)`: Computes a list of all legal moves for the current board state.
- `make_move(self, game_state, move)`: Updates the board and switches turns after a move.
- `check_win(self, game_state, move)`: Checks if a move results in a win.
- `check_draw(self)`: Determines if the game is a draw due to move limitations.

### 3. AI Implementation
- `evaluate_board(self, game_state)`: Calculates the heuristic value of the board state.
- `alpha_beta(self, game_state, current_depth, alpha, beta)`: Implements the **Alpha-Beta Pruning** algorithm for AI decision-making.
- `minimax(self, game_state, current_depth)`: Implements the **Minimax Algorithm** for AI decision-making.
- `AI_makeMove(self, game_state, turn)`: Determines the best move for AI players.

### 4. Game Modes
- `play(self)`: Main game loop that prompts the user to select a mode.
- `h_vs_h(self, max_turns)`: Human vs. Human game mode.
- `ai_vs_h(self, timeout, max_turns)`: AI vs. Human mode.
- `h_vs_ai(self, timeout, max_turns)`: Human vs. AI mode.
- `ai_vs_ai(self, timeout, max_turns, white_heuristic, black_heuristic)`: AI vs. AI mode.

### 5. Logging and Debugging
- `log_move(self, game_state, move, max_turns, timeout=None, ai_time=0, heuristic_score=0, search_score=0, states_explored=0, depth_stats=None, player=None)`: Logs game moves and AI statistics.
- `simulate_make_move(self, game_state, move)`: Simulates a move for AI evaluation.
- `simulate_unmake_move(self, game_state, move, captured_piece, original_piece)`: Undoes a simulated move.

### 6. Utility Functions
- `number_to_letter(self, number)`: Converts column indices to chess notation (e.g., `0 → "A"`).
- `is_ai_player(self, player)`: Checks if a given player is controlled by AI.


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
