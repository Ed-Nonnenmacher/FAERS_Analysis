import pandas as pd
import os,re,math,threading
from scipy.stats import fisher_exact


data={i:pd.read_csv(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output\\'+i) for i in os.listdir(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output') if i[-4:]=='.csv'}
df=pd.read_csv('faers_ae_grouping.csv').drop('Unnamed: 0',axis=1)
df1=pd.read_csv(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output\drug_data\drug_var.csv').drop('Unnamed: 0',axis=1)
base_df=pd.read_csv(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\grand_final_ae.csv').drop('Unnamed: 0',axis=1)


##-------------------------------------ANALYSIS------------------------------------
##Disproportionailty functions

def RR(a,b,c,d):
    '''Reporting Ratio'''
    try:
        return round((a*(a+b+c+d))/((a+c)*(a+b)),4)
    except (ValueError,ZeroDivisionError):
        return 'N/A'

def PRR(a,b,c,d):
    '''Proportional Reporting Ratio'''
    try:
        return round((a/(a+b))/(c/(c+d)),4)
    except (ValueError,ZeroDivisionError):
        return 'N/A'

def ROR(a,b,c,d):
    '''Reporting Odds Ratio'''
    try:
        return round((a/c)/(b/d),4)
    except (ValueError,ZeroDivisionError):
        return 'N/A'

def IC(a,b,c,d):
    '''Information component.  ln(RR) = logbase2 of reporting ratio'''
    try:
        return round(math.log2(RR(a,b,c,d)),4)
    except:
        return 'N/A'
    
def RR_MGPS(a,b,c,d):
    '''Reporting Ratio for (MGPS) multi-item gamma Poisson shrinker'''
    try:
        return round(a/(((a+b)/(a+b+c+d))*(a+b)),4)
    except (ValueError,ZeroDivisionError):
        return 'N/A'



##Objective is to compare a drug to another group of drugs
##Separate file is generate from these next blocks apart from primary loop

##------When analyzing for different drugs, these drugs will be listed as A and B (even though I dont think they should)--------
##------Be sure to swap out base_drug with whatever is in here when changin out evaluation criteria-------



comps={'Bupropion':['Bupropion']}
'''comps={'Trazadone':['Trazadone'],
       'Bupropion':['Bupropion']}'''


 ##Remove Fluoxetine when using it as comparator
 ##Remove Fluoxetine when using it as comparator
'''comps={'All_SSRI':['Fluoxetine','Sertraline','Paroxetine','Fluvoxamine','Citalopram','Escitalopram'],
       'Fluoxetine':['Fluoxetine'],
       'Sertraline':['Sertraline'],
       'Paroxetine':['Paroxetine'],
       'Fluvoxamine':['Fluvoxamine'],
       'Citalopram':['Citalopram'],
       'Escitalopram':['Escitalopram']}'''
 ##Remove Fluoxetine when using it as comparator
 ##Remove Fluoxetine when using it as comparator


'''comps={'All_SNRI':['Desvenlafaxine','Duloxetine','Venlafaxine'],
       'Desvenlafaxine':['Desvenlafaxine'],
       'Duloxetine':['Duloxetine'],
       'Venlafaxine':['Venlafaxine']}'''


'''comps={'all_stimulants':['Atomoxetine','Dexmethylphenidate','Dextroamphetamine','Lisdexamfetamine','Amphetamine/Dextroamphetamine','Amphetamine'],
       'Atomoxetine':['Atomoxetine'],
       'Dexmethylphenidate':['Dexmethylphenidate'],
       'Dextroamphetamine':['Dextroamphetamine'],
       'Lisdexamfetamine':['Lisdexamfetamine'],
       'Amphetamine/Dextroamphetamine':['Amphetamine/Dextroamphetamine'],
       'Amphetamine':['Amphetamine']}'''


'''comps={'all_anti-epileptics':['Lamotrigine','Divalproex','Oxcarbazepine','Topiramate','Clonazepam','Levetiracetam','Carbamazepine','Gabapentin','Valproic Acid','Phenobarbital'],
       'Lamotrigine':['Lamotrigine'],
       'Divalproex':['Divalproex'],
       'Oxcarbazepine':['Oxcarbazepine'],
       'Topiramate':['Topiramate'],
       'Clonazepam':['Clonazepam'],
       'Levetiracetam':['Levetiracetam'],
       'Carbamazepine':['Carbamazepine'],
       'Gabapentin':['Gabapentin'],
       'Valproic Acid':['Valproic Acid'],
       'Phenobarbital':['Phenobarbital']}'''


aes=['Cardiac','Death']
#aes=['Cardiac','Death']

##if stratifying for 1 age follow leave 1 int gap for <> logic
##if no condition, set 0 to 100

L_age=0
U_age=17

base_drug='Fluoxetine'

disp_comps=[]
for i in comps:
    print(i)
    for ae1 in aes:
        a,b,c,d=0,0,0,0
        a=sum([len(base_df[(base_df['0']==cdrug) & (base_df['pt']==ae1)& (base_df['age']>L_age-1) & (base_df['age']<U_age+1)]) for cdrug in comps[i]])
        b=sum([len(base_df[(base_df['0']==cdrug) & (base_df['pt']!=ae1)& (base_df['age']>L_age-1) & (base_df['age']<U_age+1)]) for cdrug in comps[i]])
        c=len(base_df[(base_df['0']==base_drug) & (base_df['pt']==ae1) & (base_df['age']>L_age-1) & (base_df['age']<U_age+1)])
        d=len(base_df[(base_df['0']==base_drug) & (base_df['pt']!=ae1) & (base_df['age']>L_age-1) & (base_df['age']<U_age+1)])
        print(i,ae1,a,b,c,d)
        disp_comps.append([ae1,i,RR(a,b,c,d),PRR(a,b,c,d),ROR(a,b,c,d),round(fisher_exact([[a,b],[c,d]])[0],4),fisher_exact([[a,b],[c,d]])[1],a,b,c,d])

for i in comps:
    a,b,c,d=0,0,0,0
    a=sum([len(base_df[(base_df['0']==cdrug) & (base_df['pt'].isin(aes)) & (base_df['age']>L_age-1) & (base_df['age']<U_age+1)]) for cdrug in comps[i]])
    b=sum([len(base_df[(base_df['0']==cdrug) & (base_df['age']>L_age-1) & (base_df['age']<U_age+1)]) for cdrug in comps[i]])-a
    c=len(base_df[(base_df['0']==base_drug) & (base_df['pt'].isin(aes)) & (base_df['age']>L_age-1) & (base_df['age']<U_age+1)])
    d=len(base_df[(base_df['0']==base_drug) & (base_df['age']>L_age-1) & (base_df['age']<U_age+1)])-c
    print(i,ae1,a,b,c,d)
    disp_comps.append(['All_AE',i,RR(a,b,c,d),PRR(a,b,c,d),ROR(a,b,c,d),round(fisher_exact([[a,b],[c,d]])[0],4),fisher_exact([[a,b],[c,d]])[1],a,b,c,d])


comp_df=pd.DataFrame(disp_comps,columns=['ae','drug','RR','PRR','ROR','Fisher_exactOR','Fisher_exactP','A','B','C','D'])
comp_df.to_csv('disproportionailty_comps_11.csv')



##WILL HAVE TO INCORPORATE DRUG PAIRS, WHERE WE LIST BASE_DRUG ALONG WITH SOME OTHER DRUG OF OUR CHOICE
