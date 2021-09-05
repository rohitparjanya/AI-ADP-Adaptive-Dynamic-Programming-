import numpy as np
import random
import pygame
import keyboard
import time

# drawing the GRID
def drawGrid():
    blockSize = 50  # Set the size of the grid block
    for x in range(1, 9):
        for y in range(1, 9):
            rect = pygame.Rect(x * blockSize, y * blockSize,
                               blockSize, blockSize)
            pygame.draw.rect(screen, WHITE, rect, 1)

    screen.blit(GreenImg, (1 * blockSize, 8 * blockSize))
    screen.blit(GreenImg, (6 * blockSize, 2 * blockSize))
    screen.blit(GreenImg, (7 * blockSize, 4 * blockSize))
    screen.blit(powImg, (5 * blockSize, 8 * blockSize))
    screen.blit(restartImg, (4 * blockSize, 1 * blockSize))
    screen.blit(restartImg, (4 * blockSize, 7 * blockSize))
    # start state
    screen.blit(startImg, (1 * blockSize, 0 * blockSize))
    # --walls
    screen.blit(wallImg, (2 * blockSize, 5 * blockSize))
    screen.blit(wallImg, (2 * blockSize, 7 * blockSize))
    screen.blit(wallImg, (2 * blockSize, 8 * blockSize))
    screen.blit(wallImg, (3 * blockSize, 2 * blockSize))
    screen.blit(wallImg, (3 * blockSize, 3 * blockSize))
    screen.blit(wallImg, (3 * blockSize, 5 * blockSize))
    screen.blit(wallImg, (4 * blockSize, 5 * blockSize))
    screen.blit(wallImg, (5 * blockSize, 3 * blockSize))
    screen.blit(wallImg, (5 * blockSize, 6 * blockSize))
    screen.blit(wallImg, (5 * blockSize, 7 * blockSize))
    screen.blit(wallImg, (6 * blockSize, 3 * blockSize))
    screen.blit(wallImg, (5 * blockSize, 5 * blockSize))
    screen.blit(wallImg, (7 * blockSize, 3 * blockSize))
    screen.blit(wallImg, (7 * blockSize, 5 * blockSize))
    screen.blit(wallImg, (7 * blockSize, 6 * blockSize))
    screen.blit(wallImg, (8 * blockSize, 3 * blockSize))
    myfont = pygame.font.SysFont(' ', 35)
    myfont3 = pygame.font.SysFont(' ', 15)
    textsurface = myfont.render('--ROWS--', True, (255,255,0))
    textsurface3 = myfont3.render('PLEASE PRESS ENTER KEY, ONCE THE SCREEN STABLIZES', True, (0,0,255))
    screen.blit(textsurface, (250,10))
    screen.blit(textsurface3, (110, 40))

    myfont2 = pygame.font.SysFont(' ', 35)
    textsurface2 = myfont2.render('--COlUMS--', True, (255, 255, 0))
    textsurface2 = pygame.transform.rotate(textsurface2, 90)
    screen.blit(textsurface2, (10, 250))

# reinitialize for simulation purposess
def Rein():
    screen.fill((0, 0, 0))
    drawGrid()
    Goal(GOAL[0] * blockSize, GOAL[1] * blockSize)

#draw agent movement
def tik(x, y):
    screen.blit(agentImg1, (x*blockSize, y*blockSize))
    pygame.display.flip()

#local search algorithm
def draw_finalpath(V, actions):
    s=(1,1)
    d=[]
    l=[]
    r=[]
    u=[ ]
    t1=0
    t2=0
    t3=0
    t4=0
    final = [s]

    while True:

        if s == GOAL:
            break

        for a in actions[s]:
            if a == 'D':
                d= [s[0] - 1, s[1]]
                t1=V[tuple(d)]

            if a == 'U':
                u = [s[0] + 1, s[1]]
                t2=V[tuple(u)]

            if a == 'L':
                l = [s[0], s[1] - 1]
                t3=V[tuple(l)]

            if a == 'R':
                r = [s[0], s[1] + 1]
                t4=V[tuple(r)]

        temp=[(t1,d),(t2,u),(t3,l),(t4,r)]
        rs=max(temp)
        current=tuple(rs[1])

        if current not in final:

            if (current[0] == 4 and current[1] == 1) or (current[0] == 4 and current[1] == 7):

                s = (1,1)
                final.append(current)
                final.append(s)


            elif (current[0] == 6 and current[1] == 2) or (current[0] == 1 and current[1] == 8) or (current[0] == 7 and current[1] == 4):

                s = (5, 8)
                final.append(current)
                final.append(s)

            else:
                final.append(current)
                s = current
        else:
            temp.remove(rs)
            rs = max(temp)
            s = tuple(rs[1])
    print("THE GOAL STATE IS :: ",GOAL)
    print("THE COMPLETE PATH TRAVELLED BY THE AGENT :: ",final)
    print("TOTAL COST OF THE PATH IS :: ",len(final))
    for i in final:
        tik(i[0],i[1])
        time.sleep(0.1)


