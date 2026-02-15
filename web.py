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
        # Obtencion de la ruta y los parametros de la URL
        path = self.url().path
        parametros = self.query_data()

        # Impresion en consola de datos del request
        print("# REQUEST #")
        print(f"Host: {self.headers.get('Host')}")
        print(f"User-Agent: {self.headers.get('User-Agent')}")
        print(f"Ruta: {self.path}")
        print(" ")

        # Verificacion si la ruta es la pagina principal
        if path == '/':
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            # Impresion en consola de datos del response
            print("# RESPONSE #")
            print(f"Content-Type: text/html")           
            print(f"Server: {self.server_version} {self.sys_version}")           
            print(f"Date: {self.date_time_string()}")
            print(" ")    

            # Leer y mostrar el archivo home.html
            try:
                with open('home.html', 'r', encoding='utf-8') as file:
                    home = file.read()

                # Enviar el HTML al navegador
                self.wfile.write(home.encode("utf-8"))
            except FileNotFoundError:
                # Si no existe el archivo, se muestra un mensaje de error
                self.wfile.write(b"<h1>Error: No se encuentra el archivo home.html</h1>")

        # Verificacion si la ruta comienza con "/proyecto/" para el HTML dinamico
        elif path.startswith('/proyecto/'):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            # Impresion en consola de datos del response
            print("# RESPONSE #")
            print(f"Content-Type: text/html")           
            print(f"Server: {self.server_version} {self.sys_version}")           
            print(f"Date: {self.date_time_string()}")
            print(" ")  

            # Extraer el nombre del proyecto
            proyecto = path.split('/')[-1]
            # Obtener parametro autor y si no hay se coloca Anonimo
            autor = parametros.get('autor', 'Anonimo')
            # Crear HTML con el proyecto y autor
            htmlDinamico = f"""<h1>Proyecto: {proyecto}     Autor: {autor}</h1>
                <h1> Hola Web </h1>
                <p> URL Parse Result : {self.url()} </p>
                <p> Path Original: {self.path} </p>
                <p> Headers: {self.headers} </p>
                <p> Query: {self.query_data()} </p>
            """

            # Enviar el HTML al navegador
            self.wfile.write(htmlDinamico.encode('utf-8'))

        else:
            # Mostrar el error 404 para cualquier ruta desconocida
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            # Impresion en consola de datos del response
            print("# RESPONSE #")
            print(f"Content-Type: text/html")           
            print(f"Server: {self.server_version} {self.sys_version}")           
            print(f"Date: {self.date_time_string()}")
            print(" ")  

            # Crear HTML de error
            errorHtml = """
            <html>
                <head><title>Error 404</title></head>
                <body>
                    <h1>Error 404 - Pagina No Encontrada</h1>
                    <p>La ruta no existe</p>
                </body>
            </html>
            """

            # Enviar el HTML al navegador
            self.wfile.write(errorHtml.encode("utf-8"))

if __name__ == "__main__":
    print("Starting server")
    # Crear el servidor HTTP en localhost puerto 8000
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    # Iniciar el servidor para escuchar peticiones indefinidamente
    server.serve_forever()
