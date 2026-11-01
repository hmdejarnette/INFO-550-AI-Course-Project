import problems as prb
import algorithms as alg

agar = prb.Agar()

agent = alg.RandomAgent()

for _ in range(1000):
  
  if agar.isTerminal():
    print(f"Winner: {agar.getWinner()}")
    break
  move = agent.getMove(agar)
  agar.doMove(move)
  agar.showState(10)


print(
  f"Mass: {agar.player_mass}"
)
