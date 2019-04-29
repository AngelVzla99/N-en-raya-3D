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


############################## VARIABLES REFERENTES A UNA PARTIDA ######################################
class jugador:
    def __init__(self, nombre, turno):
    	self.nombre = nombre
    	self.filas = 0
    	self.columnas = 0
    	self.diagonales = 0
    	self.enZ = 0
    	self.turn = turno
player1 = jugador("", randint(1, 2))
player2 = jugador("", 3 - player1.turn)
T = [[[0]]]
tablero = 0
fila = 0
columna = 0
turno = 1
otro = True
done = False



############################# CONSTANTES REFERENTE A LA RESOLUCION DE LA PANTALLA #######################
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
resolucion = screen_size()
largo = int(resolucion[0]/2)
alto = int(resolucion[1]/2)
pygame.init()
pantalla = pygame.display.set_mode(resolucion)
reloj1 = pygame.time.Clock()



############################# IMAGENES QUE SE USARAN EN EL JUEGO #########################################
titulo = pygame.image.load("probandoTitulo.jpg")
titulo = pygame.transform.scale(titulo, (int(resolucion[0]/2.5), int(resolucion[1]/3)))
equis = pygame.image.load("Equis.png")
equis = pygame.transform.scale(equis, [int(largo)-5, int(alto)-5])
circulo = pygame.image.load("Circulo.png")
circulo = pygame.transform.scale(circulo, [int(largo)-5, int(alto)-5])
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
nombre1 = ""
nombre2 = ""
PHor1 = ""
PVer1 = ""
PDiag1 = ""
PEntTab1 = ""
PHor1 = ""
PVer1 = ""
PDiag1 = ""
PEntTab1 = ""
UltMen = ""




############################################## SUBPROGRAMAS ######################################################
# Verifica si aun hay algun espacio donde se pueda colocar fichas en el supertablero
def quedanFichas(T: [[[int]]]) -> bool:
	hayFichas = any( any( any(T[i][j][k]==0 for k in range(0, len(T))) for j in range(0, len(T))) for i in range(0, len(T)) )
	return hayFichas

# Verifica si la posicion donde se desea jugar es valida. Una jugada se considera valida si no hay ninguna ficha en la posicion indicada
def esValida(T: [[[int]]], tablero: int, fila: int, columna: int) -> bool:
	if tablero > len(T)-1 or tablero < 0 or fila > len(T)-1 or fila < 0 or columna > len(T)-1 or columna < 0:
		return False
	valido = (T[tablero][fila][columna] == 0)
	return valido

# Verifica si se formo una linea horizontal en la posicion donde se realizo la jugada
def hayLineaHorizontal(T: [[[int]]], tablero: int, fila: int, turno: int) -> bool:
	lineaHorizontal = all( T[tablero][fila][i]==turno for i in range(0, len(T)) )
	return lineaHorizontal

# Verifica si se formo una linea vertical en la posicion donde se realizo la jugada
def hayLineaVertical(T: [[[int]]], tablero: int ,columna: int , turno: int) -> bool:
	lineaVertical = all( T[tablero][i][columna]==turno for i in range(0, len(T)) )
	return lineaVertical

# Verifica si se formo una linea en la diagonal principal en la posicion donde se realizo la jugada
def hayLineaDiagonal(T: [[[int]]], tablero: int , fila: int, columna: int, turno: int) -> bool:
	lineaDiagonal = False
	if fila == columna:
		lineaDiagonal = all( T[tablero][i][i]==turno for i in range(0, len(T)) )
	return lineaDiagonal

# Verifica si se formo una linea en la diagonal inversa en la posicion donde se realizo la jugada
def hayLineaDiagonalInversa(T: [[[int]]], tablero: int , fila: int, columna: int, turno: int) -> bool:
	if fila + columna == len(T)-1:
		return all( T[tablero][i][len(T)-1-i]==turno for i in range(0, len(T)) )
	else:
		return False

