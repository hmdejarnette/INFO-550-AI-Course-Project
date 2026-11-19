import problems as prb
import algorithms as alg


compsToRun = [3]


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

def train_snake(
    num_games=100,
    eval_interval=25
):

    learner = alg.TabularAgent()

    history = {
        "games": [],
        "states": [],
        "avg_score": [],
        "avg_lifetime": []
    }

    for game_num in range(num_games):
        snake = prb.Snake()
        previous_score = 0
  
        lifetime = 0
        max_steps = 1000
        
        while (
            not snake.isTerminal()
            and lifetime < max_steps # simplest way I found to reduce inf loops
        ):
            state = learner.initializeState(snake)
            action = learner.getMove(snake)
            snake.doMove(action)
            next_state = snake.getDiscreteFeatures()
            reward = 0

            # Food reward
            if snake.score > previous_score:
                reward = 1
                previous_score = snake.score

            # Death penalty
            if snake.isTerminal():
                reward = -1

            learner.update(
                state,
                action,
                next_state,
                reward,
                snake.getLegalMoves()
            )

        learner.decayEpsilon()

        if (game_num + 1) % eval_interval == 0:
            avg_score, avg_lifetime = evaluate_snake(
                learner,
                100
            )

            history["games"].append(
                game_num + 1
            )

            history["states"].append(
                learner.getTableSize()
            )

            history["avg_score"].append(
                avg_score
            )

            history["avg_lifetime"].append(
                avg_lifetime
            )

            print(
                f"Games:{game_num+1} "
                f"States:{learner.getTableSize()} "
                f"Score:{avg_score:.2f} "
                f"Life:{avg_lifetime:.2f}"
            )

    return learner, history

def evaluate_snake(
    learner,
    num_games=100
):

    learner.setEvaluationMode()
    old_epsilon = learner.epsilon
    learner.epsilon = 0
    total_score = 0
    total_lifetime = 0

    for _ in range(num_games):
        snake = prb.Snake()
        lifetime = 0
        max_steps = 1000
        
        while (
            not snake.isTerminal()
            and lifetime < max_steps # simplest way I found to reduce inf loops
        ):
            move = learner.getMove(snake)
            snake.doMove(move)
            lifetime += 1
        total_score += snake.score
        total_lifetime += lifetime
    learner.epsilon = old_epsilon
    learner.setTrainingMode()

    return (
        total_score / num_games,
        total_lifetime / num_games
    )


def train_pong(
    num_games=5000,
    eval_interval=250
):

    learner = alg.TabularAgent()

    opponent = alg.RandomAgent()

    history = {
        "games": [],
        "states": [],
        "win_rate": []
    }

    for game_num in range(num_games):

        pong = prb.Pong()

        while not pong.isTerminal():

            state = learner.initializeState(pong)

            action = learner.getMove(pong)

            enemy_action = opponent.getMove(pong)

            pong.doMove(
                (
                    action,
                    enemy_action
                )
            )

            next_state = pong.getDiscreteFeatures()

            reward = 0

            if pong.isTerminal():

                winner = pong.getWinner()

                if winner == 0:

                    reward = 10

                elif winner == 1:

                    reward = -10

            learner.update(
                state,
                action,
                next_state,
                reward,
                pong.getLegalMoves()
            )

        learner.decayEpsilon()

        if (game_num + 1) % eval_interval == 0:

            win_rate = evaluate_pong(
                learner,
                100
            )

            history["games"].append(
                game_num + 1
            )

            history["states"].append(
                learner.getTableSize()
            )

            history["win_rate"].append(
                win_rate
            )

            print(
                f"Games:{game_num+1} "
                f"States:{learner.getTableSize()} "
                f"WinRate:{win_rate:.3f}"
            )

    return learner, history


def evaluate_pong(
    learner,
    num_games=100
):

    learner.setEvaluationMode()

    old_epsilon = learner.epsilon

    learner.epsilon = 0

    opponent = alg.RandomAgent()

    wins = 0

    for _ in range(num_games):

        pong = prb.Pong()

        while not pong.isTerminal():

            action = learner.getMove(pong)

            enemy_action = opponent.getMove(pong)

            pong.doMove(
                (
                    action,
                    enemy_action
                )
            )

        if pong.getWinner() == 0:

            wins += 1

    learner.epsilon = old_epsilon

    learner.setTrainingMode()

    return wins / num_games



if __name__ == "__main__":

    if 0 in compsToRun:
        compare_random_agents()

    if 1 in compsToRun:
        print("\n===== TICTACTOE TRAINING! =====\n")
        learner, history = train_tictactoe(
            num_games=10000,
            eval_interval=500
        )

        print("\n===== TICTACTOE HISTORY =====\n")

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

    if 2 in compsToRun:
        print("\n===== SNAKE TRAINING! =====\n")
        learner, history = train_snake(
            num_games=5000,
            eval_interval=250
        )

        print("\n===== SNAKE HISTORY =====\n")

        for g, s, score, life in zip(
            history["games"],
            history["states"],
            history["avg_score"],
            history["avg_lifetime"]
        ):

            print(
                f"Games:{g:5d} "
                f"States:{s:5d} "
                f"Score:{score:.2f} "
                f"Life:{life:.2f}"
            )
    if 3 in compsToRun:
        print(
            "\n===== PONG TRAINING! =====\n"
        )
    
        learner, history = train_pong(
            num_games=5000,
            eval_interval=250
        )
    
        print(
            "\n===== PONG HISTORY =====\n"
        )
    
        for g, s, w in zip(
            history["games"],
            history["states"],
            history["win_rate"]
        ):
            print(
                f"Games:{g:5d} "
                f"States:{s:5d} "
                f"WinRate:{w:.3f}"
            )
