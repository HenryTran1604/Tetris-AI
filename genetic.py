from functools import reduce
import random
import statistics
import time
from operator import itemgetter
from tetris import Tetris
from sys import stdout

def create_individual(size): # tạo ra cá thể ngẫu nhiên trọng số [aggregate_height, complete_line, number_of_hole, bumpiness]
    result = []
    for i in range(0, size):
        result.append(random.uniform(-10, 10))
    return result

def individual_from_distribution(average, std):
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
        tmp = individual_from_distribution(average, std)
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

survivors_rate = 0.2 # số lượng sống sót
pieceLimit = 10 # số lượng tetromino chơi tối đa
number = 1 # số lượng cá thể trong 1 quần thể
batch = 12 # số lần lặp
size = 4 # số lượng thuộc tính trong hàm heuristic


# tạo ra 10 cá thể đầu tiên
survivors = [[-7.079322515535496, 0.4084491347254038, -7.402904430910445, -2.7844637476685787],
            [-7.474811040277999, 1.7388998167593965, -7.403164993532727, -6.42470716303297],
            [-1.5396056314838051, 1.28985252553531, -9.55939973079273, -6.020212792774943],
            [-2.6858983840113106, 4.066945649094353, -6.6028598255064175, -3.6113692499628147],
            [-8.5479653838089, 1.60494594308804, -1.8232423721829427, -6.6662509160349535],
            [-5.1201195901469365, 0.07286751923358015, -0.8109293327422344, -5.00506161296176],
            [-0.6592821298420546, 3.728099144510246, -1.0053831195536995, -4.057497731586515],
            [-9.901236706651698, 0.34674512247742717, -7.457239312581076, -6.639724294314924],
            [-1.2647311775882684, 0.8029345834888093, -7.653044559806861, -4.871298554686161],
            [-6.611752028945782, 4.250725580320059, -5.023691054269568, -6.60469459079245]]


generation = survivors

average = compute_average(survivors)
extra_var_multiplier = max((1.0-10/float(batch/2)),0)
std = list(map(lambda std: std + 0.001 * extra_var_multiplier, compute_standard_deviation(survivors)))

print("")
# print("time elapsed: ", time.time() - start_tidme)
print("average: ", average)
print("std: ", std)
print("")

for individual in generation_from_distribution(number-len(generation), size, average, std):
    generation.append(individual)


#generation = create_generation(number, size)
for iteration in range(11, batch):
    start_time = time.time()
    seeds = []
    for _ in range(0, 5):
        seeds.append(random.randint(0, 100000000))

    print("")
    print("")
    print("--- Batch " + str(iteration) + " ---")
    print("")
    scores = []
    for index, indiv in enumerate(generation):
        message = "\rindiv. " + str(index) + "/" + str(len(generation))
        stdout.write(message)
        stdout.flush()
        scores.append([fitness(indiv, seeds, pieceLimit), indiv])
    print()
    for value in (list(reversed(sorted(scores, key=itemgetter(0))))):
        print(value)
    survivors = select_best_individuals(scores, int(len(scores)*survivors_rate))
    print(len(survivors))
    generation = survivors

    average = compute_average(survivors)
    extra_var_multiplier = max((1.0-iteration/float(batch/2)),0)
    std = list(map(lambda std: std + 0.001 * extra_var_multiplier, compute_standard_deviation(survivors)))

    print("")
    print("time elapsed: ", time.time() - start_time)
    print("average: ", average)
    print("std: ", std)
    print("")

    for individual in generation_from_distribution(number-len(generation), size, average, std):
        generation.append(individual)