#draw agent
def agent(x, y):
    screen.blit(agentImg, (x, y))
    pygame.display.flip()

#draw GOAL
def Goal(x, y):
    screen.blit(GoalImg, (x, y))




# complete learning happens here
def ActualRL():
    # Hyperparameters
    # SMALL_ENOUGH = 0.9
    GAMMA = 0.9
    NOISE = 0.1

    # Define all states
    all_states = []
    for i in range(1, 9):
        for j in range(1, 9):
            all_states.append((i, j))

    # Define rewards for all states
    rewards = {}
    for i in all_states:
        if i == (4, 1):
            rewards[i] = -80
        elif i == (4, 7):
            rewards[i] = -80
        # power position
        elif i == (5, 8):
            rewards[i] = 80
        # green positions
        elif i == (1, 8):
            rewards[i] = 50
        elif i == (6, 2):
            rewards[i] = 50
        elif i == (7, 3):
            rewards[i] =50
        elif i == (GOAL[0], GOAL[1]):
            rewards[i] = 100
        else:
            rewards[i] = 0

    # Dictionary of possible actions. We have two "end" states (1,2 and 2,2)
    actions = {
        (1, 1): ('U', 'R'),
        (1, 2): ('R', 'L', 'U'),
        (1, 3): ('R', 'L', 'U'),
        (1, 4): ('R', 'L', 'U'),
        (1, 5): ('R', 'L'),
        (1, 6): ('R', 'L', 'U'),
        (1, 7): ('R', 'L'),
        (1, 8): ('L', ' '),
        (2, 1): ('D', 'R', 'U'),
        (2, 2): ('D', 'R', 'L'),
        (2, 3): ('D', 'R', 'L'),
        (2, 4): ('D', 'L', 'U'),
        # (2, 5):('D', 'R', 'L', 'U'),
        (2, 6): ('D', 'U'),
        # (2, 7):('D', 'R', 'L', 'U'),
        # (2, 8):('D', 'R', 'L', 'U'),
        (3, 1): ('D', 'U'),
        # (3, 2):('D', 'R', 'L', 'U'),
        # (3, 3):('D', 'R', 'L', 'U'),
        (3, 4): ('D', 'U'),
        # (3, 5):('D', 'R', 'L', 'U'),
        (3, 6): ('D', 'R', 'U'),
        (3, 7): ('R', 'L', 'U'),
        (3, 8): ('L', 'U'),
        (4, 1): ('D', 'R', 'U'),
        (4, 2): ('R', 'L', 'U'),
        (4, 3): ('R', 'L'),
        (4, 4): ('D', 'L', 'U'),
        # (4, 5):('D', 'R', 'L', 'U'),
        (4, 6): ('D', 'R'),
        (4, 7): ('D', 'R', 'L'),
        (4, 8): ('D', 'L', 'U'),
        (5, 1): ('D', 'R', 'U'),
        (5, 2): ('D', 'L', 'U'),
        # (5, 3):('D', 'R', 'L', 'U'),
        (5, 4): ('D', 'U'),
        # (5, 5):('D', 'R', 'L', 'U'),
        # (5, 6):('D', 'R', 'L', 'U'),
        # (5, 7):('D', 'R', 'L', 'U'),
        (5, 8): ('D', 'U'),
        (6, 1): ('D', 'R', 'U'),
        (6, 2): ('D', 'L', 'U'),
        # (6, 3):('D', 'R', 'L', 'U'),
        (6, 4): ('D', 'R', 'U'),
        (6, 5): ('R', 'L'),
        (6, 6): ('R', 'L'),
        (6, 7): ('R', 'L', 'U'),
        (6, 8): ('D', 'L', 'U'),
        (7, 1): ('D', 'R', 'U'),
        (7, 2): ('D', 'L', 'U'),
        # (7, 3):('D', 'R', 'L', 'U'),
        (7, 4): ('D', 'U'),
        # (7, 5):('D', 'R', 'L', 'U'),
        # (7, 6):('D', 'R', 'L', 'U'),
        (7, 7): ('D', 'R', 'U'),
        (7, 8): ('D', 'L', 'U'),
        (8, 1): ('D', 'R'),
        (8, 2): ('D', 'L'),
        # (8, 3):('D', 'R', 'L', 'U'),
        (8, 4): ('D', 'R'),
        (8, 5): ('R', 'L'),
        (8, 6): ('R', 'L'),
        (8, 7): ('D', 'R', 'L'),
        (8, 8): ('D', 'L'),

    }

    # Define an initial policy
    policy = {}
    for s in actions.keys():
        policy[s] = np.random.choice(actions[s])

    # Define initial value function
    V = {}
    for s in all_states:
        if s in actions.keys():
            V[s] = 0
        if s == (4, 1):
            V[s] = -5
        if s == (4, 7):
            V[s] = -5
        if s == (1, 8):
            V[s] = 0.5
        if s == (6, 2):
            V[s] = 0.5
        if s == (7, 4):
            V[s] = 0.5
        if s == (GOAL[0], GOAL[1]):
            V[s] = 1

    '''==================================================
                        Value Iteration
    =================================================='''

    iteration = 0
    while True:
        biggest_change = 0
        for s in all_states:

            if s in policy:

                old_v = V[s]
                new_v = 0

                for a in actions[s]:
                    if a == 'D':
                        nxt = [s[0] - 1, s[1]]
                    if a == 'U':
                        nxt = [s[0] + 1, s[1]]
                    if a == 'L':
                        nxt = [s[0], s[1] - 1]
                    if a == 'R':
                        nxt = [s[0], s[1] + 1]

                    # Choose a new random action to do (transition probability)
                    random_1 = np.random.choice([i for i in actions[s] if i != a])
                    if random_1 == 'D':
                        if (s[0] == 4 and s[1] == 1) or (s[0] == 4 and s[1] == 7):
                            print("---Restaring states--")
                            act = [1, 1]
                            print("from state", s, " visiting", tuple(act))
                            print("----------------")

                        elif (s[0] == 6 and s[1] == 2) or (s[0] == 1 and s[1] == 8) or (s[0] == 7 and s[1] == 4):
                            print("---Goto power states--")
                            act = [5, 8]
                            print("from state", s, " visiting", tuple(act))
                            print("----------------")
                        else:
                            act = [s[0] - 1, s[1]]
                            agent(act[0] * blockSize, act[1] * blockSize)
                            print("from state", s, " action to", tuple(act))

                    if random_1 == 'U':
                        if (s[0] == 4 and s[1] == 1) or (s[0] == 4 and s[1] == 7):
                            print("---Restaring states--")
                            act = [1, 1]
                            print("from state", s, " visiting", tuple(act))
                            print("----------------")

                        elif (s[0] == 6 and s[1] == 2) or (s[0] == 1 and s[1] == 8) or (s[0] == 7 and s[1] == 4):
                            print("---Goto power states--")
                            act = [5, 8]
                            print("from state", s, " visiting", tuple(act))
                            print("----------------")
                        else:
                            act = [s[0] + 1, s[1]]
                            agent(act[0] * blockSize, act[1] * blockSize)
                            print("from state", s, " action to", tuple(act))

                    if random_1 == 'L':
                        if (s[0] == 4 and s[1] == 1) or (s[0] == 4 and s[1] == 7):
                            print("---Restaring states--")
                            act = [1, 1]
                            print("from state", s, " visiting", tuple(act))
                            print("----------------")

                        elif (s[0] == 6 and s[1] == 2) or (s[0] == 1 and s[1] == 8) or (s[0] == 7 and s[1] == 4):
                            print("---Goto power states--")
                            act = [5, 8]
                            print("from state", s, " visiting", tuple(act))
                            print("----------------")
                        else:
                            act = [s[0], s[1] - 1]
                            agent(act[0] * blockSize, act[1] * blockSize)
                            print("from state", s, " action to", tuple(act))

                    if random_1 == 'R':
                        if (s[0] == 4 and s[1] == 1) or (s[0] == 4 and s[1] == 7):
                            print("---Restaring states--")
                            act = [1, 1]
                            print("from state", s, " visiting", tuple(act))
                            print("----------------")

                        elif (s[0] == 6 and s[1] == 2) or (s[0] == 1 and s[1] == 8) or (s[0] == 7 and s[1] == 4):
                            print("---Goto power states--")
                            act = [5, 8]
                            print("from state", s, " visiting", tuple(act))
                            print("----------------")
                        else:
                            act = [s[0], s[1] + 1]
                            agent(act[0] * blockSize, act[1] * blockSize)
                            print("from state", s, " action to", tuple(act))

                    if random_1 == ' ':
                        if (s[0] == 4 and s[1] == 1) or (s[0] == 4 and s[1] == 7):
                            print("---Restaring states--")
                            act = [1, 1]
                            print("from state", s, " visiting", tuple(act))
                            print("----------------")

                        elif (s[0] == 6 and s[1] == 2) or (s[0] == 1 and s[1] == 8) or (s[0] == 7 and s[1] == 4):
                            print("---Goto power states--")
                            act = [5, 8]
                            print("from state", s, " visiting", tuple(act))
                            print("----------------")
                        else:
                            act = [s[0], s[1] - 1]
                            agent(act[0] * blockSize, act[1] * blockSize)
                            print("from state", s, " action to", tuple(act))

                    # Calculate the value
                    nxt = tuple(nxt)
                    act = tuple(act)

                    v = rewards[s] + (GAMMA * ((1 - NOISE) * V[nxt] + (NOISE * V[act])))
                    if v > new_v:  # Is this the best action so far? If so, keep it
                        new_v = v
                        policy[s] = a

                # Save the best of all actions for the state
                V[s] = float(new_v)
                biggest_change = max(biggest_change, np.abs(old_v - V[s]))

        # See if the loop should stop now -->biggest_change < SMALL_ENOUGH
        if iteration == 100:
            pygame.display.flip()
            print("-------------------HASH MAP FOR STORAGE OF UTILITIES AT ITERATION--", iteration)
            for k, v in V.items():
                print("STATE: ",k, "   ::   UTILITY :", v)
            print("-------------------HASH MAP FOR POLICY-------------------------")
            for k,v in policy.items():
                print("STATE: ", k, "   ::   ACTION :", v)
            return V,actions

        Rein()
        print("\n")
        print("ITERATION NO:", iteration, "\n")
        print("HASH MAP FOR STORAGE OF UTILITIES AT ITERATION", iteration)
        for k, v in V.items():
            print(k, "   :   ", v)
        iteration += 1






