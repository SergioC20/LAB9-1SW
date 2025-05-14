import sys
import threading
import ldclient
from ldclient.config import Config
from ldclient.context import Context

LD_SDK_KEY = "sdk-b03a7264-8a0d-432f-b575-25f98403b8f0"  

# Crear el cliente con configuración
ld_client = ldclient.LDClient(Config(LD_SDK_KEY))

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

def close_client():
    print("\nCerrando conexión con LaunchDarkly...")
    ld_client.close()
    print("Conexión cerrada.")

# Ejecución principal
if __name__ == "__main__":
    try:
        # Crear un contexto de usuario válido
        user_context = Context.builder("usuario-123") \
            .name("Usuario de prueba") \
            .set("role", "tester") \
            .build()

        # Obtener el valor del flag desde LaunchDarkly
        version_mejorada = ld_client.variation("version-2.0-mejorada", user_context, False)
        print(f"Resultado del flag: {version_mejorada}")

        if version_mejorada:
            print("Ejecutando la Versión 2.0 - Mejorada")
            main_v2()
        else:
            print("Ejecutando la Versión 1.0 - Básica")
            main_v1()
        
        print("\nEjecución completada.")

    finally:
        # Cerrar el cliente en un hilo separado para evitar bloqueos
        threading.Thread(target=close_client, daemon=True).start()
        sys.stdout.flush()
