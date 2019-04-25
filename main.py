N = int(input("Ingresa la dimension del supertablero: "))
T = [[[0 for i in range(0, N)] for j in range(0, N)] for k in range(0, N)]
tablero = 0
fila = 0
columna = 0
turno = 1

class jugador:
    def __init__(self, N, nombre, turno):
    	self.nombre = nombre
    	self.filas = 0
    	self.columnas = 0
    	self.diagonales = 0
    	self.enZ = 0
    	self.turn = turno


def quedanFichas(T: [[[int]]]) -> bool:
	hayFichas = any( any( any(T[i][j][k]==0 for k in range(0, N)) for j in range(0, N)) for i in range(0, N) )
	return hayFichas

def esValida(T: [[[int]]], tablero: int, fila: int, columna: int) -> bool:
	valido = (T[tablero][fila][columna] == 0)
	return valido

def hayLineaHorizontal(T: [[[int]]], tablero: int, fila: int, turno: int) -> bool:
	lineaHorizontal = all( T[tablero][fila][i]==turno for i in range(0, len(T)) )
	return lineaHorizontal

def hayLineaVertical(T: [[[int]]], tablero: int ,columna: int , turno: int) -> bool:
	lineaVertical = all( T[tablero][i][columna]==turno for i in range(0, len(T)) )
	return lineaVertical

def hayLineaDiagonal(T: [[[int]]], tablero: int , fila: int, columna: int, turno: int) -> bool:
	lineaDiagonal = False
	if fila == columna:
		lineaDiagonal = all( T[tablero][i][i]==turno for i in range(0, len(T)) )
	return lineaDiagonal

def hayLineaDiagonalInversa(T: [[[int]]], tablero: int , fila: int, columna: int, turno: int) -> bool:
	if fila + columna == len(T)-1:
		return all( T[tablero][i][len(T)-1-i]==turno for i in range(0, len(T)) )
	else:
		return False

def hayLineaEnZ(T: [[[int]]], fila: int, columna: int, turno: int) -> bool:
	lineaEnZ = all( T[i][fila][columna]==turno for i in range(0, len(T)) )
	return lineaEnZ

def reflejarJugada(A: [[[int]]], tablero: int, fila: int, columna: int, turno: int):
	A[tablero][fila][columna] = turno


def hayLinea(T: [[[int]]], tablero: int, fila: int, columna: int, player: jugador):
	if hayLineaHorizontal(T, tablero, fila, player.turn):
		player.filas += 1
		print(player.nombre, " hiciste una linea horizontal.")
	if hayLineaVertical(T, tablero, columna, player.turn):
		player.columnas += 1
		print(player.nombre, " hiciste una linea vertical.")
	if hayLineaDiagonal(T, tablero, fila, columna, player.turn):
		player.diagonales += 1
		print(player.nombre, " hiciste una linea diagonal.")
	if hayLineaDiagonalInversa(T, tablero, fila, columna, player.turn):
		player.diagonales += 1
		print(player.nombre, " hiciste una linea diagonal.")
	if hayLineaEnZ(T, fila, columna, player.turn):
		player.enZ += 1
		print(player.nombre, " hiciste una linea en Z.")


def pedirJugada(player1: jugador, player2: jugador) -> (int, int, int):
	if player1.turn == turno:
		tablero = int(input(player1.nombre + " indique el tablero: "))
		fila = int(input(player1.nombre + " indique la fila: "))
		columna = int(input(player1.nombre + " indiquela columna: "))
	else:
		tablero = int(input(player2.nombre + " indique el tablero: "))
		fila = int(input(player2.nombre + " indique la fila: "))
		columna = int(input(player2.nombre + " indiquela columna: "))

	return tablero, fila, columna

player1 = jugador(N, "Amin", 1)
player2 = jugador(N, "Angel", 2)

while quedanFichas(T):
	tablero, fila, columna = pedirJugada(player1, player2)
	if esValida(T, tablero, fila, columna):
		reflejarJugada(T, tablero, fila, columna, turno)
		if turno==player1.turn:
			hayLinea(T, tablero, fila, columna, player1)
			turno = 3 - turno
		else:
			hayLinea(T, tablero, fila, columna, player2)
			turno = 3 - turno
	else:
		print("La jugada no es valida. Intente nuevamente.")

total1 = player1.filas + player1.columnas + player1.diagonales + player1.enZ
total2 = player2.filas + player2.columnas + player2.diagonales + player2.enZ
print("El jugador ", player1.nombre, " logro hacer ", total1, " lineas.")
print("El jugador ", player2.nombre, " logro hacer ", total2, " lineas.")
if total1>total2:
	print("Ha ganado ", player1.nombre)
elif total2>total1:
	print("Ha ganado ", player2.nombre)
else:
	print("Ha sido un empate.")

