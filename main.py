import random
from agent import Agent
import statistics

NUM_AGENTS = 100

def create_agents():
    return [Agent(i) for i in range(NUM_AGENTS)]


def run_consensus_learning():
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


def main():
    print("Analyzing...")
    results_consensus_learning = []
    for i in range(10000):
        results_consensus_learning.append(run_consensus_learning())
    consensus_learning_mean = statistics.mean(results_consensus_learning)

    print(f"Average consensus reached at round: {consensus_learning_mean}")

if __name__ == '__main__':
    main()
