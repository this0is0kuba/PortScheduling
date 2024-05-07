import random

class Generator:

    def __init__(self, ships_number: int, maxtime: int) -> None:
        
        self.ships_number = ships_number
        self.maxtime = maxtime

    def generate(self):
        
        p_small = 0.5
        p_middle = 0.3
        # p_big = 0.2

        ship_info = []

        for _ in range(self.ships_number):

            p = random.random()
            arrivalTime = random.randint(0, self.maxtime-5)

            if p < p_small:
                ship_info.append((1, arrivalTime))

            elif p < p_small + p_middle:
                ship_info.append((2, arrivalTime))

            else:
                ship_info.append((3, arrivalTime))


        ship_info.sort(key= lambda info: info[1])

        ship_size = [t[0] for t in ship_info]
        arrival = [t[1] for t in ship_info]

        return (ship_size, arrival)  # [ship_size, arrival]
