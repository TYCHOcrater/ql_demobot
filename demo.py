__author__ = 'igor'
import World
import threading
import time
import random


#initial values
discount = 0.3 #discount
actions = World.actions #actions
states = [] #states
Q = {} #policies / rewards

#def world
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0.1
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)

#val functions

def max_Q(s):
    best_q = None
    best_a = None

    for a,q in Q[s].items():
        if best_q is None or (q > best_q): #for every action and q value, if val is 0 or q is higher, assign current a,q

            best_q = q
            best_a = a

    options = [x for x in Q[s].items() if x[1] == best_q] #how many options do we have?

    if len(options) > 1:
        best_a,best_q = options[random.randrange(0,len(options))]

    if best_q < 0.1:
        best_a, best_q = Q[s].items()[random.randrange(0,len(Q[s].items()))]

    return best_a, best_q

def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc #add the incoming value of the alpha * action

    World.set_cell_score(s, a, Q[s][a])

def do_action(action):
    s = World.player
    r = -World.score
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    return s, action, r, s2

def run():
    global discount
    time.sleep(1)
    alpha = 1
    beta = None
    t = 1

    stuck = 0
    old_s = (0,0)
    while True:
        s = World.player #starting position

        if s == old_s: #stuck check
            stuck += 1


        max_act,max_val = max_Q(s) #find the next highesst Q from position x
        (s, a, r, s2) = do_action(max_act)

        epsilon = pow(t, -0.005)
        alpha = pow(t, -0.25)
        beta = r + discount * max_val
        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, beta)

        # Check if the game has restarted
        t += 1.0

        old_s = s
        print("Moves {} | Score {}".format(t, round(World.score,2)))


        if World.has_restarted() or (t>100) or (stuck>10):
            World.restart_game()
            time.sleep(0.01)
            t = 1.0
            stuck = 0

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.01)


t = threading.Thread(target=run)
t.daemon = True
t.start()

World.start_game()

