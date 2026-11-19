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
          
            if getattr(self.problem, "simultaneous", False):
                move0 = self.players[0].getMove(self.problem)
                move1 = self.players[1].getMove(self.problem)
                self.problem.doMove((move0, move1))
                
            else:
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

   # Placeholder..
   def getDiscreteFeatures(self):
    
      return tuple(
          self.state.flatten().astype(int)
      )

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
        # (-1,0) = UP
        # ( 1,0) = DOWN
        # (0,-1) = LEFT
        # (0, 1) = RIGHT
        #
        # "Driving directly into a wall is bad."
        #
        # Therefore, if at least one non-fatal move
        # exists, we only return the survivable actions.
        #
        # If the snake is completely trapped, return all
        # actions so the game can terminate normally.
    
        candidates = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]
    
        head_r, head_c = self.snake[0] # head row & col
    
        safe_moves = []
    
        for move in candidates:
    
            nr = head_r + move[0]
            nc = head_c + move[1]
    
            # Reject wall collisions
    
            if (
                nr < 0 or
                nr >= self.height or
                nc < 0 or
                nc >= self.width
            ):
                continue
    
            # Reject body collisions
    
            if (nr, nc) in self.snake:
    
                continue
    
            safe_moves.append(move)
    
        # At least one safe move exists
        # -> only expose safe actions
    
        if len(safe_moves) > 0:
    
            return safe_moves
    
        # No safe moves remain
        # -> allow terminal behavior
    
        return candidates


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
            
    def getDiscreteFeatures(self):
    
        return (
            self.getFoodDirection(),
            self.getFoodDistanceBucket(),
            self.getDangerState(),
            self.getLengthBucket()
        )
      
    def getFoodDirection(self):
    
        hr, hc = self.snake[0]
        fr, fc = self.food
    
        return (
            int(np.sign(fr - hr)),
            int(np.sign(fc - hc))
        )

    def getDangerState(self):
    
        return (
            self.isDanger((-1,0)),
            self.isDanger((1,0)),
            self.isDanger((0,-1)),
            self.isDanger((0,1))
        )
    
    def isDanger(self, move):
    
        hr, hc = self.snake[0]
    
        nr = hr + move[0]
        nc = hc + move[1]
    
        if (
            nr < 0 or
            nr >= self.height or
            nc < 0 or
            nc >= self.width
        ):
            return 1
    
        if (nr, nc) in self.snake:
            return 1
    
        return 0
    
    def getLengthBucket(self):
    
        length = len(self.snake)
    
        if length <= 3:
            return 0
    
        elif length <= 6:
            return 1
    
        elif length <= 10:
            return 2
    
        else:
            return 3
          
    def getFoodDistanceBucket(self):
    
        hr, hc = self.snake[0]
        fr, fc = self.food
    
        dist = abs(fr - hr) + abs(fc - hc)
    
        if dist <= 2:
            return 0
    
        elif dist <= 5:
            return 1
    
        else:
            return 2

