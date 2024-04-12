from .dataGenerator.generator import Generator
from .partial import PartialAlgorithm

maxtime = 10
number_of_ships = 5

generator = Generator(number_of_ships, maxtime)
ship_size, arrival = generator.generate()

partial = PartialAlgorithm(ship_size, arrival)
solution = partial.solve()

print("obj: ", solution["obj"])
print("start: ", solution["start"])



