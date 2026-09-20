import problems as prb
import algorithms as alg

def run_TicTacToe_demo():
  
  print("\n== Tic Tac Toe! ==\n")

  demoGame = prb.Game(
    prb.TicTacToe(),
    alg.RandomAgent(),
    alg.RandomAgent()
  )

  demoGame.playGame()

if __name__ == "__main__":
  run_TicTacToe_demo()
