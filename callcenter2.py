import salabim as sim
import numpy as np
import pandas as pd
from statistics import mean
from collections import defaultdict

lang_idx = {'Hindi': 0, 'Bengali': 1, 'Marathi': 2, 'Kannada': 3, 'Malayalam': 4, 'Telugu': 5, 'Tamil': 6, 'English': 7}
idx_lang = {v: k for k, v in lang_idx.items()}

class CallGenerator(sim.Component):
	def __init__(self, name='call generator'):
		super().__init__(name=name)
		self.calls_generated = 0
		self.languages = list(lang_idx.keys())
		self.lang_dist = [0.43, 0.09, 0.08, 0.06, 0.03, 0.06, 0.07, 0.18]

	def process(self):
		while True:
			i = np.random.choice(len(self.languages), 1, p=self.lang_dist)[0]
			Call(self.languages[i])
			self.calls_generated += 1
			yield self.hold(sim.Exponential(arr_mean).sample())

class WaitingLine:
	def __init__(self, language):
		self.language = language
		self.queue = sim.Queue()


class Call(sim.Component):
	def __init__(self, language):
		super().__init__()
		self.language = language
		self.arrival_time = env.now()

	def process(self):
		i = lang_idx[self.language]
		self.enter(WaitingLines[i].queue)

		# The call will be taken by the employee who is available, speaks the same language and has the least active time:
		avl_employees = []

		for Employee in Employees:
			if self.language in Employee.languages and Employee.ispassive():
				avl_employees.append(Employee)
		
		if len(avl_employees) > 0:
			min_employee = min(avl_employees, key = lambda x: x.active_time)
			min_employee.activate()
		
		# The patient hangs up after waiting for some time:
		yield self.hold(7 + sim.Exponential(2).sample())
		if self in WaitingLines[i].queue:
			self.leave(WaitingLines[i].queue)
			num_reneged[i] += 1
		else:
			yield self.passivate()


class TeleCaller(sim.Component):
	def __init__(self, *languages):
		super().__init__()
		self.languages = list(languages)
		self.wline_idx = [lang_idx[l] for l in self.languages]
		self.active_time = 0
		self.calls_completed = defaultdict(int)

	def process(self):
		while True:
			passive_condition = True
			for i in self.wline_idx:
				passive_condition = passive_condition and len(WaitingLines[i].queue) == 0

			if passive_condition == True:
				yield self.passivate()

			# Pick the call waiting for the longest time:
			wlines = []
			for i in self.wline_idx:
				if len(WaitingLines[i].queue) != 0:
					wlines.append(WaitingLines[i])

			min_wline = min(wlines, key=lambda x: x.queue[0].arrival_time)
			self.job = min_wline.queue.pop()

			processing_time = sim.Exponential(1).sample() + truncated_normal(proc_mean, proc_sd)

			# Update the active time:
			if processing_time + env.now() <= run_time:
				self.active_time += processing_time
			else:
				self.active_time += run_time - env.now()

			yield self.hold(processing_time)

			self.calls_completed[self.job.language] += 1
			self.job.activate()

def truncated_normal(m, sd):
	r = sim.Normal(m, sd).sample()
	while r < 0:
		r = sim.Normal(m, sd).sample()
	return r

'''
def run_sim(employee_languages, arrival_mean=0.857, processing_mean=6.93255, processing_sd=4, time = 15000, verbose=True, save=None):
	# employee_languages = [('Hindi,'), ('Hindi', 'Bengali'), ...] is a list of tuples of languages of employees.
	global WaitingLines
	global Employees
	global env
	global run_time
	global arr_mean
	global proc_mean
	global proc_sd
	global call_generator
	global run_time
	global num_reneged

	run_time = time
	arr_mean = arrival_mean
	proc_mean = processing_mean
	proc_sd = processing_sd
	num_reneged = [0]*8

	env = sim.Environment(trace=False, random_seed='*')
	call_generator = CallGenerator()
	
	Employees = []
	WaitingLines = [WaitingLine(idx_lang[i]) for i in range(8)]

	for l in employee_languages:
		Employees.append(TeleCaller(*l))

	env.run(till = run_time)

	AvgWaitingTimes = [0]*8
	MaxWaitingTimes = [0]*8
	for i in range(8):
		AvgWaitingTimes[i] = WaitingLines[i].queue.length_of_stay.mean()
		MaxWaitingTimes[i] = WaitingLines[i].queue.length_of_stay.maximum()

	Utilizations = [0]*len(Employees)
	for i, Employee in enumerate(Employees):
		Utilizations[i] = Employee.active_time/run_time*100
	
	WaitingTimeDF = pd.DataFrame({'Avg Waiting Time': AvgWaitingTimes, 'Max Waiting Time': MaxWaitingTimes, 'Calls Lost': num_reneged}, index = list(lang_idx.keys()))
	UtilizationDF = pd.DataFrame({'Languages': [', '.join(l) for l in employee_languages], 'Utilization': Utilizations})
	
	# Display the results:
	if verbose == True:
		print('Waiting Time (minutes):')
		print(WaitingTimeDF)
		print('\nEmployee Utilization (percentage):')
		print(UtilizationDF)

	# Save the output in excel:
	if save is not None:
		writer = pd.ExcelWriter(save)
		WaitingTimeDF.to_excel(writer, sheet_name='Waiting Time')
		UtilizationDF.to_excel(writer, sheet_name='Utilization')
		writer.save()

	return (WaitingTimeDF, UtilizationDF)


def simplify(W, U):
	avgWT = 0
	for i in range(8):
		avgWT += call_generator.lang_dist[i]*W.iloc[i,0]
	
	maxWT = max(W.iloc[:,1])
	avgUtil = mean(U.iloc[:,1])

	return (avgWT, maxWT, avgUtil)
'''

