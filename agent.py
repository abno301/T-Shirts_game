import random

class Agent:
    def __init__(self, agent_id: int):
        self.id = agent_id
        self.color = random.choice(["blue", "red"])  # Random initial color
        self.noOfBlue = 0
        self.noOfRed = 0

    def observe_color(self, partner_color: str):
        """Record the observed color of another agent."""
        if partner_color == "blue":
            self.noOfBlue += 1
        elif partner_color == "red":
            self.noOfRed += 1

    def update_color(self):
        """Update color based on majority observed in last interactions."""
        if self.noOfRed > self.noOfBlue:
            self.color = "red"
        elif self.noOfBlue > self.noOfRed:
            self.color = "blue"
        # Reset counts after each update cycle
        self.noOfBlue = 0
        self.noOfRed = 0

    def __repr__(self):
        return f"Agent({self.id}, {self.color})"