import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from waitress import serve
from flask import Flask
from flask_restplus import Resource, Api, fields
application = Flask(__name__)
api = Api(application,
          version='0.1',
          title='Our sample API',
          description='This is our sample API',
)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    serve(application, host='0.0.0.0', port=80)
