from flask import Flask, request, abort

from fvhiot.utils.data import data_pack
from fvhiot.utils.http import extract_data_from_flask_request
from fvhiot.utils.kafka import FvhKafkaProducer


app = Flask(__name__)
app.config.from_pyfile('config.py')

fvh_kp = FvhKafkaProducer(app)


# Wild-card catch-all handler
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'HEAD'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'HEAD'])
def catchall(path: str):
    """
    Endpoint for remote IoT sensors.

    Check that request path matches ENDPOINT_PATH
    and optionally validate request credentials, device id etc.
    and if everything is ok send serialised request to a kafka topic.

    :param path: request path
    :return:
    """
    if app.config.get('ENDPOINT_PATH') != path:
        abort(404, description="Resource not found")
    data = extract_data_from_flask_request(request)
    data['path'] = path
    body_max_size = app.config.get('REQUEST_BODY_MAX_SIZE', 4096)
    if len(data['request']['body']) > body_max_size:
        return f'Request body too large (>{body_max_size}B)', 400
    producer = fvh_kp.producer
    producer.send(app.config.get('TOPIC_RAW_REQUESTS'), value=data_pack(data))
    print(data)
    return 'OK'
