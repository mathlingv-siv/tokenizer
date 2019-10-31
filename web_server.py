"""this module contains methods for working with a web server
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from search_engine import SearchEngine, Context_Window


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """create an html page with a search button,
        query, limit and offset fields
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
                            <label for="limit">
                            show 
                            <input type="number" name="limit">
                            </label>
                            <label for="offset">
                            documents starting from the
                            <input type="number" name="offset">
                            one
                            </label>
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
        query = str(form.getvalue("query"))
        limit = form.getvalue("limit")
        if not limit:
            limit = 10
        else:
            limit = int(limit)
        offset = form.getvalue("offset")
        if not offset or int(offset) < 0:
            offset = 0
        else:
            offset = int(offset)
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
                            <label for="limit">show 
                            <input type="number" name="limit" value="%d"/>
                            </label>
                            <label for="offset">
                            documents starting from the
                            <input type="number" name="offset" value="%d"/>
                            one
                            </label>""" % (query, limit, offset), encoding="utf-8"))
        # create a list of pairs (limit, offset) for quotes
        # in each document to pass it to the search function
        n = 0
        quotes_per_doc = []
        while n < limit:
            doc_limit = form.getvalue("doc%dlimit" % n)
            doc_offset = form.getvalue("doc%doffset" % n)
            if not doc_limit:
                doc_limit = 3
            else:
                doc_limit = int(doc_limit)
            if not doc_offset:
                doc_offset = 0
            else:
                doc_offset = int(doc_offset)
            if doc_offset < 0:
                doc_offset = 0
            quotes_per_doc.append((doc_limit, doc_offset))
            n+=1
        search = self.server.search_engine.limit_quote_search(query, limit, offset, quotes_per_doc)
        # ordered file list
        self.wfile.write(bytes('<ol>', encoding="utf-8"))
        if not search:
            self.wfile.write(bytes('Not Found', encoding="utf-8"))        
        for i, filename in enumerate(search):               
            self.wfile.write(bytes('<li><p>%s</p>' % filename, encoding="utf-8"))
            # create limit and offset for each document            
            quote_limit = quotes_per_doc[i][0]
            quote_offset = quotes_per_doc[i][1]
            # field names that take into account
            # the number of the document in the output
            self.wfile.write(bytes("""
                    <label for="doc%dlimit">show
                    <input type="number" name="doc%dlimit" value="%d"/>
                    </label>
                    <label for="doc%doffset">
                    quotes starting from the
                    <input type="number" name="doc%doffset" value="%d"/>
                    one
                    </label>""" % (i, i, quote_limit, i, i, quote_offset),
                                   encoding="utf-8"))            
            # unordered quote list
            self.wfile.write(bytes('<ul>', encoding="utf-8"))
            # show quote_limit quotes starting from quote_offset
            if not search[filename] or quote_limit < 0:
                self.wfile.write(bytes('<br>Not Found', encoding="utf-8"))
            else:
                for window in search[filename]:
                    self.wfile.write(bytes('<li><p>%s</p></li>' % window, encoding="utf-8"))                
            self.wfile.write(bytes('</ul></li>', encoding="utf-8"))            
        self.wfile.write(bytes("""</ol></form></body></html>""", encoding="utf-8"))            
        

def main():
    server = HTTPServer(('', 8090), RequestHandler)
    server.search_engine = SearchEngine('database')
    server.serve_forever()


if __name__ == "__main__":
    main()
