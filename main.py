# Felix Kleindienst
# Pascal Schadei
# Pauline Klingner
# Robin Schneider
# Theo Fischer 224200585

# running at
# http://battlesnake.api64.de

import random
import typing
import itertools

def food_distance(food: typing.Dict, head: typing.Dict) -> int:
    '''
    food_distance calculates the distance from the head to the food using the Manhattan distance formula
    '''
    return abs(food["x"] - head["x"]) + abs(food["y"] - head["y"])


def predict_game_state(small_game_state: typing.Dict, recursion_depth: int) -> typing.Tuple[int, int, int]:
    '''
    predict_game_state is called on every turn and returns a dictionary with the predicted game state for the next turn
    it predicts the position of the snake heads in the next turn and adds them to the game state, so that we can check for collisions with the snake heads in the next turn
    '''
    if recursion_depth == 0:
        return (1, 1, 0)
    else:
        # determine the safe moves for each snake so that we can predict the position of the snake heads in the next turn
        predicted_game_state = small_game_state.copy()
        safe_moves = {}
        for snake in small_game_state['board']['snakes']:
            is_move_safe = collision_detection(small_game_state, snake['head'])
            # collect safe moves per snake
            safe_moves[snake['id']] = []
            for move, isSafe in is_move_safe.items():
                if isSafe:
                    safe_moves[snake['id']].append(move)
            if len(safe_moves) == 0 and snake['id'] == small_game_state['you']['id']:
                return (1, 0, 0) # TODO: might want to return a different value instead of 1 here to indicate at which recursion depth we died
            elif len(safe_moves) == 0:
                predicted_game_state['board']['snakes'].remove(snake)
        
        # build choices as a list of complete move-sets (one move per snake)
        # each element is a dict mapping snake_id -> move
        choices = []
        snake_ids = [snake['id'] for snake in predicted_game_state['board']['snakes']]
        moves_lists = [safe_moves.get(sid, []) for sid in snake_ids]
        # Cartesian product of moves for all snakes
        for combo in itertools.product(*moves_lists):
            move_set = {snake_id: move for snake_id, move in zip(snake_ids, combo)}
            choices.append(move_set)
        
        tries = 0
        alive = 0
        for move_set in choices:
            choice_game_state = predicted_game_state.copy()
            for snake in choice_game_state['board']['snakes']:
                move = move_set.get(snake['id'])
                if move == "up":
                    snake['head']['y'] += 1
                elif move == "down":
                    snake['head']['y'] -= 1
                elif move == "right":
                    snake['head']['x'] += 1
                elif move == "left":
                    snake['head']['x'] -= 1
            outcome = predict_game_state(choice_game_state, recursion_depth - 1)
            tries += outcome[0]
            alive += outcome[1]
        
        return (tries, alive, 0)


def predict_game_tree(small_game_state: typing.Dict, recursion_depth: int, first_move: str) -> float:
    '''
    predict_game_tree is called on every turn for every safe move and returns a score for that move based on the predicted game state for the next turn
    it uses the predict_game_state function to predict the game state for the next turn
    '''
    # determine the safe moves for each snake so that we can predict the position of the snake heads in the next turn
    predicted_game_state = small_game_state.copy()
    safe_moves = {}
    for snake in small_game_state['board']['snakes']:
        is_move_safe = collision_detection(small_game_state, snake['head'])
        # collect safe moves per snake
        safe_moves[snake['id']] = []
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves[snake['id']].append(move)
        if len(safe_moves) == 0:
            predicted_game_state['board']['snakes'].remove(snake)
        
    # build choices as a list of complete move-sets (one move per snake)
    # each element is a dict mapping snake_id -> move
    choices = []
    snake_ids = [snake['id'] for snake in predicted_game_state['board']['snakes']]
    moves_lists = [safe_moves.get(sid, []) for sid in snake_ids]
    # Cartesian product of moves for all snakes
    for combo in itertools.product(*moves_lists):
        move_set = {snake_id: move for snake_id, move in zip(snake_ids, combo)}
        if first_move == move_set.get(small_game_state['you']['id']):
            choices.append(move_set)
        
    tries = 0
    alive = 0
    for move_set in choices:
        choice_game_state = predicted_game_state.copy()
        for snake in choice_game_state['board']['snakes']:
            move = move_set.get(snake['id'])
            if move == "up":
                snake['head']['y'] += 1
            elif move == "down":
                snake['head']['y'] -= 1
            elif move == "right":
                snake['head']['x'] += 1
            elif move == "left":
                snake['head']['x'] -= 1
        outcome = predict_game_state(choice_game_state, recursion_depth - 1)
        tries += outcome[0]
        alive += outcome[1]
    print(f"Move: {first_move}, Tries: {tries}, Alive: {alive}")
    return alive / tries if tries > 0 else 0.0


