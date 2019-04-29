import pygame
from pygame.locals import *

key_to_function = {
    pygame.K_w:      (lambda x: x.moveInward(x.location)),
    pygame.K_s:      (lambda x: x.moveForward(x.location)),
    pygame.K_DOWN:   (lambda x: x.moveDOWN(x.location)),
    pygame.K_UP:     (lambda x: x.moveUP(x.location)),
    pygame.K_RIGHT:  (lambda x: x.moveRIGHT(x.location)),
    pygame.K_LEFT:   (lambda x: x.moveLEFT(x.location)),
    pygame.K_RETURN: (lambda x: x.chooseNode(x.location))  
}

N = 5
espacio_tablero = 

# declare our global variables for the game
XO   = "X"   # track whose turn it is; X goes first
grid = [ [ None, None, None ], \
         [ None, None, None ], \
         [ None, None, None ] ]

winner = None

# declare our support functions

def initBoard(ttt):
    # initialize the board and return it as a variable
    # ---------------------------------------------------------------
    # ttt : a properly initialized pyGame display variable

    # set up the background surface
    background = pygame.Surface (ttt.get_size())
    background = background.convert()
    background.fill ((250, 250, 250))

    pygame.draw.line (background, (0,0,0), (N*100/2,0), (N*100/2,100), 2)

    # draw the grid lines
    i = 0
    while i < N:
        # vertical lines...
        pygame.draw.line (background, (0,0,0), (i*100, 0+espacio_tablero), (i*100, N*100+espacio_tablero), 2)
        # horizontal lines...
        pygame.draw.line (background, (0,0,0), (0, i*100+espacio_tablero), (N*100, i*100+espacio_tablero), 2)
        i += 1

    # return the board
    return background

def drawStatus (board):
    # draw the status (i.e., player turn, etc) at the bottom of the board
    # ---------------------------------------------------------------
    # board : the initialized game board surface where the status will
    #         be drawn

    # gain access to global variables
    global XO, winner

    # determine the status message
    if (winner is None):
        message = XO + "'s turn"
    else:
        message = winner + " won!"
        
    # render the status message
    font = pygame.font.Font(None, 25)

    # copy the rendered message onto the board
    #board.fill ((250, 250, 250), (0, N*100, N*100, 100))              # (color, (0,x,y, FONDO SUP ))
    #board.blit(font.render(message, 1, (10, 10, 10)) , (10, N*100))   # (text, (FONDO  LATERAL, altura) )

    board.blit(font.render("Jugador 1: ", 1, (10, 10, 10)), (5, 0)) 
    board.blit(font.render("Lineas horizontales: ", 1, (10, 10, 10)), (5, 20)) 
    board.blit(font.render("Lineas Verticales: ", 1, (10, 10, 10)), (5, 40)) 
    board.blit(font.render("Lineas Diagonales: ", 1, (10, 10, 10)), (5, 60)) 
    board.blit(font.render("Lineas En Z: ", 1, (10, 10, 10)), (5, 80)) 

    board.blit(font.render("Jugador 2: ", 1, (10, 10, 10)), (N*100/2+20, 0)) 
    board.blit(font.render("Lineas horizontales: ", 1, (10, 10, 10)), (N*100/2+20, 20)) 
    board.blit(font.render("Lineas Verticales: ", 1, (10, 10, 10)), (N*100/2+20, 40)) 
    board.blit(font.render("Lineas Diagonales: ", 1, (10, 10, 10)), (N*100/2+20, 60)) 
    board.blit(font.render("Lineas En Z: ", 1, (10, 10, 10)), (N*100/2+20, 80))


def showBoard (ttt, board):
    # redraw the game board on the display
    # ---------------------------------------------------------------
    # ttt   : the initialized pyGame display
    # board : the game board surface

    drawStatus (board)
    ttt.blit (board, (0, 0))
    pygame.display.flip()


def graficarJugada(tablero, x, y, turno):
    centerX = 50 + y*100
    centerY =  50 + x*100 + espacio_tablero
    if turno == 1:
        pygame.draw.circle (board, (0,0,0), (centerX, centerY), 44, 2)
    else:
        pygame.draw.line (board, (0,0,0), (centerX - 22, centerY - 22), (centerX + 22, centerY + 22), 2)

        pygame.draw.line (board, (0,0,0), (centerX + 22, centerY - 22), (centerX - 22, centerY + 22), 2)

# -------------------------------------------------
# Funciones para seleccionar un vector

#def moveForward(self,location):
    

#def moveInward(self,location):
    

#def moveDOWN(self,location):
    

#def moveUP(self,location):
    

#def moveRIGHT(self,location):
    

#def moveLEFT(self,location):


# --------------------------------------------------------------------
# initialize pygame and our window
pygame.init()
ttt = pygame.display.set_mode ((N*100, N*100+espacio_tablero))
pygame.display.set_caption ('Tic-Tac-Toe')

# create the game board
board = initBoard (ttt)

# main event loop
running = 1

while (running == 1):
    for event in pygame.event.get():
        if event.type is QUIT:
            running = 0
            clickBoard(board)
        elif event.type == pygame.KEYDOWN:
            if event.key in key_to_function:
                key_to_function[event.key]

        graficarJugada(1, 0, 0,0)
        graficarJugada(1, 1, 1,1)
        graficarJugada(1, 1, 2,0)
        graficarJugada(1, 1, 3,1)
        graficarJugada(1, 1, 4,0)
        graficarJugada(1, 0, 4,1)

        # update the display
        showBoard (ttt, board)