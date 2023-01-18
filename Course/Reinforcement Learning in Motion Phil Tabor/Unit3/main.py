from env import *
from agent import Robot
from tqdm import tqdm
import matplotlib.pyplot as plt

enjoyment = {}
strategies = (0.0, 0.1, 0.01)
alphas = ("constant", "fraction")
video = 2
pull = 1000
simulation = 200


if __name__ == '__main__':
    if video == 1:
        for strategy in strategies:
            enjoyment[strategy] = []
            visit = 0
            experience = 0
            for _ in tqdm(range(simulation)):  # Simulation
                machine = Slots(6)
                person = Robot(machine.action_space, epsilon=strategy)
                for _ in range(pull):  # pulls
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

    elif video == 2:
        for alpha in alphas:
            enjoyment[alpha] = []
            visit = 0
            experience = 0
            for _ in tqdm(range(simulation)):  # Simulation
                machine = ConstantSlot(6)
                person = Robot(machine.action_space, epsilon=0.1, alpha=alpha)
                for _ in range(pull):  # pulls
                    choice = person.choice()
                    reward = machine.payout(choice)
                    mean = person.assessment(choice, reward)
                new_score = person.happiness()

                if visit < 1:
                    experience = new_score
                else:
                    experience = experience + (1 / (visit + 1))*(new_score - experience)

                visit += 1
                enjoyment[alpha].append(new_score)

    else:
        print("no video")

    for k, v in enjoyment.items():
        plt.plot(range(1, len(v) + 1), v, '.-', label=k)
    plt.legend()  # To draw legend
    plt.show()
