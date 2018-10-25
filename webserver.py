from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## http://localhost:1235

## import CRUD operations
from database_setup import Base, Category, CategoryItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

## Create session and connect to DB
engine = create_engine('sqlite:///itemcatalogue.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

## In order to add columns to table (above copy and below)
## myThirdCategory = Category(name="Skating")
## session.add(myThirdCategory)
## session.commit()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/categories/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>Make a new restaurant!</h1>"
                output += '''
                    <form method='POST' enctype='multipart/form-data' action='/categories/new'>
                    <input name="newCategoryName" type="text">
                    <input type="submit" value="Create"> </form>
                    '''
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith('/edit'):
                categoryIdPath = self.path.split('/')[2]
                myCategoryQuery = session.query(Category).filter_by(id=categoryIdPath).one()

                if myCategoryQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myCategoryQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/categories/%s/edit'>" % categoryIdPath
                    output += "<input name='newCategoryName' type='text' placeholder='%s'>" % myCategoryQuery.name
                    output += "<input type='submit' value='Rename'> </form>"
                    output += "</body></html>"
                    self.wfile.write(output)

            if self.path.endswith('/delete'):
                categoryIdPath = self.path.split('/')[2]
                myCategoryQuery = session.query(Category).filter_by(id=categoryIdPath).one()

                if myCategoryQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += "Are you sure you want to delete %s" % myCategoryQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/categories/%s/delete'>" % categoryIdPath
                    output += "<input type='submit' value='Delete'> </form>"
                    output += "</body></html>"
                    self.wfile.write(output)


            if self.path.endswith('/categories'):
                categories = session.query(Category).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html></body>"
                output += "<a href='categories/new'>Make a new category here</a><br><br>"
                for category in categories:
                    output += category.name
                    output += "</br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % category.id
                    output += "</br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % category.id
                    output += "</br></br>"
                
                output += "<body></html>"
                self.wfile.write(output)
                # print output
                return

        except IOError:
            self.send_error(404, 'File not Found %s' % self.path)

    def do_POST(self):
        try:

            if self.path.endswith('/delete'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newCategoryName')
                    categoryIdPath = self.path.split('/')[2]

                    myCategoryQuery = session.query(Category).filter_by(id=categoryIdPath).one()

                    if myCategoryQuery != []:
                        session.delete(myCategoryQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/categories')
                        self.end_headers()


            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newCategoryName')
                    categoryIdPath = self.path.split('/')[2]

                    myCategoryQuery = session.query(Category).filter_by(id=categoryIdPath).one()

                    if myCategoryQuery != []:
                        myCategoryQuery.name = messagecontent[0]
                        session.add(myCategoryQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/categories')
                        self.end_headers()


            if self.path.endswith('/categories/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newCategoryName')

                    # Create new Category class
                    newCategory = Category(name=messagecontent[0])
                    session.add(newCategory)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/categories')
                    self.end_headers()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print 'Web server running on port %s' % port
        server.serve_forever()
    except KeyboardInterrupt:
        print '^ entered, stopping web server...'
        server.socket.close()


if __name__ == '__main__':
    main()
