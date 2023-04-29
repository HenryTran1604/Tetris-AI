from functools import reduce
import random
from operator import itemgetter
from tetris import Tetris

def nomalize(indiv):
    tmp = sum(x ** 2 for x in indiv)
    return [x/tmp for x in indiv]

def create_individual(size): # tạo ra cá thể ngẫu nhiên trọng số [aggregate_height, complete_line, number_of_hole, bumpiness]
    result = []
    for i in range(0, size):
        result.append(random.uniform(-10, 10))
    result = nomalize(result)
    return result

def create_generation(number, size): # tạo ra quần thể chưa number cá thể
    results = []
    for _ in range(0, number):
        tmp = create_individual(size)
        results.append(tmp)
    return results


def mutate(x): # tạo đột biến, thay đổi 1 vị trí từ 0 đến 3 với xác suất 0.4
    x[random.randint(0, len(x) - 1)] += random.random() * 0.4 - 0.2
    x = nomalize(x)
    return x

def cross_over(x, y): # lai chéo giữa các  cá thể bố mẹ.
    result = []
    for i in range(0, len(x)):
        if random.uniform(0, 1) > 0.5:
            result.append(y[i])
        else:
            result.append(x[i])
    return result


def select_best_individuals(scores, number): # chọn ra number cá thể tốt nhất
    bests = list(reversed(sorted(scores, key=itemgetter(0))))[0:number]
    return list(map(lambda x: x[0], bests)), list(map(lambda x: x[1], bests))

def fitness(individual, seeds, pieceLimit): # hàm fitness bằng trung bình cộng các điểm qua các lần chơi của 1 cá thể
    results = []
    for seed in seeds:
        results.append(Tetris(display= False, user=False, seed=seed).run(individual, pieceLimit))
    return int(sum(results)/len(results))


def compute_average(population): # tính trung bình các giá trị heuristic của quần thể
    result = list(reduce(lambda i1, i2: [a+b for a,b in zip(i1, i2)], population))
    result = list(map(lambda x: x/len(population), result))
    return result

