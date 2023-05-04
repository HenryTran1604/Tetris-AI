from sys import stdout
import time
from environment.genetics import *
import random
survivors_rate = 0.7 # số lượng sống sót
bests_rate = 0.1
mutate_chance = 0.05
pieceLimit = 500 # số lượng tetromino chơi tối đa
number = 50 # số lượng cá thể trong 1 quần thể
batch = 2 # số lần lặp
size = 4 # số lượng thuộc tính trong hàm heuristic


generation = create_generation(number, size)

optimal_weight = [0, [0]*4]
total_duration = 0
with open('weights/v1.txt', 'w') as file:
    for iteration in range(0, batch):
        start_time = time.time()
        seeds = []
        for _ in range(0, 5):
            seeds.append(random.randint(0, 100000000))

        file.write("\n")
        file.write("--- Batch " + str(iteration+1) + " ---")
        file.write("\n")
        scores = []
        print(f'\nBatch {iteration+1}/{batch}')
        
        for index, indiv in enumerate(generation):
            message = "\rindiv. " + str(index+1) + "/" + str(len(generation))
            stdout.write(message)
            stdout.flush()
            scores.append([fitness(indiv, seeds, pieceLimit), indiv])
        file.write('\n')
        for value in (list(reversed(sorted(scores, key=itemgetter(0))))):
            file.write(str(value) + '\n')
    
        survivors_score, survivors = select_survivors(scores, int(len(scores)*survivors_rate))
        if survivors_score[0] > optimal_weight[0]:
            optimal_weight = [survivors_score[0], survivors[0]]
        # file.write(len(bests))
        generation = survivors
        file.write("average: " + str(compute_average(generation)))
        duration = time.time() - start_time
        file.write(f'\ntrain for generation {iteration+1} take {duration} seconds')
        total_duration += duration
        while len(generation) < number:
            individual = cross_over(*random.sample(survivors[:int(bests_rate * number)], k=2))
            if random.uniform(0, 1) < 0.05:
                individual = mutate(individual)
            generation.append(individual)
    file.write(f'\ntotal time for training: {total_duration} seconds')

with open('weights/optimal.txt', 'w') as file:
    for i in range(size):
        file.write(str(optimal_weight[1][i]) + ' ')
