import gym
# import universe

from numpy import argmax
from scipy.special import expit as sigm, softmax
from numpy import tanh


t_max = 5_000

average_eps = 1


# installation instructions:
# https://becominghuman.ai/getting-mario-back-into-the-gym-setting-up-super-mario-bros-in-openais-gym-8e39a96c1e41


# env = gym.make('ChopperCommand-ram-v0')
env = gym.make('BipedalWalker-v2')

# print(env.observation_space)
# print(env.action_space)
#
# print(env.reset())
# print(env.action_space.sample())


def play_a_round(topology):

    for _ in range(average_eps):

        state = env.reset()
        done = False
        total_reward = 0
        t = 0

        while not done:

            # env.render()

            action = topology(state) # argmax(topology(state))

            # print(action) # TODO : remove

            state, reward, done, _ = env.step(action)  # feedback from environment

            total_reward += reward

            if done:
                env.reset()
            else:
                t += 1
                done = t == t_max

    return total_reward / average_eps


# env.close()

def play(topology):

    from time import sleep

    while 1:

        state = env.reset()

        done = False
        while not done:
            env.render()

            action = topology(state)

            state, reward, done, _ = env.step(action)

        sleep(5)


# g = Topology()
# mutate_add_connection(g)
#
# gc = Topology()
# mutate_add_connection(gc)
#
# g_child = crossover(g, gc)
#
# mutate_split_connection(g_child)