def collision_detection(small_game_state: typing.Dict, my_head: typing.Dict) -> typing.Dict:
    '''
    collision_detection is called on every turn and returns a dictionary with the safe moves
    first it checks if there is a collision with the wall or with any snake body, then it checks if there is a collision with any snake head in the next turn, if there is a collision with a snake head in the next turn, it marks the move as unsafe
    '''
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    snakes = small_game_state['board']['snakes']
    for snake in snakes:
        # Check for collisions with the snake's body and the walls
        for segment in snake['body']:
            if (segment["x"] == my_head["x"] and segment["y"] == my_head["y"] + 1) or my_head["y"] == small_game_state['board']['height'] - 1:
                is_move_safe["up"] = False
            if (segment["x"] == my_head["x"] and segment["y"] == my_head["y"] - 1) or my_head["y"] == 0:
                is_move_safe["down"] = False
            if (segment["x"] == my_head["x"] + 1 and segment["y"] == my_head["y"]) or my_head["x"] == small_game_state['board']['width'] - 1:
                is_move_safe["right"] = False
            if (segment["x"] == my_head["x"] - 1 and segment["y"] == my_head["y"]) or my_head["x"] == 0:
                is_move_safe["left"] = False
                
    # Try to not move into a position where the opponent can also move to.
    is_move_very_safe = is_move_safe.copy()
    for snake in snakes:
        head = snake['head']
        if head["x"] == my_head["x"] and head["y"] == my_head["y"]:
            continue
        if is_move_very_safe["up"] and (abs(head["x"] - my_head["x"]) == 1 and head["y"] == my_head["y"] + 1) or (head["x"] == my_head["x"] and head["y"] == my_head["y"] + 2):
            is_move_very_safe["up"] = False
        if is_move_very_safe["down"] and (abs(head["x"] - my_head["x"]) == 1 and head["y"] == my_head["y"] - 1) or (head["x"] == my_head["x"] and head["y"] == my_head["y"] - 2):
            is_move_very_safe["down"] = False
        if is_move_very_safe["right"] and (head["x"] == my_head["x"] + 1 and abs(head["y"] - my_head["y"]) == 1) or (head["x"] == my_head["x"] + 2 and head["y"] == my_head["y"]):
            is_move_very_safe["right"] = False
        if is_move_very_safe["left"] and (head["x"] == my_head["x"] - 1 and abs(head["y"] - my_head["y"]) == 1) or (head["x"] == my_head["x"] - 2 and head["y"] == my_head["y"]):
            is_move_very_safe["left"] = False
        if is_move_very_safe["up"] == False and is_move_very_safe["right"] == False and is_move_very_safe["down"] == False and is_move_very_safe["left"] == False:
            return is_move_safe
            
    return is_move_very_safe


def choose_move(small_game_state: typing.Dict, safe_moves: list[str]) -> str:
    '''
    choose_move is called on every turn and returns the move that leads to food if there is food in the safe moves, otherwise it returns a random move from the safe moves
    '''
    my_head = small_game_state["you"]["body"][0]
    is_move_safe = collision_detection(small_game_state, my_head)

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(
            f"MOVE {small_game_state['turn']}: No safe moves detected! Moving down")
        return "down"

    '''food = small_game_state['board']['food']
    my_head = small_game_state["you"]["body"][0]
    preferred_moves = safe_moves.copy()
    min_distance = float('inf')
    for move in safe_moves:
        if move == "up":
            target = {"x": my_head["x"], "y": my_head["y"] + 1}
        elif move == "down":
            target = {"x": my_head["x"], "y": my_head["y"] - 1}
        elif move == "right":
            target = {"x": my_head["x"] + 1, "y": my_head["y"]}
        else:  # move == "left"
            target = {"x": my_head["x"] - 1, "y": my_head["y"]}
        for food_item in food:
            distance = food_distance(food_item, target)
            if distance < min_distance:
                min_distance = distance
                preferred_moves= [move]
            elif distance == min_distance:
                preferred_moves.append(move)'''
    
    max_score = float('-inf')
    preferred_moves = safe_moves.copy()           
    for move in safe_moves:
        score = predict_game_tree(small_game_state, 3, move)
        if score > max_score:
            max_score = score
            preferred_moves = [move]
        elif score == max_score:
            preferred_moves.append(move)

    return random.choice(preferred_moves)


