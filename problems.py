'''
This file will contain your the code for your problems. 
'''

import numpy as np
import cv2

class Game:

    def __init__(self,
                 problem,
                 pZero,
                 pOne=None,
                 verbose=True,
                 singlePlayer=False):

        self.problem = problem
        self.players = [pZero]

        if pOne is not None: #Enable Multiplayer!
            self.players.append(pOne)

        self.verbose = verbose
        self.singlePlayer = singlePlayer

        if self.verbose:
            self.problem.showState()      
            
    def playGame(self):
        pCur = 0
        while not self.problem.isTerminal():
            move = self.players[pCur].getMove(self.problem)
            self.problem.doMove(move)
            if self.verbose:
                self.problem.showState()
            if not self.singlePlayer:
                pCur = abs(pCur - 1)
        if self.singlePlayer:
            print(f"Game Over! Score: {self.problem.score}")
            return self.problem.score
        wIndex = self.problem.getWinner()
        if wIndex == -1:
            winner = "DRAW"
        else:
            winner = self.players[wIndex]
        print(f"The Winner is {winner} ({wIndex})!")
        if self.verbose:
            self.problem.showState(4000)

        return wIndex
              
class TicTacToe:
   def __init__(self):
      self.state = np.zeros((3,3))      
      self.ticks=-1      
   def getLegalMoves(self, state=None):
      if state is None:
         state = self.state
      moves = []
      mark = 1
      if np.sum(np.abs(state))%2!=0:
         mark = -1       
      for i in range(state.shape[0]):
         for j in range(state.shape[1]):
            if state[i,j]==0:
               moves.append((mark,(i,j)))
      return moves             
   def getSuccessor(self, move, state):
      mark = move[0]
      loc = move[1]
      state[loc] = mark
      return state
   def doMove(self,move):
      self.state = self.getSuccessor(move,self.state)
      self.ticks+=1
   def isTerminal(self, state=None):
      if state is None:
         state = self.state         
      terminal = False
      val = self.evalTerminal(state)      
      if val ==0 and np.sum(np.abs(state))==9:
         terminal = True
      if val!=0:
         terminal = True
      return terminal
   def evalTerminal(self, state=None):
      if state is None:
         state = self.state
      val = 0      
      
      pZeroWins = [np.max(np.sum(state,0))==3,np.max(np.sum(state,1))==3,np.trace(state)==3,np.trace(state[:,::-1])==3]
      pOneWins = [np.min(np.sum(state,0))==-3,np.min(np.sum(state,1))==-3,np.trace(state)==-3,np.trace(state[:,::-1])==-3]

      if np.any(pZeroWins):
         val = 1
      if np.any(pOneWins):
         val = -1
      return val
   def getWinner(self, state=None):
      if state is None:
         state = self.state
      val = self.evalTerminal(state)
      if val==1:
         return 0 
      elif val==-1:
         return 1
      else:
         return -1
   def showState(self, ms = 1000,state=None):
      if state is None:
         state = self.state  

      screen = np.zeros((150,150)).astype(np.uint8)         
      screen = cv2.line(screen,(0,49),(149,49),255) 
      screen = cv2.line(screen,(0,99),(149,99),255)
      screen = cv2.line(screen,(49,0),(49,149),255) 
      screen = cv2.line(screen,(99,0),(99,149),255)

      for i in range(state.shape[0]):
         for j in range(state.shape[1]):
            if state[i,j]==1:
               screen = cv2.line(screen,(5 +j*50,5+i*50),(44+j*50,44+i*50),255,2,cv2.LINE_AA) 
               screen = cv2.line(screen,(44+j*50,5+i*50),(5 +j*50,44+i*50),255,2,cv2.LINE_AA) 
            if state[i,j]==-1:
               screen = cv2.circle(screen, (25 +j*50,25+i*50), 20, 255, 2,cv2.LINE_AA) 
               
      cv2.imshow('TicTacToe',screen)
      cv2.waitKey(ms)


class Snake:

    def __init__(self, width=10, height=10):

        self.width = width
        self.height = height

        self.snake = [(5, 5)]
        self.food = None
        self.spawnFood()
        
        self.score = 0
        self.ticks = -1

        self.alive = True
        
        self.history = []
      
    def getLegalMoves(self, state=None):

        return [
            (-1, 0),  # up
            (1, 0),   # down
            (0, -1),  # left
            (0, 1)    # right
        ]

    def doMove(self, move):

        head_r, head_c = self.snake[0]

        new_head = (
            head_r + move[0],
            head_c + move[1]
        )

        self.snake.insert(0, new_head)
        
        if new_head == self.food: #Food found!
            self.score += 1
            self.spawnFood()
        else:
            self.snake.pop()

        self.ticks += 1

        self.checkCollision()
        
        #Save state for training later!
        self.history.append({
          "tick": self.ticks,
          "head": self.snake[0],
          "food": self.food,
          "length": len(self.snake),
          "score": self.score
        })

    def checkCollision(self):

        r, c = self.snake[0]

        if (r < 0 or c < 0 or r >= self.height or c >= self.width):
              
            self.alive = False
            
        if self.snake[0] in self.snake[1:]:
    
            self.alive = False
            
    def isTerminal(self, state=None):
        return not self.alive
      
    def getWinner(self, state=None):#For format reasons..
        return 0

    def showState(self, ms=100):
        #Make our screen
        screen = np.zeros((self.height * 20, self.width * 20), dtype=np.uint8 )
        #Draw our snake
        for r, c in self.snake:
            cv2.rectangle(screen,
                         (c * 20, r * 20),
                         (c * 20 + 19, r * 20 + 19),
                          255,
                          -1 )
        fr, fc = self.food
        #Draw the food
        cv2.circle(screen, (fc * 20 + 10, fr * 20 + 10), 7, 127, -1 )
        print(
          f"Tick:{self.ticks}  "
          f"Length:{len(self.snake)}  "
          f"Score:{self.score}"
        )
        #Show it all
        cv2.imshow("Snake", screen)
        cv2.waitKey(ms)
        
    def spawnFood(self):
      while True:
          r = np.random.randint(self.height)
          c = np.random.randint(self.width)
  
          if (r, c) not in self.snake:
              self.food = (r, c)
              return

    #Will use later..        
    def getFeatures(self):
    
        head = self.snake[0]
    
        return {
            "head_x": head[0],
            "head_y": head[1],
            "food_x": self.food[0],
            "food_y": self.food[1],
            "length": len(self.snake)
        }
