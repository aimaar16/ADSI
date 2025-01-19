import requests
from bs4 import BeautifulSoup
import re

# URL base del sistema
url = "http://localhost:5000"

def verificarAccesoReporte(url):
    """Verifica que el usuario pueda acceder a la página de reporte."""
    response = requests.get(url + "/report.html")
    if re.search(r"\bReportar Película\b", response.text):
        print("Acceso a la página de reporte: OK")
    else:
        print("Acceso a la página de reporte: FALLO")

def validarCuadroTextoVisible(url):
    """Verifica que el cuadro de texto para describir el problema esté presente."""
    response = requests.get(url + "/report.html?movie_title=TestMovie")
    soup = BeautifulSoup(response.text, "html.parser")
    cuadro_texto = soup.find("textarea", {"id": "bug_description"})
    if cuadro_texto:
        print("Cuadro de texto para descripción visible: OK")
    else:
        print("Cuadro de texto para descripción no visible: FALLO")

def validarBotonEnvio(url):
    """Verifica que el botón de envío esté presente y correctamente etiquetado."""
    response = requests.get(url + "/report.html")
    soup = BeautifulSoup(response.text, "html.parser")
    boton_envio = soup.find("button", {"type": "submit"})
    if boton_envio and "Reportar" in boton_envio.text:
        print("Botón de envío presente y etiquetado correctamente: OK")
    else:
        print("Botón de envío no presente o etiquetado incorrectamente: FALLO")

def validarInteraccionJS(url):
    """Verifica que el formulario contenga un evento asociado al botón."""
    response = requests.get(url + "/report.html")
    if re.search(r"showSuccessMessage", response.text):
        print("Evento de JavaScript asociado al botón de envío: OK")
    else:
        print("No se detectó evento de JavaScript en el botón de envío: FALLO")

def validarTituloPelícula(url):
    """Verifica que el título de la película se muestre correctamente en la página."""
    response = requests.get(url + "/report.html?movie_title=TestMovie")
    if re.search(r'Reportar un problema con "TestMovie"', response.text):
        print("Título de la película mostrado correctamente: OK")
    else:
        print("Error al mostrar el título de la película: FALLO")

if __name__ == "__main__":
    print("=== INICIANDO PRUEBAS AUTOMATIZADAS ===")
    verificarAccesoReporte(url)
    validarCuadroTextoVisible(url)
    validarBotonEnvio(url)
    validarInteraccionJS(url)
    validarTituloPelícula(url)
    print("=== PRUEBAS FINALIZADAS ===")

