N = int(input("Ingresa la dimension del supertablero"))
T = [[[0 for i in range(0, N)] for j in range(0, N)] for k in range(0, N)]
tableroActual = 0
fila = 0
columna = 0
turno = 0

def quedanFichas() -> bool:
	hayFichas = any( any( any(T[i][j][k]==0 for k in range(0, N)) for j in range(0, N)) for i in range(0, N) )
	return hayFichas

def esValida() -> bool:

def hayLineaHorizontal() -> bool:
def hayLineaVertical() -> bool:
def hayLineaDiagonal() -> bool:
def hayLineaEnZ() -> bool:

def hayLinea(): 

def pedirJugada():

if hayLinea():
	sumarLineas()


