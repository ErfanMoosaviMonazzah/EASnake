import numpy as np 
class Snake:
    def __init__(self, inp_layer_size = 12, out_layer_size = 4, hidden_layer_count = 2, hidden_layer_nueron_counts = [18, 18]):
        # intializing the NN weights
        self.brain = [np.random.random((inp_layer_size, hidden_layer_nueron_counts[0]))]
        for i in range(1, hidden_layer_count):
            self.brain.append(np.random.random((hidden_layer_nueron_counts[i-1], hidden_layer_nueron_counts[i])))
        self.brain.append(np.random.random((hidden_layer_nueron_counts[-1], out_layer_size)))
        self.body_parts_loc = []
        self.is_alive = True
        
    def grow(self, new_part_loc):
        self.body_parts_loc.append(new_part_loc)      
          
    def decide(self, inp):
        x = inp
        for w in self.brain:
            x = w.T @ x
        # U, D, L, R = 0, 1, 2, 3
        return np.argmax(x)
    
    
    
class Board:
    def __init__(self, board_size = 38, snake = Snake(), verbose = True):
        self.verbose = verbose
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size))
        
        self.snake = snake
        self.score = 0
        
        self.head_loc = np.array([board_size//2, board_size//2])
        self.snake.grow(self.head_loc)
        self.gen_food()
        
    def reach_food(self, direction):
        if direction == 'n':
            return (self.head_loc[0] > self.food_loc[0]) and (self.head_loc[1] == self.food_loc[1])
        if direction == 's':
            return (self.head_loc[0] < self.food_loc[0]) and (self.head_loc[1] == self.food_loc[1])
        if direction == 'w':
            return (self.head_loc[0] == self.food_loc[0]) and (self.head_loc[1] > self.food_loc[1])
        if direction == 'e':
            return (self.head_loc[0] == self.food_loc[0]) and (self.head_loc[1] > self.food_loc[1])
        
        
    def reach_body(self, direction):
        for body in self.snake.body_parts_loc:
            if direction == 'n':
                return (self.head_loc[0] > body[0]) and (self.head_loc[1] == body[1])
            if direction == 's':
                return (self.head_loc[0] < body[0]) and (self.head_loc[1] == body[1])
            if direction == 'w':
                return (self.head_loc[0] == body[0]) and (self.head_loc[1] > body[1])
            if direction == 'e':
                return (self.head_loc[0] == body[0]) and (self.head_loc[1] > body[1])
            
    def distance_to_wall(self, direction):
        if direction == 'n':
            return self.head_loc[0]
        if direction == 's':
            return self.board_size - 1 - self.head_loc[0]
        if direction == 'w':
            return self.head_loc[1]
        if direction == 'e':
            return self.board_size - 1 - self.head_loc[1]
            
    
    def observe(self):
        obs = []
        # up
        obs.append(self.reach_food('n'))
        obs.append(self.reach_body('n'))
        obs.append(self.distance_to_wall('n'))
        # down
        obs.append(self.reach_food('s'))
        obs.append(self.reach_body('s'))
        obs.append(self.distance_to_wall('s'))
        # left
        obs.append(self.reach_food('w'))
        obs.append(self.reach_body('w'))
        obs.append(self.distance_to_wall('w'))
        # right
        obs.append(self.reach_food('e'))
        obs.append(self.reach_body('e'))
        obs.append(self.distance_to_wall('e'))
        
        return [int(o) for o in obs]
        
        
    def gen_food(self):
        while True:
            is_ok = True
            food_loc = np.random.randint((self.board_size, self.board_size))
            for body in self.snake.body_parts_loc:
                if np.all(body == food_loc):
                    is_ok = False
                    break
            if is_ok:
                self.food_loc = food_loc
                return
            
        
    def play(self):
        dis = 1
        while self.snake.is_alive:
            if self.verbose:
                print(f'Moved: {dis}')
            self.play_one_step()
            dis += 1
        return self.score
        
    def play_one_step(self):
        x = self.observe()
        decision = self.snake.decide(x)
        
        if decision == 0: # head up
            self.head_loc[0] -= 1
        if decision == 1: # head down
            self.head_loc[0] += 1
        if decision == 2: # head left
            self.head_loc[1] -= 1
        if decision == 3: # head right
            self.head_loc[0] += 1
        
        # check for head-wall collision
        if np.any(np.sign(self.head_loc) == -1) or np.any(self.head_loc >= np.array([self.board_size, self.board_size])):
            self.snake.is_alive = False
            return
        
        # check for head-body collision
        for i in range(1, len(self.snake.body_parts_loc)):
            if np.all(self.head_loc == self.snake.body_parts_loc[i]):
                self.snake.is_alive = False
                return
        
        # update snake body location
        # head goes to new loc, part before head comes to head loc and ...
        self.snake.body_parts_loc = [self.head_loc] + self.snake.body_parts_loc[:-1]
        
        # gain score if food eaten
        if np.any(self.head_loc == self.food_loc):
            self.score += 1
            # generated new food
            self.gen_food()
            
        if self.verbose:
            print(decision)
        
        
        
        
    