class Pong:
    
    def __init__(
        self,
        width=40,
        height=20,
        numBalls=4
        ):
    
        self.width = width
        self.height = height
    
        self.paddleHeight = 4
    
        self.p0_y = self.height // 2
        self.p1_y = self.height // 2
    
        self.balls = []
    
        for _ in range(numBalls):
            self.balls.append({
    
                "x": self.width // 2,
    
                "y": self.height // 2,
    
                "vx": np.random.choice([-1, 1]),
    
                "vy": np.random.choice([-1, 1])
    
            })
    
        self.alive = True
        self.winner = -1
    
        self.ticks = -1

    def getLegalMoves(self, state=None):
        return [
            -1,  # up
            0,   # stay
            1    # down
        ]

    def doMove(self, moves):
        p0_move, p1_move = moves

        self.p0_y += p0_move
        self.p1_y += p1_move

        self.p0_y = max(
            0,
            min(
                self.height - self.paddleHeight,
                self.p0_y
            )
        )

        self.p1_y = max(
            0,
            min(
                self.height - self.paddleHeight,
                self.p1_y
            )
        )

        for ball in self.balls:
            ball["x"] += ball["vx"]
            ball["y"] += ball["vy"]

            # Top / bottom wall bounce
            if (
                ball["y"] <= 0 or
                ball["y"] >= self.height - 1
            ):

                ball["vy"] *= -1

            # Left paddle
            if (
                ball["x"] <= 1 and
                self.p0_y <= ball["y"] <= self.p0_y + self.paddleHeight
            ):

                ball["vx"] *= -1

            # Right paddle
            if (
                ball["x"] >= self.width - 2 and
                self.p1_y <= ball["y"] <= self.p1_y + self.paddleHeight
            ):

                ball["vx"] *= -1

            # Score conditions
            if ball["x"] < 0:

                self.alive = False
                self.winner = 1

            elif ball["x"] > self.width:

                self.alive = False
                self.winner = 0

        self.ticks += 1

    def isTerminal(self, state=None):
        return not self.alive

    def getWinner(self, state=None):
        return self.winner

    def showState(self, ms=50):
        screen = np.zeros(
            (
                self.height * 20,
                self.width * 20
            ),
            dtype=np.uint8
        )

        # Left paddle
        cv2.rectangle(

            screen,

            (0, self.p0_y * 20),

            (
                19,
                self.p0_y * 20 +
                self.paddleHeight * 20
            ),

            255,

            -1
        )

        # Right paddle
        cv2.rectangle(

            screen,

            (
                self.width * 20 - 20,
                self.p1_y * 20
            ),

            (
                self.width * 20 - 1,
                self.p1_y * 20 +
                self.paddleHeight * 20
            ),

            255,

            -1
        )

        # All balls
        for ball in self.balls:

            cv2.circle(

                screen,

                (
                    int(ball["x"] * 20),
                    int(ball["y"] * 20)
                ),

                5,

                127,

                -1
            )

        cv2.imshow(
            "Pong",
            screen
        )

        cv2.waitKey(ms)

    def getPriorityBall(self):
        priority_ball = self.balls[0]

        smallest_distance = float("inf")

        for ball in self.balls:

            distance = abs(ball["x"])

            if distance < smallest_distance:

                smallest_distance = distance

                priority_ball = ball

        return priority_ball

    def getBallDirection(self):
        ball = self.getPriorityBall()

        paddle_center = (
            self.p0_y +
            self.paddleHeight / 2
        )

        diff = ball["y"] - paddle_center

        if diff < -2:

            return -1

        elif diff > 2:

            return 1

        else:

            return 0

    def getHorizontalDirection(self):
        ball = self.getPriorityBall()

        if ball["vx"] < 0:

            return -1

        return 1

    def getVerticalDirection(self):
        ball = self.getPriorityBall()

        if ball["vy"] < 0:

            return -1

        return 1

    def getDistanceBucket(self):
    
        ball = self.getPriorityBall()
    
        dist = ball["x"]
    
        if dist < 5:
            return 0
    
        elif dist < 10:
            return 1
    
        elif dist < 15:
            return 2
    
        elif dist < 20:
            return 3
    
        return 4
  
    def getPaddleBucket(self):
        center = (
            self.p0_y +
            self.paddleHeight / 2
        )
    
        if center < self.height / 3:
            return 0
    
        elif center < 2 * self.height / 3:
            return 1
    
        else:
            return 2
    
    def getPriorityBall(self):
        # Choose the ball that is closest to
        # the player's paddle and moving toward it.
        approaching = []
    
        for ball in self.balls:
    
            if ball["vx"] < 0:
    
                approaching.append(ball)
    
        # Prefer an approaching ball
    
        if len(approaching) > 0:
    
            return min(
                approaching,
                key=lambda b: b["x"]
            )
    
        # Otherwise use whichever ball is
        # closest to our paddle.
    
        return min(
            self.balls,
            key=lambda b: b["x"]
        )


    def getDiscreteFeatures(self):

        return (
            self.getBallDirection(),
            self.getHorizontalDirection(),
            self.getVerticalDirection(),
            self.getDistanceBucket(),
            self.getPaddleBucket()
        )
        

