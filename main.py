import random
import copy
class State:
    def __init__(self, route:[], distance:int=0):
        self.route = route
        self.distance = distance
    def __eq__(self, other):
        for i in range(len(self.route)):
            if(self.route[i] != other.route[i]):
                return False
        return True
    def __lt__(self, other):
         return self.distance < other.distance
    def __repr__(self):
        return ('({0},{1})\n'.format(self.route, self.distance))
    def copy(self):
        return State(self.route, self.distance)
    def deepcopy(self):
        return State(copy.deepcopy(self.route), copy.deepcopy(self.distance))
    def update_distance(self, matrix, home):
        
        self.distance = 0
        from_index = home
        for i in range(len(self.route)):
            self.distance += matrix[from_index][self.route[i]]
            from_index = self.route[i]
        self.distance += matrix[from_index][home]
class City:
    def __init__(self, index:int, distance:int):
        self.index = index
        self.distance = distance
    def __lt__(self, other):
         return self.distance < other.distance
def get_random_solution(matrix:[], home:int, city_indexes:[], size:int, use_weights=False):
    cities = city_indexes.copy()
    cities.pop(home)
    population = []
    for i in range(size):
        if(use_weights == True):
            state = get_random_solution_with_weights(matrix, home)
        else:
            random.shuffle(cities)
            state = State(cities[:])
            state.update_distance(matrix, home)
        population.append(state)
    population.sort()
    return population[0]
def get_best_solution_by_distance(matrix:[], home:int):
    
    route = []
    from_index = home
    length = len(matrix) - 1
    while len(route) < length:
        row = matrix[from_index]
        cities = {}
        for i in range(len(row)):
            cities[i] = City(i, row[i])
        del cities[home]
        for i in route:
            del cities[i]
        sorted = list(cities.values())
        sorted.sort()
        from_index = sorted[0].index
        route.append(from_index)
    state = State(route)
    state.update_distance(matrix, home)
    return state
def get_random_solution_with_weights(matrix:[], home:int):
    
    route = []
    from_index = home
    length = len(matrix) - 1
    while len(route) < length:
        row = matrix[from_index]
        cities = {}
        for i in range(len(row)):
            cities[i] = City(i, row[i])
        del cities[home]
        for i in route:
            del cities[i]
        total_weight = 0
        for key, city in cities.items():
            total_weight += city.distance
        weights = []
        for key, city in cities.items():
            weights.append(total_weight / city.distance)
        from_index = random.choices(list(cities.keys()), weights=weights)[0]
        route.append(from_index)
    state = State(route)
    state.update_distance(matrix, home)
    return state
def mutate(matrix:[], home:int, state:State, mutation_rate:float=0.01):
    
    mutated_state = state.deepcopy()
    for i in range(len(mutated_state.route)):
        if(random.random() < mutation_rate):
            j = int(random.random() * len(state.route))
            city_1 = mutated_state.route[i]
            city_2 = mutated_state.route[j]
            mutated_state.route[i] = city_2
            mutated_state.route[j] = city_1
    mutated_state.update_distance(matrix, home)
    return mutated_state
def hill_climbing(matrix:[], home:int, initial_state:State, max_iterations:int, mutation_rate:float=0.01):
    best_state = initial_state
    iterator = 0
    while True:
        neighbor = mutate(matrix, home, best_state, mutation_rate)
        if(neighbor.distance >= best_state.distance):
            iterator += 1
            if (iterator > max_iterations):
                break
        if(neighbor.distance < best_state.distance):
            best_state = neighbor
    return best_state
def main():



    # cities = ['New York', 'Los Angeles', 'Chicago', 'Minneapolis', 'Denver', 'Dallas', 'Seattle', 'Boston', 'San Francisco', 'St. Louis', 'Houston', 'Phoenix', 'Salt Lake City']
    # city_indexes = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    # home = 2 # Chicago
    # max_iterations = 1000
    # matrix = [[0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
    #         [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
    #         [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
    #         [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
    #         [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
    #         [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
    #         [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
    #         [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
    #         [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
    #         [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
    #         [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
    #         [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
    #         [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0]]



    cities = ['Ternopil', 'Lviv', 'Kyiv', 'Odessa']
    city_indexes = [0,1,2,3]
    home = 0
    max_iterations = 4
    matrix = [[0   , 135 , 600, 1000],
              [135 , 0   , 735, 1100],
              [600 , 735 , 0  , 400 ],
              [1000, 1100, 400, 0   ]]



    state = get_best_solution_by_distance(matrix, home)
    print('-- Best solution by distance --')
    print(cities[home], end='')
    for i in range(0, len(state.route)):
       print(' -> ' + cities[state.route[i]], end='')
    print(' -> ' + cities[home], end='')
    print('\n\nTotal distance: {0} miles'.format(state.distance))
    print()
    state = get_random_solution(matrix, home, city_indexes, 100)
    print('-- Best random solution --')
    print(cities[home], end='')
    for i in range(0, len(state.route)):
       print(' -> ' + cities[state.route[i]], end='')
    print(' -> ' + cities[home], end='')
    print('\n\nTotal distance: {0} miles'.format(state.distance))
    print()
    state = get_random_solution(matrix, home, city_indexes, 100, use_weights=True)
    print('-- Best random solution with weights --')
    print(cities[home], end='')
    for i in range(0, len(state.route)):
       print(' -> ' + cities[state.route[i]], end='')
    print(' -> ' + cities[home], end='')
    print('\n\nTotal distance: {0} miles'.format(state.distance))
    print()
    state = get_best_solution_by_distance(matrix, home)
    state = hill_climbing(matrix, home, state, 1000, 0.1)
    print('-- Hill climbing solution --')
    print(cities[home], end='')
    for i in range(0, len(state.route)):
       print(' -> ' + cities[state.route[i]], end='')
    print(' -> ' + cities[home], end='')
    print('\n\nTotal distance: {0} miles'.format(state.distance))
    print()
if __name__ == "__main__": main()