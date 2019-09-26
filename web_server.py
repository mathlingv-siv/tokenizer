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
                            <br>show 
                            <input type="number" name="limit">
                            documents starting from the
                            <input type="number" name="offset">
                            one
                            <br>
                            <br>with
                            <input type="number" name="doc_lim" value="%d"/>
                            quotes in each starting from the
                            <input type="number" name="doc_off" value="%d"/>
                            one,
                            if these values are not specified in the fields below
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
        if not offset:
            offset = 0
        else:
            offset = int(offset)
        doc_lim = form.getvalue("doc_lim")
        if not doc_lim:
            doc_lim = 3
        else:
            doc_lim = int(doc_lim)
        doc_off = form.getvalue("doc_off")
        if not doc_off:
            doc_off = 0
        else:
            doc_off = int(doc_off)
        #engine = SearchEngine('database')
        #search = engine.search_extended_context(query, 3)
        search = self.server.search_engine.search_extended_context(query, 2)
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
                            <br>show 
                            <input type="number" name="limit" value="%d"/>
                            documents starting from the
                            <input type="number" name="offset" value="%d"/>
                            one
                            <br>
                            <br>with
                            <input type="number" name="doc_lim" value="%d"/>
                            quotes in each starting from the
                            <input type="number" name="doc_off" value="%d"/>
                            one,
                            if these values are not specified in the fields below
                            """ % (query, limit, offset, doc_lim, doc_off), encoding="utf-8"))
        # ordered file list
        self.wfile.write(bytes('<ol>', encoding="utf-8"))
        if not search:
            self.wfile.write(bytes('Not Found', encoding="utf-8"))        
        for i, filename in enumerate(search):
            # show limit documents starting from offset
            if i >= offset and i < limit+offset:                
                self.wfile.write(bytes('<li><p>%s</p></li>' % filename, encoding="utf-8"))
                # create limit and offset for each document
                doc_limit = form.getvalue("doc%dlimit" % i)
                doc_offset = form.getvalue("doc%doffset" % i)
                if not doc_limit:
                    doc_limit = doc_lim
                else:
                    doc_limit = int(doc_limit)
                if not doc_offset:
                    doc_offset = doc_off
                else:
                    doc_offset = int(doc_offset)
                # generate field names taking into account
                # the number of the document in the search results
                # (doc0limit, doc0offset, doc1limit, doc1offset...)
                self.wfile.write(bytes("""
                        show
                        <input type="number" name="doc%dlimit" value="%d"/>
                        quotes starting from the
                        <input type="number" name="doc%doffset" value="%d"/>
                        one""" % (i, doc_limit, i, doc_offset), encoding="utf-8"))
                # unordered quote list
                self.wfile.write(bytes('<ul>', encoding="utf-8"))
                # show doc_limit quotes starting from doc_offset
                for n, window in enumerate(search[filename]):
                    if n >= doc_offset and n < doc_limit + doc_offset:
                        quote = window.highlight()
                        self.wfile.write(bytes('<li><p>%s</p></li>' % quote, encoding="utf-8"))
                    if n == doc_limit + doc_offset:
                        break
                self.wfile.write(bytes('</ul>', encoding="utf-8"))
            if i == limit+offset:
                break
        self.wfile.write(bytes("""</ol></form></body></html>""", encoding="utf-8"))


def main():
    server = HTTPServer(('', 8090), RequestHandler)
    server.search_engine = SearchEngine('database')
    server.serve_forever()


if __name__ == "__main__":
    main()
