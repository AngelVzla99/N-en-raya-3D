import pygame, subprocess
from random import randint
from pygame.locals import *

#
# Proyecto: N EN RAYA TRIDIMENSIONAL
#
# DESCRIPCION: Parecido al juego 3 en raya, pero en este caso, el juego consta de N tableros de tamanyo NxN, donde, ademas de las lineas horizontales, verticales y diagonales en un mismo tablero, tambien se considerara una linea cuando un jugador consigue colocar una ficha en la misma casilla de los N tableros. Ademas, el juego no se termina cuando un jugador logra una linea, sino que se sigue hasta que se completen las NxNxN casillas, considerandose ganador quien logre realizar mas lineas.
#
#
# Autor:
#		Amin Arriaga y Angel Garces
#
# Ultima modificacion: 27/04/2019


########################################### CLASE JUGADOR ################################################
class Jugador:
    def __init__(self, nombre, turno):
    	# Guardamos el nombre del Jugador
    	self.nombre = nombre

    	# Guardamos el numero de lineas en filas, columnas, diagonales y entre tableros que ha hecho el Jugador
    	self.filas = 0
    	self.columnas = 0
    	self.diagonales = 0
    	self.enZ = 0

    	# Guardamos la posicion de las lineas en filas, columnas, diagonales y entre tableros que ha hecho el Jugador
    	self.lineasFila = []
    	self.lineasCol = []
    	self.lineasDiag = []
    	self.lineasEnZ = []

    	# Guardamos el turno correspondiente del Jugador
    	self.turn = turno

    	# Guardamos el numero de victorias de un Jugador
    	self.wins = 0


############################# CONSTANTES REFERENTE A LA RESOLUCION DE LA PANTALLA #######################
resolucion = [1366,750]
largo = 680
alto = 375
pygame.init()
pantalla = pygame.display.set_mode(resolucion)
reloj1 = pygame.time.Clock()



############################# IMAGENES QUE SE USARAN EN EL JUEGO #########################################
titulo = pygame.image.load("probandoTitulo.jpg")
titulo = pygame.transform.scale(titulo, (int(resolucion[0]/2.5), int(resolucion[1]/3)))
triangulo = pygame.image.load("Triangulo.png")
triangulo = pygame.transform.scale(triangulo, [40, 30])
triangulo2 = pygame.transform.scale(triangulo, [60, 50])
trianguloInv = pygame.image.load("TrianguloInv.png")
trianguloInv1 = pygame.transform.scale(trianguloInv, [40, 30])
trianguloInv2 = pygame.transform.scale(trianguloInv, [60, 50])
fondo = pygame.image.load("Fondo.jpg")
fondo = pygame.transform.scale(fondo, resolucion)



############################# FUENTES DE TEXTO ##############################################################
subtitulos = pygame.font.Font("ka1.ttf", 50)
nombres = pygame.font.Font("ArcadeClassic.ttf", 70)
texto = pygame.font.Font("miracle.otf", 30)



############################# TEXTOS QUE SE USARAN EN EL JUEGO ###############################################
Jugador1 = subtitulos.render("Jugador 1: ", True, (0,0,0))
Jugador2 = subtitulos.render("Jugador 2: ", True, (0,0,0))
Horizontal = texto.render("Lineas  Horizontales ", True, (0,0,0))
Vertical = texto.render("Lineas  Verticales ", True, (0,0,0))
Diagonal = texto.render("Lineas  Diagonales ", True, (0,0,0))
EntreTableros = texto.render("Lineas  Entre  Tableros ", True, (0,0,0))
Tablero = texto.render("Tablero", 0 ,(0,0,0))
Tab = texto.render("Tablero ", True, (0,0,0))
Fil = texto.render("Fila ", True, (0,0,0))
Col = texto.render("Columna ", True, (0,0,0))
MultJug = subtitulos.render("Multijugador", True, (0,0,0))
Computer = subtitulos.render("Individual", True, (0,0,0))
Exit = subtitulos.render("Salir", True, (0,0,0))
NumDim = subtitulos.render("Dimension del Tablero: ", True, (0,0,0))
Yes = texto.render("Si", True, (0,0,0))
Not = texto.render("No", True, (0,0,0))




