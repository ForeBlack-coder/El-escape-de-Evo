import turtle
import random
import math
import time
import pygame
import os
import sys
import numpy as np
import vlc
import threading

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.mixer.init()
pygame.init()
fondo = pygame.mixer.Sound(resource_path("resources/mp3/fondo.mp3"))
arr = pygame.sndarray.array(fondo)
factor = 1.5
nuevo_arr = arr[::int(factor)]
sonido_fast = pygame.sndarray.make_sound(nuevo_arr)

NUM_OBSTACULOS = 8  # Aumentado número de obstáculos
VELOCIDAD_OBSTACULOS = 7.0  # Aumentada velocidad de obstáculos
VELOCIDAD_JUGADOR = 70  # Aumentada velocidad del jugador

# Estados del juego
ESTADO_INTRO = -1  # Nuevo estado para el video intro
ESTADO_MENU = 0
ESTADO_JUGANDO = 1
ESTADO_GAME_OVER = 2
ESTADO_VICTORIA = 3

estado_actual = ESTADO_INTRO  # Comenzamos con el video intro
pantalla_mostrada = False
jugando = True
video_terminado = False

# Configuración de pantalla completa
ventana = turtle.Screen()
ventana.title("El escape de evo")
ventana.setup(width=1.0, height=1.0)  # Pantalla completa
ventana.bgcolor("black")
ventana.tracer(0)

# Obtener dimensiones reales de la pantalla
ancho = ventana.getcanvas().winfo_screenwidth()
alto = ventana.getcanvas().winfo_screenheight()
limite_x = ancho // 2 - 50
limite_y = alto // 2 - 190

# Agregar formas
try:
    ventana.addshape(resource_path("resources/img/evo.gif"))
    ventana.addshape(resource_path("resources/img/coca.gif"))
    ventana.addshape(resource_path("resources/img/DEA.gif"))
except:
    print("No se pudieron cargar las imágenes, usando formas básicas")

def salir():
    global jugando
    jugando = False

def reproducir_video_intro():
    """Reproduce el video de introducción usando VLC"""
    global video_terminado, estado_actual
    
    try:
        # Configurar VLC con la ruta personalizada
        vlc_path = resource_path("video")
        os.environ['VLC_PLUGIN_PATH'] = os.path.join(vlc_path, "plugins")
        
        # Crear instancia de VLC
        instance = vlc.Instance([
            '--intf', 'dummy',
            '--vout', 'directx',
            '--fullscreen',
            '--play-and-exit'
        ])
        
        # Crear reproductor
        player = instance.media_player_new()
        
        # Cargar el video
        media = instance.media_new(resource_path("video/intro.mp4"))
        player.set_media(media)
        
        # Configurar volumen al máximo
        player.audio_set_volume(100)
        
        # Reproducir
        player.play()
        
        # Esperar a que termine el video o que sea saltado
        while not video_terminado:
            state = player.get_state()
            if state == vlc.State.Ended or state == vlc.State.Stopped or state == vlc.State.Error:
                break
            time.sleep(0.1)
        
        # Limpiar
        player.stop()
        player.release()
        instance.release()
        
        video_terminado = True
        estado_actual = ESTADO_MENU
        
        # Iniciar la música de fondo después del video
        try:
            sonido_fast.play(-1)
        except:
            print("No se pudo cargar el audio de fondo")
        
    except Exception as e:
        print(f"Error al reproducir video: {e}")
        video_terminado = True
        estado_actual = ESTADO_MENU
        
        # Iniciar la música de fondo en caso de error
        try:
            sonido_fast.play(-1)
        except:
            print("No se pudo cargar el audio de fondo")

def iniciar_video():
    """Inicia el video en un hilo separado"""
    video_thread = threading.Thread(target=reproducir_video_intro)
    video_thread.daemon = True
    video_thread.start()

def mostrar_pantalla_intro():
    """Muestra mensaje mientras se carga el video"""
    limpiar_pantalla()
    ventana.bgcolor("black")
    
    mensaje = turtle.Turtle()
    mensaje.speed(0)
    mensaje.color("white")
    mensaje.penup()
    mensaje.hideturtle()
    mensaje.goto(0, 0)
    mensaje.write("Cargando...", align="center", font=("Arial", 36, "bold"))
    
    mensaje2 = turtle.Turtle()
    mensaje2.speed(0)
    mensaje2.color("gray")
    mensaje2.penup()
    mensaje2.hideturtle()
    mensaje2.goto(0, -50)
    mensaje2.write("Presiona ESPACIO para saltar", align="center", font=("Arial", 18, "normal"))

