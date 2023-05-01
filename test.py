from tetris import Tetris
import random
class Individual:
    def __init__(self, size):
        self.size = size
        self.score = 0
        self.create_weight()

    def create_weight(self):
        self.weight = []
        for i in range(0, self.size):
            self.weight.append(random.uniform(-10, 10))
        self.nomalize()
    def nomalize(self):
        tmp = sum(x ** 2 for x in self.weight)
        for x in self.weight:
            x /= tmp
    def mutate(self):
        self.weight[random.randint(0, self.size - 1)] += random.random() * 0.4 - 0.2
        self.nomalize()
    def fitness(self, seeds, pieceLimit): # hàm fitness bằng trung bình cộng các điểm qua các lần chơi của 1 cá thể
        results = []
        for seed in seeds:
            results.append(Tetris(display=False, user=False, seed=seed).run(self.weight, pieceLimit))
        return int(sum(results)/len(results))

class Population:
    def __init__(self, number):
        self.number = number
        self.create_individuals()

    def create_individuals(self, size):
        self.individuals = []
        for i in range(self.number):
            indiv = Individual(size)
            indiv.create_individual()
            self.individuals.append(indiv)
    @staticmethod
    def cross_over(x:Individual, y:Individual): # lai chéo giữa các  cá thể bố mẹ.
        result = Individual(x.size)
        for i in range(0, len(x)):
            if random.uniform(0, 1) > 0.5:
                result.weight[i] = y[i]
            else:
                result.append(x[i])
        return result
    def select_best_individuals(scores, number): # chọn ra number cá thể tốt nhất
        bests = list(reversed(sorted(scores, key=itemgetter(0))))[0:number]
        return list(map(lambda x: x[0], bests)), list(map(lambda x: x[1], bests))
