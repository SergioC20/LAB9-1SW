import ldclient
from ldclient.config import Config

# Configuración del cliente de LaunchDarkly
LD_SDK_KEY = "tu-clave-de-sdk"  # Reemplaza con tu clave de SDK
ld_client = ldclient.LDClient(LD_SDK_KEY)

def main_v1():
    nombre = input("¿Cuál es tu nombre? ")
    print(f"Hola, {nombre}!")
    print(f"[Registro] Nombre ingresado: {nombre}")

def main_v2():
    idiomas = {
        "es": "Hola",
        "en": "Hello",
        "fr": "Bonjour"
    }
    lang = input("Selecciona un idioma (es/en/fr): ").lower()
    if lang not in idiomas:
        print("Idioma no soportado. Usando español por defecto.")
        lang = "es"
    pregunta_nombre = {
        "es": "¿Cuál es tu nombre? ",
        "en": "What is your name? ",
        "fr": "Quel est votre nom? "
    }
    nombre = input(pregunta_nombre[lang]).strip()
    if not nombre.isalpha():
        print("El nombre no puede estar vacío o contener números.")
        return
    saludo = f"{idiomas[lang]}, {nombre}!"
    print(saludo)
    print(f"[Registro] Idioma seleccionado: {lang}, Nombre ingresado: {nombre}")

# Ejecución principal
if __name__ == "__main__":
    user = {"key": "usuario-123"}  # Identificador del usuario
    feature_flag_key = "version-2.0-mejorada"

    # Verificar el estado del feature flag
    if ld_client.variation(feature_flag_key, user, False):
        main_v2()
    else:
        main_v1()

    # Cerrar el cliente de LaunchDarkly
    ld_client.close()
