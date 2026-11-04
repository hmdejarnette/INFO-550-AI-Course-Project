import problems as prb
import algorithms as alg
import cv2


def run_demo():

    print("Running Progress Report Demos...")

    print("\n===== TIC TAC TOE =====\n")

    ttt = prb.Game(
        prb.TicTacToe(),
        alg.RandomAgent(),
        alg.RandomAgent()
    )

    ttt.playGame()

    print("\n===== SNAKE =====\n")

    snake = prb.Game(
        prb.Snake(),
        alg.SnakeRandomAgent(),
        verbose=True,
        singlePlayer=True
    )

    snake.playGame()

    print("\n===== PONG =====\n")

    pong = prb.Game(
        prb.Pong(),
        alg.RandomAgent(),
        alg.RandomAgent()
    )

    pong.playGame()

    print("\n===== GRIDGARIO =====\n")

    agar = prb.Agar()

    agent = alg.RandomAgent()

    for _ in range(1000):

        if agar.isTerminal():

            winner = agar.getWinner()

            if winner == 0:
                print("Player Wins!")

            elif winner == 1:
                print("Enemy Wins!")

            break

        move = agent.getMove(agar)

        agar.doMove(move)

        agar.showState(20)

    print(f"Final Player Mass: {agar.player_mass}")
    print(f"Final Enemy Mass: {agar.enemy_mass}")

    cv2.destroyAllWindows()

def check_features(env):
    print(
        f"\nChecking {env.__class__.__name__}..."
    )
    try:
        features = env.getDiscreteFeatures()

        print(
            f"Discrete Features: {features}"
        )
    except Exception as e:
        print(
            f"{env.__class__.__name__} feature pipeline failed:"
        )

        print(e)
        return False

    print(
        f"{env.__class__.__name__} feature pipeline is valid!"
    )
    return True

if __name__ == "__main__":
    environments = [
        prb.TicTacToe(),
        prb.Snake(),
        prb.Pong(),
        prb.Agar()
    ]
    print("===== FEATURE PIPELINE CHECK =====")
    for env in environments:
        check_features(env)
    print("\n===== DEMONSTRATIONS =====")
    run_demo()
