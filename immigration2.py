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
    for i in range(20):
        #avoid division by zero
        if immigrants == 0:
            num_left.append(0)
            border.append(i+1)
        else:    
            #get a random number of immigrants to leave behind, based on a normal distribution
            normal_rand = (sum(np.random.binomial(1, 0.5, immigrants)==0)/immigrants)
            num_leave = math.trunc(immigrants * normal_rand)   
            
            #subtract the number of leavers from the total population
            immigrants = immigrants - num_leave + 10
            #data collection
            border.append(i+1)
            num_left.append(immigrants)
    data["Trial "+str(j+1)] = num_left
    

#label graph
plt.xlabel('Border #')
plt.ylabel('Number of immigrants left') 
plt.title('Number left at each border')
 
# #plot results and lines 
# colors = list("rgbcmyrgbcmy")
# for imms_left in data.values():
#     #print(imms_left)
#     #print(border)
#     x = border
#     y = imms_left
#     plt.scatter(x,y,color="grey")
#     plt.plot(x,y,color="grey")

# #average y-data to avoid ln(0) in curve fitting step
# y_lists = np.array([],int)
# for l in data.values():    
#     l_array = np.array(l)
#     y_lists = np.concatenate([y_lists,l_array],axis=0)
# #reshape concatenated array into the format i need

# y_lists = y_lists.reshape(20,21).astype(float)
# average_y = np.average(y_lists,axis=0)
# #print(average_y)

# #exponential regression
# A_vals = []
# B_vals = []
# #curve fitting using ln
# x_data = np.array(border)
# y_data = list(np.log(average_y.astype(float)))
# #print("x data is",x_data,"y data is",y_data)
# #print(y_data)
# #for i in y_data:
# #    print(i)
# #slope,intercept
# b, A_log, _r, _p, _se = scipy.stats.linregress(x_data, y_data)
# a = np.exp(A_log)
# print("a is",a,"b is",b)

# print("the equation is y=",a,"*e^(",b,"*x)")
# #plot line of best fit
# x_1 = np.array(border)
# y_1 = a * math.e **(b * x_1)
# plt.plot(x_1, y_1, color="red")
# x_2 = np.array(border)
# y_2 = 20 + 980 * math.e **(-0.5 * x_2)
# plt.plot(x_2, y_2, color="blue",label="expected")
# #label=r'$y=round(eqA,2)*e^(round(eqB,3)*x)$'

#plot results and lines 
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
    popt, pcov = scipy.optimize.curve_fit(lambda t,a,b,c: a*np.exp(b*t)+c,  x_data,  y_data,  p0=(1000, -0.5, 20))
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

print("the equation is y=",eqA,"*e^(",eqB,"*x)+",eqC)
#plot line of best fit
x_1 = np.array(border)
y_1 = c + eqA * math.e **(eqB * x_1)
plt.plot(x_1, y_1, color="red")
x_2 = np.array(border)
y_2 = 20 + 980 * math.e **(-0.5 * x_2)
plt.plot(x_2, y_2, color="blue",label="expected")


plt.legend(data.keys())
plt.show()

