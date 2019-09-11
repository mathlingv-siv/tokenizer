"""this module contains methods for working with a web server
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from search_engine import SearchEngine, Context_Window


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """create an html page with a search button
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
                            <br>
                            <br> 
                            <input type="number" name="limit" placeholder="limit">                            
                            <input type="number" name="offset" placeholder="offset">
                        </form>
                    </body>
                </html>
                """
        self.wfile.write(bytes(html, encoding="utf-8"))
        
    def do_POST(self):
        """show search results as an ordered list of filenames
        with an unordered list of quotes for each file
        and the searched word(s) highlighted
        """
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                            environ={'REQUEST_METHOD': 'POST'})
        query = str(form.getvalue('query'))
        limit = int(form.getvalue('limit'))
        offset = int(form.getvalue('offset'))
        engine = SearchEngine('database')
        search = engine.search_extended_context(query, 3)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("""
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query" value="%s"/>
                            <input type="submit" value="Search"/>
                            <br>
                            <br> 
                            <input type="number" name="limit" placeholder="limit" value="%d"/>                             
                            <input type="number" name="offset" placeholder="offset" value="%d"/>                            
                        </form>""" % (query, limit, offset), encoding="utf-8"))
        # ordered file list
        self.wfile.write(bytes('<ol>', encoding="utf-8"))
        if not search:
            self.wfile.write(bytes('Not Found', encoding="utf-8"))        
        for i, filename in enumerate(search):
            if i >= offset and i < limit+offset:
                self.wfile.write(bytes('<li><p>%s</p></li>' % filename, encoding="utf-8"))
                # unordered quote list
                self.wfile.write(bytes('<ul>', encoding="utf-8"))
                for window in search[filename]:
                    quote = window.highlight()
                    self.wfile.write(bytes('<li><p>%s</p></li>' % quote, encoding="utf-8"))
                self.wfile.write(bytes('</ul>', encoding="utf-8"))
            if i == limit+offset:
                break
        self.wfile.write(bytes("""</ol></body></html>""", encoding="utf-8"))


def main():
    server = HTTPServer(('', 8090), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
