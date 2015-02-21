import bottle
import json

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
        'color': '#00ff00',
        'head_url': 'http://images5.fanpop.com/image/photos/30100000/Santa-Voldemort-snapes-family-and-friends-30187028-600-351.jpg',
        'taunt': 'All your base are belong to us!'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json

    width = len(data['board'])
    height = len(data['board'][0])

    nagini = [s for s in data['snakes'] if s['name'] == 'nagini'][0]

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