############################################## SUBPROGRAMAS ######################################################
def quedanFichas(T: [[[int]]]) -> bool:
	# Verifica si aun hay algun espacio donde se pueda colocar fichas en el supertablero

	hayFichas = any( any( any(T[i][j][k]==0 for k in range(0, len(T))) for j in range(0, len(T))) for i in range(0, len(T)) )
	return hayFichas

def esValida(T: [[[int]]], tablero: int, fila: int, columna: int) -> bool:
	# Verifica si la posicion donde se desea jugar es valida. Una jugada se considera valida si no hay ninguna ficha en la posicion indicada

	if tablero > len(T)-1 or tablero < 0 or fila > len(T)-1 or fila < 0 or columna > len(T)-1 or columna < 0:
		return False
	valido = (T[tablero][fila][columna] == 0)
	return valido

def hayLineaHorizontal(T: [[[int]]], tablero: int, fila: int, player: Jugador) -> bool:
	# Verifica si se formo una linea horizontal en la posicion donde se realizo la jugada
	turno = player.turn

	lineaHorizontal = all( T[tablero][fila][i]==turno for i in range(0, len(T)) )

	# Guardamos la posicion donde el jugador hizo una linea
	if lineaHorizontal:
		print("Hola")
		player.lineasFila.append([tablero, fila])

	return lineaHorizontal

def hayLineaVertical(T: [[[int]]], tablero: int ,columna: int , player: Jugador) -> bool:
	# Verifica si se formo una linea vertical en la posicion donde se realizo la jugada
	turno = player.turn

	lineaVertical = all( T[tablero][i][columna]==turno for i in range(0, len(T)) )

	# Guardamos la posicion donde el jugador hizo una linea
	if lineaVertical:
		player.lineasCol.append([tablero, columna])

	return lineaVertical

def hayLineaDiagonal(T: [[[int]]], tablero: int , fila: int, columna: int, player: Jugador) -> bool:
	# Verifica si se formo una linea en la diagonal principal en la posicion donde se realizo la jugada
	turno = player.turn

	lineaDiagonal = False
	if fila == columna:
		lineaDiagonal = all( T[tablero][i][i]==turno for i in range(0, len(T)) )

	# Guardamos la posicion donde el jugador hizo una linea
	if lineaDiagonal:
		player.lineasDiag.append([tablero, True])

	return lineaDiagonal

def hayLineaDiagonalInversa(T: [[[int]]], tablero: int , fila: int, columna: int, player: Jugador) -> bool:
	# Verifica si se formo una linea en la diagonal inversa en la posicion donde se realizo la jugada
	turno = player.turn

	lineaDiagonal = False
	if fila + columna == len(T)-1:
		lineaDiagonal = all( T[tablero][i][len(T)-1-i]==turno for i in range(0, len(T)) )
	
	# Guardamos la posicion donde el jugador hizo una linea
	if lineaDiagonal:
		player.lineasDiag.append([tablero, False])

	return lineaDiagonal

def hayLineaEnZ(T: [[[int]]], fila: int, columna: int, player: Jugador) -> bool:
	# Verifica si se formo una linea en todos los tableros en la posicion donde se realizo la jugada
	turno = player.turn

	lineaEnZ = all( T[i][fila][columna]==turno for i in range(0, len(T)) )
	return lineaEnZ

def reflejarJugada(A: [[[int]]], tablero: int, fila: int, columna: int, turno: int):
	# Modifica el supertablero, reflejando la jugada realizada por cierto jugador

	A[tablero][fila][columna] = turno

