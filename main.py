import chess
import random


def get_computer_move(board: chess.Board) -> chess.Move:
    # day 1: random legal move. (we hook up stockfish on day 2)
    legal_moves = list(board.legal_moves)
    return random.choice(legal_moves)


def main():
    print("type moves in algebraic notation")
    print("type 'show' to peek at the board. type 'quit' to exit.\n")

    board = chess.Board()

    while not board.is_game_over():
        # player turn
        user_input = input("your move: ").strip()

        if user_input.lower() == 'quit':
            print("resigning. game over.")
            break

        if user_input.lower() == 'show':
            print("\n--- current board ---")
            print(board)
            print("---------------------\n")
            continue

        # parse and play user move
        try:
            move = board.parse_san(user_input)
            board.push(move)
        except ValueError:
            print("invalid move or notation. try again.")
            continue

        if board.is_game_over():
            break

        # computer turn
        comp_move = get_computer_move(board)
        comp_move_san = board.san(comp_move)  # get notation before pushing
        board.push(comp_move)

        print(f"computer plays: {comp_move_san}")

        if board.is_check():
            print("check!")

    # game end results
    if board.is_game_over():
        print("\n--- GAME OVER ---")
        print(f"result: {board.result()}")
        print(board)


if __name__ == "__main__":
    main()