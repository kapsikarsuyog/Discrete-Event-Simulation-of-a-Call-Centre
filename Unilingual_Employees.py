import callcenter2 as cc


print('Policy I: Unilingual Employees')
employee_langs = [('Hindi',)]*5 + [('Bengali',)]*2 + [('Marathi',)]*2 + [('Kannada',)]*2 + [('Malayalam',)] + [('Telugu',)]*2 + [('Tamil',)]*2 + [('English',)]*4
(W, U) = cc.run_sim(employee_langs)

#print('Policy II: Multilingual Employees')
'''

#employee_langs = [('English', 'Bengali', 'Hindi')]*5 + [('Malayalam','Telugu','Tamil','English')]*5 + [('Marathi', 'Kannada', 'English', 'Hindi')]*5

(W, U) = cc.run_sim(employee_langs)
'''