if __name__ == "__main__":

    pygame.init()

    WHITE = (255, 255, 255)
    blockSize = 50
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("R-L")
   #loading IMAGES
    agentImg = pygame.image.load('robot.png')
    agentImg1 = pygame.image.load('robot1.png')
    GoalImg = pygame.image.load('goal.png')
    powImg = pygame.image.load('power.png')
    restartImg = pygame.image.load('restart.png')
    GreenImg = pygame.image.load('green.png')
    startImg = pygame.image.load('down-arrow.png')
    wallImg = pygame.image.load('mansory.png')
    IMG = pygame.image.load('IMG.png')

    running = True
    while running:
        screen.fill((0, 0, 0))
        drawGrid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if keyboard.is_pressed(' '):                       #on press of "SPACE BAR"
                # random goal state
                goal_states = [(6, 5), (6, 6), (7, 7), (7, 8), (6, 7),(8,8),(6,8)]
                GOAL = random.choice(goal_states)
                print("current goal co-ordinates", GOAL)
                Goal(GOAL[0] * blockSize, GOAL[1] * blockSize)
                print("starting RL...")
                V,actions=ActualRL()


            if keyboard.is_pressed('\n'):                          # on press of ENTER KEY
                Goal(GOAL[0] * blockSize, GOAL[1] * blockSize)
                draw_finalpath(V, actions)


