import problems as prb
import algorithms as alg
import cv2

def run_demo():

    print("Running Progress Report Demos...")

    #
    # TIC TAC TOE
    #

    print("\n===== TIC TAC TOE =====\n")

    ttt = prb.Game(
        prb.TicTacToe(),
        alg.RandomAgent(),
        alg.RandomAgent()
    )

    ttt.playGame()

    #
    # SNAKE
    #

    print("\n===== SNAKE =====\n")

    snake = prb.Snake()

    agent = alg.SnakeRandomAgent()

    max_ticks = 250

    for _ in range(max_ticks):

        if snake.isTerminal():

            break

        move = agent.getMove(snake)

        snake.doMove(move)

        snake.showState(20)

    print(
        f"Final Score: {snake.score} "
        f"Length: {len(snake.snake)} "
        f"Ticks: {snake.ticks}"
    )

    #
    # PONG
    #

    print("\n===== PONG =====\n")

    pong = prb.Pong()

    p0 = alg.RandomAgent()
    p1 = alg.RandomAgent()

    max_ticks = 250

    for _ in range(max_ticks):

        if pong.isTerminal():

            break

        move0 = p0.getMove(pong)
        move1 = p1.getMove(pong)

        pong.doMove(
            (
                move0,
                move1
            )
        )

        pong.showState(20)

    print(
        f"Winner: {pong.getWinner()} "
        f"Ticks: {pong.ticks}"
    )

    #
    # GRIDGARIO
    #

    print("\n===== GRIDGARIO =====\n")

    agar = prb.Agar()

    agent = alg.RandomAgent()

    max_ticks = 250

    for _ in range(max_ticks):

        if agar.isTerminal():

            break

        move = agent.getMove(agar)

        agar.doMove(move)

        agar.showState(20)

    if agar.isTerminal():

        winner = agar.getWinner()

        if winner == 0:

            print("Player Wins!")

        elif winner == 1:

            print("Enemy Wins!")

    else:

        print(
            f"Demo reached tick limit "
            f"({max_ticks})"
        )

    print(
        f"Final Player Mass: {agar.player_mass}"
    )

    print(
        f"Final Enemy Mass: {agar.enemy_mass}"
    )

    cv2.destroyAllWindows()

if __name__ == "__main__":
    environments = [
        prb.TicTacToe(),
        prb.Snake(),
        prb.Pong(),
        prb.Agar()
    ]

    print("\n===== DEMONSTRATIONS =====")
    run_demo()