def info() -> typing.Dict:
    '''
    info is called when you create your Battlesnake on play.battlesnake.com
    and controls your Battlesnake's appearance
    '''
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Gruppe 6",
        "color": "#008CFF",
        "head": "pixel",
        "tail": "nr-booster",
    }


def start(game_state: typing.Dict):
    '''
    start is called when your Battlesnake begins a game
    '''
    print("GAME START")


def end(game_state: typing.Dict):
    '''
    end is called when your Battlesnake finishes a game and prints the reason why your Battlesnake lost or won
    '''
    print(f"GAME END: winner: {game_state['board']['snakes'][0]['name']} {game_state['board']['snakes'][0]['id']} with {game_state['board']['snakes'][0]['health']} health and a length of {game_state['board']['snakes'][0]['length']} segments")


def move(game_state: typing.Dict) -> typing.Dict:
    '''
    move is called on every turn and returns your next move
    '''

    '''
    print(f"gamestate: {game_state}") gamestate: {'game': {'id': '88582010-9529-4a44-8d16-173e3d37be94', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 99, 
    'board': 
    {'height': 11, 'width': 11, 
    'snakes': 
    [{'id': 'gs_MpSb6B4FpxrRkqBTYPw66BJY', 'name': 'github', 'latency': '23', 'health': 86, 'body': [{'x': 0, 'y': 5}, {'x': 1, 'y': 5}, {'x': 2, 'y': 5}, {'x': 2, 'y': 4}, {'x': 2, 'y': 3}, {'x': 3, 'y': 3}], 'head': {'x': 0, 'y': 5}, 'length': 6, 'shout': '', 'squad': '', 'customizations': {'color': '#888888', 'head': 'default', 'tail': 'default'}}, 
    {'id': 'gs_w3BDt3RXwSQWyMSVCyXycQh8', 'name': 'Loopy Bot', 'latency': '1', 'health': 1, 'body': [{'x': 9, 'y': 8}, {'x': 8, 'y': 8}, {'x': 8, 'y': 9}], 'head': {'x': 9, 'y': 8}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#800080', 'head': 'caffeine', 'tail': 'iguana'}}], 
    'food': 
    [{'x': 8, 'y': 10}, {'x': 5, 'y': 5}, {'x': 10, 'y': 6}, {'x': 9, 'y': 2}, {'x': 1, 'y': 0}, {'x': 2, 'y': 10}, {'x': 4, 'y': 0}, {'x': 10, 'y': 1}, {'x': 7, 'y': 7}, {'x': 1, 'y': 1}, {'x': 3, 'y': 0}], 
    'hazards': []}, 
    'you': {'id': 'gs_MpSb6B4FpxrRkqBTYPw66BJY', 'name': 'github', 'latency': '23', 'health': 86, 'body': [{'x': 0, 'y': 5}, {'x': 1, 'y': 5}, {'x': 2, 'y': 5}, {'x': 2, 'y': 4}, {'x': 2, 'y': 3}, {'x': 3, 'y': 3}], 'head': {'x': 0, 'y': 5}, 'length': 6, 'shout': '', 'squad': '', 'customizations': {'color': '#888888', 'head': 'default', 'tail': 'default'}}}
    '''
    small_game_state = game_state.copy()
    small_game_state.pop("game")
    for snake in small_game_state['board']['snakes']:
        snake.pop("customizations")
    is_move_safe = collision_detection(small_game_state, game_state["you"]["head"])

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    next_move = choose_move(small_game_state, safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
