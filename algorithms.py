'''
This file will contain implementations of each algorithm/agent type.
'''
import random

class RandomAgent:
  def __str__(self):
    return "Random Agent"
  def getMove(self, problem):
    moves = problem.getLegalMoves()
    return moves[random.randrange(len(moves))]
  
class SnakeRandomAgent:
    def __str__(self):
      return "Snake Random Agent"
    def getMove(self, problem):
      moves = problem.getLegalMoves()
      return moves[random.randrange(len(moves))]


class TabularAgent:

    def __init__(
        self,
        alpha=0.1,
        gamma=0.95,
        epsilon=0.1
    ):

        self.qTable = {}

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def __str__(self):
        return "Tabular Q Agent"

    def getState(self, problem):
        return problem.getDiscreteFeatures()

    def initializeState(self, problem):
        state = self.getState(problem)

        if state not in self.qTable:

            self.qTable[state] = {}

            for move in problem.getLegalMoves():

                self.qTable[state][move] = 0.0

        return state

    def getMove(self, problem):
        state = self.initializeState(problem)
        legal_moves = problem.getLegalMoves()

        # Exploration
        if random.random() < self.epsilon:
            return random.choice(legal_moves)

        # Exploitation
        best_move = legal_moves[0]
        best_value = self.qTable[state][best_move]

        for move in legal_moves:
            if self.qTable[state][move] > best_value:
                best_move = move
                best_value = self.qTable[state][move]

        return best_move

    def update(
        self,
        state,
        action,
        next_state,
        reward,
        next_legal_moves
    ):

        if next_state not in self.qTable:
            self.qTable[next_state] = {}

            for move in next_legal_moves:

                self.qTable[next_state][move] = 0.0

        current_q = self.qTable[state][action]

        if len(next_legal_moves) > 0:
            max_future_q = max(
                self.qTable[next_state].values()
            )

        else:
            max_future_q = 0.0

        updated_q = current_q + self.alpha * (
            reward +
            self.gamma * max_future_q -
            current_q
        )

        self.qTable[state][action] = updated_q
