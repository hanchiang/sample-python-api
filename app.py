import json
import falcon
import datetime

from db.index import connect_db, query, query_mutate, Queries

connect_db()

class JSONTranslator(object):
    def process_request(self, req, resp):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['body'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

class HelloWorldResource:
    def on_get(self, request, response):
        response.media = ('Hello World from Falcon Python 3.6 app with' +
                          ' Gunicorn running in a container.')

class Customers:
    def on_get(self, request, response):
        result = query(Queries.get_customers())
        response.media = result
    def on_post(self, request, response):
        req_body = request.context['body']
        result = query_mutate(Queries.create_customer(), (req_body['name'], datetime.datetime.strptime(req_body['dob'], '%Y-%m-%d').date()))
        response.media = 'Created'



app = falcon.API(middleware=[
    JSONTranslator()
])
app.add_route('/', HelloWorldResource())
app.add_route('/customers', Customers())