# Verifica si se formo una linea en todos los tableros en la posicion donde se realizo la jugada
def hayLineaEnZ(T: [[[int]]], fila: int, columna: int, turno: int) -> bool:
	lineaEnZ = all( T[i][fila][columna]==turno for i in range(0, len(T)) )
	return lineaEnZ

# Modifica el supertablero, reflejando la jugada realizada por cierto jugador
def reflejarJugada(A: [[[int]]], tablero: int, fila: int, columna: int, turno: int):
	A[tablero][fila][columna] = turno

# Verifica si se formo alguna linea, en caso de ser asi, se lo indica a los jugadores y actualiza el contador de lineas
def hayLinea(T: [[[int]]], tablero: int, fila: int, columna: int, player: jugador):
	masPuntos = False
	if hayLineaHorizontal(T, tablero, fila, player.turn):
		player.columnas += 1
		masPuntos = True
	if hayLineaVertical(T, tablero, columna, player.turn):
		player.filas += 1
		masPuntos = True
	if hayLineaDiagonal(T, tablero, fila, columna, player.turn):
		player.diagonales += 1
		masPuntos = True
	if hayLineaDiagonalInversa(T, tablero, fila, columna, player.turn):
		player.diagonales += 1
		masPuntos = True
	if hayLineaEnZ(T, fila, columna, player.turn):
		player.enZ += 1
		masPuntos = True

	if masPuntos:
		return player.nombre + "  han  aumentados  tus  puntos"
	else:
		return ""

# Muestra graficamente el puntaje de cada jugador
def mostarPuntajes(nombre1, nombre2, PHor1, PVer1, PDiag1, PEntTab1, PHor2, PVer2, PDiag2, PEntTab2):
	pantalla.blit(fondo, [0, 0]) 

	pantalla.blit(nombre1, [int(resolucion[0]/8), 20])
	pantalla.blit(Horizontal, [10, 80])
	pantalla.blit(Vertical, [10, 110])
	pantalla.blit(Diagonal, [10, 140])
	pantalla.blit(EntreTableros, [10, 170])
	pantalla.blit(PHor1, [int(3*resolucion[0]/8), 80])
	pantalla.blit(PVer1, [int(3*resolucion[0]/8), 110])
	pantalla.blit(PDiag1, [int(3*resolucion[0]/8), 140])
	pantalla.blit(PEntTab1, [int(3*resolucion[0]/8), 170])

	pantalla.blit(nombre2, [int(5*resolucion[0]/8), 20])
	pantalla.blit(Horizontal, [int(resolucion[0]/2)+10, 80])
	pantalla.blit(Vertical, [int(resolucion[0]/2)+10, 110])
	pantalla.blit(Diagonal, [int(resolucion[0]/2)+10, 140])
	pantalla.blit(EntreTableros, [int(resolucion[0]/2)+10, 170])
	pantalla.blit(PHor2, [int(7*resolucion[0]/8), 80])
	pantalla.blit(PVer2, [int(7*resolucion[0]/8), 110])
	pantalla.blit(PDiag2, [int(7*resolucion[0]/8), 140])
	pantalla.blit(PEntTab2, [int(7*resolucion[0]/8), 170])

