#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        # self.request.sendall(bytearray("OK",'utf-8'))

        # Split up the data into its components
        data = self.data.decode("utf-8").split()
        method = data[0]
        path = data[1]


        # Check if the data is not a GET request and output a 405 error
        if method != "GET":
            self.send405(self.request)
            return

        # Check whether or not the data is empty and output 404 error 
        elif not self.data:
            self.send404(self.request)
            return
        
        # Output a 200 OK when the request method is GET
        elif method == "GET":
            # self.send200(self.request, text_type="")
            if os.path.exists("www"+path+"/") and not path.endswith("/"):
                # Output a 301 error and update the path to redirect properly
                path += "/"
                # self.request.sendall(bytearray(f"HTTP/1.1 301 Moved Permanently\nLocation: {path}\nContent-Type: text/plain; charset=utf-8\n", 'utf-8'))

                self.send301(self.request, path)
                return
                

            # Check if the path is a directory or a file
            elif os.path.exists("www"+path):
                # path checking
                if path.endswith("/"):
                    path += "index.html"

                # Check whether or not the data given is a css or an html file
                text_type = ""
                if path.endswith(".css"):
                    text_type = "text/css"
                elif path.endswith(".html"):
                    text_type = "text/html"
                elif text_type == "": # If the file doesn't  exist
                    self.send404(self.request)
                    return

                # Open the file and read it
                file = open("www"+path)
                content = file.read()
                self.send200(self.request, text_type, content)
                file.close()
            
            else:
                self.send404(self.request)
                return
        


    # Sends out a 404 error
    def send404(self, request):
        request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
        request.sendall(bytearray("Content-Type: text/html\r\n\r\n",'utf-8'))
        request.sendall(bytearray("<html><body><h1>404 Not Found</h1></body></html>\r\n",'utf-8'))
        request.sendall(bytearray("<html><body><h2>The page you were looking for was not found</h2></body></html>\r\n",'utf-8'))


    # Sends out a 200 OK 
    def send200(self, request, text_type, content):
        request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
        self.request.sendall(bytearray("Content-Type: " + text_type + "\r\n",'utf-8'))
        self.request.sendall(bytearray(f"HTTP/1.1 200 OK\nContent-Type: {text_type}; charset=utf-8\n\n{content}\n", 'utf-8'))
        
        # request.sendall(bytearray("<plain><body><h1>200 OK</h1></body></plain>\r\n",'utf-8'))
        # request.sendall(bytearray("<plain><body><h2>Got a request</h2></body></plain>\r\n",'utf-8'))


    # Sends out a 405 error
    def send405(self, request):
        request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
        request.sendall(bytearray("Content-Type: text/html\r\n\r\n",'utf-8'))
        request.sendall(bytearray("<html><body><h1>405 Method Not Allowed</h1></body></html>\r\n",'utf-8'))
        request.sendall(bytearray("<html><body><h2>Submited a request that can't be handled.</h2></body></html>\r\n",'utf-8'))

    # Sends out a 301 error
    def send301(self, request, path):
        request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\n",'utf-8'))
        request.sendall(bytearray("Content-Type: text/html\r\n\r\n",'utf-8'))
        request.sendall(bytearray("<html><body><h1>301 Moved Permanently</h1></body></html>\r\n",'utf-8'))
        request.sendall(bytearray("<html><body><h2>This page has moved</h2></body></html>\r\n",'utf-8'))
        # Send the new location of the file
        request.sendall(bytearray("New location: http://" + HOST + ":" + str(PORT) + path + "\r\n",'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
