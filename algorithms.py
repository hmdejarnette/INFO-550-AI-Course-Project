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
    def __init__(self):
        self.qTable = {}

    def getState(self, problem):
        return problem.getDiscreteFeatures()
      
    def getQValue(self, state, action):
        if state not in self.qTable:
            self.qTable[state] = {}
        if action not in self.qTable[state]:
            self.qTable[state][action] = 0.0
        return self.qTable[state][action]

    def initializeActions(self, problem):
        state = self.getState(problem)
        if state not in self.qTable:
            self.qTable[state] = {}
            for action in problem.getLegalMoves():
                self.qTable[state][action] = 0.0
                
    def showTableSize(self):
        print(
            f"States Stored: {len(self.qTable)}"
        )
