N = int(input("Ingresa la dimension del supertablero"))
T = [[[0 for i in range(0, N)] for j in range(0, N)] for k in range(0, N)]
tablero = 0
fila = 0
columna = 0
turno = 0

class jugador:
    def __init__(self):
    	self.filas = 0
    	self.columnas = 0
    	self.diagonales = 0
    	self.enZ = 0


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

def hayLineaDiagonal(T: [[int]], tablero: int , fila: int, columna: int, turno: int) -> bool:
	lineaDiagonal = False
	if fila == columna:
		lineaDiagonal = all( T[tablero][i][i]==turno for i in range(0, len(T)) )
	return lineaDiagonal
	
def hayLineaDiagonalInversa(T: [[int]], tablero: int , fila: int, columna: int, turno: int) -> bool:
def hayLineaEnZ(T: [[[int]]], fila: int, columna: int, turno: int) -> bool:

def hayLinea(T, N, jugador, fila, columna, tablero):
	if hayLineaHorizontal(T,Tablero,fila,jug):
		jugador.filas += 1
	if hayLineaVertical(T,Tablero,fila,jug):
		jugador.columnas += 1
	if fila == columna:
		if hayLineaDiagonal(T,Tablero,jug):
			jugador.diagonales += 1
	if fila + columna == N-1:
		if hayLineaDiagonalInversa(T,Tablero,jug):
			jugador.diagonales += 1
	if 


def pedirJugada():

if hayLinea():
sumarLineas()
