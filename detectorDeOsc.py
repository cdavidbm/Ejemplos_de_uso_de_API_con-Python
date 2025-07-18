from pythonosc import dispatcher, osc_server


def recibir_canal1(direccion, valor):
    """Recibe datos del canal /ch/1"""
    print(f"Canal 1: {valor}")


# Configurar dispatcher
disp = dispatcher.Dispatcher()
disp.map("/ch/2", recibir_canal1)

# Crear servidor en puerto 7000
servidor = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 7000), disp)

print("Escuchando OSC en puerto 7000...")
print("Presiona Ctrl+C para detener")

try:
    servidor.serve_forever()
except KeyboardInterrupt:
    print("\nDetenido")
    servidor.shutdown()


def main():
    print("🎛️  Receptor OSC simple para canal /ch/1")
    print("📍 Escuchando en puertos 7000 y 7001")
    print("⏹️  Presiona Ctrl+C para detener\n")

    # Crear servidores para ambos puertos
    servidor1 = crear_servidor(7000)
    servidor2 = crear_servidor(7001)

    # Iniciar servidores en hilos separados
    hilo1 = threading.Thread(target=servidor1.serve_forever)
    hilo2 = threading.Thread(target=servidor2.serve_forever)

    hilo1.daemon = True
    hilo2.daemon = True

    hilo1.start()
    hilo2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidores...")
        servidor1.shutdown()
        servidor2.shutdown()
        print("✅ Servidores detenidos")


if __name__ == "__main__":
    main()
