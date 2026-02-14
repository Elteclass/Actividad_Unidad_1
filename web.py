# BaseHTTPReq... Clase base para manejar peticiones HTTP (GET, POST, ETC.)
# HTTPServer Clase que crea y ejecuta el servidor web
from http.server import BaseHTTPRequestHandler, HTTPServer

# parse_qsl Convierte query strings en diccionarios
# Divide URLs en partes (Protocolo, dominio, ruta, parametros)
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        # HTML dinamico que muestra la ruta y el actor
        path = self.url().path
        parametros = self.query_data()


        # Impresion de los datos requeridos para el request
        print("# Request #")
        print(f"Host: {self.headers.get('Host')}")
        print(f"User-Agent: {self.headers.get('User-Agent')}")
        print(f"Ruta: {self.path}")
        print(" ")

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))

    def get_response(self):
        path = self.url().path
        parametros = self.query_data()

        # Obtener el nombre del proyecto
        if path.startswith('/proyecto/'):
            proyecto = path.split('/')[-1]
            autor = parametros.get('autor', 'Anonimo')
            return f"""<h1>Proyecto: {proyecto} Autor: {autor}</h1>
                <h1> Hola Web </h1>
                <p> URL Parse Result : {self.url()} </p>
                <p> Path Original: {self.path} </p>
                <p> Headers: {self.headers} </p>
                <p> Query: {self.query_data()} </p>
            """

if __name__ == "__main__":
    print("Starting server")
    # Se agrega el puerto 8000, ya que es el comunmente usado para Servidores Web en entornos de desarrollo
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()