def hayLinea(T: [[[int]]], tablero: int, fila: int, columna: int, player: Jugador) -> str:
	# Verifica si se formo alguna linea, en caso de ser asi, se lo indica a los jugadores y actualiza el contador de lineas

	masPuntos = False
	if hayLineaHorizontal(T, tablero, fila, player):
		print("Hize linea horizontal")
		player.filas += 1
		masPuntos = True
	if hayLineaVertical(T, tablero, columna, player):
		player.columnas += 1
		masPuntos = True
	if hayLineaDiagonal(T, tablero, fila, columna, player):
		player.diagonales += 1
		masPuntos = True
	if hayLineaDiagonalInversa(T, tablero, fila, columna, player):
		player.diagonales += 1
		masPuntos = True
	if hayLineaEnZ(T, fila, columna, player):
		player.enZ += 1
		masPuntos = True

	if masPuntos:
		return player.nombre + "  han  aumentados  tus  puntos!"
	else:
		return ""

def mostarPuntajes(player1: Jugador, player2: Jugador):
	# Muestra graficamente el puntaje de cada jugador


	pantalla.blit(fondo, [0, 0]) 

	# Guardamos en vairables del tipo "surface" los datos del jugador 1
	name1 = subtitulos.render(str(player1.nombre), True, (0,0,0))
	PFilas1 = texto.render(str(player1.filas), True, (0,0,0))
	PCol1 = texto.render(str(player1.columnas), True, (0,0,0))
	PDia1 = texto.render(str(player1.diagonales), True, (0,0,0))
	PenZ1 = texto.render(str(player1.enZ), True, (0,0,0))

	# Guardamos en vairables del tipo "surface" los datos del jugador 2
	name2 = subtitulos.render(str(player2.nombre), True, (0,0,0))
	PFilas2 = texto.render(str(player2.filas), True, (0,0,0))
	PCol2 = texto.render(str(player2.columnas), True, (0,0,0))
	PDia2 = texto.render(str(player2.diagonales), True, (0,0,0))
	PenZ2 = texto.render(str(player2.enZ), True, (0,0,0))

	# Informacion del Jugador 1
	pantalla.blit(name1, [120, 20])
	pantalla.blit(Horizontal, [10, 80])
	pantalla.blit(Vertical, [10, 110])
	pantalla.blit(Diagonal, [10, 140])
	pantalla.blit(EntreTableros, [10, 170])
	pantalla.blit(PFilas1, [560, 80])
	pantalla.blit(PCol1, [560, 110])
	pantalla.blit(PDia1, [560, 140])
	pantalla.blit(PenZ1, [560, 170])

	# Informacion del Jugador 2
	pantalla.blit(name2, [800, 20])
	pantalla.blit(Horizontal, [660, 80])
	pantalla.blit(Vertical, [660, 110])
	pantalla.blit(Diagonal, [660, 140])
	pantalla.blit(EntreTableros, [660, 170])
	pantalla.blit(PFilas2, [1200, 80])
	pantalla.blit(PCol2, [1200, 110])
	pantalla.blit(PDia2, [1200, 140])
	pantalla.blit(PenZ2, [1200, 170])

