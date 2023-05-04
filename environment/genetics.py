from functools import reduce
import random
from operator import itemgetter
from tetris import Tetris

def create_individual(size):
    result = []
    for i in range(0, size):
        result.append(random.uniform(-10, 10))
    return result

def create_generation(number, size):
    population = []
    for _ in range(0, number):
        tmp = create_individual(size)
        population.append(tmp)
    return population


def mutate(x): # tạo đột biến, thay đổi 1 vị trí từ 0 đến 3
    for i in range(len(x)):
        if random.uniform(0, 1) > 0.6:
            x[i] = random.uniform(-10, 10)
    return x

def cross_over(x, y): # lai chéo giữa các  cá thể bố mẹ.
    result = []
    for i in range(0, len(x)):
        if random.uniform(0, 1) > 0.5:
            result.append(y[i])
        else:
            result.append(x[i])
    return result

def select_survivors(scores, number): # chọn ra number cá thể tốt nhất
    bests = list(reversed(sorted(scores, key=itemgetter(0))))[0:number]
    return list(map(lambda x: x[0], bests)), list(map(lambda x: x[1], bests))

def fitness(individual, seeds, pieceLimit): # hàm fitness bằng trung bình cộng các điểm qua các lần chơi của 1 cá thể
    results = []
    for seed in seeds:
        results.append(Tetris(display=False, user=False, seed=seed).run(individual, pieceLimit))
    return int(sum(results)/len(results))


def compute_average(population): # tính trung bình các giá trị heuristic của quần thể
    result = list(reduce(lambda i1, i2: [a+b for a,b in zip(i1, i2)], population))
    result = list(map(lambda x: x/len(population), result))
    return result
