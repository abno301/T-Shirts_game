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


def consensus_with_influence():
    agents = create_agents()
    consistency = [1] * NUM_AGENTS

    iteration_num = 0

    while True:
        iteration_num += 1
        color_changes = [False] * NUM_AGENTS

        for i, agent in enumerate(agents):
            other_idx = random.choice([j for j in range(NUM_AGENTS) if j != i])
            other_agent = agents[other_idx]

            influence = min(5, consistency[other_idx] / 5)

            if other_agent.color == "blue":
                agent.noOfBlue += 1 * influence
            else:
                agent.noOfRed += 1 * influence

        for i, agent in enumerate(agents):
            old_color = agent.color

            if agent.noOfRed > agent.noOfBlue:
                agent.color = "red"
            elif agent.noOfBlue > agent.noOfRed:
                agent.color = "blue"
            # If equal, keep current color

            # Reset counts for next round
            agent.noOfBlue = 0
            agent.noOfRed = 0

            # Track if color changed
            if old_color != agent.color:
                color_changes[i] = True
                consistency[i] = 1  # Reset consistency
            else:
                consistency[i] += 1  # Increase consistency

        # Check for consensus
        colors = set(agent.color for agent in agents)
        if len(colors) == 1:
            break

    return iteration_num


def consensus_with_network_effect():
    agents = create_agents()

    num_influencers = NUM_AGENTS // 10
    influencers = random.sample(range(NUM_AGENTS), num_influencers)

    iteration_num = 0

    while True:
        iteration_num += 1

        current_blue = sum(1 for agent in agents if agent.color == "blue")
        current_red = NUM_AGENTS - current_blue

        blue_bias = current_blue / NUM_AGENTS
        red_bias = current_red / NUM_AGENTS

        for i, agent in enumerate(agents):
            other_idx = random.choice([j for j in range(NUM_AGENTS) if j != i])
            other_agent = agents[other_idx]

            if other_agent.color == "blue":
                agent.noOfBlue += 1
            else:
                agent.noOfRed += 1

            if blue_bias > 0.6:  # If blue is becoming dominant
                agent.noOfBlue += blue_bias * 0.5
            if red_bias > 0.6:  # If red is becoming dominant
                agent.noOfRed += red_bias * 0.5

            if other_idx in influencers:
                if other_agent.color == "blue":
                    agent.noOfBlue += 1
                else:
                    agent.noOfRed += 1

        for agent in agents:
            if agent.noOfRed > agent.noOfBlue:
                agent.color = "red"
            elif agent.noOfBlue > agent.noOfRed:
                agent.color = "blue"

            agent.noOfBlue = 0
            agent.noOfRed = 0

        colors = set(agent.color for agent in agents)
        if len(colors) == 1:
            break

        if iteration_num > 50:
            current_blue = sum(1 for agent in agents if agent.color == "blue")
            current_red = NUM_AGENTS - current_blue

            majority_color = "blue" if current_blue > current_red else "red"
            if current_blue != current_red:  # Only if there's a clear majority
                conformists = random.sample(range(NUM_AGENTS), NUM_AGENTS // 20)
                for idx in conformists:
                    agents[idx].color = majority_color

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

    print("consensus_with_influence...")
    results_influence = []
    for i in range(NUM_SAMPLES):
        results_influence.append(consensus_with_influence())
    influence_mean = statistics.mean(results_influence)
    print(f"Average consensus reached at round: {influence_mean}")

    print("consensus_with_network_effect...")
    results_network = []
    for i in range(NUM_SAMPLES):
        results_network.append(consensus_with_network_effect())
    network_mean = statistics.mean(results_network)
    print(f"Average consensus reached at round: {network_mean}")

    # result visualisation
    labels = ['Consensus Learning', 'Consensus with Memory', 'Consensus with Influence', 'Network Effect']
    means = [consensus_learning_mean, memory_mean, influence_mean, network_mean]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, means, color=['skyblue', 'dodgerblue', 'royalblue', 'darkblue'])
    plt.ylabel('Average Rounds to Consensus')
    plt.title('Comparison of Consensus Strategies')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
