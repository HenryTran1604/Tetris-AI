from sys import stdout
import time
from environment.genetics import *
import random
survivors_rate = 0.7 # số lượng sống sót
bests_rate = 0.1
cross_over_rate = 0.1
mutate_chance = 0.05
pieceLimit = 500 # số lượng tetromino chơi tối đa
number = 100 # số lượng cá thể trong 1 quần thể
batch = 10 # số lần lặp
size = 4 # số lượng thuộc tính trong hàm heuristic


generation = create_generation(number, size)


optimal_weight = [0, [0]*4]
with open('weights/v1.txt', 'w') as file:
    for iteration in range(0, batch):
        start_time = time.time()
        seeds = []
        for _ in range(0, 5):
            seeds.append(random.randint(0, 100000000))

        file.write("\n")
        file.write("--- Batch " + str(iteration) + " ---\n")
        file.write("\n")
        scores = []
        print(f'Batch {iteration}/{batch}\n')
        
        for index, indiv in enumerate(generation):
            message = "\rindiv. " + str(index) + "/" + str(len(generation))
            stdout.write(message)
            stdout.flush()
            scores.append([fitness(indiv, seeds, pieceLimit), indiv])
        file.write('\n')
        for value in (list(reversed(sorted(scores, key=itemgetter(0))))):
            file.write(str(value) + '\n')
    
        survivors_score, survivors = select_survivors(scores, int(len(scores)*survivors_rate))
        if survivors_score[0] >= optimal_weight[0]: # ưu tiên thế hệ sau
            optimal_weight = [survivors_score[0], survivors[0]]
        # file.write(len(bests))
        generation = survivors
        file.write("average: " + str(compute_average(generation)))

        while len(generation) < number:
            individual = cross_over(*random.sample(survivors[:int(bests_rate * number)], k=2))
            if random.uniform(0, 1) < mutate_chance:
                individual = mutate(individual)
            generation.append(individual)

with open('weights/optimal.txt', 'w') as file:
    for i in range(size):
        file.write(str(optimal_weight[1][i]) + ' ')
