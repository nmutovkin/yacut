from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import check_short_id, get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!', 400)
    if 'custom_id' in data and data['custom_id']:
        is_valid, message = check_short_id(data['custom_id'], api=True)
        if not is_valid:
            raise InvalidAPIUsage(message, 400)
    else:
        data['custom_id'] = get_unique_short_id()

    url_map = URL_map()
    url_map.from_dict(data)

    db.session.add(url_map)
    db.session.commit()

    url_root = request.url_root

    return jsonify(url_map.to_dict(url_root)), 201


@app.route('/api/id/<string:id>/', methods=['GET'])
def get_short_id(id):
    url_map = URL_map.query.filter_by(short=id).first()
    if url_map is not None:
        return jsonify({'url': url_map.original}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)