# Muestra graficamente el tablero actual, con las correspondientes fichas de ambos jugadores
def dibujarTab(Tab: [[int]]):
	equis = pygame.image.load("Equis.png")
	equis = pygame.transform.scale(equis, [int(largo/len(Tab))-5, int(alto/len(Tab))-5])
	circulo = pygame.image.load("Circulo.png")
	circulo = pygame.transform.scale(circulo, [int(largo/len(Tab))-5, int(alto/len(Tab))-5])
	pygame.draw.line(pantalla, (0,0,0), [int(resolucion[0]/6), 320], [int(resolucion[0]/6)+largo, 320], 4)
	pygame.draw.line(pantalla, (0,0,0), [int(resolucion[0]/6), 320], [int(resolucion[0]/6), 320+alto], 4)

	for i in range(0, len(Tab) + 1):
		pygame.draw.line(pantalla, (0,0,0), [int(resolucion[0]/6), 320 + i*int(alto/len(Tab))], [int(resolucion[0]/6)+largo, 320 + i*int(alto/len(Tab))], 4)
		pygame.draw.line(pantalla, (0,0,0), [int(resolucion[0]/6) + i*int(largo/len(Tab)), 320], [int(resolucion[0]/6) + i*int(largo/len(Tab)), 320 + alto], 4)

	for i in range(0, len(Tab)):
		for j in range(0, len(Tab)):
			if Tab[i][j]==1:
				pantalla.blit(equis, [int(resolucion[0]/6) + i*int(largo/len(Tab)) + 2, 320 + j*int(alto/len(Tab)) + 2])
			elif Tab[i][j]==2:
				pantalla.blit(circulo, [int(resolucion[0]/6) + i*int(largo/len(Tab)) + 2, 320 + j*int(alto/len(Tab)) + 2])

# Le pide al jugador que le toque jugar la jugada que desea realizar
def pedirJugada(T: [[[int]]], player1: jugador, player2: jugador, done: bool, UltMen: str, turno: int) -> (int, int, int):
	nombre1 = subtitulos.render(player1.nombre, True, (0,0,0))
	nombre2 = subtitulos.render(player2.nombre, True, (0,0,0))
	PHor1 = texto.render(str(player1.filas), True, (0,0,0))
	PVer1 = texto.render(str(player1.columnas), True, (0,0,0))
	PDiag1 = texto.render(str(player1.diagonales), True, (0,0,0))
	PEntTab1 = texto.render(str(player1.enZ), True, (0,0,0))
	PHor2 = texto.render(str(player2.filas), True, (0,0,0))
	PVer2 = texto.render(str(player2.columnas), True, (0,0,0))
	PDiag2 = texto.render(str(player2.diagonales), True, (0,0,0))
	PEntTab2 = texto.render(str(player2.enZ), True, (0,0,0))

	JTab = texto.render("0", True, (0,0,0))
	JCol = texto.render("0", True, (0,0,0))
	JFil = texto.render("0", True, (0,0,0))

	IndJug1 = texto.render(player1.nombre + "  indique  su  jugada", True, (0,0,0))
	IndJug2 = texto.render(player2.nombre + "  indique  su  jugada", True, (0,0,0))

	Mens = texto.render(UltMen, True, (0,0,0))

	tablero = "0"
	fila = "0"
	columna = "0"

	Etablero = True
	Ecolumna = False
	Efila = False

	k = 0



	if player1.turn == turno:
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
					elif evt.key == K_RETURN and Efila and len(fila) > 1:
						Efila = False
						Ecolumna = True

					elif evt.unicode.isnumeric() and int(columna) < 3 and Ecolumna:
						columna += evt.unicode
					elif evt.key == K_BACKSPACE and Ecolumna and len(columna) > 1:
						columna = columna[:-1]
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

			mostarPuntajes(nombre1, nombre2, PHor1, PVer1, PDiag1, PEntTab1, PHor2, PVer2, PDiag2, PEntTab2)
			pantalla.blit(IndJug1, [int(resolucion[0]/3) - 20, 200])
			pantalla.blit(Tab, [10, 230])
			pantalla.blit(Fil, [int(resolucion[0]/3) + 10, 230])
			pantalla.blit(Col, [int(2*resolucion[0]/3) + 10, 230])
			pantalla.blit(JTab, [int(resolucion[0]/6) + 10, 230])
			pantalla.blit(JFil, [int(resolucion[0]/2) + 10, 230])
			pantalla.blit(JCol, [int(5*resolucion[0]/6) + 10, 230])
			pantalla.blit(Tablero, [int(3*resolucion[0]/4), 320])
			pantalla.blit(Mens, [int(resolucion[0]/6), 260])
			pantalla.blit(triangulo, [int(3*resolucion[0]/4) + 30, 360 + k*30])
			for i in range(0, len(T)):
				Num = texto.render(str(i+1), True, (0,0,0))
				pantalla.blit(Num, [int(3*resolucion[0]/4), 350 + i*30])



			dibujarTab(T[k])



			pygame.display.update()
			reloj1.tick(20)

	else:
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
					elif evt.key == K_RETURN and Efila and len(fila) > 1:
						Efila = False
						Ecolumna = True

					elif evt.unicode.isnumeric() and int(columna) < 3 and Ecolumna:
						columna += evt.unicode
					elif evt.key == K_BACKSPACE and Ecolumna and len(columna) > 1:
						columna = columna[:-1]
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

			mostarPuntajes(nombre1, nombre2, PHor1, PVer1, PDiag1, PEntTab1, PHor2, PVer2, PDiag2, PEntTab2)
			pantalla.blit(IndJug2, [int(resolucion[0]/3) - 20, 200])
			pantalla.blit(Tab, [10, 230])
			pantalla.blit(Fil, [int(resolucion[0]/3) + 10, 230])
			pantalla.blit(Col, [int(2*resolucion[0]/3) + 10, 230])
			pantalla.blit(JTab, [int(resolucion[0]/6) + 10, 230])
			pantalla.blit(JFil, [int(resolucion[0]/2) + 10, 230])
			pantalla.blit(JCol, [int(5*resolucion[0]/6) + 10, 230])
			pantalla.blit(Tablero, [int(3*resolucion[0]/4), 320])
			pantalla.blit(Mens, [int(resolucion[0]/6) - 20, 260])
			pantalla.blit(triangulo, [int(3*resolucion[0]/4) + 30, 360 + k*30])
			for i in range(0, len(T)):
				Num = texto.render(str(i+1), 0, (0,0,0))
				pantalla.blit(Num, [int(3*resolucion[0]/4), 350 + i*30])

			dibujarTab(T[k])

			pygame.display.update()
			reloj1.tick(20)

	return int(tablero)-1, int(columna)-1, int(fila)-1

