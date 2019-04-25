N = int(input("Ingresa la dimension del supertablero"))
T = [[[0 for i in range(0, N)] for j in range(0, N)] for k in range(0, N)]
tablero = 0
fila = 0
columna = 0
turno = 0

class jugador:
    def __init__(self, turno, N):
    	self.filas = 0
    	self.columnas = 0
    	self.diagonales = 0
    	self.enZ = 0
    	self.turn = turno
	self.fichas = N//2


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
	if fila + columna == N-1:
		return all( T[tablero][i][N-1-i]==turno for i in range(0, len(T)) )
	else:
		return False

def hayLineaEnZ(T: [[[int]]], fila: int, columna: int, turno: int) -> bool:
	lineaEnZ = all( T[i][fila][columna]==turno for i in range(0, len(T)) )
	return lineaEnZ


def hayLinea(T: [[[int]]], tablero: int, fila: int, columna: int, player: jugador):
	if hayLineaHorizontal(T, tablero, fila, player.turn):
		jugador.filas += 1
	if hayLineaVertical(T, tablero, columna, player.turn):
		jugador.columnas += 1
	if hayLineaDiagonal(T, tablero, fila, columna, player.turn):
		jugador.diagonales += 1
	if hayLineaDiagonalInversa(T, tablero, fila, columna, player.turn):
		jugador.diagonales += 1
	if hayLineaEnZ(T, fila, columna, player.turn):
		jugador.enZ += 1


def pedirJugada():

if hayLinea():
	sumarLineas()


