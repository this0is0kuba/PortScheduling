from solvers.dataGenerator.generator import Generator
from solvers.partial import PartialAlgorithm
import time

number_of_ships = 100
maxtime = 105
additional_time = 14
number_of_parts = 7
stop_after = 20 # stop after 8 minutes

generator = Generator(number_of_ships, maxtime, additional_time)
ship_size, arrival = generator.generate()

# additional time must be less than (maxtime + 1) / number_of_parts

start = time.time()

partial = PartialAlgorithm( [1, 3, 1, 3, 2, 1, 3, 1, 1, 2, 1, 3, 1, 1, 3, 2, 3, 3, 1, 1, 2, 3, 2, 1, 2, 3, 3, 3, 1, 2, 2, 3, 1, 3, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 3, 2, 1, 1, 3, 2, 2, 3, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 3, 2, 1, 1, 2, 3, 1, 3, 3, 2, 1, 1, 1, 2, 1, 3, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 3, 1, 2],
                            [1, 2, 2, 2, 4, 6, 7, 8, 9, 11, 11, 13, 13, 15, 16, 16, 16, 18, 18, 20, 21, 21, 22, 22, 24, 24, 25, 27, 29, 29, 29, 30, 30, 30, 32, 35, 35, 36, 36, 36, 37, 38, 38, 38, 39, 39, 40, 42, 42, 43, 43, 43, 44, 45, 45, 45, 45, 45, 47, 47, 48, 53, 53, 54, 55, 55, 57, 57, 57, 57, 58, 59, 61, 61, 64, 65, 66, 68, 69, 71, 71, 73, 73, 74, 74, 74, 75, 76, 77, 77, 78, 78, 79, 82, 82, 84, 85, 87, 88, 91],
                            maxtime, number_of_parts, additional_time, stop_after
                            )
solution = partial.solve()

end = time.time()

# [3, 1, 3, 3, 1, 1, 1, 3, 1, 3, 2, 2, 2, 3, 1, 1, 1, 2, 1, 1, 2, 1, 3, 2, 3, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1, 3, 2, 2, 1, 2, 1, 2, 1, 2, 3, 3, 2, 1, 3, 3, 3, 2, 2, 2, 1],
#                              [6, 8, 10, 22, 26, 29, 33, 39, 39, 40, 49, 51, 58, 60, 76, 84, 98, 103, 110, 110, 111, 115, 119, 121, 134, 138, 148, 149, 176, 177, 185, 185, 186, 188, 191, 192, 199, 202, 203, 212, 223, 225, 231, 234, 236, 241, 246, 251, 256, 259, 262, 265, 267, 273, 275],

print("------------------------------------------- solution -------------------------------------------")
print()
print("which: ", solution["which"])
print("ship position: ", solution["ship_position"])
print("start time: ", solution["start"])
print("obj: ", solution["obj"])
print("time: ", f"{int((end - start) // 60)}min {int((end - start) % 60)}s")
print()


