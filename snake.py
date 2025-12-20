from pynput import keyboard
import time
import random

# --- CONFIGURACIÓN DEL JUEGO ---
MAP_ANCHO = 20
MAP_ALTO = 20
velocidad = 0.15  # segundos por movimiento

# DIRECCIÓN ACTUAL
direccion = "RIGHT"

# SERPIENTE: lista de tuplas (x, y). Cabeza = serpiente[0]
serpiente = [(5, 5), (4, 5), (3, 5)]

# GENERAR COMIDA
def generar_comida(serpiente):
    while True:
        x = random.randint(0, MAP_ANCHO - 1)
        y = random.randint(0, MAP_ALTO - 1)
        if (x, y) not in serpiente:
            return (x, y)

comida = generar_comida(serpiente)

def dibujar_mapa(serpiente, comida):
    print("\n" * 5)  # "limpia" la pantalla (simple)

    # Borde superior
    print("#" * (MAP_ANCHO + 2))

    for y in range(MAP_ALTO):
        fila = "#"
        for x in range(MAP_ANCHO):

            if (x, y) == serpiente[0]:
                fila += "@"
            elif (x, y) in serpiente:
                fila += "O"
            elif (x, y) == comida:
                fila += "*"
            else:
                fila += " "

        fila += "#"
        print(fila)

    # Borde inferior
    print("#" * (MAP_ANCHO + 2))

# --- CONTROL DEL TECLADO ---
def presionar(key):
    global direccion
    try:
        if key == keyboard.Key.up and direccion != "DOWN":
            direccion = "UP"
        elif key == keyboard.Key.down and direccion != "UP":
            direccion = "DOWN"
        elif key == keyboard.Key.left and direccion != "RIGHT":
            direccion = "LEFT"
        elif key == keyboard.Key.right and direccion != "LEFT":
            direccion = "RIGHT"
    except:
        pass


listener = keyboard.Listener(on_press=presionar)
listener.start()

# --- LOOP PRINCIPAL DEL JUEGO ---
while True:

    # Obtener posición de la cabeza
    head_x, head_y = serpiente[0]

    # Mover según la dirección
    if direccion == "UP":
        head_y -= 1
    elif direccion == "DOWN":
        head_y += 1
    elif direccion == "LEFT":
        head_x -= 1
    elif direccion == "RIGHT":
        head_x += 1

    nueva_cabeza = (head_x, head_y)

    # --- DETECCIÓN DE COLISIONES ---
    # Contra paredes
    if (head_x < 0 or head_x >= MAP_ANCHO or
        head_y < 0 or head_y >= MAP_ALTO):
        print("FIN DEL JUEGO: la serpiente chocó con la pared.")
        break

    # Contra su propio cuerpo
    if nueva_cabeza in serpiente:
        print("FIN DEL JUEGO: la serpiente chocó consigo misma.")
        break

    # --- MOVIMIENTO DE LA SERPIENTE ---
    # Insertar nueva cabeza
    serpiente.insert(0, nueva_cabeza)

    # ¿Comió la comida?
    if nueva_cabeza == comida:
        print("La serpiente comió comida")
        comida = generar_comida(serpiente)
        velocidad -= 0.01
        
    else:
        serpiente.pop()  # quitar la cola (solo si no comió)

    dibujar_mapa(serpiente, comida)
    time.sleep(velocidad)

listener.stop()
print("Game Over")