def dibujarTab(Tab: [[int]], player1: Jugador, player2: Jugador, tablero: int):
	# Muestra graficamente el tablero actual, con las correspondientes fichas de ambos jugadores

	# Cargamos las imagenes de la X y el O. No se hizo antes pues su tamanyo depende de la dimensaion del tablero
	equis = pygame.image.load("Equis.png")
	equis = pygame.transform.scale(equis, [int(largo/len(Tab))-5, int(alto/len(Tab))-5])
	circulo = pygame.image.load("Circulo.png")
	circulo = pygame.transform.scale(circulo, [int(largo/len(Tab))-5, int(alto/len(Tab))-5])

	# Dibujamos la linea superior e izquierda del Tablero
	pygame.draw.line(pantalla, (0,0,0), [100, 320], [100+largo, 320], 4)
	pygame.draw.line(pantalla, (0,0,0), [100, 320], [100, 320+alto], 4)

	# Dibujamos las lineas internas del tablero 
	for i in range(0, len(Tab) + 1):
		pygame.draw.line(pantalla, (0,0,0), [100, 320 + i*(alto/len(Tab))], [100+largo, 320 + i*(alto/len(Tab))], 4)
		pygame.draw.line(pantalla, (0,0,0), [100 + i*(largo/len(Tab)), 320], [100 + i*(largo/len(Tab)), 320 + alto], 4)

	# Dibujamos las X's y O's correspondientes
	for i in range(0, len(Tab)):
		for j in range(0, len(Tab)):
			if Tab[i][j]==1:
				pantalla.blit(equis, [100 + j*(largo/len(Tab)) + 2, 320 + i*(alto/len(Tab)) + 2])
			elif Tab[i][j]==2:
				pantalla.blit(circulo, [100 + j*(largo/len(Tab)) + 2, 320 + i*(alto/len(Tab)) + 2])

	# Dibujamos las lineas correspondientes al Jugador 1
	for linea in player1.lineasFila:
		if linea[0] == tablero:
			pygame.draw.line(pantalla, (255,0,0), [100, 320 + (linea[1] + 1/2)*(alto/len(Tab))], [100+largo, 320 + (linea[1] + 1/2)*(alto/len(Tab))], 4)

	for linea in player2.lineasFila:
		if linea[0] == tablero:
			pygame.draw.line(pantalla, (255,0,0), [100, 320 + (linea[1] + 1/2)*(alto/len(Tab))], [100+largo, 320 + (linea[1] + 1/2)*(alto/len(Tab))], 4)



def jugada(T: [[[int]]], player1: Jugador, player2: Jugador, IndJug, Mensaje) -> (int, int, int):
	# Le pedimos a un jugador la jugada que realizara

	# Sera el texto que se mostrara en la interfaz, e indica lo que va escribiendo el jugador
	tablero = "0"
	fila = "0"
	columna = "0"

	# Indica que es lo siguiente que le toca al jugador elegir
	Etablero = True
	Ecolumna = False
	Efila = False

	# Indica si el jugador ya termino de elegir
	done = False

	# Variable que mueve la flecha para indicar al jugador en que tablero se encuentra
	k = 0

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.unicode.isnumeric() and int(tablero) < 3 and Etablero:
					tablero += evt.unicode
				elif evt.key == K_BACKSPACE and Etablero and len(tablero) > 1:
					tablero = tablero[:-1]
				elif evt.key == K_RETURN and Etablero and len(tablero) > 1:
					Etablero = False
					Efila = True

				elif evt.unicode.isnumeric() and int(fila) < 3 and Efila:
					fila += evt.unicode
				elif evt.key == K_BACKSPACE and Efila and len(fila) > 1:
					fila = fila[:-1]
				elif evt.key == K_BACKSPACE and Efila and len(fila) == 1:
					Efila = False
					Etablero = True
				elif evt.key == K_RETURN and Efila and len(fila) > 1:
					Efila = False
					Ecolumna = True

				elif evt.unicode.isnumeric() and int(columna) < 3 and Ecolumna:
					columna += evt.unicode
				elif evt.key == K_BACKSPACE and Ecolumna and len(columna) > 1:
					columna = columna[:-1]
				elif evt.key == K_BACKSPACE and Ecolumna and len(columna) == 1:
					Ecolumna = False
					Efila = True
				elif evt.key == K_RETURN and Ecolumna and len(columna) > 1:
					Ecolumna = False
					done = True

				if evt.key == K_UP and k > 0:
					k -= 1
				if evt.key == K_DOWN and k < len(T)-1:
					k += 1

			if evt.type == pygame.QUIT:
				pygame.quit()

		tableroAct = tablero
		columnaAct = columna
		filaAct = fila
		JTab = texto.render(tableroAct.lstrip("0"), True, (0,0,0))
		JCol = texto.render(columnaAct.lstrip("0"), True, (0,0,0))
		JFil = texto.render(filaAct.lstrip("0"), True, (0,0,0))

		mostarPuntajes(player1, player2)

		pantalla.blit(IndJug, [430, 200])
		pantalla.blit(Tab, [10, 230])
		pantalla.blit(Fil, [460, 230])
		pantalla.blit(Col, [910, 230])
		pantalla.blit(JTab, [220, 230])
		pantalla.blit(JFil, [630, 230])
		pantalla.blit(JCol, [1130, 230])
		pantalla.blit(Tablero, [980, 320])
		pantalla.blit(Mensaje, [100, 260])
		pantalla.blit(triangulo, [1050, 345 + k*30])
		for i in range(0, len(T)):
			Num = texto.render(str(i+1), True, (0,0,0))
			pantalla.blit(Num, [1020, 350 + i*30])

		dibujarTab(T[k], player1, player2, k)

		pygame.display.update()
		reloj1.tick(20)

	return int(tablero), int(fila), int(columna)

