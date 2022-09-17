from socket import *
import os
import re


def createServer():
    serversocket = socket(
        AF_INET,
        SOCK_STREAM,
    )
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        serversocket.bind(("localhost", 9000))
        serversocket.listen(5)
        while True:
            (clientsocket, address) = serversocket.accept()
            rd = clientsocket.recv(5000).decode()
            pieces = rd.split("\n")

            querystring = re.search("=.* ", pieces[0])  # get path from request
            if querystring:
                desired_path = querystring.group()[1:-1]
                previous_path = os.path.dirname(desired_path)
            else:
                desired_path = os.getcwd()
                previous_path = os.path.dirname(os.getcwd())
            if len(pieces) > 0:
                print(pieces[0])

            ##### HTML DIRECTORY LIST #######
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type: text/html; charset=utf-8\r\n"
            data += "\r\n"
            data += "<html><body>"
            data += '<a href="/?dir={}">{}</a><br>'.format(previous_path, "...")
            create_tag = (
                lambda x: '<a href="/?dir={}">{}</a><br>'.format(
                    desired_path + "/" + x, x
                )
                if os.path.isdir(desired_path + "/" + x)
                else "<a>{}</a><br>".format(x)
            )
            directories = os.listdir(os.path.abspath(desired_path))
            data += "".join(list(map(create_tag, directories)))
            data += "</body></html>\r\n\r\n"
            ##### HTML DIRECTORY LIST END #######

            clientsocket.sendall(data.encode())
            clientsocket.shutdown(SHUT_WR)

    except KeyboardInterrupt as e:
        print("\nShutting down...\n")
    except Exception as exc:
        print("Error: \n")
        print(exc)

    serversocket.close()


print("Access http://localhost:9000")
createServer()
