import random
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
from scipy import optimize


data = {}


for j in range(10):
    #initialize data
    num_left = [1000]
    border = [0]
    immigrants = 1000
    for i in range(10):
        #avoid division by zero
        if immigrants == 0:
            num_left.append(0)
            border.append(i+1)
        else:    
            #get a random number of immigrants to leave behind, based on a normal distribution
            normal_rand = (sum(np.random.binomial(1, 0.5, immigrants)==0)/immigrants)
            num_leave = math.trunc(immigrants * normal_rand)   
            
            #subtract the number of leavers from the total population
            immigrants = immigrants - num_leave        
            
            #data collection
            border.append(i+1)
            num_left.append(immigrants)
    data["Trial "+str(j+1)] = num_left
    
#exponential regression to find equation of line



#label graph
plt.xlabel('Border #')
plt.ylabel('Number of immigrants left') 
plt.title('Number left at each border')
 
#plot results and lines 
colors = list("rgbcmyrgbcmy")
for imms_left in data.values():
    print(imms_left)
    print(border)
    x = border
    y = imms_left
    plt.scatter(x,y,color="grey")
    plt.plot(x,y,color="grey")

#exponential regression
A_vals = []
B_vals = []
#iterate over y-values from repeated trials to get an average for a and b where y=a*e^bx
for y in data.values():
    x_data = np.array(border)
    y_data = np.array(y)
    n = scipy.optimize.curve_fit(lambda t,a,b: a*np.exp(b*t),  x_data,  y_data,  p0=(1000, -0.5))
    a = n[0][0]
    b = n[0][1]
    A_vals.append(a)
    B_vals.append(b)

#get average a and b values
eqA = sum(A_vals)/len(A_vals)
eqB = sum(B_vals)/len(B_vals)

print("the equation is y=",eqA,"*e^(",eqB,"*x)")
#plot line of best fit
x_1 = np.array(border)
y_1 = eqA * math.e **(eqB * x_1)
plt.plot(x_1, y_1, color="red")
#label=r'$y=round(eqA,2)*e^(round(eqB,3)*x)$'

plt.legend(data.keys())
plt.show()

