import callcenter as cc
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

# Plotting the no. of employees (unilingual) and average waiting times:
def plot1():
	AvgWT = np.zeros((8,8))
	for n in range(8):
		employee_langs = [('Hindi',),('Bengali',),('Marathi',),('Kannada',),('Telugu',),('Malayalam',),('Tamil',),('English',)]*(n+2)
		(W,U) = cc.run_sim(employee_langs, verbose=False)
		AvgWT[:,n] = np.array(W.iloc[:,0])

	x_range = [i+2 for i in range(8)]
	plt.figure()
	for i in range(8):
		plt.subplot(2,2,i%4 +1)
		plt.plot(x_range, AvgWT[i,:], 'o-')
		plt.xlabel('No. of Employees')
		plt.ylabel('Avg. Waiting Time (minutes)')
		plt.title(cc.idx_lang[i])
		if i == 3:
			plt.tight_layout()
			plt.show()
			plt.figure()
	plt.tight_layout()
	plt.show()

# Effect of changing the call arrival rate on the multilingual configuration:
def plot2():
	AvgWT = [0]*16
	AvgUtil = [0]*16
	arrival_means = [0.5 + 0.025*i for i in range(16)]
	employee_langs = [('English', 'Bengali', 'Hindi')]*5 + [('Malayalam','Telugu','Tamil','English')]*5 + [('Marathi', 'Kannada', 'English', 'Hindi')]*5
	for n in range(16):
		(W, U) = cc.run_sim(employee_langs, arrival_mean=arrival_means[n], verbose=False)
		(AvgWT[n], _, AvgUtil[n]) = cc.simplify(W, U)

	plt.figure()
	plt.plot(arrival_means, AvgWT, 'o-')
	plt.xlabel('Average inter-arrival time (minutes)')
	plt.ylabel('Average waiting time')
	plt.show()

	plt.figure()
	plt.plot(arrival_means, AvgUtil, 'o-')
	plt.xlabel('Average inter-arrival time (minutes)')
	plt.ylabel('Average utilization of employees (percentage)')
	plt.show()


if __name__ == '__main__':
	#plot1()
	plot2()
