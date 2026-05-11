import chess
import chess.engine
import sys


STOCKFISH_PATH = "stockfish"


def main():
    print("\n" + "=" * 35)
    print("  BLINDFOLD CHESS: ENGINE EDITION  ")
    print("=" * 35)
    print("Type moves in SAN (e.g. d4, e4).")
    print("Type 'show' to view, 'quit' to exit.\n")

    board = chess.Board()

    # engine
    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        # skill level - 0 to 20
        engine.configure({"Skill Level": 5})
    except FileNotFoundError:
        print("Error: Stockfish not found.")
        sys.exit(1)

    try:
        while not board.is_game_over():
            user_input = input("your move: ").strip()

            if user_input.lower() == 'quit':
                print("Resigning. Game over.")
                break

            if user_input.lower() == 'show':
                print("\n--- current board ---")
                print(board)
                print("---------------------\n")
                continue

            try:
                move = board.parse_san(user_input)
                board.push(move)
            except ValueError:
                print("Invalid move or notation. Try again.")
                continue

            if board.is_game_over():
                break


            result = engine.play(board, chess.engine.Limit(time=0.5))
            comp_move = result.move

            comp_move_san = board.san(comp_move)
            board.push(comp_move)

            print(f"Stockfish plays: {comp_move_san}")

            if board.is_check():
                print("Check!")

    finally:

        engine.quit()

    # results
    if board.is_game_over():
        print("\n--- GAME OVER ---")
        print(f"Result: {board.result()}")
        print(board)


if __name__ == "__main__":
    main()