def pedirJugada(T: [[[int]]], player1: Jugador, player2: Jugador, UltMen: str, turno: int) -> (int, int, int):
	# Le pide al jugador que le toque jugar la jugada que desea realizar

	IndJug1 = texto.render(player1.nombre + "  indique  su  jugada", True, (0,0,0))
	IndJug2 = texto.render(player2.nombre + "  indique  su  jugada", True, (0,0,0))
	Mens = texto.render(UltMen, True, (0,0,0))

	if player1.turn == turno:
		tablero, fila, columna = jugada(T, player1, player2, IndJug1, Mens)

	else:
		tablero, fila, columna = jugada(T, player1, player2, IndJug2, Mens)

	return tablero-1, fila-1, columna-1

def resultado(T: [[[int]]], player1: Jugador, player2: Jugador, total1: int, total2: int) -> bool:
	# Muestra el resultado de la partida

	# Variable que mueve la flecha para indicar al jugador en que tablero se encuentra
	k = 0

	# Variable que mueve la flecha para indicar al jugador si desea jugar otra partida o no
	m = 0

	# Indica si el jugador ya termino de elegir
	done = False

	if total1 > total2:
		Mensj = texto.render(player1.nombre + "  ha  ganado  la  partida.  Desean  jugar  otra?", True, (0,0,0))
		player1.wins += 1
	elif total2 > total1:
		Mensj = texto.render(player2.nombre + "  ha  ganado  la  partida.  Desean  jugar  otra?", True, (0,0,0))
		player2.wins += 1
	else:
		Mensj = texto.render("El  juego  termino  en  empate.  Desean  jugar  otra?", True, (0,0,0))

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.key == K_UP and k > 0:
					k -= 1
				if evt.key == K_DOWN and k < len(T)-1:
					k += 1
				if evt.key == K_RIGHT:
					m = 1
				if evt.key == K_LEFT:
					m = 0
				if evt.key == K_RETURN and m == 0:
					return True
				if evt.key == K_RETURN and m == 1:
					return False

			if evt.type == pygame.QUIT:
				pygame.quit()


		mostarPuntajes(player1, player2)

		pantalla.blit(Tablero, [980, 320])
		pantalla.blit(triangulo, [1050, 345 + k*30])
		pantalla.blit(Mensj, [100, 260])
		pantalla.blit(Yes, [900, 260])
		pantalla.blit(Not, [1100, 260])
		pantalla.blit(triangulo, [950 + m*220, 260])

		for i in range(0, len(T)):
			Num = texto.render(str(i+1), 0, (0,0,0))
			pantalla.blit(Num, [1020, 350 + i*30])

		dibujarTab(T[k], player1, player2, k)

		pygame.display.update()
		reloj1.tick(20)

