from solvers.dataGenerator.generator import Generator
from solvers.partialFast import PartialAlgorithmFast
import time

number_of_ships = 100
maxtime = 24 * 4
additional_time = 24
number_of_parts = 3
stop_after = number_of_parts * 5

generator = Generator(number_of_ships, maxtime, additional_time)
ship_size, arrival = generator.generate()

# additional time must be less than (maxtime + 1) / number_of_parts

start = time.time()

partial = PartialAlgorithmFast( [1, 1, 2, 2, 1, 1, 2, 1, 1, 3, 1, 2, 3, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 3, 2, 2, 1, 1, 2, 1, 1, 3, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 3, 1, 1, 1, 1, 3, 2, 1, 1, 1, 2, 2, 3, 3, 3, 2, 2, 3, 1, 2, 1, 1, 1, 3, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 3, 1, 2, 1, 2, 1, 3, 3, 2, 1, 1, 2, 2, 3, 1],
                                [1, 1, 1, 2, 5, 5, 6, 7, 7, 7, 9, 9, 11, 12, 12, 14, 18, 19, 19, 22, 22, 25, 25, 27, 28, 28, 29, 29, 29, 30, 31, 33, 34, 35, 35, 37, 37, 39, 39, 39, 40, 40, 40, 40, 42, 42, 42, 43, 44, 44, 44, 45, 45, 45, 47, 48, 48, 48, 48, 48, 49, 49, 50, 50, 51, 52, 52, 53, 53, 53, 53, 54, 54, 55, 55, 57, 58, 58, 58, 59, 59, 60, 60, 61, 62, 63, 63, 64, 64, 65, 65, 65, 65, 66, 66, 70, 71, 72, 72, 72],
                            maxtime, number_of_parts, additional_time, stop_after
                            )
solution = partial.solve()

end = time.time()

print("------------------------------------------- solution -------------------------------------------")
print()
print("which: ", solution["which"])
print("ship position: ", solution["ship_position"])
print("start time: ", solution["start"])
print("obj: ", solution["obj"])
print("time: ", f"{int((end - start) // 60)}min {int((end - start) % 60)}s")
print()