def mostrar_menu():
    """Muestra el menú principal con imagen de fondo"""
    limpiar_pantalla()
    
    # Intentar cargar imagen de fondo del menú
    try:
        ventana.bgpic(resource_path("resources/img/menu-background.gif"))
    except:
        ventana.bgcolor("black")
        print("No se pudo cargar la imagen de fondo del menú")
    
    # Título del juego
    titulo = turtle.Turtle()
    titulo.speed(0)
    titulo.color("green")
    titulo.penup()
    titulo.hideturtle()
    titulo.goto(0, 100)
    titulo.write("EL ESCAPE DE EVO", align="center", font=("Arial", 48, "bold"))
 
    # Instrucciones
    instrucciones = turtle.Turtle()
    instrucciones.speed(0)
    instrucciones.color("yellow")
    instrucciones.penup()
    instrucciones.hideturtle()
    instrucciones.goto(0, 0)
    instrucciones.write("Presiona ESPACIO para jugar", align="center", font=("Arial", 24, "normal"))
    
    instrucciones2 = turtle.Turtle()
    instrucciones2.speed(0)
    instrucciones2.color("yellow")
    instrucciones2.penup()
    instrucciones2.hideturtle()
    instrucciones2.goto(0, -50)
    instrucciones2.write("Presiona ESC para salir", align="center", font=("Arial", 24, "normal"))
    
    # Controles
    controles = turtle.Turtle()
    controles.speed(0)
    controles.color("cyan")
    controles.penup()
    controles.hideturtle()
    controles.goto(0, -150)
    controles.write("Controles: WASD o Flechas para moverte", align="center", font=("Arial", 18, "normal"))
    
    objetivo = turtle.Turtle()
    objetivo.speed(0)
    objetivo.color("white")
    objetivo.penup()
    objetivo.hideturtle()
    objetivo.goto(0, -200)
    objetivo.write("Objetivo: Recolecta 10 puntos evitando enemigos", align="center", font=("Arial", 18, "normal"))

def mostrar_game_over(max_puntos, total_muertes):
    """Muestra la pantalla de game over"""
    limpiar_pantalla()
    
    mensaje = turtle.Turtle()
    mensaje.speed(0)
    mensaje.color("red")
    mensaje.penup()
    mensaje.hideturtle()
    mensaje.goto(0, 100)
    mensaje.write("¡PERDISTE!", align="center", font=("Arial", 48, "bold"))
    
    estadisticas = turtle.Turtle()
    estadisticas.speed(0)
    estadisticas.color("white")
    estadisticas.penup()
    estadisticas.hideturtle()
    estadisticas.goto(0, 20)
    estadisticas.write(f"Máximo puntaje: {max_puntos}", align="center", font=("Arial", 24, "normal"))
    
    muertes_msg = turtle.Turtle()
    muertes_msg.speed(0)
    muertes_msg.color("white")
    muertes_msg.penup()
    muertes_msg.hideturtle()
    muertes_msg.goto(0, -20)
    muertes_msg.write(f"Total de muertes: {total_muertes}", align="center", font=("Arial", 24, "normal"))
    
    opciones = turtle.Turtle()
    opciones.speed(0)
    opciones.color("yellow")
    opciones.penup()
    opciones.hideturtle()
    opciones.goto(0, -80)
    opciones.write("Presiona R para volver a jugar o ESC para salir", align="center", font=("Arial", 20, "normal"))

def mostrar_victoria(max_puntos, total_muertes):
    """Muestra la pantalla de victoria"""
    limpiar_pantalla()
    
    mensaje = turtle.Turtle()
    mensaje.speed(0)
    mensaje.color("green")
    mensaje.penup()
    mensaje.hideturtle()
    mensaje.goto(0, 100)
    mensaje.write("¡GANASTE!", align="center", font=("Arial", 48, "bold"))
    
    estadisticas = turtle.Turtle()
    estadisticas.speed(0)
    estadisticas.color("white")
    estadisticas.penup()
    estadisticas.hideturtle()
    estadisticas.goto(0, 20)
    estadisticas.write(f"Máximo puntaje: {max_puntos}", align="center", font=("Arial", 24, "normal"))
    
    muertes_msg = turtle.Turtle()
    muertes_msg.speed(0)
    muertes_msg.color("white")
    muertes_msg.penup()
    muertes_msg.hideturtle()
    muertes_msg.goto(0, -20)
    muertes_msg.write(f"Total de muertes: {total_muertes}", align="center", font=("Arial", 24, "normal"))
    
    opciones = turtle.Turtle()
    opciones.speed(0)
    opciones.color("yellow")
    opciones.penup()
    opciones.hideturtle()
    opciones.goto(0, -80)
    opciones.write("Presiona R para volver a jugar o ESC para salir", align="center", font=("Arial", 20, "normal"))

def limpiar_pantalla():
    """Limpia todos los elementos de la pantalla"""
    for t in ventana.turtles():
        t.hideturtle()
        t.clear()
    ventana.bgcolor("black")

