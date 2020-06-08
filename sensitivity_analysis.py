import callcenter as cc
import pandas as pd
import numpy as np

# Sensitivity Analysis

# Some employees are be added to the multilingual employee configuration:

employee_langs = [('English', 'Bengali', 'Hindi')]*5 + [('Malayalam','Telugu','Tamil','English')]*5 + [('Marathi', 'Kannada', 'English', 'Hindi')]*5

configurations1 = [employee_langs + [('English', 'Bengali', 'Hindi')], employee_langs + [('English', 'Bengali', 'Hindi')]*2, 
	employee_langs + [('Malayalam','Telugu','Tamil','English')], employee_langs + [('Malayalam','Telugu','Tamil','English')]*2, 
	employee_langs + [('Marathi', 'Kannada', 'English', 'Hindi')], employee_langs + [('Marathi', 'Kannada', 'English', 'Hindi')]*2, 
	employee_langs + [('Hindi', 'Marathi', 'English')], employee_langs + [('English', 'Tamil', 'Telugu')], employee_langs + [('Hindi', 'Bengali')], employee_langs + [('Hindi', 'Bengali')]*2,
	employee_langs + [('English', 'Telugu')], employee_langs + [('English', 'Telugu')]*2]

n = len(configurations1)

increments = np.expand_dims([len(config)-len(employee_langs) for config in configurations1],axis=1)

(W_def, U_def) = cc.run_sim(employee_langs, verbose=False)
avg_W_def = np.transpose(W_def.iloc[:,0])

avg_W = np.zeros((n,8))
percent_dec = np.zeros((n,8))

for i, config in enumerate(configurations1):
	(W,U) = cc.run_sim(config, verbose=False)
	avg_W[i,:] = np.transpose(W.iloc[:,0])
	percent_dec[i, :] =(avg_W_def - avg_W[i,:])/avg_W_def * 100

employee_added_langs =[', '.join(l) for l in [('English', 'Bengali', 'Hindi')]*2 + [('Malayalam','Telugu','Tamil','English')]*2 + [('Marathi', 'Kannada', 'English', 'Hindi')]*2 + [('Hindi', 'Marathi', 'English')] + [('English', 'Tamil', 'Telugu')] + [('Hindi', 'Bengali')]*2 + [('English', 'Telugu')]*2]

avg_W_df = pd.DataFrame(data=np.c_[increments, avg_W], columns = ['No. of emp added']+list(cc.lang_idx.keys()), 
	index=employee_added_langs)

perc_dec_W_df = pd.DataFrame(data=np.c_[increments, percent_dec], columns = ['No. of emp added']+list(cc.lang_idx.keys()), 
	index=employee_added_langs)

#print('Effect of adding employees to the multilingual configuration on the average waiting time (minutes):\n')
#print(avg_W_df)

print('Percentage decrease in average waiting time after adding employees to the multilingual configuration:\n')
print(perc_dec_W_df)

# Some employees are removed from the multilingual employee configuration:
c1 = employee_langs.copy()
c2 = employee_langs.copy()
c3 = employee_langs.copy()

c1.remove(('English', 'Bengali', 'Hindi'))
c4 = c1.copy()
c4.remove(('English', 'Bengali', 'Hindi'))
c2.remove(('Malayalam','Telugu','Tamil','English'))
c5 = c2.copy()
c5.remove(('Malayalam','Telugu','Tamil','English'))
c3.remove(('Marathi', 'Kannada', 'English', 'Hindi'))
c6 = c3.copy()
c6.remove(('Marathi', 'Kannada', 'English', 'Hindi'))

configurations2 = [c1,c4,c2,c5,c3,c6]

employee_added_langs_2 = [', '.join(l) for l in [('English', 'Bengali', 'Hindi')]*2 + [('Malayalam','Telugu','Tamil','English')]*2 + [('Marathi', 'Kannada', 'English', 'Hindi')]*2]

n2 = len(configurations2)

decrements = np.expand_dims([1,2,1,2,1,2], axis=1)

avg_W_2 = np.zeros((n2,8))
percent_inc = np.zeros((n2,8))

for i, config in enumerate(configurations2):
	(W,U) = cc.run_sim(config, verbose=False)
	avg_W_2[i,:] = np.transpose(W.iloc[:,0])
	percent_inc[i, :] = (-avg_W_def + avg_W_2[i,:])/avg_W_def * 100

avg_W_df_2 = pd.DataFrame(data=np.c_[decrements, avg_W_2], columns = ['No. of emp removed']+list(cc.lang_idx.keys()), 
	index=employee_added_langs_2)

perc_inc_W_df = pd.DataFrame(data=np.c_[decrements, percent_inc], columns = ['No. of emp removed']+list(cc.lang_idx.keys()), 
	index=employee_added_langs_2)

print('Percentage increase in average waiting time after removing employees from the multilingual configuration:\n')
print(perc_inc_W_df)


save = True
if save == True:
	writer = pd.ExcelWriter('output.xlsx')
	perc_dec_W_df.to_excel(writer, sheet_name='Adding Employees')
	perc_inc_W_df.to_excel(writer, sheet_name='Removing Employees')
	writer.save()
