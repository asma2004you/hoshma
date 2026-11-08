# -*- coding: utf-8 -*-
"""
Simple Reflex Agent - Temperature Control for 2 Houses
Target: 20 degrees, initial temps: house 1 = 17, house 2 = 24
"""


class TemperatureControlAgent:
    def __init__(self):
        self.target = 20  # percept
        self.houses = [17, 24]  # 2 houses with initial temperatures

    def interpret_input(self, house):
        temp = self.houses[house]  # state
        if temp < self.target:
            return 'cold'
        elif temp > self.target:
            return 'hot'
        else:
            return 'ok'

    def rule_action(self, house, state):
        if state == 'cold':
            print(f"Turning heater ON for house {house + 1}")
            self.houses[house] += 1
        elif state == 'hot':
            print(f"Turning cooler ON for house {house + 1}")
            self.houses[house] -= 1
        else:
            print(f"House {house + 1} reached target, system OFF")


agent = TemperatureControlAgent()
print("Initial temperatures:", agent.houses)
for _ in range(3):
    for house in range(len(agent.houses)):
        state = agent.interpret_input(house)
        agent.rule_action(house, state)
    print("Temperatures after round:", agent.houses)
print("Final temperatures:", agent.houses)
