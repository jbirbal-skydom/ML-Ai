from env import Slots
from agent import Robot
from tqdm import tqdm
import matplotlib.pyplot as plt

enjoyment = {}
strategies = (0.0, 0.1, 0.01)


if __name__ == '__main__':
    for strategy in strategies:
        enjoyment[strategy] = []
        visit = 0
        experience = 0
        for _ in tqdm(range(2000)):  # Simulation
            machine = Slots(6)
            person = Robot(machine.action_space, epsilon=strategy)
            for _ in range(1000):  # pulls
                choice = person.choice()
                arm, reward = machine.payout(choice)
                mean = person.assessment(choice, reward)
            new_score = person.happiness()

            if visit < 1:
                experience = new_score
            else:
                experience = experience + (1 / (visit + 1))*(new_score - experience)

            visit += 1
            enjoyment[strategy].append(experience)

    for k, v in enjoyment.items():
        plt.plot(range(1, len(v) + 1), v, '.-', label=k)
    plt.legend()  # To draw legend
    plt.show()
