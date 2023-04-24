from functools import reduce
import random
import time
from operator import itemgetter
from tetris import Tetris
from sys import stdout

def create_individual(size): # tạo ra cá thể ngẫu nhiên trọng số [aggregate_height, complete_line, number_of_hole, bumpiness]
    result = []
    for i in range(0, size):
        result.append(random.uniform(-10, 10))
    return result

def create_generation(number, size): # tạo ra quần thể chưa number cá thể
    results = []
    for _ in range(0, number):
        tmp = create_individual(size)
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
        results.append(Tetris(playWithUI= True, user=False, seed=seed).run(indiv, pieceLimit))
    return int(sum(results)/len(results))


survivors_rate = 0.2 # số lượng sống sót
pieceLimit = 20 # số lượng tetromino chơi tối đa
number = 10 # số lượng cá thể trong 1 quần thể
batch = 12 # số lần lặp
size = 4 # số lượng thuộc tính trong hàm heuristic



generation = []


tmp = len(generation)
for _ in range(0, number - tmp):
    generation.append(create_individual(size))


#generation = create_generation(number, size)
with open('weights/old/v1.txt', 'w') as file:
    for iteration in range(11, batch):
        start_time = time.time()
        seeds = []
        for _ in range(0, 5):
            seeds.append(random.randint(0, 100000000))

        file.write("\n")
        file.write("\n")
        file.write("--- Batch " + str(iteration) + " ---\n")
        file.write("\n")
        scores = []
        for index, indiv in enumerate(generation):
            message = "\rindiv. " + str(index) + "/" + str(len(generation))
            stdout.write(message)
            stdout.flush()
            scores.append([fitness(indiv, seeds, pieceLimit), indiv])
        file.write('\n')
        for value in (list(reversed(sorted(scores, key=itemgetter(0))))):
            file.write(str(value) + '\n')
        survivors = select_best_individuals(scores, int(len(scores)*survivors_rate))
        # file.write(len(survivors))
        generation = survivors


        tmp = len(generation)
        for individual in range(0, number - tmp):
            generation.append(individual)
