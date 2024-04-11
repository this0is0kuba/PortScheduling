import random

def generator(ships_number: int, maxtime: int):
     
    p_small = 0.5
    p_middle = 0.3
    # p_big = 0.2

    ship_info = []

    for i in range(ships_number):

        p = random.random()
        arrivalTime = random.randint(0, maxtime-5)

        if p < p_small:
            ship_info.append((1, arrivalTime))

        elif p < p_small + p_middle:
            ship_info.append((2, arrivalTime))

        else:
            ship_info.append((3, arrivalTime))


    ship_info.sort(key= lambda info: info[1])

    print("ship_size: [", end="")
    for i in range(ships_number):

        print(ship_info[i][0], end="")

        if i != ships_number - 1:
            print(", ", end="")
    
    print("]", end="")

    print()

    print("arrival: [", end="")
    for i in range(ships_number):

        print(ship_info[i][1], end="")

        if i != ships_number - 1:
            print(", ", end="")
    
    print("]", end="")

generator(20, 12)

    

