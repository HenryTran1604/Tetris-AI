from functools import reduce
import random
import statistics
from operator import itemgetter
from tetris import Tetris
from sys import stdout

def create_individual(size): # tạo ra cá thể ngẫu nhiên trọng số [aggregate_height, complete_line, number_of_hole, bumpiness]
    result = []
    for i in range(0, size):
        result.append(random.uniform(-10, 10))
    return result

def individual_from_distribution(average, std, size):
    result = []
    for i in range(0, size):
        result.append(random.normalvariate(average[i], std[i]))
    return result

def create_generation(number, size): # tạo ra quần thể chưa number cá thể
    results = []
    for _ in range(0, number):
        tmp = create_individual(size)
        results.append(tmp)
    return results

def generation_from_distribution(number, size, average, std):
    results = []
    for _ in range(0, number):
        tmp = individual_from_distribution(average, std, size)
        results.append(tmp)
    return results

def mutate(x): # tạo đột biến, thay đổi 1 vị trí từ 0 đến 3 với xác suất 0.6
    tmp = create_individual(len(x))
    for i in range(0, len(x)):
        if random.uniform(0, 1) > 0.6:
            x[i] = tmp[i]
    return x

def cross_indivuals(x, y): # lai chéo giữa các  cá thể bố mẹ.
    result = []
    for i in range(0, len(x)):
        if random.uniform(0, 1) > 0.5:
            result.append(y[i])
        else:
            result.append(x[i])
    return x

def select_best_individuals(scores, number): # chọn ra number cá thể tốt nhất
    bests = list(reversed(sorted(scores, key=itemgetter(0))))[0:number]
    return list(map(lambda x: x[1], bests))

def fitness(individual, seeds, pieceLimit): # hàm fitness bằng trung bình cộng các điểm qua các lần chơi của 1 cá thể
    results = []
    for seed in seeds:
        results.append(Tetris(display= True, user=False, seed=seed).run(individual, pieceLimit))
    return int(sum(results)/len(results))

def compute_average(population): # tính trung bình các giá trị heuristic của quần thể
    result = list(reduce(lambda i1, i2: [a+b for a,b in zip(i1, i2)], population))
    result = list(map(lambda x: x/len(population), result))
    return result

def compute_standard_deviation(population):
    result = [[] for _ in range(0, len(population[0]))]
    for individual in population:
        for index, weight in enumerate(individual):
            result[index].append(weight)
    result = list(map(lambda weights: statistics.stdev(weights), result))
    return result
