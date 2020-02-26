import pandas as pd
import os,re,sys,csv

#2

#The purpose of this .py is to create outcome lists/columns
#We must create a single Series of values   1 or 0   throughout a list of all unique drugs in base DF
#To do this, we must ierate over a set of unique drugs, checking if each drug is within our group of interest

#THIS MUST BE DONE AFTER BUILDING YOUR BASE DF#THIS MUST BE DONE AFTER BUILDING YOUR BASE DF#THIS MUST BE DONE AFTER BUILDING YOUR BASE DF
#THIS MUST BE DONE AFTER BUILDING YOUR BASE DF#THIS MUST BE DONE AFTER BUILDING YOUR BASE DF#THIS MUST BE DONE AFTER BUILDING YOUR BASE DF



def from_Drug(str_,los):
    for x in los:
        reg=re.compile(r'.*%s.*'%x,re.IGNORECASE)
        if reg.search(str_):
            return 1
    else:
        return 0

def drug_consol(str_,los):
    if str_==str_:
        for x in los:
            reg=re.compile(r'.*%s.*'%los[x],re.IGNORECASE)
            if reg.search(str_):
                return x
        else:
            return str_
    else:
        return str_


drug_classes={'ssri':['FLUOXETINE','SERTRALINE','PAROXETINE','fluvoxamine','CITALOPRAM','escitalopram'],
              'snri':['desvenlafaxine','duloxetine','venlafaxine'],
              'beta2':['albuterol','levalbuterol','formoterol','salmeterol'],
              'stimulants':['methylphenidate','dexmethylphenidate','dextroamphetamine','lisdexamfetamine',
           'amphetamine','atomoxetine'],
              'prot_pmp_inh':['esomeprazole','lansoprazole','omeprazole','pantoprazole'],
              'opioids':['codeine','oxycodone','hydrocodone','hydromorphone','morphine','tramadol','fentanyl']
                }



df=pd.read_csv('faers_ALL_ae_grouping.csv')

#unordered list of unique drugs CURRENTLY COMMENTED OUT AS WE ONLY NEED TO CLEAN DRUG NAMES
'''drugs=df[['prod_ai','drugname']]

#some earlier years did not have prod_ai as a variable, so substituting in drugname to fillin gaps and limit nan's
#1: We create an array of all drug_ai & drugnames
drugs=drugs.values

#2: ----------Objective: To marry together both prod_ai and drugname columns----------

#We iterate over the list, replacing the first item of each iteration IF AND ONLY IF the first item == NAN
#this is done by if i[0]!=i[0] because nan cannot equal to itself
#If i[0]!=i[0] then replace i[0] with i[1] (replacing prod_ai with drugname
drug_idx=[]

for i in drugs:
    if i[0]!=i[0]:
        i[0]=i[1]
    drug_idx.append(i[0])
'''
#3
#----------Objective: to create a single drug name for each drug we are focusing on (ie. Buproprion)
#In this block is to clean dirty data inputs within drug information for the drugs we are focusing
#we are unifying many inconsistent drug labels with a regular expression
print('Drug cleaning',end='')
drug_cleaning={'Methylphenidate':'(?<!DEX)methyl ?[phf]{1,2}en','Dexmethylphenidate':'dexmethyl ?[phf]{1,2}en'}

print('.',end='')
drug_idx=[drug_consol(i,drug_cleaning) for i in drug_idx]
print('..',end='')



pd.DataFrame(drug_idx).to_csv(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output\drug_data\drug_var.csv')
print('.',end='')
drug_idx={i for i in drug_idx if i==i}
print('..',end='')
print('  Data managment done.  Now generating files...')

#3: Now we begin to check the deduplicated list of drugs and decide if they belong to our output variables or not.

for class_ in drug_classes:
    df_otp=pd.DataFrame([from_Drug(i,drug_classes[class_]) for i in drug_idx],
                    columns=['Y'],
                    index=drug_idx)
    print(class_,len(df_otp))
    print(df_otp['Y'].value_counts())
    df_otp.to_csv(f'C:\\Users\\enonnenmacher\\AppData\\Local\\Programs\\Python\\Python37\\faers_data\\output\\{class_}.csv')
print('Job done. =)')
#import tableA_B_3
