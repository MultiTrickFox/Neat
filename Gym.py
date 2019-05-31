import gym


# installation instructions:
# https://becominghuman.ai/getting-mario-back-into-the-gym-setting-up-super-mario-bros-in-openais-gym-8e39a96c1e41

def test(topology):
    from numpy.random import randn
    return randn()


'gym_flappy_bird'
env = gym.make('SuperMarioBros-1-1-v0')
# env = gym.make('gym_flappy_bird')


def play_a_round(topology):

    state = env.reset()
    done = False
    t = 0

    while not done:

        action = env.action_space.sample()  # choose random action
        # TODO : action = topology(state)

        state, reward, done, info = env.step(action)  # feedback from environment

        t += 1
        print(info)
        if t % 10 == 0: done = True
        # if not t % 100:
        #     print(t, info)





# g = Topology()
# mutate_add_connection(g)
#
# gc = Topology()
# mutate_add_connection(gc)
#
# g_child = crossover(g, gc)
#
# mutate_split_connection(g_child)
