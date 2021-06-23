from case_generator import case_gen

import matplotlib.pyplot as plt
import numpy as np
import math


coords = case_gen()[0]

hub = coords[0]

line_weights = {}

axes = plt.gca()
axes.set_xlim([0,70])
axes.set_ylim([-10,60])



for i in range(0,180,5):
    slope = math.tan(i*math.pi/180)
    leftweight = 0
    rightweight = 0

    for village in coords:
        if (village[1]-hub[1])-slope*(village[0]-hub[0]) >= 0:
            leftweight = leftweight + 1

        elif (village[1]-hub[1])-slope*(village[0]-hub[0]) < 0:
            rightweight = rightweight + 1
    
    line_weight = abs(leftweight-rightweight)

    line_weights[(i,slope)] = line_weight

    # Create the vectors X and Y
    x = np.array(range(100))
    y = slope*(x-hub[0])+hub[1]




    # Create the plot
    plt.plot(x,y)

x_coords = []
y_coords = []

for village in coords:
    x_coords.append(village[0])
    y_coords.append(village[1])


plt.scatter(x_coords,y_coords)
#plt.plot(x_coords,y_coords)
plt.plot(hub[0],hub[1])


print(line_weights)


# Show the plot
plt.show()





