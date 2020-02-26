import pandas as pd
#1
#This files purpose is to reclassify diseases as a more broad category.
#This is done by iterating over the dataframe, and checking if the 6th item in each row is within the predefined list
#Each predefined list is manually created and curated by user.
#Each item in each predefined list should be spelled exactly how it is in FAERS "pt"
#End of script, a new array is created from the original, but only keeping records that list one of the new groups just created
#    ^  basically everything is stripped except for the adverse events of interest


#To increase total data size/more rows, increase the size of groups by adding in more criteria (like expanding cardiac to be more broad by including additional cardiac AE's)



def check(los):
	if los[6] in cardiac:
		los[6]='Cardiac'
	return los

'''def combo_pt(sub_df):
	if len(sub_df[(sub_df['pt']=='Seizure') | (sub_df['pt']=='Muscle rigidity')])>2:
		return sub_df.replace({'Seizure':'Serotonin syndrome','Muscle rigidity':'Serotonin syndrome'})
	if len(sub_df[(sub_df['pt']=='Seizure') | (sub_df['pt']=='Muscle spasticity')])>2:
		return sub_df.replace({'Seizure':'Serotonin syndrome','Muscle spasticity':'Serotonin syndrome'})
	else:
		return sub_df
'''

df=pd.read_csv(r'faers_base.csv',low_memory=False)
#dfd=pd.DataFrame(columns='primaryid	caseid	age	sex	occr_country	prod_ai	pt	drugname'.split('\t'))

#in order to begin grouping diseases into categories, build your lists of disease.
#Note:  The must be present in your raw data frame from FAERS.
#Note:  Functionality for disease combos is in combo_pt  (there are no cases so far with both)

cardiac=['Acute cardiac event',
         'Cardiac arrest','Sudden death','Cardiac death',
         'Arrhythmia','Cardiac arrest','Cardiac arrest neonatal','Sudden cardiac death']
#ss=['Serotonin syndrome','Muscle rigidity']
death=['Sudden death','Sudden infant death syndrome','Accidental death',
       'Brain death','Premature baby death','Foetal death','Apparent death',
       'Death neonatal']
print('beginning reclassifciation')
cases=list(set(df['caseid']))

'''
for i in cases:
	dfd=pd.concat([dfd,combo_pt(df[df['caseid']==i])])'''
	
print('done reclassifying SS')
#df=dfd

#turn into an array
arr=[list(i) for i in df.values]
before=[i[6] for i in arr]

for i in arr:
        if i[6] in cardiac:
                i[6]='Cardiac'
#        if i[6] in ss:
#                i[6]='Serotonin syndrome'
        if i[6] in death:
                i[6]='Death'
                
after=[i[6] for i in arr]        
print('Cardiac:  (before: %d) | (after: %d)'%(before.count('Cardiac'),after.count('Cardiac')))
#print('Serotonin syndrome:  (before: %d) | (after: %d)'%(before.count('Serotonin syndrome'),after.count('Serotonin syndrome')))
print('Death:  (before: %d) | (after: %d)'%(before.count('Death'),after.count('Death')))

df1=pd.DataFrame(arr,columns=['primaryid', 'caseid', 'age', 'sex', 'occr_country','prod_ai', 'pt',  'drugname'])

df1.to_csv('faers_ALL_ae_grouping_altered_cardiac.csv')

#this is done to trim the data down to increase speed and efficiency of entire system and SHOULD NOT BE USED
#FOR ANYTHING ELSE EXCEPT FOR CREATING AE FREQUENCY MATRIX
final_df=df1[(df1['pt']=='Cardiac') | (df1['pt']=='Death')]
final_df.to_csv('faers_ae_grouping_altered_cardiac.csv')
