import random
import matplotlib.pyplot as plt
import math

border = []
num_left = []
immigrants = 1000
for i in range(17):
    print("____________________________")
    print("In iteration",i,"there are",immigrants,"immigrants left")
    num_leave = math.trunc(immigrants * random.random())    
    print(num_leave,"stay at the border")
    immigrants = immigrants - num_leave
    print(immigrants,"keep going")
    border.append(i)
    num_left.append(immigrants)
    print("____________________________")

print("x-axis:",border)
print("y-axis:",num_left)

plt.plot(x, y)
 
# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
 
# giving a title to my graph
plt.title('My first graph!')
 
# function to show the plot
plt.show()