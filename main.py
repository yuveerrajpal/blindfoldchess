import chess
import chess.engine
import sys

STOCKFISH_PATH = "stockfish"
BLUNDER_THRESHOLD = 200


def get_evaluation(engine, board):

    info = engine.analyse(board, chess.engine.Limit(time=0.1))

    return info["score"].white().score(mate_score=10000)


def main():
    print("\n" + "=" * 35)
    print("  BLINDFOLD CHESS: TACTICS COACH  ")
    print("=" * 35)
    print("type moves in SAN (e.g. d4, e4).")
    print("type 'show' to view, 'quit' to exit.\n")

    board = chess.Board()

    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        engine.configure({"skill level": 5})
    except FileNotFoundError:
        print("error: stockfish not found.")
        sys.exit(1)

    try:
        while not board.is_game_over():

            is_white_turn = board.turn == chess.WHITE
            eval_before = get_evaluation(engine, board)

            user_input = input("your move: ").strip()

            if user_input.lower() == 'quit':
                print("resigned. game over.")
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
                print("invalid move or notation. try again.")
                continue

            if board.is_game_over():
                break


            eval_after = get_evaluation(engine, board)


            if is_white_turn:
                eval_drop = eval_before - eval_after
            else:
                eval_drop = eval_after - eval_before


            if eval_drop >= BLUNDER_THRESHOLD:
                print(f"BLUNDER DETECTED@")
                print(f"evaluation dropped by {eval_drop / 100:.2f} points.")
                print("you missed a tactic or hung a piece.")

                choice = input("type 'undo' to take it back, or hit enter to continue: ").strip()
                if choice.lower() == 'undo':
                    board.pop()  # Remove your bad move
                    print("move undone. try again.\n")
                    continue
                else:
                    continue


            result = engine.play(board, chess.engine.Limit(time=0.5))
            comp_move_san = board.san(result.move)
            board.push(result.move)

            print(f"Stockfish plays: {comp_move_san}")

            if board.is_check():
                print("Check!")

    finally:
        engine.quit()

    if board.is_game_over():
        print("\n--- GAME OVER ---")
        print(f"result: {board.result()}")
        print(board)


if __name__ == "__main__":
    main()