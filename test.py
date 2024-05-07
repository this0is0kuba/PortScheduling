from solvers.dataGenerator.generator import Generator
from solvers.partial import PartialAlgorithm

number_of_ships = 6
maxtime = 12

generator = Generator(number_of_ships, maxtime)
ship_size, arrival = generator.generate()

partial = PartialAlgorithm(ship_size, arrival, maxtime, 5)
solution = partial.solve()

print(solution)



