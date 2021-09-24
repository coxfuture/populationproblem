import random
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
from scipy import optimize
from scipy import stats


data = {}
num_trials = 20
num_borders = 200 
loopct = ((num_trials*num_borders)/100)
for j in range(num_trials):
    #initialize data
    num_left = [1000]
    border = [0]
    immigrants = 1000
    for i in range(num_borders):
        print("test",j,"loop",i,"{:.2f}".format((j*num_borders+i)/(loopct)),"%\ done")
        #avoid division by zero
        if immigrants == 0:
            num_left.append(0)
            border.append(i+1)
        else:    
            #get a random number of immigrants to leave behind, based on a normal distribution
            normal_rand = (sum(np.random.binomial(1, 0.5, math.trunc(immigrants))==0)/immigrants)
            num_leave = math.trunc(immigrants * normal_rand)   
            
            #r = (births-deaths)/population
            #imms = imms*e^(rt)
            r = (0.0002*i)
            immigrants = (immigrants - num_leave) + math.e**(r*i)
            #data collection
            border.append(i+1)
            num_left.append(immigrants)
    data["Trial "+str(j+1)] = num_left
    

plt.xlabel('Border #')
plt.ylabel('Number of immigrants left') 
plt.title('Number left at each border')

colors = list("rgbcmyrgbcmy")
for imms_left in data.values():
    #print(imms_left)
    #print(border)
    x = border
    y = imms_left
    plt.scatter(x,y,color="grey")
    plt.plot(x,y,color="grey")

#exponential regression
A_vals = []
B_vals = []
C_vals = []
#iterate over y-values from repeated trials to get an average for a and b where y=a*e^bx
for y in data.values():
    x_data = np.array(border)
    y_data = np.array(y)
    popt, pcov = scipy.optimize.curve_fit(lambda t,a,b,c: a*np.exp(b*t)+np.exp(c*t),  x_data,  y_data,  p0=(1000, -0.5, 0.02))
    print(popt)
    a = popt[0]
    b = popt[1]
    c = popt[2]
    A_vals.append(a)
    B_vals.append(b)
    C_vals.append(c)

#get average a and b values
eqA = sum(A_vals)/len(A_vals)
eqB = sum(B_vals)/len(B_vals)
eqC = sum(C_vals)/len(C_vals)

print("the equation is y=",eqA,"*e^(",eqB,"*x)+e^(",eqC,"x)")
#plot line of best fit
x_1 = np.array(border)
y_1 = eqA * math.e **(eqB * x_1)+ math.e **(eqC * x_1)
plt.plot(x_1, y_1, color="red")
# x_2 = np.array(border)
# y_2 = 20 + 980 * math.e **(-0.5 * x_2)
# plt.plot(x_2, y_2, color="blue",label="expected")


plt.legend(data.keys())
plt.show()