# Muestra el resultado de la partida
def resultado(T: [[[int]]], player1: jugador, player2: jugador, done: bool, total1: int, total2: int) -> bool:
	nombre1 = subtitulos.render(player1.nombre, True, (0,0,0))
	nombre2 = subtitulos.render(player2.nombre, True, (0,0,0))
	PHor1 = texto.render(str(player1.filas), True, (0,0,0))
	PVer1 = texto.render(str(player1.columnas), True, (0,0,0))
	PDiag1 = texto.render(str(player1.diagonales), True, (0,0,0))
	PEntTab1 = texto.render(str(player1.enZ), True, (0,0,0))
	PHor2 = texto.render(str(player2.filas), True, (0,0,0))
	PVer2 = texto.render(str(player2.columnas), True, (0,0,0))
	PDiag2 = texto.render(str(player2.diagonales), True, (0,0,0))
	PEntTab2 = texto.render(str(player2.enZ), True, (0,0,0))
	k = 0
	m = 0
	Yes = texto.render("Si", True, (0,0,0))
	Not = texto.render("No", True, (0,0,0))

	if total1 > total2:
		Mensj = texto.render(player1.nombre + "  ha  ganado  la  partida.  Desean  jugar  otra?", True, (0,0,0))
	elif total2 > total1:
		Mensj = texto.render(player2.nombre + "  ha  ganado  la  partida.  Desean  jugar  otra?", True, (0,0,0))
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


			mostarPuntajes(nombre1, nombre2, PHor1, PVer1, PDiag1, PEntTab1, PHor2, PVer2, PDiag2, PEntTab2)
			pantalla.blit(Tablero, [int(3*resolucion[0]/4), 320])
			pantalla.blit(triangulo, [int(3*resolucion[0]/4) + 30, 355 + k*30])
			pantalla.blit(Mensj, [int(resolucion[0]/15) - 40, 260])
			pantalla.blit(Yes, [int(2*resolucion[0]/3), 260])
			pantalla.blit(Not, [int(7*resolucion[0]/8) - 20, 260])
			pantalla.blit(triangulo, [int(2*resolucion[0]/3 + 60 + m*270), 260])

			for i in range(0, len(T)):
				Num = texto.render(str(i+1), 0, (0,0,0))
				pantalla.blit(Num, [int(3*resolucion[0]/4), 350 + i*30])

			dibujarTab(T[k])

			pygame.display.update()
			reloj1.tick(20)