def inicializar_juego():
    """Inicializa todos los elementos del juego"""
    global jugador, estrella, obstaculos, estado
    
    limpiar_pantalla()
    
    try:
        ventana.bgpic(resource_path("resources/img/Laboratorio.gif"))
    except:
        ventana.bgcolor("dark green")
    
    # Recrear jugador
    jugador = turtle.Turtle()
    jugador.speed(0)
    try:
        jugador.shape(resource_path("resources/img/evo.gif"))
    except:
        jugador.shape("square")
        jugador.color("blue")
    jugador.penup()
    jugador.goto(0, 0)
    
    # Recrear estrella
    estrella = turtle.Turtle()
    estrella.speed(0)
    try:
        estrella.shape(resource_path("resources/img/coca.gif"))
    except:
        estrella.shape("circle")
        estrella.color("yellow")
    estrella.penup()
    estrella.goto(random.randint(-limite_x, limite_x), random.randint(-limite_y, limite_y))
    
    # Recrear obstáculos
    obstaculos = []
    for _ in range(NUM_OBSTACULOS):
        obstaculo = turtle.Turtle()
        obstaculo.speed(0)
        try:
            obstaculo.shape(resource_path("resources/img/DEA.gif"))
        except:
            obstaculo.shape("triangle")
            obstaculo.color("red")
        obstaculo.penup()
        obstaculo.goto(random.randint(-limite_x, limite_x), random.randint(-limite_y, limite_y))
        obstaculo.dx = VELOCIDAD_OBSTACULOS * random.choice([-1, 1])
        obstaculo.dy = VELOCIDAD_OBSTACULOS * random.choice([-1, 1])
        obstaculos.append(obstaculo)
    
    # Recrear estado del juego
    estado = EstadoJuego()

class EstadoJuego:
    def __init__(self):
        self.puntuacion = 0
        self.muertes = 0
        self.MAX_MUERTES = 0
        self.MAX_PUNTAJES = 0
        self.tiempo_inicio = time.time()
        
        self.marcador = turtle.Turtle()
        self.marcador.speed(0)
        self.marcador.color("white")
        self.marcador.penup()
        self.marcador.hideturtle()
        self.marcador.goto(0, limite_y - 50)
        
        self.marcador_muertes = turtle.Turtle()
        self.marcador_muertes.speed(0)
        self.marcador_muertes.color("blue")
        self.marcador_muertes.penup()
        self.marcador_muertes.hideturtle()
        self.marcador_muertes.goto(-limite_x + 50, limite_y - 50)
        
        self.marcador_tiempo = turtle.Turtle()
        self.marcador_tiempo.speed(0)
        self.marcador_tiempo.color("yellow")
        self.marcador_tiempo.penup()
        self.marcador_tiempo.hideturtle()
        self.marcador_tiempo.goto(limite_x - 50, limite_y - 50)
    
    def actualizar_marcadores(self):
        self.marcador.clear()
        self.marcador.write(f"Puntuación: {self.puntuacion}  ", align="center", font=("Courier", 24, "normal"))
        
        self.marcador_muertes.clear()
        self.marcador_muertes.write(f"Muertes: {self.muertes}", align="left", font=("Courier", 24, "normal"))
        
        tiempo_actual = int(time.time() - self.tiempo_inicio)
        minutos = tiempo_actual // 60
        segundos = tiempo_actual % 60
        self.marcador_tiempo.clear()
        self.marcador_tiempo.write(f"  Tiempo: {minutos:02d}:{segundos:02d}", align="right", font=("Courier", 24, "normal"))
    
    def registrar_muerte(self):
        global estado_actual
        self.muertes += 1
        self.puntuacion = 0
        self.tiempo_inicio = time.time() 
        if self.muertes > self.MAX_MUERTES:
            self.MAX_MUERTES = self.muertes
        if self.muertes >= 5:
            estado_actual = ESTADO_GAME_OVER
        
    def sumar_puntos(self, puntos):
        global estado_actual
        self.puntuacion += puntos
        if self.puntuacion > self.MAX_PUNTAJES:
            self.MAX_PUNTAJES = self.puntuacion
        if self.puntuacion >= 10:
            estado_actual = ESTADO_VICTORIA

# Funciones de movimiento con mayor velocidad
def mover_arriba():
    if estado_actual == ESTADO_JUGANDO:
        y = jugador.ycor()
        if y < limite_y:
            jugador.sety(y + VELOCIDAD_JUGADOR)

def mover_abajo():
    if estado_actual == ESTADO_JUGANDO:
        y = jugador.ycor()
        if y > -limite_y:
            jugador.sety(y - VELOCIDAD_JUGADOR)

