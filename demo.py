import problems as prb
import algorithms as alg

def run_demo():
    print("Running Progress Report Demos...")
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

def check_features(env):
    # Grab our environment
    name = env.__class__.__name__
    
    # Standardize explicit dummy states to prevent internal unpacking crashes...
    if name == 'TicTacToe':
        state = [0] * 9                               # 9 board squares
    elif name == 'Pong':
        state = [0.0, 0.0, 0.0, 0.0, 0.0]             # paddle_y, ball_x, ball_y, vx, vy
    elif name == 'Snake':
        state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]        # head_x, head_y, food_x, food_y, vx, vy
    elif name == 'Agario':
        state = [10.0, 0.0, 0.0, 0.0, 0.0]            # mass, player_x, player_y, food_x, food_y
    else:
        state = []
    
    try:
        f_none = env.getFeatures(state, action=None)
        f_act = env.getFeatures(state, action=0)
    except Exception as e:
        print(f"{env.__class__.__name__} failed layout execution: {e}")
        return False

    if not isinstance(f_none, dict) or "bias" not in f_none:
        print(f"{env.__class__.__name__} is missing valid dictionary or bias key!")
        return False

            
    print(f"{env.__class__.__name__} feature pipeline is valid!")
    return True

if __name__ == "__main__":
    # Test pipelines right before running your legacy run_demo loop 
    for env_class in [prb.TicTacToe, prb.Pong, prb.Snake]:
        check_features(env_class())
        
    run_demo()
