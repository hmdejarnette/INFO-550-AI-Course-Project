import problems as prb
import algorithms as alg


compsToRun = [1]


def compare_random_agents(num_games=100):
    winsZero = 0
    winsOne = 0
    draws = 0

    for _ in range(num_games):
        game = prb.Game(
            prb.TicTacToe(),
            alg.RandomAgent(),
            alg.RandomAgent(),
            False
        )

        outcome = game.playGame()

        if outcome == 0:
            winsZero += 1

        elif outcome == 1:
            winsOne += 1

        else:
            draws += 1

    print("\n===== RANDOM VS RANDOM =====\n")

    print(f"P0 Wins : {winsZero}")
    print(f"P1 Wins : {winsOne}")
    print(f"Draws   : {draws}")

def train_tictactoe(num_games=1000):
    learner = alg.TabularAgent()
    opponent = alg.RandomAgent()

    wins = 0
    losses = 0
    draws = 0

    for game_num in range(num_games):
        game = prb.TicTacToe()

        while not game.isTerminal():
            state = learner.initializeState(game)
            action = learner.getMove(game)
            game.doMove(action)

            if game.isTerminal():
                winner = game.getWinner()

                if winner == 0:
                    reward = 1
                    wins += 1

                elif winner == -1:
                    reward = 0
                    draws += 1

                else:
                    reward = -1
                    losses += 1

                learner.update(
                    state,
                    action,
                    state,
                    reward,
                    []
                )

                break

            enemy_move = opponent.getMove(game)
            game.doMove(enemy_move)
            next_state = game.getDiscreteFeatures()

            if game.isTerminal():
                winner = game.getWinner()

                if winner == 0:
                    reward = 1
                    wins += 1

                elif winner == -1:
                    reward = 0
                    draws += 1

                else:
                    reward = -1
                    losses += 1

                learner.update(
                    state,
                    action,
                    next_state,
                    reward,
                    []
                )

                break

            learner.update(
                state,
                action,
                next_state,
                0,
                game.getLegalMoves()
            )

        if (game_num + 1) % 100 == 0:
            print(
                f"Games: {game_num + 1} "
                f"States: {len(learner.qTable)}"
            )

    print("\n===== TRAINING COMPLETE =====\n")

    print(f"Wins   : {wins}")
    print(f"Losses : {losses}")
    print(f"Draws  : {draws}")

    print(
        f"States Learned: "
        f"{len(learner.qTable)}"
    )

    return learner

if __name__ == "__main__":

    if 0 in compsToRun:

        compare_random_agents()

    if 1 in compsToRun:

        train_tictactoe(1000)
