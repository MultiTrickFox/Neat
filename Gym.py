import gym


t_max = 50

# installation instructions:
# https://becominghuman.ai/getting-mario-back-into-the-gym-setting-up-super-mario-bros-in-openais-gym-8e39a96c1e41


def test(topology):
    from numpy.random import randn
    return randn()


# env = gym.make('SuperMarioBros-1-1-v0')
# env = gym.make('gym_flappy_bird')
env = gym.make('CartPole-v0')

# print(env.action_space)
# print(env.observation_space)


def play_a_round(topology):

    state = env.reset()
    done = False
    t = 0

    while not done:

        env.render()

        # action = env.action_space.sample()  # choose random action
        # print(type(action))
        action = topology(state)[-1]

        state, reward, done, _ = env.step(action)  # feedback from environment

        t += 1
        done = t == t_max


# test.

# from Topology import Topology
# play_a_round(Topology())

env.close()

# g = Topology()
# mutate_add_connection(g)
#
# gc = Topology()
# mutate_add_connection(gc)
#
# g_child = crossover(g, gc)
#
# mutate_split_connection(g_child)
