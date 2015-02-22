import bottle
import json
import sys

from random import choice
# This comment means nothing I am just testing something

UP = u'up'
RIGHT = u'right'
DOWN = u'down'
LEFT = u'left'

smacktalk = [
              'All your base are belong to us',
              '#GETREKT',
              '#GETSHREKT',
              'BOOM HEADSHOT!',
              'Im sorry Dave, Im afraid i cant do that',
              'Rippety-tip-top-kek',
              'When the bass goes harangity woup woup woup clackity grind',
              'Dmitrii please'
            ]

@bottle.get('/')
def index():
    return """
        <a href="https://github.com/james-gray/nagini">
            nagini
        </a>
    """


@bottle.post('/start')
def start():
    # data = bottle.request.json

    return json.dumps({
        'name': 'nagini',
        'color': '#22ff00',
        'head_url': 'https://raw.githubusercontent.com/james-gray/nagini/master/SnakeHead.png',
        'taunt': choice(smacktalk)
    })

def get_adjacent_cells(nagini, board):
    width = len(board)
    height = len(board[0])

    coords = nagini['coords']
    head_x, head_y = coords[0][0], coords[0][1]

    adjacents = []

    if head_x + 1 < width:
        adjacents.append({'x': head_x+1, 'y': head_y, 'direction': RIGHT})
    if head_x - 1 >= 0:
        adjacents.append({'x': head_x-1, 'y': head_y, 'direction': LEFT})
    if head_y + 1 < height:
        adjacents.append({'x': head_x, 'y': head_y+1, 'direction': DOWN})
    if head_y - 1 >= 0:
        adjacents.append({'x': head_x, 'y': head_y-1, 'direction': UP})

    return adjacents

def seppuku(nagini, board):
    coords = nagini['coords']
    head_x, head_y = coords[0][0], coords[0][1]
    adjacents = get_adjacent_cells(nagini, board)

    directions = [
        adj['direction']
        for adj in adjacents
        if board[adj['x']][adj['y']]['snake'] == 'nagini'
    ]

    return choice(directions)


def look_ahead(head_x, head_y, board):
    width = len(board)
    height = len(board[0])

    directions = []
    safe_states = ('empty', 'food')

    if head_x + 1 < width - 1 and board[head_x+1][head_y]['state'] in safe_states:
        directions.append(RIGHT)
    if head_x - 1 >= 1 and board[head_x-1][head_y]['state'] in safe_states:
        directions.append(LEFT)
    if head_y + 1 < height - 1 and board[head_x][head_y+1]['state'] in safe_states:
        directions.append(DOWN)
    if head_y - 1 >= 1 and board[head_x][head_y-1]['state'] in safe_states:
        directions.append(UP)

    return directions

def get_possible_directions(nagini, board):
    coords = nagini['coords']
    head_x, head_y = coords[0][0], coords[0][1]

    look_ahead1 = look_ahead(head_x, head_y, board)

    directions = []

    for direction in look_ahead1:
        if direction == UP:
            look_aheadUP = look_ahead(head_x, head_y-1, board)
            if len(look_aheadUP) > 0:
                directions.append(UP)
        elif direction == DOWN:
            look_aheadDOWN = look_ahead(head_x, head_y+1, board)
            if len(look_aheadDOWN) > 0:
                directions.append(DOWN)
        elif direction == LEFT:
            look_aheadLEFT = look_ahead(head_x-1, head_y, board)
            if len(look_aheadLEFT) > 0:
                directions.append(LEFT)
        elif direction == RIGHT:
            look_aheadRIGHT = look_ahead(head_x+1, head_y, board)
            if len(look_aheadRIGHT) > 0:
                directions.append(RIGHT)

    return directions

@bottle.post('/move')
def move():
    data = bottle.request.json

    width = len(data['board'])
    height = len(data['board'][0])

    nagini = [s for s in data['snakes'] if s['name'] == 'nagini'][0]
    coords = nagini['coords']
    head_x, head_y = coords[0][0], coords[0][1]

    directions = get_possible_directions(nagini, data['board'])
    if not directions:
        # Commit suicide honorably so as not to give any victories to
        # the other inferior snakes!
        return json.dumps({
            'move': seppuku(nagini, data['board']),
            'taunt': 'You will always remember this as the day you almost caught Captain Jack Sparrow!'
        })

    # If not on an edge, start moving towards one
    if not any([head_x in (1, width-2), head_y in (1, height-2)]):
        edge_distances = [
            (UP, head_y - 1),
            (RIGHT, width - head_x - 2),
            (DOWN, height - head_y - 2),
            (LEFT, head_x -1)
        ]
        dist_min = sys.maxint
        # min_index = -1

        # Find the closest edge's index
        for i, d in enumerate(edge_distances):
            if d[1] < dist_min:
                dist_min = edge_distances[i][1]
                index = i

        direction = edge_distances[index][0]

    elif head_y == 1 and 1 <= head_x <= width-3:
        direction = RIGHT
    elif head_x == width-2 and 1 <= head_y <= height-3:
        direction = DOWN
    elif head_y == height-2 and 2 <= head_x <= width-2:
        direction = LEFT
    else:
        direction = UP

    return json.dumps({
        'move': direction if direction in directions else choice(directions),
        'taunt': choice(smacktalk)
    })


@bottle.post('/end')
def end():
    # data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