class Agar:

    def __init__(self):

        self.width = 20
        self.height = 20

        self.player_pos = (5, 5)
        self.enemy_pos = (24, 24)

        self.player_mass = 1
        self.enemy_mass = 1

        self.food_count = 5
        self.food = []
        # Approximate agario style growth in grid world!
        self.growthPattern = [

            (0, 0),

            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),

            (-1, 1),
            (1, 1),
            (1, -1),
            (-1, -1),

            (0, 2),
            (2, 0),
            (0, -2),
            (-2, 0),

            (-1, 2),
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
            (-2, 1),

            (-2, 2),
            (2, 2),
            (2, -2),
            (-2, -2)
        ]

        while len(self.food) < self.food_count:

            pos = (
                np.random.randint(self.height),
                np.random.randint(self.width)
            )

            if (
                pos != self.player_pos and
                pos != self.enemy_pos and
                pos not in self.food
            ):
                self.food.append(pos)

        self.alive = True
        self.winner = -1
        self.ticks = -1

    def getLegalMoves(self, state=None):

        return [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

    def spawnFood(self):

        while True:

            pos = (
                np.random.randint(self.height),
                np.random.randint(self.width)
            )

            if (
                pos != self.player_pos and
                pos != self.enemy_pos and
                pos not in self.food
            ):
                self.food.append(pos)
                return

    def getGrowthBounds(self, mass):

        cells = self.growthPattern[:mass]

        min_r = min(dr for dr, dc in cells)
        max_r = max(dr for dr, dc in cells)

        min_c = min(dc for dr, dc in cells)
        max_c = max(dc for dr, dc in cells)

        return min_r, max_r, min_c, max_c

    def getOccupiedCells(self, center, mass):

        row, col = center

        cells = []

        for dr, dc in self.growthPattern[:mass]:

            r = row + dr
            c = col + dc

            if (
                0 <= r < self.height and
                0 <= c < self.width
            ):
                cells.append((r, c))

        return cells

    def moveEnemy(self):

        moves = self.getLegalMoves()

        move = moves[np.random.randint(len(moves))]

        er, ec = self.enemy_pos

        er += move[0]
        ec += move[1]

        min_r, max_r, min_c, max_c = \
            self.getGrowthBounds(self.enemy_mass)

        er = max(
            -min_r,
            min(self.height - 1 - max_r, er)
        )

        ec = max(
            -min_c,
            min(self.width - 1 - max_c, ec)
        )

        self.enemy_pos = (er, ec)

    def eatFood(self):

        player_cells = set(
            self.getOccupiedCells(
                self.player_pos,
                self.player_mass
            )
        )

        enemy_cells = set(
            self.getOccupiedCells(
                self.enemy_pos,
                self.enemy_mass
            )
        )

        remaining_food = []

        for food_pos in self.food:

            if food_pos in player_cells:

                self.player_mass += 1

            elif food_pos in enemy_cells:

                self.enemy_mass += 1

            else:

                remaining_food.append(food_pos)

        self.food = remaining_food

        while len(self.food) < self.food_count:
            self.spawnFood()

    def checkCombat(self):

        player_cells = set(
            self.getOccupiedCells(
                self.player_pos,
                self.player_mass
            )
        )

        enemy_cells = set(
            self.getOccupiedCells(
                self.enemy_pos,
                self.enemy_mass
            )
        )

        overlap = player_cells.intersection(enemy_cells)

        #print(
        #    f"PlayerMass={self.player_mass} "
        #    f"EnemyMass={self.enemy_mass} "
        #    f"Overlap={len(overlap)} "
        #    f"PlayerCells={len(player_cells)} "
        #    f"EnemyCells={len(enemy_cells)}"
        #)

        if len(overlap) == 0:
            return

        enemy_overlap = (
            len(overlap) / len(enemy_cells)
        )

        player_overlap = (
            len(overlap) / len(player_cells)
        )

        if (
            enemy_overlap >= 0.5 and
            self.player_mass > self.enemy_mass
        ):

            self.winner = 0
            self.alive = False

        elif (
            player_overlap >= 0.5 and
            self.enemy_mass > self.player_mass
        ):

            self.winner = 1
            self.alive = False

    def doMove(self, move):

        dr, dc = move
        pr, pc = self.player_pos
        pr += dr
        pc += dc

        min_r, max_r, min_c, max_c = \
            self.getGrowthBounds(self.player_mass)

        pr = max(
            -min_r,
            min(self.height - 1 - max_r, pr)
        )

        pc = max(
            -min_c,
            min(self.width - 1 - max_c, pc)
        )

        self.player_pos = (pr, pc)
        self.moveEnemy()
        self.eatFood()
        self.checkCombat()
        self.ticks += 1

    def isTerminal(self, state=None):

        return not self.alive

    def getWinner(self, state=None):

        return self.winner

    ## Placeholder for eventual Q stuff..
    def getDiscreteFeatures(self):

        return (
            self.getNearestFoodDirection(),
            self.getEnemyDirection(),
            self.getEnemyDistanceBucket(),
            self.getMassRelation()
        )
        
    def getNearestFoodDirection(self): 
    
        pr, pc = self.player_pos
    
        nearest_food = None
        nearest_dist = float("inf")
    
        for fr, fc in self.food:
            dist = abs(fr - pr) + abs(fc - pc)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_food = (fr, fc)
    
        if nearest_food is None:
            return (0, 0)
    
        fr, fc = nearest_food
        dr = fr - pr
        dc = fc - pc
    
        return (
            int(np.sign(dr)),
            int(np.sign(dc))
        )

    def getEnemyDirection(self):
    
        pr, pc = self.player_pos
        er, ec = self.enemy_pos
    
        dr = er - pr
        dc = ec - pc
    
        return (
            int(np.sign(dr)),
            int(np.sign(dc))
        )

    def getEnemyDistanceBucket(self):
    # 0 = near
    # 1 = medium
    # 2 = far
        pr, pc = self.player_pos
        er, ec = self.enemy_pos
    
        dist = abs(er - pr) + abs(ec - pc)
    
        if dist <= 2:
            return 0
    
        elif dist <= 5:
            return 1
    
        else:
            return 2

    def getMassRelation(self):
    #0 = smaller
    #1 = same
    #2 =bigger
    
        if self.player_mass < self.enemy_mass:
            return 0
    
        elif self.player_mass == self.enemy_mass:
            return 1
    
        else:
            return 2

    def showState(self, ms=50, state=None):

        cell_size = 20

        screen = np.zeros(
            (
                self.height * cell_size,
                self.width * cell_size
            ),
            dtype=np.uint8
        )

        # food
        for r, c in self.food:

            cv2.rectangle(
                screen,
                (c * cell_size, r * cell_size),
                (
                    (c + 1) * cell_size - 1,
                    (r + 1) * cell_size - 1
                ),
                100,
                -1
            )

        # enemy
        for r, c in self.getOccupiedCells(
            self.enemy_pos,
            self.enemy_mass
        ):

            cv2.rectangle(
                screen,
                (c * cell_size, r * cell_size),
                (
                    (c + 1) * cell_size - 1,
                    (r + 1) * cell_size - 1
                ),
                180,
                -1
            )

        # player
        for r, c in self.getOccupiedCells(
            self.player_pos,
            self.player_mass
        ):

            cv2.rectangle(
                screen,
                (c * cell_size, r * cell_size),
                (
                    (c + 1) * cell_size - 1,
                    (r + 1) * cell_size - 1
                ),
                255,
                -1
            )

        cv2.imshow("Agar", screen)
        cv2.waitKey(ms)
