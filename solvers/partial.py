from minizinc import Instance, Model, Solver
from datetime import timedelta
import math

class PartialAlgorithm:

    def __init__(self, ship_size: list[int], arrival: list[int], maxtime: int, number_of_parts: int, additional_time: int, stop_after: int):

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

        self.reclaim_time = 2

        self.nr = 12
        self.nre = 41
        self.platform_length = [14, 21, 21, 27, 27, 38, 38, 40, 14, 14, 20, 12]
        self.platform_time = [2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]
        self.reclaimers_number = [2, 2, 2, 3, 3, 7, 7, 10, 1, 1, 2, 1]
        self.reclaimers_platform = [1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7,
                                    7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 10, 11, 11, 12]
        
        self.additional_time = additional_time
        self.time_part = math.ceil( (maxtime - self.additional_time + 1) / self.number_of_parts)
        self.earlier_solution = None
        self.stop_after = stop_after
        
        # solution
        self.which = []
        self.ship_position = []
        self.start = []
        self.obj = 0

    def solve(self):

        print("ship_size: ", self.ship_size)
        print("arrival: ", self.arrival)
        print()
        
        for i in range(self.number_of_parts):

            if i == 0:
                self.solve_using_standard_method(i)

            else: 

                if self.earlier_solution == None:
                    self.solve_using_standard_method(i)
                
                else:
                    idx_range = self.find_earlier_range(self.earlier_solution['left'])

                    if len(idx_range) == 0:
                        self.solve_using_standard_method(i)
                    else:
                        self.solve_using_partial_method(i)

        print()
        print()

        return {
            "which": self.which,
            "ship_position": self.ship_position,
            "start": self.start,
            "obj": self.obj
        }


    def solve_using_standard_method(self, i):
            
            print("\n\n--------------------- part number: ", i , " (standard method) ", f" time = [{self.time_part * i}, {(self.time_part) * (1 + i) - 1}]", " ---------------------")
        
            min_index, max_index = self.find_range(i)

            if min_index > max_index:

                self.earlier_solution = None
                return

            model = Model("portScheduling2.mzn")
            solver = Solver.lookup("com.google.ortools.sat")
            instance = Instance(solver, model)

            self.set_initial_values(instance, i)

            max_time = timedelta(seconds=60*self.stop_after/self.number_of_parts)
            result = instance.solve(timeout=max_time, processes=8)

            dict_result = {
                "which": result["which"],
                "ship_position": result["ship_position"],
                "start": result["start"],
                "left": result["left"],
                "reclaimers_position": result["reclaimers_position"],
                "obj": result["objective"],
                "min_index": min_index,
                "max_index": max_index
            }

            print("ship_indexes: ", [x for x in range(min_index, max_index+1)])
            print("ship_size: ", self.ship_size[min_index:max_index+1])
            print("which: ", result["which"])
            print("start: ", [time + i * self.time_part for time in result["start"]])
            print("left: ", result["left"])
            print("obj: ", result["objective"])
            print("min index: ", min_index)
            print("max_index: ", max_index)

            self.which.extend(result["which"])
            self.ship_position.extend(result["ship_position"])
            self.start.extend([time + i * self.time_part for time in result["start"]])
            self.obj += result["objective"]

            self.earlier_solution = dict_result

    def solve_using_partial_method(self, i):
            
            print("\n\n--------------------- part number: ", i , " (partial method) ", f" time = [{self.time_part * i}, {(self.time_part) * (1 + i) - 1}]", " ---------------------")
            
            min_index, max_index = self.find_range(i)

            if min_index > max_index:

                self.earlier_solution = None
                return

            model = Model("portSchedulingPartial.mzn")
            solver = Solver.lookup("com.google.ortools.sat")
            instance = Instance(solver, model)

            self.set_initial_values(instance, i)
            self.set_earlier_values(instance, i)

            max_time = timedelta(seconds=60*self.stop_after/self.number_of_parts)
            result = instance.solve(timeout=max_time, processes=8)

            dict_result = {
                "which": result["which"],
                "ship_position": result["ship_position"],
                "start": result["start"],
                "left": result["left"],
                "reclaimers_position": result["reclaimers_position"],
                "obj": result["objective"],
                "min_index": min_index,
                "max_index": max_index
            }

            print("ship_indexes: ", [x for x in range(min_index, max_index+1)])
            print("ship_size: ", self.ship_size[min_index:max_index+1])
            print("which: ", result["which"])
            print("start: ", [time + i * self.time_part for time in result["start"]])
            print("left: ", [time + i * self.time_part for time in result["left"]])
            print("obj: ", result["objective"])
            print("min index: ", min_index)
            print("max_index: ", max_index)

            self.which.extend(result["which"])
            self.ship_position.extend(result["ship_position"])
            self.start.extend([time + i * self.time_part for time in result["start"]])
            self.obj += result["objective"]

            self.earlier_solution = dict_result

    def set_initial_values(self, instance: Instance, part_number: int): 

        min_idx, max_idx = self.find_range(part_number)

        instance["nsh"] = max_idx - min_idx + 1
        instance["ship_size"] = self.ship_size[min_idx:max_idx+1]
        instance["load_goods"] = self.load_goods[min_idx:max_idx+1]
        instance["maxtime"] = self.arrival[max_idx] - (self.time_part * part_number) + self.additional_time
        instance["arrival"] = [time - (self.time_part * part_number) for time in self.arrival[min_idx:max_idx+1]]
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

        print()
        print("initial values")

        print("nsh: ", max_idx - min_idx + 1)
        print("ship size: ", self.ship_size[min_idx:max_idx+1])
        print("load_goods: ", self.load_goods[min_idx:max_idx+1])
        print("actual maxtime: ", self.arrival[max_idx] + self.additional_time)
        print("set maxtime: ", self.arrival[max_idx] - (self.time_part * part_number) + self.additional_time)
        print("actual arrival: ", [time for time in self.arrival[min_idx:max_idx+1]])
        print("set arrival: ", [time - (self.time_part * part_number) for time in self.arrival[min_idx:max_idx+1]])

        print()



        return (min_idx, max_idx)

    def set_earlier_values(self, instance: Instance, part_number: int): 

        idx_range = self.find_earlier_range(self.earlier_solution['left'])
        max_earlier_time = max(self.earlier_solution["left"]) - self.time_part

        instance["pns"] = len(idx_range)
        instance["max_earlier_time"] = max_earlier_time
        instance["prev_ship_size"] = [self.ship_size[idx + self.earlier_solution["min_index"] + 1] for idx in idx_range]
        instance["prev_which"] = [self.earlier_solution["which"][idx] for idx in idx_range]
        instance["prev_ship_position"] = [self.earlier_solution["ship_position"][idx] for idx in idx_range]
        instance["prev_start"] = [ max(self.earlier_solution["start"][idx] - self.time_part, 0) for idx in idx_range]
        instance["prev_left"] = [self.earlier_solution["left"][idx] - self.time_part for idx in idx_range]

        prev_reclaimers_position = []

        for rec in self.earlier_solution["reclaimers_position"]:
            prev_reclaimers_position.append(rec[self.time_part:max(self.earlier_solution["left"])])

        instance["earlier_reclaimers_position"] = prev_reclaimers_position

        print()
        print("set earlier")
        print("pns: ", len(idx_range))
        print("max_earlier_time: ", max_earlier_time)
        print("prev_ship_size: ", [self.ship_size[idx + self.earlier_solution["min_index"] + 1] for idx in idx_range])
        print("prev_which: ", [self.earlier_solution["which"][idx] for idx in idx_range])
        print("prev start: ",  [ max(self.earlier_solution["start"][idx] - self.time_part, 0) for idx in idx_range])
        print("prev left: ", [self.earlier_solution["left"][idx] - self.time_part for idx in idx_range])
        print()

    def find_range(self, part_number):

        min_time = self.time_part * part_number
        max_time = self.time_part * (part_number + 1) - 1

        min_index = float('inf')
        max_index = -1

        for idx, time in enumerate(self.arrival):
            
            if time >= min_time and idx < min_index:
                min_index = idx
            
            if time <= max_time and idx > max_index:
                max_index = idx

        return (min_index, max_index)
    
    def find_earlier_range(self, left_arr):

        idx_range = []

        for idx, time in enumerate(left_arr):
            
            if time > self.time_part:
                idx_range.append(idx)

        return idx_range

