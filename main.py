import random

from agent import Agent

# simulation params
NUM_AGENTS = 100
NUM_ROUNDS = 50

if __name__ == '__main__':
    agents = [Agent(i) for i in range(NUM_AGENTS)]
    print(agents)

    for _ in range(NUM_ROUNDS):
        random.shuffle(agents) # za random pare

        # vsak agent interacta z enim drugim agentom
        for i in range(0, NUM_AGENTS, 2):
            a, b = agents[i], agents[i + 1]
            a.observe_color(b.color)
            b.observe_color(a.color)

        for agent in agents:
            agent.update_color()

    print(agents)
