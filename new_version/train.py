from new_version.genetic import *
import time
survivors_rate = 0.2 # số lượng sống sót
pieceLimit = 500 # số lượng tetromino chơi tối đa
number = 30 # số lượng cá thể trong 1 quần thể
batch = 50 # số lần lặp
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
with open('weights/new/v1.txt', 'w') as file:
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
        file.write(str(len(survivors)) + '\n')
        generation = survivors

        average = compute_average(survivors)
        extra_var_multiplier = max((1.0-iteration/float(batch/2)),0)
        std = list(map(lambda std: std + 0.001 * extra_var_multiplier, compute_standard_deviation(survivors)))

        file.write("\n")
        file.write("time elapsed: " + str(time.time() - start_time) + '\n')
        file.write("average: " +  str(average) + '\n')
        file.write("std: " + str(std))
        file.write("\n")

        for individual in generation_from_distribution(number-len(generation), size, average, std):
            generation.append(individual)
