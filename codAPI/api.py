import re
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from codAPI.graph_handler import GraphHandler


class RequestHandler(SimpleHTTPRequestHandler):
    _handler = GraphHandler()

    def _send_response(self, response_code, result):
        self.send_response(response_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(result.encode("utf-8"))

    def do_GET(self):
        if self.path == '/codapi/resources/countries':
            results = self._handler.get_all_available_countries()
            self._send_response(200, results)
        elif re.search(r'.+/countries/[a-zA-Z]{2,3}/all', self.path):
            results = self._handler.get_cases_by_country_code(self.path.rsplit("/", 2)[1])
            self._send_response(200, results)
        elif re.search('/codapi/resources/articles/*', self.path):
            article_id = self.path.split("/")[-1]
            results = self._handler.get_article_by_id(article_id)
            if results == '[]':
                self._send_response(404, json.dumps({"message": "Resource not found"}))
            else:
                self._send_response(200, results)


if __name__ == '__main__':
    Handler = RequestHandler
    try:
        httpd = HTTPServer(("localhost", 8082), Handler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("exiting")
        exit()
