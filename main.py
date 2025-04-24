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


def consensus_with_multiple_observations(num_observations=3, stubbornness=0.2):
    agents = create_agents()
    iteration_num = 0

    while True:
        iteration_num += 1

        for agent in agents:
            others = random.sample([a for a in agents if a.id != agent.id],
                                   min(num_observations, NUM_AGENTS - 1))

            agent.noOfBlue = 0
            agent.noOfRed = 0

            for i, other in enumerate(others):
                weight = (num_observations - i) / num_observations
                if other.color == "blue":
                    agent.noOfBlue += weight
                else:
                    agent.noOfRed += weight

            if agent.color == "blue":
                agent.noOfBlue += stubbornness
            else:
                agent.noOfRed += stubbornness

        for agent in agents:
            if agent.noOfRed > agent.noOfBlue:
                agent.color = "red"
            elif agent.noOfBlue > agent.noOfRed:
                agent.color = "blue"
            # If equal, keep current color

        colors = set(agent.color for agent in agents)
        if len(colors) == 1:
            break

    return iteration_num


def main():
    print("consensus_with_color_count...")
    results_consensus_learning = []
    for i in range(NUM_SAMPLES):
        results_consensus_learning.append(consensus_with_color_count())
    consensus_learning_mean = statistics.mean(results_consensus_learning)
    print(f"Average consensus reached at round: {consensus_learning_mean}")

    print("consensus_with_memory...")
    results_consensus_with_memory = []
    for i in range(NUM_SAMPLES):
        results_consensus_with_memory.append(consensus_with_memory())
    memory_mean = statistics.mean(results_consensus_with_memory)
    print(f"Average consensus reached at round: {memory_mean}")

    print("consensus_with_multiple_observations...")
    results_multiple_observations = []
    for i in range(NUM_SAMPLES):
        results_multiple_observations.append(consensus_with_multiple_observations())
    multiple_obs_mean = statistics.mean(results_multiple_observations)
    print(f"Average consensus reached at round: {multiple_obs_mean}")

    labels = ['Consensus Learning', 'Consensus with Memory', 'Multiple Observations']
    means = [consensus_learning_mean, memory_mean, multiple_obs_mean]

    plt.bar(labels, means, color=['skyblue', 'dodgerblue', 'royalblue'])
    plt.ylabel('Average Rounds to Consensus')
    plt.title('Comparison of Consensus Strategies')
    plt.tight_layout()
    plt.show()



if __name__ == '__main__':
    main()