def guardarNombre(player1: Jugador, player2: Jugador, turn: int):
	# Guarda el nombre indicado por el usuario

	# Indica cuando el jugador ya termino de colocar el nombre
	done = False

	if turn == 1:
		mensj = "Jugador 1   indique   su   nombre."
	else:
		mensj = "Jugador 2   indique   su   nombre."

	while not done:
		for evt in pygame.event.get():
			if turn == 1:
				if evt.type == KEYDOWN:
					if evt.unicode.isalpha() and len(player1.nombre) < 11:
						player1.nombre += evt.unicode
					elif evt.key == K_BACKSPACE:
						player1.nombre = player1.nombre[:-1]
					elif evt.key == K_RETURN and len(player1.nombre) > 0:
						done = True
				if evt.type == pygame.QUIT:
					pygame.quit()
			else:
				if evt.type == KEYDOWN:
					if evt.unicode.isalpha() and len(player2.nombre) < 11:
						player2.nombre += evt.unicode
					elif evt.key == K_BACKSPACE:
						player2.nombre = player2.nombre[:-1]
					elif evt.key == K_RETURN and len(player2.nombre) > 0:
						done = True
				if evt.type == pygame.QUIT:
					pygame.quit()

		pantalla.blit(fondo, [0, 0]) 
		pantalla.blit(titulo, [450, 50])
		pantalla.blit(Jugador1, [300, 375])
		pantalla.blit(Jugador2, [300, 495])
		pantalla.blit(NumDim, [100, 615])
		pantalla.blit(trianguloInv2, [180, 380 + (turn-1)*120])

		Mensj = texto.render(mensj, True, (0,0,0))
		pantalla.blit(Mensj, [400, 320])

		nombre1 = nombres.render(player1.nombre, True, (0,0,0))
		pantalla.blit(nombre1, [750, 375])

		nombre2 = nombres.render(player2.nombre, True, (0,0,0))
		pantalla.blit(nombre2, [750, 495])

		pygame.display.update()
		reloj1.tick(20) 

	if turn == 1:
		return nombre1
	else:
		return nombre2

def pantallaMultiJug(player1: Jugador, player2: Jugador) -> int:
	# En esta pantalla se le pide a los dos jugadores su nombre, asi como la dimension del supertablero

	# Dimension del tablero
	N = "0"

	# Nombres de los jugadores
	nombre1 = guardarNombre(player1, player2, 1)
	nombre2 = guardarNombre(player1, player2, 2)

	mensj = "Indiquen   la   dimension   del   super-tablero."

	# Indica cuando el usuario ya decidio la dimension del super-tablero
	done = False

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.unicode.isnumeric() and len(N) < 3:
					N += evt.unicode
				elif evt.key == K_BACKSPACE:
					N = N[:-1]
				elif evt.key == K_RETURN and len(N) > 1 and int(N)<12:
					done = True
				elif evt.key == K_RETURN and len(N) > 1 and int(N)>11:
					mensj = "El   supertablero   no   puede   ser   tan   grande."
			if evt.type == pygame.QUIT:
				pygame.quit()

		pantalla.blit(fondo, [0, 0]) 
		pantalla.blit(titulo, [450, 50])
		pantalla.blit(Jugador1, [300, 375])
		pantalla.blit(Jugador2, [300, 495])
		pantalla.blit(NumDim, [100, 615])
		pantalla.blit(nombre1, [750, 375])
		pantalla.blit(nombre2, [750, 495])
		pantalla.blit(trianguloInv2, [10, 615])

		Mensj = texto.render(mensj, True, (0,0,0))
		pantalla.blit(Mensj, [400, 320])

		NAct = N

		Num = nombres.render(NAct.lstrip("0"), True, (0,0,0))
		pantalla.blit(Num, [int(3*resolucion[0]/4), int(5*resolucion[1]/6)])

		pygame.display.update()
		reloj1.tick(20)


	return int(N)

