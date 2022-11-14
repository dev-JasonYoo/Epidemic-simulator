from lib import *

## Initialize Person instances
population = [ Person(ID_num, 0, 0, 0) for ID_num in range(100) ]

##corona = Epid(0)
##population[0].set_status(corona)

## Initialize Place instances
square1 = Place('square1', 10, [10, 10], 0, [])
square2 = Place('square2', 10, [10, 10], 0, ['square1'])

##square1_dimension = square1.dimension
##for person in population[:10]:
##    x = randint(0, square1_dimension[0] - 1)
##    y = randint(0, square1_dimension[1] - 1)
##    square1.field[x][y] = person

n = 10

assign(population[:n], square1)
print_field(square1)

for _ in range(30):
    square1.field = update_position_in_place(population[:n], square1)
    print_field(square1)
    input()
