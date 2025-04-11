import pygame

WIDTH, HEIGHT = 1000, 700
AGENT_SIZE = 50
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
NUM_AGENTS = 100
NUM_ROUNDS = 100
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("T-Shirts Game Simulation")
clock = pygame.time.Clock()

def draw_agents(agents):
    columns = WIDTH // AGENT_SIZE
    rows = HEIGHT // AGENT_SIZE

    for i, agent in enumerate(agents):
        col = i % columns
        row = i // columns
        x = col * AGENT_SIZE
        y = row * AGENT_SIZE
        color = BLUE if agent.color == "blue" else RED
        pygame.draw.rect(screen, color, (x, y, AGENT_SIZE - 5, AGENT_SIZE - 5))


def draw_buttons():
    pygame.draw.rect(screen, GRAY, generate_button)
    pygame.draw.rect(screen, GRAY, play_button)
    font = pygame.font.SysFont(None, 32)
    gen_text = font.render("Generate", True, BLACK)
    play_text = font.render("Play", True, BLACK)
    screen.blit(gen_text, gen_text.get_rect(center=generate_button.center))
    screen.blit(play_text, play_text.get_rect(center=play_button.center))


def start_game():
    pygame.init()

    generate_button = pygame.Rect((WIDTH // 4 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_HEIGHT - 10),
                                  (BUTTON_WIDTH, BUTTON_HEIGHT))
    play_button = pygame.Rect((3 * WIDTH // 4 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_HEIGHT - 10),
                              (BUTTON_WIDTH, BUTTON_HEIGHT))


def run_game(agents):
    round_num = 0
    while True:
        round_num += 1

        for agent in agents:
            observed_agents = random.sample(agents, k=1)
            for other in observed_agents:
                if agent.id != other.id:
                    agent.observe_color(other.color)

        for agent in agents:
            agent.update_color()

        # Check if all agents have the same color
        colors = set(agent.color for agent in agents)
        if len(colors) == 1:
            # print(f"Consensus reached at round {round_num}, color: {colors.pop()}")
            break

    print(agents)


def run_game():
    agents = []
    running = True
    simulation_running = False

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if generate_button.collidepoint(mouse_pos):
                    agents = create_agents()
                    simulation_running = False
                elif play_button.collidepoint(mouse_pos) and agents:
                    simulation_running = True
                    run_game(agents)
                    simulation_running = False

        draw_buttons()
        if agents and not simulation_running:
            draw_agents(agents)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()