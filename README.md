# Juego de la Serpiente (Snake) en Python

Proyecto final de la asignatura **Lógica de Programación**. Este juego implementa la clásica serpiente en la consola, utilizando entrada por teclado para mover la serpiente, generación aleatoria de comida y detección de colisiones.

##  Características
- Mapa de **20x20** con bordes.
- Control por teclado con las flechas **↑ ↓ ← →**.
- Comida generada aleatoriamente (`*`).
- La serpiente crece al comer y **aumenta la velocidad** progresivamente.
- Detección de colisiones: **paredes** y **cuerpo**.
- Representación en consola: cabeza `@`, cuerpo `O`.

##  Tecnologías y librerías
- **Python 3.8+**
- Librerías estándar: `time`, `random`.
- Librería externa: `pynput` (para capturar el teclado).

##  Requisitos
Asegúrate de tener Python instalado. Luego instala `pynput`:

```bash
pip install pynput
```

> **Nota:** En algunos sistemas, puede requerir permisos de acceso al teclado o ejecución desde la terminal.

##  Ejecución
1. Guarda el código en un archivo, por ejemplo `snake.py`.
2. Ejecuta desde la terminal:

```bash
python snake.py
```

##  Controles
- **Flecha arriba**: mover hacia arriba.
- **Flecha abajo**: mover hacia abajo.
- **Flecha izquierda**: mover hacia la izquierda.
- **Flecha derecha**: mover hacia la derecha.

Las direcciones opuestas inmediatas están bloqueadas para evitar que la serpiente se "doble" sobre sí misma (por ejemplo, si va a la derecha, no puede cambiar a la izquierda en el mismo instante).

##  Estructura del código
```text
snake.py
├── Configuración del juego (MAP_ANCHO, MAP_ALTO, velocidad, dirección, serpiente)
├── generar_comida(serpiente): posición aleatoria evitando la serpiente
├── dibujar_mapa(serpiente, comida): impresión de bordes, serpiente y comida
├── presionar(key): captura y actualiza dirección con pynput
├── Listener de teclado: keyboard.Listener(on_press=presionar)
└── Loop principal:
    ├── cálculo de nueva cabeza según dirección
    ├── detección de colisiones (paredes y cuerpo)
    ├── actualización (crecer si come, mover si no)
    ├── redibujar mapa
    └── control de velocidad
```

##  Explicación por secciones
### 1) Configuración del juego
- `MAP_ANCHO`, `MAP_ALTO`: dimensiones del mapa.
- `velocidad`: segundos entre movimientos (disminuye al comer).
- `direccion`: estado global de dirección actual (`UP`, `DOWN`, `LEFT`, `RIGHT`).
- `serpiente`: lista de tuplas `(x, y)` donde `serpiente[0]` es la cabeza.

### 2) Generación de comida
```python
def generar_comida(serpiente):
    while True:
        x = random.randint(0, MAP_ANCHO - 1)
        y = random.randint(0, MAP_ALTO - 1)
        if (x, y) not in serpiente:
            return (x, y)
```
- Bucle que elige coordenadas aleatorias dentro del mapa.
- Garantiza que la comida **no** aparezca sobre el cuerpo de la serpiente.

### 3) Dibujo del mapa
```python
def dibujar_mapa(serpiente, comida):
    print("\n" * 5)  # limpia la consola
    print("#" * (MAP_ANCHO + 2))  # borde superior
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
    print("#" * (MAP_ANCHO + 2))  # borde inferior
```
- Imprime bordes, la cabeza `@`, el cuerpo `O` y la comida `*`.
- Inserta saltos de línea para simular limpieza de pantalla.

### 4) Control del teclado
```python
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
```
- Cambia la dirección sólo si no es opuesta a la actual.
- Envuelto en `try/except` para evitar errores por entradas no manejadas.

### 5) Loop principal
```python
while True:
    head_x, head_y = serpiente[0]
    if direccion == "UP":
        head_y -= 1
    elif direccion == "DOWN":
        head_y += 1
    elif direccion == "LEFT":
        head_x -= 1
    elif direccion == "RIGHT":
        head_x += 1
    nueva_cabeza = (head_x, head_y)

    # colisión con paredes
    if (head_x < 0 or head_x >= MAP_ANCHO or
        head_y < 0 or head_y >= MAP_ALTO):
        print("FIN DEL JUEGO: la serpiente chocó con la pared.")
        break

    # colisión con el cuerpo
    if nueva_cabeza in serpiente:
        print("FIN DEL JUEGO: la serpiente chocó consigo misma.")
        break

    serpiente.insert(0, nueva_cabeza)  # mover cabeza

    if nueva_cabeza == comida:
        print("La serpiente comió comida")
        comida = generar_comida(serpiente)
        velocidad -= 0.01  # aumentar dificultad
    else:
        serpiente.pop()  # mover cola

    dibujar_mapa(serpiente, comida)
    time.sleep(velocidad)
```
- Calcula la nueva posición de la cabeza según la dirección.
- Verifica colisiones antes de actualizar el estado.
- Si come: genera nueva comida y **reduce** el tiempo de espera (más rapidez).
- Si no come: elimina el último segmento (movimiento).

##  Consejos de uso y compatibilidad
- Ejecuta en una **terminal real** (CMD/PowerShell, Terminal de macOS o Linux) para que las teclas se capturen correctamente.
- En algunos IDEs la captura de teclado con `pynput` puede comportarse distinto.

##  Mejoras futuras (ideas)
- Puntaje y registro de récords.
- Interfaz gráfica con `tkinter` o `pygame`.
- Pausa/Reanudar.
- Múltiples niveles o tamaños de mapa.
- Obstáculos y power-ups.

##  Licencia
Este proyecto se comparte bajo la licencia **MIT**. Siéntete libre de usarlo y mejorarlo.

##  Autor
**LUZARDO SOLEDISPA GUSTAVO ANTONIO** — Estudiante.

