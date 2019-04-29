import pygame
import subprocess
from pygame.locals import *


def screen_size():
    size = (None, None)
    args = ["xrandr", "-q", "-d", ":0"]
    proc = subprocess.Popen(args,stdout=subprocess.PIPE)
    for line in proc.stdout:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
            if "Screen" in line:
                size = (int(line.split()[7]),  int(line.split()[9][:-1]))
    return size

size = screen_size()
print(size[0])



def main():
	######################################## ESTO SE HACE AL PRINCIPIO SIEMPRE ########################################
	pygame.init() # Con pygame.init se inicializan todos los modulos. Tambien hay funciones que inicializan modulos en especifico
	pantalla = pygame.display.set_mode(size) # Ahora fijamos la pantalla, el arreglo que se pasa por parametro indica ancho y alto
	pygame.display.set_caption("Practicando PyGame") # Titulo de la venta
	salir = False # Variable usada para salir de bucle principal
	reloj1 = pygame.time.Clock() # Variable usada para que el bucle principal no consuma toda la memoria
	####################################################################################################################

	white = (255, 255, 255)
	black = (0, 0, 0)
	rojo = (200, 10, 15)
	done = False

	# Crearemos una superficie:
	s1 = pygame.Surface([100, 150])
	s1.fill(black)
	equis = pygame.image.load("Equis.png")
	circulo = pygame.image.load("Circulo.png")
	fondo = pygame.image.load("Fondo.png")
	fondoC = pygame.transform.scale(fondo, size)
	fondoC.set_alpha(100) # Agrega transparencia a la imagen
	fuente1 = pygame.font.Font("ka1.ttf", 50)
	nombres = pygame.font.Font("ArcadeClassic.ttf", 70)
	texto = fuente1.render("Jugador 1", 0, black)
	texto2 = fuente1.render("Jugador 2: ", 0, black)
	titulo = pygame.image.load("probandoTitulo.jpg")
	tituloAct = pygame.transform.scale(titulo, (600, 300))

	player1 = nombres.render("", 0, black)
	player2 = nombres.render("", 0, black)
	nombre1 = ""
	nombre2 = ""

	# Crearemos un rectangulo:
	r1 = pygame.Rect(50, 50, 200, 45) # (posicionX, posicionY, ancho, largo)

	######################################## BUCLE PRINCIPAL ######################################################
	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.unicode.isalpha() and len(nombre1) < 15:
					nombre1 += evt.unicode
				elif evt.key == K_BACKSPACE:
					nombre1 = nombre1[:-1]
				elif evt.key == K_RETURN:
					done = True
			if evt.type == pygame.QUIT:
				pygame.quit()
		pantalla.blit(fondoC, [0, 0]) 
		pantalla.blit(tituloAct, [400, 50])
		pantalla.blit(texto, [100, 450])
		pantalla.blit(texto2, [100, 600])

		player1 = nombres.render(nombre1, True, black)
		pantalla.blit(player1, [600, 450])

		pygame.display.update()
		reloj1.tick(20) 

	done = False

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.unicode.isalpha() and len(nombre2) < 15:
					nombre2 += evt.unicode
				elif evt.key == K_BACKSPACE:
					nombre2 = nombre2[:-1]
				elif evt.key == K_RETURN:
					done = True
			if evt.type == pygame.QUIT:
				pygame.quit()
		pantalla.blit(fondoC, [0, 0]) 
		pantalla.blit(tituloAct, [400, 50])
		pantalla.blit(texto, [100, 450])
		pantalla.blit(texto2, [100, 600])
		pantalla.blit(player1, [600, 450])

		player2 = nombres.render(nombre2, True, black)
		pantalla.blit(player2, [600, 600])


		pygame.display.update()
		reloj1.tick(20) 



	while not salir:
		for event in pygame.event.get(): # Esto recorrera todos los eventos de PyGame
			if event.type == pygame.QUIT: #QUIT es el evento de cerrar la ventana
				salir = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				r1.move_ip(4,4) # Mueve al rectangulo con respecto a la posicion actual
		pantalla.fill(white) # Le da un color a la ventana
		pantalla.blit(fondoC, [0, 0]) # Dibuja a la superficie s1 sobre pantalla en la posicion indicada
		pantalla.blit(texto, [100, 450])
		pantalla.blit(texto2, [100, 600])
		#pygame.draw.rect(pantalla, rojo, r1) # Dibuja al rectangulo r1 sobre la superficie pantalla
		pantalla.blit(tituloAct, [400, 50])

		pygame.display.update() # Actualiza la pantalla, debe de hacerse esta actualizacion constantemente
		reloj1.tick(20) # Esto hace que el bucle principal se actualice cada 20 fps
	###############################################################################################################

	pygame.quit(white) # Cierra la ventana

main()