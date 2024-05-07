from minizinc import Instance, Model, Solver
from datetime import timedelta

class PartialAlgorithm:

    def __init__(self, ship_size: list[int], arrival: list[int], maxtime: int, number_of_parts: int):

        self.nsh = len(ship_size)
        self.ship_size = ship_size

        self.load_goods = []
        for i in range(self.nsh):
            self.load_goods.append(False)

        self.maxtime = maxtime
        self.arrival = arrival
        self.number_of_parts = number_of_parts

        self.ship_types_number = 3
        self.ship_speed = [1, 1, 1]
        self.ship_width = [1, 2, 2]
        self.ship_length = [5, 10, 15]

        self.reclaim_time = 1

        self.nr = 12
        self.nre = 41
        self.platform_length = [14, 21, 21, 27, 27, 38, 38, 40, 14, 14, 20, 12]
        self.platform_time = [3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1]
        self.reclaimers_number = [2, 2, 2, 3, 3, 7, 7, 10, 1, 1, 2, 1]
        self.reclaimers_platform = [1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7,
                                    7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 10, 11, 11, 12]

    def solve(self):

        model = Model("portSchedulingPartial.mzn")
        solver = Solver.lookup("com.google.ortools.sat")
        instance = Instance(solver, model)

        instance["nsh"] = self.nsh
        instance["ship_size"] = self.ship_size
        instance["load_goods"] = self.load_goods
        instance["maxtime"] = self.maxtime
        instance["arrival"] = self.arrival
        instance["ship_types_number"] = self.ship_types_number
        instance["ship_speed"] = self.ship_speed
        instance["ship_width"] = self.ship_width
        instance ["ship_length"] = self.ship_length
        instance["reclaim_time"] = self.reclaim_time
        instance["nr"] = self.nr
        instance["nre"] = self.nre
        instance["platform_length"] = self.platform_length
        instance["platform_time"] = self.platform_time
        instance["reclaimers_number"] = self.reclaimers_number
        instance["reclaimers_platform"] = self.reclaimers_platform

        max_time = timedelta(seconds=60)
        result = instance.solve(timeout=max_time, processes=8)
        
        return {
            "start": result["start"],
            "which": result["which"],
            "ship_position": result["ship_position"],
            "obj": result["objective"]
        }

    