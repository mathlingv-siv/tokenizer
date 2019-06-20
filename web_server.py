"""this module contains methods for working with a web werver

"""
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """create an html page with a field and a search button

        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = """
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query">
                            <input type="submit" value="Search">
                        </form>
                    </body>
                </html>
                """
        self.wfile.write(bytes(html, encoding="utf-8"))


def main():
    server = HTTPServer(('', 80), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
