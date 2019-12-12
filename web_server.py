"""this module contains methods for working with a web server
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from search_engine import SearchEngine, Context_Window
import time


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """create an html page with a search button,
        query, limit field and buttons for going forward
        and backward through the files
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
                            documents on a page
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
        start_time = time.time()
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                            environ={'REQUEST_METHOD': 'POST'})
        # remember previous query to start next search with new parameters
        pr_query = form.getvalue("pr_query")
        query = str(form.getvalue("query"))
        if pr_query == None or pr_query == "None":
            pr_query = query
        else:            
            if pr_query != query:
                pr_query = "None"        
        doc_action = form.getvalue("action")
        limit = form.getvalue("limit")
        if not limit:
            limit = 10
        else:
            limit = int(limit)
        offset = form.getvalue("offset")
        if not offset or int(offset) < 0 or pr_query == "None":
            offset = 0
        else:
            offset = int(offset)
        # specify actions when a button is pressed
        if doc_action == "Previous" and offset != 0:
            offset = offset - limit           
        elif doc_action  == "Next":
            offset = limit + offset
        elif doc_action == "First Page":
            offset = 0
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("""
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query" value="%s"/>
                            <input type="submit" value="Search"/>
                            <input type="hidden" name="pr_query" value="%s"/>
                            <br>
                            <br>
                            <label for="limit">show 
                            <input type="number" name="limit" value="%d"/>
                            documents on a page
                            </label>
                            <input type="hidden" name="offset" value="%d"/>                                                         
                            """ % (query, pr_query, limit, offset), encoding="utf-8"))
        # create a list of pairs (limit, offset) for quotes
        # in each document to pass it to the search function
        n = 0
        quotes_per_doc = []        
        check_quotes = []
        while n < limit+1:
            quote_action = form.getvalue("action%d" % n)
            doc_limit = form.getvalue("doc%dlimit" % n)
            doc_offset = form.getvalue("doc%doffset" % n)
            if not doc_limit:
                doc_limit = 3
            else:
                doc_limit = int(doc_limit)
            if not doc_offset or pr_query == "None":
                doc_offset = 0
            elif doc_action == "Previous" or doc_action  == "Next" or  doc_action == "First Page":
                doc_offset = 0
            else:
                doc_offset = int(doc_offset)
            if doc_offset < 0:
               doc_offset = 0
            # specify actions when a button is pressed
            if quote_action == "Previous" and doc_offset != 0:
                doc_offset = doc_offset - doc_limit                 
            elif quote_action == "Next":
                doc_offset = doc_limit + doc_offset
            elif quote_action == "To the beginning":
                doc_offset = 0
            quotes_per_doc.append((doc_limit+1, doc_offset))
            n+=1
        search = self.server.search_engine.limit_quote_search(query, limit+1, offset, quotes_per_doc)
        sorted_key_list = sorted(search)        
        # ordered file list
        self.wfile.write(bytes('<ol>', encoding="utf-8"))
        if not search:
            self.wfile.write(bytes('Not Found', encoding="utf-8"))        
        for i, filename in enumerate(sorted_key_list[:limit]):               
            self.wfile.write(bytes('<li><p>%s</p>' % filename, encoding="utf-8"))
            # create limit and offset for each document            
            quote_limit = quotes_per_doc[i][0]
            quote_offset = quotes_per_doc[i][1]
            # field names that take into account
            # the number of the document in the output
            self.wfile.write(bytes("""
                    <label for="doc%dlimit">show
                    <input type="number" name="doc%dlimit" value="%d"/>
                    quotes
                    </label>
                    <input type="hidden" name="doc%doffset" value="%d"/>
                    """ % (i, i, quote_limit-1, i, quote_offset), encoding="utf-8"))            
            # unordered quote list
            self.wfile.write(bytes('<ul>', encoding="utf-8"))
            # show quote_limit quotes starting from quote_offset            
            if not (search[filename] or quote_limit < 0):
                self.wfile.write(bytes('<br>Not Found<br><br>', encoding="utf-8"))
            else:
                x = 0
                for window in search[filename]:
                    if x < quote_limit - 1:
                        self.wfile.write(bytes('<li><p>%s</p></li>' % window, encoding="utf-8"))
                    x += 1
            self.wfile.write(bytes('</ul></li>', encoding="utf-8"))
            # disable buttons (quotes) in particular cases
            prq_disabled = ""
            nq_disabled = ""
            if quote_offset == 0:
                prq_disabled = "disabled"
            if len(search[filename]) < quotes_per_doc[i][0]:
                nq_disabled = "disabled"
            self.wfile.write(bytes("""
                            <input type="submit" name="action%d" value="Previous" %s/>
                            <input type="submit" name="action%d" value="To the beginning" %s/>
                            <input type="submit" name="action%d" value="Next" %s/>
                            """ % (i, prq_disabled, i, prq_disabled, i, nq_disabled), encoding="utf-8"))            
        self.wfile.write(bytes('</ol>', encoding="utf-8"))
        # disable buttons (docs) in particular cases
        pr_disabled = ""
        n_disabled = ""
        if offset == 0:
            pr_disabled = "disabled"
        if len(search.keys()) < limit+1:
            n_disabled = "disabled"
        self.wfile.write(bytes("""
                        <input type="submit" name="action" value="Previous" %s/>
                        <input type="submit" name="action" value="First Page" %s/>
                        <input type="submit" name="action" value="Next" %s/>
                        """ % (pr_disabled, pr_disabled, n_disabled), encoding="utf-8"))        
        self.wfile.write(bytes("""</form></body></html>""", encoding="utf-8"))
        print('time:', time.time() - start_time)
        

def main():
    server = HTTPServer(('', 8090), RequestHandler)
    server.search_engine = SearchEngine('database')
    server.serve_forever()


if __name__ == "__main__":
    main()