def mover_izquierda():
    if estado_actual == ESTADO_JUGANDO:
        x = jugador.xcor()
        if x > -limite_x:
            jugador.setx(x - VELOCIDAD_JUGADOR)
        jugador.setheading(180)

def mover_derecha():
    if estado_actual == ESTADO_JUGANDO:
        x = jugador.xcor()
        if x < limite_x:
            jugador.setx(x + VELOCIDAD_JUGADOR)
        jugador.setheading(0)

# Funciones de control del juego
def saltar_intro():
    """Permite saltar el video de introducción"""
    global estado_actual, video_terminado
    if estado_actual == ESTADO_INTRO:
        video_terminado = True
        # No cambiar el estado aquí, dejar que lo haga el hilo del video

def iniciar_juego():
    global estado_actual, pantalla_mostrada
    if estado_actual == ESTADO_MENU:
        limpiar_pantalla()
        estado_actual = ESTADO_JUGANDO
        pantalla_mostrada = False
        inicializar_juego()
    elif estado_actual == ESTADO_INTRO:
        # Si están en intro, saltar al menú
        saltar_intro()

def reiniciar_juego():
    global estado_actual, pantalla_mostrada
    if estado_actual == ESTADO_GAME_OVER or estado_actual == ESTADO_VICTORIA:
        limpiar_pantalla()
        estado_actual = ESTADO_JUGANDO
        pantalla_mostrada = False
        inicializar_juego()

def volver_menu():
    global estado_actual
    estado_actual = ESTADO_MENU

# Configurar controles
ventana.listen()
ventana.onkey(mover_arriba, "Up")
ventana.onkey(mover_arriba, "w")
ventana.onkey(mover_abajo, "Down")
ventana.onkey(mover_abajo, "s")
ventana.onkey(mover_izquierda, "Left")
ventana.onkey(mover_izquierda, "a")
ventana.onkey(mover_derecha, "Right")
ventana.onkey(mover_derecha, "d")
ventana.onkey(salir, "Escape")
ventana.onkey(iniciar_juego, "space")  # Funciona para intro y menú
ventana.onkey(reiniciar_juego, "r")

def distancia(t1, t2):
    return math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))

# Mostrar pantalla de introducción e iniciar video
mostrar_pantalla_intro()
iniciar_video()

# No reproducir la música de fondo hasta después del video
# try:
#     sonido_fast.play(-1)  # Reproducir en loop
# except:
#     print("No se pudo cargar el audio de fondo")

# Bucle principal del juego
while jugando:
    ventana.update()
    
    if estado_actual == ESTADO_INTRO:
        # Esperar a que termine el video o que el usuario lo salte
        if video_terminado:
            estado_actual = ESTADO_MENU
            pantalla_mostrada = False
        time.sleep(0.016)
    
    elif estado_actual == ESTADO_MENU:
        if not pantalla_mostrada:
            mostrar_menu()
            pantalla_mostrada = True
        time.sleep(0.016)
        
    elif estado_actual == ESTADO_JUGANDO:
        # Lógica del juego
        estado.actualizar_marcadores()
        
        for obstaculo in obstaculos:
            obstaculo.setx(obstaculo.xcor() + obstaculo.dx)
            obstaculo.sety(obstaculo.ycor() + obstaculo.dy)

            # Rebotar en los bordes
            if obstaculo.xcor() > limite_x or obstaculo.xcor() < -limite_x:
                obstaculo.dx *= -1
            if obstaculo.ycor() > limite_y or obstaculo.ycor() < -limite_y:
                obstaculo.dy *= -1

            # Colisión con jugador
            if distancia(jugador, obstaculo) < 40:
                jugador.goto(random.randint(-limite_x, limite_x), random.randint(-limite_y, limite_y))
                estado.registrar_muerte()
                estado.actualizar_marcadores()

        # Colisión con estrella
        if distancia(jugador, estrella) < 50:
            estrella.goto(random.randint(-limite_x, limite_x), random.randint(-limite_y, limite_y))
            estado.sumar_puntos(1)
            estado.actualizar_marcadores()
        
        time.sleep(0.016)
        
    elif estado_actual == ESTADO_GAME_OVER:
        if not pantalla_mostrada:
            mostrar_game_over(estado.MAX_PUNTAJES, estado.MAX_MUERTES)
            pantalla_mostrada = True
        time.sleep(0.016)

    elif estado_actual == ESTADO_VICTORIA:
        if not pantalla_mostrada:
            mostrar_victoria(estado.MAX_PUNTAJES, estado.MAX_MUERTES)
            pantalla_mostrada = True
        time.sleep(0.016)

    else:
        # Estados temporales, solo esperamos input
        time.sleep(0.016)

ventana.bye()
try:
    fondo.stop()
except:
    pass
