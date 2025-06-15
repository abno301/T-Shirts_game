import random

from agent import Agent
import statistics
import matplotlib.pyplot as plt
import pandas as pd

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


def calculate_metrics(results_list, method_name):
    """Calculate multiple metrics for the given consensus results"""
    mean = statistics.mean(results_list)
    std_dev = statistics.stdev(results_list)
    efficiency = mean + (std_dev / 2)

    # Additional metrics
    median = statistics.median(results_list)
    min_rounds = min(results_list)
    max_rounds = max(results_list)
    interquartile_range = statistics.quantiles(results_list)[2] - statistics.quantiles(results_list)[0]
    reliability = 1 / (std_dev + 1)  # Higher is better
    convergence_speed = 100 / mean  # Higher is better
    stability = 1 / interquartile_range if interquartile_range > 0 else float('inf')
    worst_case_performance = max_rounds / mean  # Lower is better

    return {
        'Algorithm': method_name,
        'Mean Rounds': mean,
        'Median Rounds': median,
        'Std Dev': std_dev,
        'Min Rounds': min_rounds,
        'Max Rounds': max_rounds,
        'IQR': interquartile_range,
        'Efficiency Score': efficiency,
        'Reliability Score': reliability,
        'Convergence Speed': convergence_speed,
        'Stability Score': stability,
        'Worst Case Factor': worst_case_performance
    }


def main():
    # Run simulations and collect results
    print("Running simulations...")
    methods = [
        ('Consensus Learning', consensus_with_color_count),
        ('Consensus with Memory', consensus_with_memory),
        ('Consensus with Influence', consensus_with_influence),
        ('Network Effect', consensus_with_network_effect)
    ]

    all_results = {}
    metrics_list = []

    for name, method in methods:
        print(f"Running {name}...")
        results = [method() for _ in range(NUM_SAMPLES)]
        all_results[name] = results
        metrics = calculate_metrics(results, name)
        metrics_list.append(metrics)

        # Print basic stats
        print(f"Average: {metrics['Mean Rounds']:.2f}, StdDev: {metrics['Std Dev']:.2f}, "
              f"Efficiency Score: {metrics['Efficiency Score']:.2f}")

    # Create DataFrame for all metrics
    metrics_df = pd.DataFrame(metrics_list)

    # Visualization
    fig, axes = plt.subplots(3, 2, figsize=(15, 15))
    labels = [m['Algorithm'] for m in metrics_list]
    colors = ['skyblue', 'dodgerblue', 'royalblue', 'darkblue']

    # 1. Mean with error bars (std dev)
    axes[0, 0].bar(labels, metrics_df['Mean Rounds'], yerr=metrics_df['Std Dev'],
                   capsize=7, color=colors)
    axes[0, 0].set_ylabel('Rounds to Consensus')
    axes[0, 0].set_title('Mean Rounds with Std Dev')

    # 2. Box plots for distribution
    boxplot_data = [all_results[name] for name in labels]
    axes[0, 1].boxplot(boxplot_data, labels=labels)
    axes[0, 1].set_ylabel('Rounds to Consensus')
    axes[0, 1].set_title('Distribution of Consensus Rounds')

    # 3. Efficiency score
    axes[1, 0].bar(labels, metrics_df['Efficiency Score'], color=colors)
    axes[1, 0].set_ylabel('Score (lower is better)')
    axes[1, 0].set_title('Efficiency Score')
    for i, v in enumerate(metrics_df['Efficiency Score']):
        axes[1, 0].text(i, v + 0.5, f"{v:.1f}", ha='center')

    # 4. Reliability score
    axes[1, 1].bar(labels, metrics_df['Reliability Score'], color=colors)
    axes[1, 1].set_ylabel('Score (higher is better)')
    axes[1, 1].set_title('Reliability Score')
    for i, v in enumerate(metrics_df['Reliability Score']):
        axes[1, 1].text(i, v + 0.05, f"{v:.2f}", ha='center')

    # 5. Convergence speed
    axes[2, 0].bar(labels, metrics_df['Convergence Speed'], color=colors)
    axes[2, 0].set_ylabel('Speed (higher is better)')
    axes[2, 0].set_title('Convergence Speed')
    for i, v in enumerate(metrics_df['Convergence Speed']):
        axes[2, 0].text(i, v + 0.5, f"{v:.1f}", ha='center')

    # 6. Worst case factor
    axes[2, 1].bar(labels, metrics_df['Worst Case Factor'], color=colors)
    axes[2, 1].set_ylabel('Factor (lower is better)')
    axes[2, 1].set_title('Worst Case Factor')
    for i, v in enumerate(metrics_df['Worst Case Factor']):
        axes[2, 1].text(i, v + 0.1, f"{v:.1f}", ha='center')

    plt.tight_layout()
    plt.savefig('consensus_comprehensive_comparison.png')
    plt.show()

    # Create a normalized radar chart for multi-dimensional comparison
    import numpy as np
    metrics_to_plot = ['Efficiency Score', 'Reliability Score', 'Convergence Speed',
                       'Stability Score', 'Worst Case Factor']

    # Normalize metrics (invert some so higher is always better)
    normalized_metrics = metrics_df.copy()
    for metric in metrics_to_plot:
        if metric in ['Efficiency Score', 'Worst Case Factor']:
            # Lower is better, so invert
            max_val = max(normalized_metrics[metric])
            normalized_metrics[metric] = [max_val / val if val != 0 else 0 for val in normalized_metrics[metric]]
        else:
            # Higher is better, normalize to 0-1
            max_val = max(normalized_metrics[metric])
            normalized_metrics[metric] = [val / max_val if max_val != 0 else 0 for val in normalized_metrics[metric]]

    # Radar chart
    angles = np.linspace(0, 2 * np.pi, len(metrics_to_plot), endpoint=False).tolist()
    angles += angles[:1]  # Close the loop

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    for i, (name, color) in enumerate(zip(labels, colors)):
        values = normalized_metrics.iloc[i][metrics_to_plot].tolist()
        values += values[:1]  # Close the loop
        ax.plot(angles, values, color=color, linewidth=2, label=name)
        ax.fill(angles, values, color=color, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics_to_plot)
    ax.set_title('Multi-dimensional Algorithm Comparison', size=15)
    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig('consensus_radar_comparison.png')
    plt.show()

    # Display comprehensive metrics table
    print("\nComprehensive Metrics for All Algorithms:")
    print(metrics_df.set_index('Algorithm'))

    # Ranking by different metrics
    print("\nAlgorithms Ranked by Efficiency (lower is better):")
    print(metrics_df.sort_values('Efficiency Score')[['Algorithm', 'Efficiency Score']])

    print("\nAlgorithms Ranked by Reliability (higher is better):")
    print(metrics_df.sort_values('Reliability Score', ascending=False)[['Algorithm', 'Reliability Score']])

    print("\nAlgorithms Ranked by Convergence Speed (higher is better):")
    print(metrics_df.sort_values('Convergence Speed', ascending=False)[['Algorithm', 'Convergence Speed']])

    # Overall ranking (combined normalized scores)
    metrics_df['Overall Score'] = (
            normalized_metrics['Efficiency Score'] +
            normalized_metrics['Reliability Score'] +
            normalized_metrics['Convergence Speed'] +
            normalized_metrics['Stability Score'] +
            normalized_metrics['Worst Case Factor']
    )

    print("\nAlgorithms Ranked by Overall Score (higher is better):")
    print(metrics_df.sort_values('Overall Score', ascending=False)[['Algorithm', 'Overall Score']])

if __name__ == '__main__':
    main()
