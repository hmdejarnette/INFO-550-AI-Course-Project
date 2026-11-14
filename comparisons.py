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


def train_tictactoe(
    num_games=10000,
    eval_interval=500
):

    learner = alg.TabularAgent()

    opponent = alg.RandomAgent()

    history = {
        "games": [],
        "states": [],
        "avg_q": [],
        "win_rate": []
    }

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

                elif winner == -1:
                    reward = 0

                else:
                    reward = -1

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

                elif winner == -1:
                    reward = 0

                else:
                    reward = -1

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
        learner.decayEpsilon()

        if (game_num + 1) % eval_interval == 0:
            win_rate = evaluate_tictactoe(
                learner,
                100
            )
            history["games"].append(
                game_num + 1
            )
            history["states"].append(
                learner.getTableSize()
            )
            history["avg_q"].append(
                learner.getAverageQ()
            )
            history["win_rate"].append(
                win_rate
            )
            print(
                f"Games:{game_num+1} "
                f"States:{learner.getTableSize()} "
                f"Win%:{win_rate:.2f}"
            )

    return learner, history

def evaluate_tictactoe(
    learner,
    num_games=1000
):

    learner.setEvaluationMode()

    old_epsilon = learner.epsilon
    learner.epsilon = 0

    opponent = alg.RandomAgent()

    wins = 0

    for _ in range(num_games):
        game = prb.TicTacToe()

        while not game.isTerminal():
            move = learner.getMove(game)
            game.doMove(move)

            if game.isTerminal():
                break

            enemy_move = opponent.getMove(game)

            game.doMove(enemy_move)

        if game.getWinner() == 0:
            wins += 1

    learner.epsilon = old_epsilon

    learner.setTrainingMode()

    return wins / num_games


if __name__ == "__main__":

    learner, history = train_tictactoe(
        num_games=10000,
        eval_interval=500
    )

    print("\n===== HISTORY =====\n")

    for g, s, q, w in zip(
        history["games"],
        history["states"],
        history["avg_q"],
        history["win_rate"]
    ):

        print(
            f"Games:{g:5d} "
            f"States:{s:5d} "
            f"AvgQ:{q:.3f} "
            f"Win%:{w:.3f}"
        )
