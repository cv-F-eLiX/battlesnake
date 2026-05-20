# Felix Kleindienst
# Pascal Schadei
# Pauline Klingner
# Robin Schneider
# Theo Fischer 224200585

# running at
# http://battlesnake.api64.de

import random
import typing


def collision_detection(game_state: typing.Dict) -> typing.Dict:
    '''
    collision_detection is called on every turn and returns a dictionary with the safe moves
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
    
    food= game_state['board']['food']
    my_head = game_state["you"]["body"][0]
    for food_item in food:
        if food_item["x"] == my_head["x"] and food_item["y"] == my_head["y"] + 1 and "up" in safe_moves:
            return "up"
        if food_item["x"] == my_head["x"] and food_item["y"] == my_head["y"] - 1 and "down" in safe_moves:
            return "down"
        if food_item["x"] == my_head["x"] + 1 and food_item["y"] == my_head["y"] and "right" in safe_moves:
            return "right"
        if food_item["x"] == my_head["x"] - 1 and food_item["y"] == my_head["y"] and "left" in safe_moves:
            return "left"
    return random.choice(safe_moves)

def info() -> typing.Dict:
    '''
    info is called when you create your Battlesnake on play.battlesnake.com
    and controls your Battlesnake's appearance
    '''
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Gruppe 6",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
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
