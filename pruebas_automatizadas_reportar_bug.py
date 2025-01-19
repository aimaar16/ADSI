import requests
from bs4 import BeautifulSoup
import re

# URL base del sistema
url = "http://localhost:5000"

def interfazReporteBugVisible(url):
    """Verifica si la interfaz de reportar bug es visible."""
    response = requests.get(url + "/report.html?movie_id=1&movie_title=TestMovie")
    if re.search(r"\bReportar Bug\b", response.text):  # Busca el texto "Reportar Bug" en la página
        print("Interfaz de Reporte de Bug Visible")
    else:
        print("Interfaz de Reporte de Bug No Visible")

def cuadroTextoVisible(url):
    """Verifica si el cuadro de texto para describir el bug es visible."""
    response = requests.get(url + "/report.html?movie_id=1&movie_title=TestMovie")
    soup = BeautifulSoup(response.text, "html.parser")
    cuadro_texto = soup.find("textarea", {"id": "bug_description"})  # Cambia 'id' si es necesario
    if cuadro_texto:
        print("Cuadro de texto para descripción visible")
    else:
        print("Cuadro de texto para descripción no visible")

def subirArchivoFuncional(url):
    """Prueba subir un archivo válido."""
    files = {"file_upload": ("test.png", b"archivo de prueba", "image/png")}  # Cambia el nombre del campo si es necesario
    data = {"movie_title": "TestMovie", "bug_description": "Este es un bug de prueba"}
    response = requests.post(url + "/report_bug", data=data, files=files)
    if response.url.find("Gracias") != -1:  # Cambia según el mensaje esperado
        print("Archivo subido correctamente")
    else:
        print("Error al subir el archivo")

def enviarReporteSinArchivo(url):
    """Prueba enviar un reporte sin subir archivo."""
    data = {"movie_title": "TestMovie", "bug_description": "Bug sin archivo adjunto"}
    response = requests.post(url + "/report_bug", data=data)
    if response.url.find("Gracias") != -1:  # Cambia según el mensaje esperado
        print("Reporte enviado correctamente sin archivo adjunto")
    else:
        print("Error al enviar reporte sin archivo adjunto")

def validarCamposVacios(url):
    """Prueba enviar un reporte con el cuadro de texto vacío."""
    data = {"movie_title": "TestMovie", "bug_description": ""}
    response = requests.post(url + "/report_bug", data=data)
    if re.search(r"\bEl campo no puede estar vacío\b", response.text):  # Cambia según el mensaje esperado
        print("Validación de campo vacío exitosa")
    else:
        print("Error en validación de campo vacío")

def enviarArchivoInvalido(url):
    """Prueba subir un archivo con un formato no permitido."""
    files = {"file_upload": ("malware.exe", b"archivo no permitido", "application/octet-stream")}
    data = {"movie_title": "TestMovie", "bug_description": "Prueba con archivo no permitido"}
    response = requests.post(url + "/report_bug", data=data, files=files)
    if re.search(r"\bFormato no permitido\b", response.text):  # Cambia según el mensaje esperado
        print("Validación de archivo inválido exitosa")
    else:
        print("Error en validación de archivo inválido")

if __name__ == "__main__":
    print("=== INICIANDO PRUEBAS AUTOMATIZADAS DE REPORTAR BUG ===")
    interfazReporteBugVisible(url)
    cuadroTextoVisible(url)
    subirArchivoFuncional(url)
    enviarReporteSinArchivo(url)
    validarCamposVacios(url)
    enviarArchivoInvalido(url)
    print("=== PRUEBAS FINALIZADAS ===")

