import random
import callcenter as cc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# n = 30 peak cycles will be simulated:
n = 30

MaxWaitTimes = np.zeros((n,8))
AvgWaitTimes = np.zeros((n,8))

# Multiligual:
#employee_langs = [('English', 'Bengali', 'Hindi')]*5 + [('Malayalam','Telugu','Tamil','English')]*5 + [('Marathi', 'Kannada', 'English', 'Hindi')]*5

# Unilingual:
#employee_langs = [('Hindi',)]*7 + [('Bengali',)]*3 + [('Marathi',)]*3 +[ ('Kannada',)]*2+ [('Malayalam',)]*2+ [('Telugu',)]*3+ [('Tamil',)]*3 + [('English',)]*4 
employee_langs = [('Hindi',)]*4 + [('Bengali','Hindi')]*3 + [('Marathi','Hindi')]*3 +[ ('Kannada',)]*2+ [('Malayalam',)]*1 +[('Malayalam','English')]*1+ [('Telugu','Kannada')]*1+ [('Telugu',)]*2 + [('Tamil','English')]*1+ [('Tamil',)]*2 + [('English',)]*2
#employee_langs = [('Hindi',)]*5 + [('Bengali',)]*2 + [('Marathi',)]*2 +[ ('Kannada',)]*2+ [('Malayalam',)]*2+ [('Telugu',)]*2+ [('Tamil',)]*2 + [('English',)]*3 
# Bilingual:

#employee_langs = [('Hindi','Malayalam')]*5 + [('Bengali','Telugu')]*3 + [('Marathi','Kannada')]*3 + [('English', 'Tamil')]*4 


ind1 = int((random.random())*len(employee_langs))
ind2 = int((random.random())*len(employee_langs))
del employee_langs[ind1]
del employee_langs[ind2]	


n_employees = len(employee_langs)

Utils = np.zeros((n,n_employees))

for i in range(n):
	(W, U) = cc.run_sim(employee_langs, time=480, verbose=False)
	MaxWaitTimes[i,:] = np.transpose(np.array(W.iloc[:,1]))
	AvgWaitTimes[i,:] = np.transpose(np.array(W.iloc[:,0]))
	Utils[i,:] = np.transpose(np.array(U.iloc[:,1]))

# Compute the maximum of the maximum waiting times ():
MaxMaxWaitTimes = np.max(MaxWaitTimes, axis=0)

# Compute the average of the average waiting times:
AvgAvgWaitTimes = np.mean(AvgWaitTimes, axis=0)
AvgUtils = np.mean(Utils, axis=0)

D1 = pd.DataFrame({'Average Waiting Time': AvgAvgWaitTimes, 'Maximum Waiting Time': MaxMaxWaitTimes}, index=list(cc.lang_idx.keys()))
D2 = pd.DataFrame({'Languages': [', '.join(l) for l in employee_langs], 'Average Utilization': AvgUtils})

# Display the results:
print(D1)
print(D2)

'''
save = False
if save == True:
	writer = pd.ExcelWriter('output.xlsx')
	D1.to_excel(writer, sheet_name='Waiting Time')
	D2.to_excel(writer, sheet_name='Utilization')
	writer.save()
'''

# Plot the histograms of maximum waiting times:
plt.figure()
for i in range(8):
	plt.subplot(3,3,i+1)
	plt.hist(MaxWaitTimes[:,i], bins=25)
	plt.xlabel('Max Waiting Time (minutes)')
	plt.ylabel('Frequency')
	plt.title(cc.idx_lang[i])
plt.tight_layout()
plt.show()
