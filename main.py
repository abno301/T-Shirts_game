import random

from agent import Agent
import statistics
import matplotlib.pyplot as plt

NUM_AGENTS = 100
NUM_SAMPLES = 100


def create_agents():
    return [Agent(i) for i in range(NUM_AGENTS)]


def consensus_with_color_count():
    # create 100 agents
    agents = create_agents()
    iteration_num = 0
    comparison_count = 0
    while True:
        iteration_num += 1
        for agent in agents:
            other_agent = random.sample(agents, k=1)[0]
            if other_agent.id != agent:
                agent.observe_color(other_agent.color)
                comparison_count += 1

        for agent in agents:
            agent.update_color()

        colors = set(agent.color for agent in agents)
        if len(colors) == 1:
            # print(f"Consensus reached at round {iteration_num}: {colors.pop()}")
            break
    return iteration_num


def consensus_with_memory(memory_size=5):
    agents = create_agents()
    for agent in agents:
        agent.memory = []

    iteration_num = 0

    while True:
        iteration_num += 1

        for agent in agents:
            other_agent = random.choice([a for a in agents if a.id != agent.id])

            agent.memory.append(other_agent.color)

        if iteration_num % 5 == 0:
            for agent in agents:
                red_count = agent.memory.count("red")
                blue_count = agent.memory.count("blue")

                if red_count > blue_count:
                    agent.color = "red"
                elif blue_count > red_count:
                    agent.color = "blue"

        colors = set(agent.color for agent in agents)
        if len(colors) == 1:
            # print(f"Consensus reached at round {iteration_num}: {colors.pop()}")
            break

    return iteration_num


def main():
    print("consensus_with_color_count...")
    results_consensus_learning = []
    for i in range(NUM_SAMPLES):
        results_consensus_learning.append(consensus_with_color_count())
    consensus_learning_mean = statistics.mean(results_consensus_learning)

    print(f"Average consensus reached at round: {consensus_learning_mean}")

    print("consensus_with_color_count...")
    results_consensus_with_memory = []
    for i in range(NUM_SAMPLES):
        results_consensus_with_memory.append(consensus_with_memory())
    results_mean = statistics.mean(results_consensus_with_memory)

    print(f"Average consensus reached at round: {results_mean}")

    # result visualisation
    labels = ['Consensus Learning', 'Consensus with Memory']
    means = [consensus_learning_mean, results_mean]

    plt.bar(labels, means, color=['skyblue', 'dodgerblue'])
    plt.ylabel('Average Rounds to Consensus')
    plt.title('Comparison of Consensus Strategies')

    plt.show()


if __name__ == '__main__':
    main()
