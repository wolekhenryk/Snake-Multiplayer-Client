import pygame
import socket
import sys
from components.constant import *


def init_pygame():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    return win


def draw_board(board, win):
    win.fill(WHITE)
    cell_width = WIDTH // len(board[0])
    cell_height = HEIGHT // len(board)
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            color = BLACK  # Default color
            if cell == 'G':
                color = GREEN
            elif cell == 'Y':
                color = YELLOW
            elif cell == 'P':
                color = PINK
            elif cell == 'B':
                color = BLUE
            elif cell == 'F':
                color = RED
           
            elif cell == 'E':
                color = ECRU
            elif cell == 'S':
                color = SALMON
            elif cell == 'V':
                color = VIOLET
            elif cell == 'T':
                color = TEAL
            elif cell == 'O':
                color = ORANGE          
            elif cell == 'C':
                color = CYAN
            elif cell == 'M':
                color = MAGENTA
           

            pygame.draw.rect(win, color, (j * cell_width, i * cell_height, cell_width, cell_height))
    pygame.display.update()


def main():
    win = init_pygame()

    # Try to establish a connection with the game server
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
        client_socket.connect((SERVER, PORT)) #connecting to server (IP) on specific port
        client_socket.settimeout(0.3)  # Set a short timeout for socket operations

        #receive board parameters from server
        size_data = client_socket.recv(4)
        board_size = int.from_bytes(size_data, byteorder='big')
        board_mem = board_size ** 2

    except Exception as e:
        # Handle exceptions during connection by quitting pygame and exiting
        print("Error connecting to server:", e)
        pygame.quit()
        sys.exit()

    # Game loop: handles game updates and user inputs
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    client_socket.send(b'U')
                elif event.key == pygame.K_DOWN:
                    client_socket.send(b'D')
                elif event.key == pygame.K_LEFT:
                    client_socket.send(b'L')
                elif event.key == pygame.K_RIGHT:
                    client_socket.send(b'R')


        try:
            data = client_socket.recv(board_mem) #receive board from server
            if data:
                decoded_data = data.decode('utf-8')
                board = [list(decoded_data[i:i + board_size]) for i in range(0, len(decoded_data), board_size)]
                draw_board(board, win)

        except socket.timeout:
            print("Socket timeout")
            break
        except Exception as e:
            print("Error receiving data:", e)
            break

        # Limit the frame rate to 60 frames per second
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