# Verifica si se desea jugar otra partida. 
def otraPartida(player1: jugador, player2: jugador, n: int, A: [[[int]]],  done: bool) -> bool:
	nombre1 = subtitulos.render(player1.nombre, True, (0,0,0))
	nombre2 = subtitulos.render(player2.nombre, True, (0,0,0))
	PHor1 = texto.render(str(player1.filas), True, (0,0,0))
	PVer1 = texto.render(str(player1.columnas), True, (0,0,0))
	PDiag1 = texto.render(str(player1.diagonales), True, (0,0,0))
	PEntTab1 = texto.render(str(player1.enZ), True, (0,0,0))
	PHor2 = texto.render(str(player2.filas), True, (0,0,0))
	PVer2 = texto.render(str(player2.columnas), True, (0,0,0))
	PDiag2 = texto.render(str(player2.diagonales), True, (0,0,0))
	PEntTab2 = texto.render(str(player2.enZ), True, (0,0,0))
	k = 0
	m = 0
	Yes = texto.render("Si", True, (0,0,0))
	Not = texto.render("No", True, (0,0,0))
	cambDim = False
	player1.nombre = ""
	player1.filas = 0
	player1.columnas = 0
	player1.diagonales = 0
	player1.enZ = 0

	player2.nombre = ""
	player2.filas = 0
	player2.columnas = 0
	player2.diagonales = 0
	player2.enZ = 0

# En esta pantalla se le pide a los dos jugadores su nombre, asi como la dimension del supertablero
def pantallaMultiJug(done: bool) -> int:
	nombre1 = ""
	nombre2 = ""
	N = "0"
	mensj = ""

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.unicode.isalpha() and len(player1.nombre) < 11:
					player1.nombre += evt.unicode
				elif evt.key == K_BACKSPACE:
					player1.nombre = player1.nombre[:-1]
				elif evt.key == K_RETURN and len(player1.nombre) > 0:
					done = True
			if evt.type == pygame.QUIT:
				pygame.quit()

		pantalla.blit(fondo, [0, 0]) 
		pantalla.blit(titulo, [int((resolucion[0]-resolucion[0]/2.5)/2), 50])
		pantalla.blit(Jugador1, [int(resolucion[0]/5), int(resolucion[1]/2)])
		pantalla.blit(Jugador2, [int(resolucion[0]/5), int(4*resolucion[1]/6)])
		pantalla.blit(NumDim, [int(resolucion[0]/11), int(5*resolucion[1]/6)])
		pantalla.blit(trianguloInv2, [int(resolucion[0]/8), int(resolucion[1]/2)+5])

		nombre1 = nombres.render(player1.nombre, True, (0,0,0))
		pantalla.blit(nombre1, [int(resolucion[0]/2), int(resolucion[1]/2)])

		pygame.display.update()
		reloj1.tick(20) 

	done = False

	while not done:
		for evt in pygame.event.get():
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
		pantalla.blit(titulo, [int((resolucion[0]-resolucion[0]/2.5)/2), 50])
		pantalla.blit(Jugador1, [int(resolucion[0]/5), int(resolucion[1]/2)])
		pantalla.blit(Jugador2, [int(resolucion[0]/5), int(4*resolucion[1]/6)])
		pantalla.blit(NumDim, [int(resolucion[0]/11), int(5*resolucion[1]/6)])
		pantalla.blit(nombre1, [int(resolucion[0]/2), int(resolucion[1]/2)])
		pantalla.blit(trianguloInv2, [int(resolucion[0]/8), int(4*resolucion[1]/6)+5])

		nombre2 = nombres.render(player2.nombre, True, (0,0,0))
		pantalla.blit(nombre2, [int(resolucion[0]/2), int(4*resolucion[1]/6)])

		pygame.display.update()
		reloj1.tick(20)

	done = False

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.unicode.isnumeric() and len(N) < 3:
					N += evt.unicode
				elif evt.key == K_BACKSPACE:
					N = N[:-1]
				elif evt.key == K_RETURN and len(N) > 1 and int(N)<11:
					done = True
				elif evt.key == K_RETURN and len(N) > 1 and int(N)>10:
					mensj = "El  supertablero  no  puede  ser  tan  grande"
			if evt.type == pygame.QUIT:
				pygame.quit()

		pantalla.blit(fondo, [0, 0]) 
		pantalla.blit(titulo, [int((resolucion[0]-resolucion[0]/2.5)/2), 50])
		pantalla.blit(Jugador1, [int(resolucion[0]/5), int(resolucion[1]/2)])
		pantalla.blit(Jugador2, [int(resolucion[0]/5), int(4*resolucion[1]/6)])
		pantalla.blit(NumDim, [int(resolucion[0]/11), int(5*resolucion[1]/6)])
		pantalla.blit(nombre1, [int(resolucion[0]/2), int(resolucion[1]/2)])
		pantalla.blit(nombre2, [int(resolucion[0]/2), int(4*resolucion[1]/6)])
		pantalla.blit(trianguloInv2, [10, int(5*resolucion[1]/6)+5])

		Mensj = texto.render(mensj, True, (0,0,0))
		pantalla.blit(Mensj, [int(resolucion[0]/11), int(10*resolucion[1]/11)])

		NAct = N

		Num = nombres.render(NAct.lstrip("0"), True, (0,0,0))
		pantalla.blit(Num, [int(3*resolucion[0]/4), int(5*resolucion[1]/6)])

		pygame.display.update()
		reloj1.tick(20)

	done = False
	return int(N)

