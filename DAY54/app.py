
import random
import math
import matplotlib.pyplot as plt

CELL_SIZE = 20  

class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.happiness = random.uniform(50, 100)
        self.energy = random.uniform(50, 100)
        self.social = random.uniform(30, 70)

    def interact(self, other):
        factor = (self.social + other.social) / 200
        delta = random.uniform(-5, 5) * factor
        self.happiness = min(100, max(0, self.happiness + delta))
        other.happiness = min(100, max(0, other.happiness + delta))
        cost = random.uniform(1, 3)
        self.energy = max(0, self.energy - cost)
        other.energy = max(0, other.energy - cost)

    def daily_decay(self):
        self.energy = max(0, self.energy - random.uniform(0, 2))
        self.happiness = max(0, self.happiness - random.uniform(0, 1))

class Society:
    def __init__(self, population_size):
        self.population = [Person(i, f"Person_{i}") for i in range(population_size)]
        self.day = 0
        self.avg_happiness_history = []
        self.avg_energy_history = []
        self.avg_social_history = []

    def simulate_day(self):
        interactions = random.randint(3, 7)
        for person in self.population:
            for _ in range(interactions):
                other = random.choice(self.population)
                if other.id != person.id:
                    person.interact(other)
            person.daily_decay()
        self.day += 1
        self.record_metrics()

    def record_metrics(self):
        total_happiness = sum(p.happiness for p in self.population)
        total_energy = sum(p.energy for p in self.population)
        total_social = sum(p.social for p in self.population)
        n = len(self.population)
        self.avg_happiness_history.append(total_happiness / n)
        self.avg_energy_history.append(total_energy / n)
        self.avg_social_history.append(total_social / n)

    def run_simulation(self, days):
        for _ in range(days):
            self.simulate_day()

    def get_metrics(self):
        return {
            "avg_happiness": self.avg_happiness_history,
            "avg_energy": self.avg_energy_history,
            "avg_social": self.avg_social_history
        }

def plot_metrics(metrics):
    days = range(1, len(metrics["avg_happiness"]) + 1)
    plt.figure(figsize=(10,6))
    plt.plot(days, metrics["avg_happiness"], label="Average Happiness", color="orange", linewidth=2)
    plt.plot(days, metrics["avg_energy"], label="Average Energy", color="blue", linewidth=2)
    plt.plot(days, metrics["avg_social"], label="Average Social", color="green", linewidth=2)
    plt.xlabel("Day")
    plt.ylabel("Value")
    plt.title("Society Metrics Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    population_size = 100
    simulation_days = 50
    society = Society(population_size)
    society.run_simulation(simulation_days)
    metrics = society.get_metrics()
    print("Simulation complete!")
    print("Final Average Happiness:", metrics["avg_happiness"][-1])
    print("Final Average Energy:", metrics["avg_energy"][-1])
    print("Final Average Social:", metrics["avg_social"][-1])
    plot_metrics(metrics)

if __name__ == "__main__":
    main()
