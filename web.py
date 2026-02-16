# BaseHTTPReq... Clase base para manejar peticiones HTTP (GET, POST, ETC.)
# HTTPServer Clase que crea y ejecuta el servidor web
from http.server import BaseHTTPRequestHandler, HTTPServer

# parse_qsl Convierte query strings en diccionarios
# Divide URLs en partes (Protocolo, dominio, ruta, parametros)
from urllib.parse import parse_qsl, urlparse

class WebRequestHandler(BaseHTTPRequestHandler):
    # Crear diccionario que almacena el contenido HTML
    # La clave es la ruta y el valor es el HTML
    contenido =  {
        '/': None,
        '/proyecto/1':"""
                <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Proyecto 1 - Ana Lee</title>
            </head>
            <body>
                <h1>Proyecto 1: Web Estática</h1>
                <h2>App de recomendación de libros</h2>
                <p>Este proyecto es una aplicación web estática que recomienda libros basándose en tus preferencias de lectura.</p>
                <h3>Características:</h3>
                <ul>
                    <li>Interfaz limpia y minimalista</li>
                    <li>Categorías de libros: Ficción, No Ficción, Fantasía, Romance</li>
                    <li>Sistema de filtros por género y autor</li>
                    <li>Reseñas de usuarios</li>
                </ul>
                <h3>Tecnologías utilizadas:</h3>
                <ul>
                    <li>HTML5</li>
                    <li>CSS3</li>
                    <li>JavaScript vanilla</li>
                </ul>
                <br>
                <a href="/">← Volver al inicio</a>
            </body>
        </html>
        """,
        '/proyecto/2':"""
        <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Proyecto 2 - Ana Lee</title>
            </head>
            <body>
                <h1>Proyecto 2: Web App MeFalta</h1>
                <h2>¿Qué película o serie me falta ver?</h2>
                <p>MeFalta es una aplicación web que te ayuda a llevar un registro de películas y series que quieres ver.</p>
                <h3>Características:</h3>
                <ul>
                    <li>Lista personalizada de pendientes</li>
                    <li>Integración con APIs de películas (TMDB)</li>
                    <li>Sistema de calificación personal</li>
                    <li>Recordatorios de estrenos</li>
                    <li>Compartir listas con amigos</li>
                </ul>
                <h3>Tecnologías utilizadas:</h3>
                <ul>
                    <li>Frontend: React + TypeScript</li>
                    <li>Backend: Node.js + Express</li>
                    <li>Base de datos: MongoDB</li>
                    <li>API: TMDB (The Movie Database)</li>
                </ul>
                <br>
                <a href="/">← Volver al inicio</a>
            </body>
        </html>
        """,
        '/proyecto/3':"""
        <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Proyecto 3 - Ana Lee</title>
            </head>
            <body>
                <h1>Proyecto 3: Web App Foto22</h1>
                <h2>Gestión inteligente de fotos</h2>
                <p>Foto22 es una aplicación web moderna para organizar, editar y compartir tus fotografías de forma eficiente.</p>
                <h3>Características:</h3>
                <ul>
                    <li>Almacenamiento en la nube ilimitado</li>
                    <li>Organización automática por fecha y ubicación</li>
                    <li>Editor de fotos integrado</li>
                    <li>Reconocimiento facial con IA</li>
                    <li>Álbumes compartidos con control de privacidad</li>
                    <li>Búsqueda inteligente por contenido</li>
                </ul>
                <h3>Tecnologías utilizadas:</h3>
                <ul>
                    <li>Frontend: React + htmx</li>
                    <li>Backend: FastAPI (Python)</li>
                    <li>Storage: AWS S3</li>
                    <li>IA: TensorFlow para reconocimiento de imágenes</li>
                    <li>Base de datos: PostgreSQL</li>
                </ul>
                <br>
                <a href="/">← Volver al inicio</a>
            </body>
        </html>
        """
    }


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

        # Verificacion si la ruta existe en el diccionario
        if path in self.contenido:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            # Impresion en consola de datos del response
            print("# RESPONSE #")
            print(f"Content-Type: text/html")           
            print(f"Server: {self.server_version} {self.sys_version}")           
            print(f"Date: {self.date_time_string()}")
            print(" ")    

            # Verificacion si la ruta es '/' y el valor None, para cargar archivo home.html
            if path == '/' and self.contenido[path] is None:
                # Leer y mostrar el archivo home.html
                try:
                    with open('home.html', 'r', encoding='utf-8') as file:
                        home = file.read()
                    # Enviar el HTML al navegador
                    self.wfile.write(home.encode("utf-8"))
                except FileNotFoundError:
                    # Si no existe el archivo, se muestra un mensaje de error
                    self.wfile.write(b"<h1>Error: No se encuentra el archivo home.html</h1>")
            else:
                html = self.contenido[path]
                self.wfile.write(html.encode('utf-8'))

        # Si la ruta no existe en el diccionario, se muestra el error 404
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
                    <p>La ruta no existe en el servidor</p>
                    <a href="/">Volver al inicio</a>
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
