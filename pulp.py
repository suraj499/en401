#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pulp import *


# In[2]:


DESTINATIONS = ['D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12','D13','D14','D15'] #creating destinations,origins and vehicles
ORIGINS = ['O1','O2','O3','O4','O5']
VEHICLES = list(range(1,76))


# In[3]:


cbc = {'D1': 52000,         #basic construction cost of destinations
      'D2': 57000,
      'D3': 54600,
      'D4': 49000,
      'D5': 52500,
      'D6': 49000,
      'D7': 45400,
      'D8': 47000,
      'D9': 44000,
      'D10': 56000,
      'D11': 55000,
      'D12': 49000,
      'D13': 53000,
      'D14': 53000,
      'D15': 49500}
do = {}                     #distances of destination of charging station to origin
dd = {}                     #distances of destination of charging station to destinations
for i in range(1,16):
    do[i]={}
    for j in range(1,16):
        do[i].update({'D'+str(j):(int((j-1)/5)+1+(j-1)%5)}) 
for i in range(16,31):
    do[i]={}
    for j in range(1,16):
        do[i].update({'D'+str(j):int((j-1)/5)+1+abs((j-1)%5-(1)%5)})
for i in range(31,46):
    do[i]={}
    for j in range(1,16):
        do[i].update({'D'+str(j):int((j-1)/5)+1+abs((j-1)%5-(2)%5)})

for i in range(46,61):
    do[i]={}
    for j in range(1,16):
        do[i].update({'D'+str(j):int((j-1)/5)+1+abs((j-1)%5-(3)%5)})

for i in range(61,76):
    do[i]={}
    for j in range(1,16):
        do[i].update({'D'+str(j):int((j-1)/5)+1+abs((j-1)%5-(4)%5)})

for k in range(1,16):  
    for i in range(k,61+k,15):
        dd[i]={}
        for j in range(1,16):
            dd[i].update({'D'+str(j):abs(int((k-1)/5)-int((j-1)/5))+abs((k-1)%5-(j-1)%5)})


# In[4]:


prob = LpProblem('charging',LpMinimize)            #defining the lp problem
xdj = LpVariable.dicts('xdj',DESTINATIONS,0,1,LpBinary)     #defining decision variables
ndj = LpVariable.dicts('ndj',DESTINATIONS,0)
yvidj=LpVariable.dicts('yvidj',[(i,j) for i in VEHICLES for j in DESTINATIONS],0,1,LpBinary)


# In[5]:


#objective function
prob += lpSum((cbc[j]+25000)*ndj[j]*0.1174 for j in DESTINATIONS)+lpSum(3000*(do[i][j] + dd[i][j])*yvidj[(i,j)] for i in VEHICLES for j in DESTINATIONS)    


# In[6]:


#adding constraints
for j in DESTINATIONS:
    prob+=lpSum(yvidj[(i,j)] for i in VEHICLES)==1

for j in DESTINATIONS:
    prob+=lpSum(xdj[j])==7

for i in VEHICLES:
    for j in DESTINATIONS:
        prob+= yvidj[(i,j)] <= xdj[j]
    
for j in DESTINATIONS:
    prob+= ndj[j]>=lpSum(yvidj[(i,j)] for i in VEHICLES)


# In[7]:


prob.writeLP('charging.lp')    #solving the lp problem
prob.solve()


# In[ ]:




