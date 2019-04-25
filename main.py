N = int(input("Ingresa la dimension del supertablero"))
T = [[[0 for i in range(0, N)] for j in range(0, N)] for k in range(0, N)]
tablero = 0
fila = 0
columna = 0
turno = 0

def quedanFichas() -> bool:
	hayFichas = any( any( any(T[i][j][k]==0 for k in range(0, N)) for j in range(0, N)) for i in range(0, N) )
	return hayFichas

def esValida() -> bool:

def hayLineaHorizontal(T,Tablero,fila,jug) -> bool:
def hayLineaVertical(T,Tablero,columna,jug) -> bool:
def hayLineaDiagonal(T,Tablero,jug) -> bool:
def hayLineaDiagonalInversa(T,Tablero,jug) -> bool:
def hayLineaEnZ() -> bool:

def hayLinea():
	if hayLineaHorizontal()


def pedirJugada():

if hayLinea():
sumarLineas()
