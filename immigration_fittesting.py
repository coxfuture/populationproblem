import random
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
from scipy import optimize
from scipy import stats


data = {}


for j in range(20):
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
    

#label graph
plt.xlabel('Border #')
plt.ylabel('Number of immigrants left') 
plt.title('Number left at each border')
 
#plot results and lines 
colors = list("rgbcmyrgbcmy")
for imms_left in data.values():
    #print(imms_left)
    #print(border)
    x = border
    y = imms_left
    plt.scatter(x,y,color="grey")
    plt.plot(x,y,color="grey")

#average y-data to avoid ln(0) in curve fitting step
y_lists = np.array([],int)
for l in data.values():    
    l_array = np.array(l)
    y_lists = np.concatenate([y_lists,l_array],axis=0)
#reshape concatenated array into the format i need
y_lists = y_lists.reshape(20,11).astype(float)
average_y = np.average(y_lists,axis=0)
#print(average_y)

#exponential regression
A_vals = []
B_vals = []
#curve fitting using ln
x_data = np.array(border)
y_data = np.log(list(average_y.astype(float)))
b, A_log, _r, _p, _se = scipy.stats.linregress(x_data, y_data)
a = np.exp(A_log)
#b, A_log = np.polyfit(x_data, y_data, 1)

#print("a and b values :",A_vals,B_vals)
#get average a and b values
# eqA = sum(A_vals)/len(A_vals)
# eqB = sum(B_vals)/len(B_vals)

print("the equation is y=",a,"*e^(",b,"*x)")
#plot line of best fit
x_1 = np.array(border)
y_1 = a * math.e **(b * x_1)
plt.plot(x_1, y_1, color="red")
x_2 = np.array(border)
y_2 = 1000 * math.e **(-0.69 * x_2)
plt.plot(x_2, y_2, color="blue",label="expected")
#label=r'$y=round(eqA,2)*e^(round(eqB,3)*x)$'

plt.legend(data.keys())
plt.show()

