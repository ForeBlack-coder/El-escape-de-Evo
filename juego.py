import turtle
import random
import math
import time
import pygame

pygame.mixer.init()
pygame.init()
fondo = pygame.mixer.Sound("resources/fondo.mp3")

NUM_OBSTACULOS = 6
VELOCIDAD_OBSTACULOS = 4.5

ventana = turtle.Screen()
ventana.title("El escape de evo")
ventana.bgpic("resources/Laboratorio.gif")
ventana.setup(width=950, height=650) 
ventana.tracer(0)

ventana.addshape("resources/evo.gif")
ventana.addshape("resources/coca.gif")
ventana.addshape("resources/DEA.gif")
jugando = True

def salir():
    global jugando
    jugando = False

jugador = turtle.Turtle()
jugador.speed(0)
jugador.shape("evo.gif")
jugador.penup()
jugador.goto(0, 0)

estrella = turtle.Turtle()
estrella.speed(0)
estrella.shape("coca.gif")
estrella.penup()
estrella.goto(random.randint(-380, 380), random.randint(-280, 280))

obstaculos = []
for _ in range(NUM_OBSTACULOS):
    obstaculo = turtle.Turtle()
    obstaculo.speed(0)
    obstaculo.shape("DEA.gif")
    obstaculo.penup()
    obstaculo.goto(random.randint(-380, 380), random.randint(-280, 280))
    obstaculo.dx = VELOCIDAD_OBSTACULOS * random.choice([-1, 1])
    obstaculo.dy = VELOCIDAD_OBSTACULOS * random.choice([-1, 1])
    obstaculos.append(obstaculo)

class EstadoJuego:
    def __init__(self):
        self.puntuacion = 0
        self.muertes = 0
        self.MAX_MUERTES = 0
        self.MAX_PUNTAJES = 0
        self.tiempo_inicio = time.time()
        
        self.marcador = turtle.Turtle()
        self.marcador.speed(0)
        self.marcador.color("green")
        self.marcador.penup()
        self.marcador.hideturtle()
        self.marcador.goto(0, 260)
        
        self.marcador_muertes = turtle.Turtle()
        self.marcador_muertes.speed(0)
        self.marcador_muertes.color("blue")
        self.marcador_muertes.penup()
        self.marcador_muertes.hideturtle()
        self.marcador_muertes.goto(-380, 260)
        
        self.marcador_tiempo = turtle.Turtle()
        self.marcador_tiempo.speed(0)
        self.marcador_tiempo.color("yellow")
        self.marcador_tiempo.penup()
        self.marcador_tiempo.hideturtle()
        self.marcador_tiempo.goto(380, 260)
    
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
        self.muertes += 1
        self.puntuacion = 0
        self.tiempo_inicio = time.time() 
        if self.muertes > self.MAX_MUERTES:
            self.MAX_MUERTES = self.muertes
        if self.muertes >= 5:
            print(f"Tuviste marcador maximo de {self.MAX_PUNTAJES} puntos, consumiste {self.MAX_MUERTES} muertes")
            print("Perdiste")
            global jugando
            jugando = False
        
    def sumar_puntos(self, puntos):
        self.puntuacion += puntos
        if self.puntuacion > self.MAX_PUNTAJES:
            self.MAX_PUNTAJES = self.puntuacion
        if self.puntuacion >= 10:
            print(f"Tuviste marcador maximo de {self.MAX_PUNTAJES} puntos, consumiste {self.MAX_MUERTES} muertes")
            print("Ganaste")
            global jugando
            jugando = False

estado = EstadoJuego()

def mover_arriba():
    y = jugador.ycor()
    if y < 290:
        jugador.sety(y + 35)

def mover_abajo():
    y = jugador.ycor()
    if y > -290:
        jugador.sety(y - 35)

def mover_izquierda():
    x = jugador.xcor()
    if x > -390:
        jugador.setx(x - 35)
    jugador.setheading(180)

def mover_derecha():
    x = jugador.xcor()
    if x < 390:
        jugador.setx(x + 35)
    jugador.setheading(0)


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
global puntuacion, muertes, MAX_MUERTES, MAX_PUNTAJES, MAX_TIEMPO
puntuacion = 0
muertes = 0
MAX_MUERTES = 0

def distancia(t1, t2):
    return math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
fondo.play()
while jugando:

    ventana.update()
    estado.actualizar_marcadores()  
    for obstaculo in obstaculos:
        obstaculo.setx(obstaculo.xcor() + obstaculo.dx)
        obstaculo.sety(obstaculo.ycor() + obstaculo.dy)

      
        if obstaculo.xcor() > 380 or obstaculo.xcor() < -380:
            obstaculo.dx *= -1
        if obstaculo.ycor() > 280 or obstaculo.ycor() < -280:
            obstaculo.dy *= -1

       
        if distancia(jugador, obstaculo) < 40:
            jugador.goto(random.randint(-380, 380), random.randint(-280, 280))
            estado.registrar_muerte()
            estado.actualizar_marcadores()

   
    if distancia(jugador, estrella) < 40:
        estrella.goto(random.randint(-380, 380), random.randint(-280, 280))
        estado.sumar_puntos(1)
        estado.actualizar_marcadores()
    time.sleep(0.016)  
ventana.bye()
fondo.stop()