def run_sim(employee_languages, arrival_mean=0.857, processing_mean=7, processing_sd=4, time = 15000, verbose=True, save=None):
	# employee_languages = [('Hindi,'), ('Hindi', 'Bengali'), ...] is a list of tuples of languages of employees.
	global WaitingLines
	global Employees
	global env
	global run_time
	global arr_mean
	global proc_mean
	global proc_sd
	global call_generator
	global run_time
	global num_reneged

	run_time = time
	arr_mean = arrival_mean
	proc_mean = processing_mean
	proc_sd = processing_sd

	env = sim.Environment(trace=False, random_seed='*')
	call_generator = CallGenerator()
	
	Employees = []
	num_reneged = [0]*8
	
	WaitingLines = [WaitingLine(idx_lang[i]) for i in range(8)]

	for l in employee_languages:
		Employees.append(TeleCaller(*l))

	env.run(till = run_time)

	AvgWaitingTimes = [0]*8
	StdWaitingTimes = [0]*8
	MaxWaitingTimes = [0]*8
	AvgQueueLen = [0]*8
	StdQueueLen = [0]*8

	for i in range(8):
		AvgWaitingTimes[i] = WaitingLines[i].queue.length_of_stay.mean()
		MaxWaitingTimes[i] = WaitingLines[i].queue.length_of_stay.maximum()
		StdWaitingTimes[i] = WaitingLines[i].queue.length_of_stay.std()
		AvgQueueLen[i] = WaitingLines[i].queue.length.mean()
		StdQueueLen[i] = WaitingLines[i].queue.length.std()

	Utilizations = [0]*len(Employees)
	for i, Employee in enumerate(Employees):
		Utilizations[i] = Employee.active_time/run_time*100
	
	WaitingTimeDF = pd.DataFrame({'Avg Waiting Time': AvgWaitingTimes, 'Max Waiting Time': MaxWaitingTimes,
		'Std Dev Waiting Time': StdWaitingTimes, 'Avg Calls Waiting': AvgQueueLen,
		'Std Dev Calls Waiting': StdQueueLen, 'Calls Lost': num_reneged}, index = list(lang_idx.keys()))
	
	UtilizationDF = pd.DataFrame({'Languages': [', '.join(l) for l in employee_languages], 'Utilization': Utilizations})
	
	# Display the results:
	if verbose == True:
		print('Waiting Time (minutes):')
		print(WaitingTimeDF)
		print('\nEmployee Utilization (percentage):')
		print(UtilizationDF)

	# Save the output in excel:
	if save is not None:
		writer = pd.ExcelWriter(save)
		WaitingTimeDF.to_excel(writer, sheet_name='Waiting Time')
		UtilizationDF.to_excel(writer, sheet_name='Utilization')
		writer.save()

	return (WaitingTimeDF, UtilizationDF)


if __name__ == '__main__':
	employee_languages = [('Hindi',)]*4 + [('Hindi', 'Marathi')]*2 + [('Bengali',)]*2 + [('Hindi', 'Bengali')] + [('English',)]*2 + [('English','Marathi')]*3 + [('Telugu','Tamil')]*3 + [('Kannada', 'Malayalam')]*3
	run_sim(employee_languages)
	print('Total calls generated = ' + str(call_generator.calls_generated))