# Pantalla donde se realiza una juego
def partida(done: bool, otro: bool, T: [[[int]]], player1: jugador, player2: jugador, turno: int, UltMen: str, N: int):
		while quedanFichas(T):
			tablero, fila, columna = pedirJugada(T, player1, player2, done, UltMen, turno)
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

# Pantalla principal, tiene las opciones de jugar multijugador, contra la computadora o salir del juego
def pantallaPrinc(done: bool) -> bool:
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
		pantalla.blit(titulo, [int((resolucion[0]-resolucion[0]/2.5)/2), 50])
		pantalla.blit(MultJug, [int(resolucion[0]/4), int(resolucion[1]/2)])
		pantalla.blit(Computer, [int(resolucion[0]/4), int(4*resolucion[1]/6)])
		pantalla.blit(Exit, [int(resolucion[0]/4), int(5*resolucion[1]/6)])
		pantalla.blit(triangulo2, [int(2*resolucion[0]/3), int((3+k)*resolucion[1]/6) + 10])

		pygame.display.update()
		reloj1.tick(20) 

	done = False

# Subprograma principal que llama a los demas subprogramas
def main():
	otro = True
	multijugador = pantallaPrinc(False)
	turno = 1
	N = 0
	T = [[[0]]]

	if multijugador:
		while otro:

			N = pantallaMultiJug(False)
			print(N)

			T = [[[0 for i in range(0, N)] for j in range(0, N)] for k in range(0, N)]

			UltMen = ""

			partida(False, otro, T, player1, player2, turno, UltMen, N)

			total1 = player1.filas + player1.columnas + player1.diagonales + player1.enZ
			total2 = player2.filas + player2.columnas + player2.diagonales + player2.enZ
			otro = resultado(T, player1, player2, done, total1, total2)
			if otro:
				otraPartida(player1, player2, N, T, done)
				turno = 3 - turno

	otraPartida(player1, player2, N, T, done)
	main()





main()