def partida(otro: bool, T: [[[int]]], player1: Jugador, player2: Jugador, turno: int, UltMen: str, N: int) -> bool:
	# Pantalla donde se realiza una juego
	while quedanFichas(T):

		# Le pedimos al usuario correspondiente el taablero, fila y columna donde quiere jugar 
		tablero, fila, columna = pedirJugada(T, player1, player2, UltMen, turno)

		# Mensaje que se le va informando a los jugadores
		UltMen = ""

		if esValida(T, tablero, fila, columna):

			reflejarJugada(T, tablero, fila, columna, turno)

			if turno==player1.turn:
				UltMen = hayLinea(T, tablero, fila, columna, player1)
				turno = 3 - turno
			else:
				UltMen = hayLinea(T, tablero, fila, columna, player2)
				turno = 3 - turno
		else:
			UltMen = "La  jugada  no  es  valida"

	return True

def pantallaPrinc() -> bool:
	# Pantalla principal, tiene las opciones de jugar multijugador, contra la computadora o salir del juego

	# Indica cuando el usuario ya decidio el modo de juego
	done = False

	# Variable que mueve la flecha para indicarle al usuario en cual opcion se encuentra
	k = 0

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.key == K_UP and k > 0:
					k -= 1
				if evt.key == K_DOWN and k < 2:
					k += 1
				if evt.key == K_RETURN and k == 0:
					return True
				if evt.key == K_RETURN and k == 1:
					return False
				if evt.key == K_RETURN and k == 2:
					pygame.quit()
			if evt.type == pygame.QUIT:
				pygame.quit()

		pantalla.blit(fondo, [0, 0]) 
		pantalla.blit(titulo, [450, 50])
		pantalla.blit(MultJug, [375, 375])
		pantalla.blit(Computer, [375, 495])
		pantalla.blit(Exit, [375, 615])
		pantalla.blit(triangulo2, [900, 380 + k*120])

		pygame.display.update()
		reloj1.tick(20) 




def main():
	# Funcion Principal

	while True:

		# Creamos las dos instancias de la clase Jugador, los cuales tendran la informacion de ambos jugadores
		#player1 = Jugador("", randint(1, 2))
		#player2 = Jugador("", 3 - player1.turn)

		# Mientras la variable otro sea True, se repetira la partida entre los dos jugadores
		otro = True

		# El primer turno siempre es 1
		turno = 1

		# Creamos la matriz tridimensional que representara al super-tablero
		T = [[[0]]]

		# Entramos al menu principal
		multijugador = pantallaPrinc()

		# Si se decidio jugar una partida multijugador
		if multijugador:
			# Creamos las dos instancias de la clase Jugador, los cuales tendran la informacion de ambos jugadores
			player1 = Jugador("", randint(1, 2))
			player2 = Jugador("", 3 - player1.turn)

			# Llamamos a la pantalla donde los jugadores deciden sus nombres y la dimension del super-tablero
			N = pantallaMultiJug(player1, player2)

			while otro:
				# Restauramos a 0 los puntajes de ambos jugadores
				player1.filas = 0
				player1.columnas = 0
				player1.diagonales = 0
				player1.enZ = 0

				player2.filas = 0
				player2.columnas = 0
				player2.diagonales = 0
				player2.enZ = 0

				# Vaciamos el super-tablero
				T = [[[0 for i in range(0, N)] for j in range(0, N)] for k in range(0, N)]

				# Vaciamos el ultimo mensaje
				UltMen = ""

				# Llamamos a una partida. Termino sera True si la partida llega a su final
				termino = partida(otro, T, player1, player2, turno, UltMen, N)

				# Sumamos los puntos que obtuvieron el jugador1 y el jugador2 respectivamente
				total1 = player1.filas + player1.columnas + player1.diagonales + player1.enZ
				total2 = player2.filas + player2.columnas + player2.diagonales + player2.enZ

				# Verificamos si los jugadores quieren jugar otra partida
				if termino:
					otro = resultado(T, player1, player2, total1, total2)
					turno = 3 - turno
				else:
					otro = False

main()