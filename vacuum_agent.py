class VacuumAgent:
    def __init__(self):
        self.location = 0  # (row, col) = (0,0)
        # 2x2 grid as 4 cells: (0,0) (0,1) (1,1) (1,0)
        self.environment = ['dirty', 'clean', 'dirty', 'clean']

    def interpret_input(self):
        return self.environment[self.location]  # state

    def rule_action(self, state):
        # condition-action rules of the simple reflex agent
        if state == 'dirty':
            print("Cleaning cell", self.location)
            self.environment[self.location] = 'clean'
        else:
            print("Moving to the next cell")
            self.location = (self.location + 1) % len(self.environment)

    def show(self):
        print("  Position:", self.location, "| Environment:", self.environment)


agent = VacuumAgent()
print("Initial environment:", agent.environment)

steps = 0
while 'dirty' in agent.environment and steps < 20:  # goal: no dirty cell left
    state = agent.interpret_input()
    agent.rule_action(state)
    agent.show()
    steps += 1

print("Final environment:", agent.environment)
print("Goal reached:", 'dirty' not in agent.environment, "in", steps, "steps")

try:
    input("\nPress Enter to close ...")
except EOFError:
    pass
