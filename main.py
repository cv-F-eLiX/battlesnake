# Felix Kleindienst
# Pascal Schadei
# Pauline Klingner
# Robin Schneider
# Theo Fischer 224200585

# running at
# http://battlesnake.api64.de

import random
import typing

def food_distance(food: typing.Dict, head: typing.Dict) -> int:
    '''
    food_distance calculates the distance from the head to the food using the Manhattan distance formula
    '''
    return abs(food["x"] - head["x"]) + abs(food["y"] - head["y"])


def collision_detection(game_state: typing.Dict) -> typing.Dict:
    '''
    collision_detection is called on every turn and returns a dictionary with the safe moves
    first it checks if there is a collision with the wall or with any snake body, then it checks if there is a collision with any snake head in the next turn, if there is a collision with a snake head in the next turn, it marks the move as unsafe
    '''
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    snakes = game_state['board']['snakes']
    for snake in snakes:
        for segment in snake['body']:
            if (segment["x"] == my_head["x"] and segment["y"] == my_head["y"] + 1) or my_head["y"] == game_state['board']['height'] - 1:
                is_move_safe["up"] = False
            if (segment["x"] == my_head["x"] and segment["y"] == my_head["y"] - 1) or my_head["y"] == 0:
                is_move_safe["down"] = False
            if (segment["x"] == my_head["x"] + 1 and segment["y"] == my_head["y"]) or my_head["x"] == game_state['board']['width'] - 1:
                is_move_safe["right"] = False
            if (segment["x"] == my_head["x"] - 1 and segment["y"] == my_head["y"]) or my_head["x"] == 0:
                is_move_safe["left"] = False
        head = snake['head']
        if head["x"] == my_head["x"] and head["y"] == my_head["y"]:
            continue
        if (abs(head["x"] - my_head["x"]) == 1 and head["y"] == my_head["y"] + 1) or (head["x"] == my_head["x"] and head["y"] == my_head["y"] + 2):
            is_move_safe["up"] = False
        if (abs(head["x"] - my_head["x"]) == 1 and head["y"] == my_head["y"] - 1) or (head["x"] == my_head["x"] and head["y"] == my_head["y"] - 2):
            is_move_safe["down"] = False
        if (head["x"] == my_head["x"] + 1 and abs(head["y"] - my_head["y"]) == 1) or (head["x"] == my_head["x"] + 2 and head["y"] == my_head["y"]):
            is_move_safe["right"] = False
        if (head["x"] == my_head["x"] - 1 and abs(head["y"] - my_head["y"]) == 1) or (head["x"] == my_head["x"] - 2 and head["y"] == my_head["y"]):
            is_move_safe["left"] = False
    return is_move_safe


def choose_move(game_state: typing.Dict, safe_moves: list[str]) -> str:
    '''
    choose_move is called on every turn and returns the move that leads to food if there is food in the safe moves, otherwise it returns a random move from the safe moves
    '''
    is_move_safe = collision_detection(game_state)

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(
            f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return "down"

    food = game_state['board']['food']
    my_head = game_state["you"]["body"][0]
    preferred_moves = []
    min_distance = float('inf')
    for move in preferred_moves:
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
        "author": "Gruppe 6",  # TODO: Your Battlesnake Username
        "color": "#008CFF",  # TODO: Choose color
        "head": "pixel",  # TODO: Choose head
        "tail": "nr-booster",  # TODO: Choose tail
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

    is_move_safe = collision_detection(game_state)

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    next_move = choose_move(game_state, safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
