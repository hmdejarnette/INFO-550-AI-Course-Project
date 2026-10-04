import problems as prb
import algorithms as alg

print("===== TIC TAC TOE =====")

ttt = prb.Game(
    prb.TicTacToe(),
    alg.RandomAgent(),
    alg.RandomAgent()
)
ttt.playGame()

print("===== SNAKE =====")

snake = prb.Game(
    prb.Snake(),
    alg.SnakeRandomAgent(),
    verbose=True,
    singlePlayer=True
)
snake.playGame()

print("===== PONG =====")

pongGame = prb.Game(
    prb.Pong(),
    alg.RandomAgent(),
    alg.RandomAgent()
)

pongGame.playGame()
