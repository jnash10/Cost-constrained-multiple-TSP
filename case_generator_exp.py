#given integers n, m generate n random points in a mxm matrix. 
#return both - the n points, and a distance matrix for those n points

from random import randint
import numpy as np

n = int(input("how many disctricts do you want(enter integer): "))
m = 50
cities = []

for i in range(0,n) :
    cities.append((randint(0,m),randint(0,m)))

#cities = np.array(cities)

#print(cities[0],cities[1])

def dist(a, b):
    return int(((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2))

#print(dist(cities[0],cities[1]))

dist_matrix = []

for city in cities:
    city_dist = []
    for i in range(0,n):
        city_dist.append(dist(city,cities[i]))
    #print(type(city_dist), city_dist)
    dist_matrix.append(city_dist)

dist_matrix = np.array(dist_matrix)

print("\nthe cities are: \n\n", cities)

print("\n \n \n \nthe distance matrix is: \n")
print(np.array2string(dist_matrix, separator = ', '))
