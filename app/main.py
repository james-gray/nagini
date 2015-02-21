import bottle
import json
import sys
# This comment means nothing I am just testing something

UP = u'up'
RIGHT = u'right'
DOWN = u'down'
LEFT = u'left'

@bottle.get('/')
def index():
    return """
        <a href="https://github.com/james-gray/nagini">
            nagini
        </a>
    """


@bottle.post('/start')
def start():
    data = bottle.request.json

    return json.dumps({
        'name': 'nagini',
        'color': '#22ff00',
        'head_url': 'https://raw.githubusercontent.com/james-gray/nagini/master/SnakeHead.png',
        'taunt': 'All your base are belong to us!'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json

    width = len(data['board'])
    height = len(data['board'][0])

    nagini = [s for s in data['snakes'] if s['name'] == 'nagini'][0]
    coords = nagini['coords']
    head_x, head_y = coords[0][0], coords[0][1]

    # If not on an edge, start moving towards one
    if not any([head_x in (0, width-1), head_y in (0, height-1)]):
        edge_distances = [
            (UP, head_y),
            (RIGHT, width - head_x - 1),
            (DOWN, height - head_y - 1),
            (LEFT, head_x)
        ]
        dist_min = sys.maxint
        min_index = -1

        for i, d in enumerate(edge_distances):
            if d[1] < dist_min:
                dist_min = edge_distances[i][1]
                index = i

        direction = edge_distances[index][0]

        return json.dumps({
            'move': direction,
            'taunt': direction
        })

    return json.dumps({
        'move': 'left',
        'taunt': 'All your base are belong to us!'
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
