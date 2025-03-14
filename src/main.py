import pygame
import sys
from cellular_parser import *
from cellular_automata import *

if __name__ == '__main__':
    # Little test
    if len(sys.argv) < 2:
        print("Error : Please provide path to cellular automaton file.")
        sys.exit(0)

    parsed = None
    with open(sys.argv[1]) as stream:
        parsed = parse(tokenize(stream.read()))

    a = parsed[0]
    c = parsed[1]

    center = c.leftmost

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True

    compteur = 0

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        left = center
        right = center
        i = 0
        while left != None or right != None:
            left_coord = 390 - 19 * i
            right_coord = 390 + 19 * i

            if left != None:
                if left.get_value().get_current_state() == State.Alive:
                    pygame.draw.rect(screen, "black", (left_coord, 295, 20, 20))    
                pygame.draw.rect(screen, "black" if i != 0 else "red", (left_coord, 295, 20, 20), 2)
                left = left.get_towards(Direction.Left)

            if right != None:
                if i != 0:
                    if right.get_value().get_current_state() == State.Alive:
                        pygame.draw.rect(screen, "black", (right_coord, 295, 20, 20))
                    pygame.draw.rect(screen, "black", (right_coord, 295, 20, 20), 2)

                right = right.get_towards(Direction.Right)
            i += 1

        pygame.display.flip()

        clock.tick(60)
        compteur = (compteur + 1)%5
        if compteur == 0:
            a.step(c)

    pygame.quit()