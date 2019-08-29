import random
from easy21_environment import Game



env_states = list(range(0,22))
env_action_space = ["stick", "hit"]

q_dict = dict.fromkeys(env_states, 0)
for k in q_dict:
    q_dict[k] = dict.fromkeys(env_action_space, 0)

alpha = 0.3
epsilon = 1
gamma = 0.7
epsilon_decay = 0.99


episodes = 100
r_sum = 0
print(q_dict)
for i in range(episodes):
    game = Game()
    state, action, reward, done = 0, 'hit', 0, False

    while not done:

        if random.uniform(0, 1) < epsilon:
            new_action = random.choice(env_action_space)
        else:
            new_action = max(q_dict[state], key=q_dict[state].get)

        new_max = q_dict[state][new_action]

        state, action, reward, done = game.step(new_action)
        if state >= 0 and state <= 21:
            q_dict[state][action] = (1 - alpha) * q_dict[state][action] + alpha * (reward + gamma * new_max)

            if (1 - alpha) * q_dict[state][action] + alpha * (reward + gamma * new_max) > 0:
                print((1 - alpha) * q_dict[state][action] + alpha * (reward + gamma * new_max))
       # print(state, action, new_action)


        epsilon = max(0.1, epsilon * epsilon_decay)

    r_sum += reward
    #print("cuuu", reward)

print(r_sum/episodes)
print(q_dict)





