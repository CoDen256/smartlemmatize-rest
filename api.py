from bottle import route, run, template, request, response
from sublem import launch


@route('/sublem/ltc')
def index():
    id = request.query.id
    season = request.query.s
    episode = request.query.e

    response.content_type = 'application/json'
    return launch(id, season, episode)


run(host='localhost', port=8080)
