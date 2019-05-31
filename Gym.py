import gym

from math import exp

def sigm(x):
    return 1 / (1 + exp(-x))


t_max = 199


# # env = gym.make('gym_flappy_bird')
# env = gym.make('SuperMarioBros-1-1-v0')
# installation instructions:
# https://becominghuman.ai/getting-mario-back-into-the-gym-setting-up-super-mario-bros-in-openais-gym-8e39a96c1e41


env = gym.make('CartPole-v0')

# print(env.action_space)
# print(env.observation_space)


def play_a_round(topology):

    state = env.reset()
    done = False
    total_reward = 0
    t = 0

    while not done:

        env.render()

        action = int(round(sigm(topology(state)[-1])))

        state, reward, done, _ = env.step(action)  # feedback from environment

        total_reward += reward

        if done:
            env.reset()
        else:
            t += 1
            done = t == t_max

    return total_reward


# env.close()

def play(topology):

    state = env.reset()

    while 1:
        env.render()

        action = int(round(sigm(topology(state)[-1])))

        state, reward, done, _ = env.step(action)


# g = Topology()
# mutate_add_connection(g)
#
# gc = Topology()
# mutate_add_connection(gc)
#
# g_child = crossover(g, gc)
#
# mutate_split_connection(g_child)
