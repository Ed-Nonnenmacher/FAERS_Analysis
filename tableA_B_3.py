import pandas as pd
import os,re,math,threading
from scipy.stats import fisher_exact

##3

##each drug class/group of drugs that are known to cause their variable name
##(ie. drugs with a 1 in death variable are known to cause death, and drugs in
##ss with a 1 are known to cause serotonin syndrome)
##TableA is a merged version of all 3 together in a single DF (used as training data as the outcome variable Y=b0+b1x1+b2x2+b3x3)

def qc(d,denom):
    '''drug use with adverse event / total drug use for each element of X
        This creates an adverse event frequency matrix'''
    dff=base_df[base_df['0']==d]
    return [len(dff[dff['pt']==event])/denom for event in ae]

def drug_n_event(d,denom):
    '''drug use with adverse event / total drug use for each element of X
        This creates an adverse event frequency matrix'''
    dff=df[df[0]==d]
    return [len(dff[dff['pt']==event])/denom for event in ae]


##building dataframes
data={i:pd.read_csv(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output\\'+i) for i in os.listdir(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output') if i[-4:]=='.csv'}
df=pd.read_csv('faers_ae_grouping.csv').drop('Unnamed: 0',axis=1)
df1=pd.read_csv(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output\drug_data\drug_var.csv').drop('Unnamed: 0',axis=1)
base_df=pd.read_csv(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\faers_ALL_ae_grouping.csv').drop('Unnamed: 0',axis=1)

keys=list(data.keys())


##dataframe of only 3 AE groups: Cardiac, SS, death, and is used only to increase speed of this script in func
drugs1=df[['prod_ai','drugname']]
drugs1=drugs1.values
drug_idx1=[]
for i in drugs1:
    if i[0]!=i[0]:
        i[0]=i[1]
    drug_idx1.append(i[0])
 
df.drop(['prod_ai','drugname'],inplace=True,axis=1)
df=df.join(pd.DataFrame(drug_idx1))


##dataframe of all adverse effects: n=1.04million
#base_df.drop(['prod_ai','drugname'],inplace=True,axis=1)
#base_df=base_df.join(df1)


##all drugs list, deduplicated, to be used to iterate over for primary loop
drugs=list(data[keys[0]]['Unnamed: 0'])
ae=set(pd.read_csv('faers_ae_grouping.csv')['pt'])

drug_idx2=list(df1['0'])



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
    
comps={'all_ssri':['Sertraline','Paroxetine','Fluvoxamine','Citalopram','Escitalopram','Bupropion'],
       'Bupropion':['Bupropion'],
       'Sertraline':['Sertraline'],
       'Paroxetine':['Paroxetine'],
       'Fluvoxamine':['Fluvoxamine'],
       'Citalopram':['Citalopram'],
       'Escitalopram':['Escitalopram'],
       'Trazadone':['Trazadone']}

aes=['Cardiac','Serotonin syndrome','Death']

##if stratifying for 1 age follow leave 1 int gap for <> logic
##if no condition, set 0-100

L_age=0
U_age=100

base_drug='Fluoxetine'

disp_comps=[]
for i in comps:
    print(i)
    for ae1 in aes:
        a,b,c,d=0,0,0,0
        print(ae1)
        a+=sum([len(base_df[(base_df['0']==cdrug) & (base_df['pt']==ae1)& (base_df['age']>L_age-1) & (base_df['age']<U_age+1)]) for cdrug in comps[i]])
        b+=sum([len(base_df[(base_df['0']==cdrug) & (base_df['pt']!=ae1)& (base_df['age']>L_age-1) & (base_df['age']<U_age+1)]) for cdrug in comps[i]])
        c=len(base_df[(base_df['0']==base_drug) & (base_df['pt']==ae1) & (base_df['age']>L_age-1) & (base_df['age']<U_age+1)])
        d=len(base_df[(base_df['0']==base_drug) & (base_df['pt']!=ae1) & (base_df['age']>L_age-1) & (base_df['age']<U_age+1)])
        disp_comps.append([ae1,i,RR(a,b,c,d),PRR(a,b,c,d),ROR(a,b,c,d),round(fisher_exact([[a,b],[c,d]])[0],4),fisher_exact([[a,b],[c,d]])[1],a,b,c,d])

for i in comps:
    a+=sum([len(base_df[(base_df['0']==cdrug) & (base_df['pt'].isin(aes)) & (base_df['age']>L_age) & (base_df['age']<U_age)]) for cdrug in comps[i]])
    b=sum([len(base_df[(base_df['0']==cdrug) & (base_df['age']>L_age) & (base_df['age']<U_age)]) for cdrug in comps[i]])-a
    c=len(base_df[(base_df['0']==base_drug) & (base_df['pt'].isin(aes)) & (base_df['age']>L_age) & (base_df['age']<U_age)])
    d=len(base_df[(base_df['0']==base_drug) & (base_df['age']>L_age) & (base_df['age']<U_age)])-c
    print(i,a,b,c,d)
    disp_comps.append(['All_AE',i,RR(a,b,c,d),PRR(a,b,c,d),ROR(a,b,c,d),IC(a,b,c,d),RR_MGPS(a,b,c,d),round(fisher_exact([[a,b],[c,d]])[0],4),fisher_exact([[a,b],[c,d]])[1]])


comp_df=pd.DataFrame(disp_comps,columns=['ae','drug','RR','PRR','ROR','Fisher_exactOR','Fisher_exactP','A','B','C','D'])
comp_df.to_csv('disproportionailty_comps_3.csv')



sys.exit()


##------------------------------------Primary Loop------------------------------------

##ORDER OF FUNCTIONS FOR COLUMNS!!!   -------RR_MGPS, RR, PRR, ROR, IC-------

def speed(drug,aes):
    result=[]
    denom=drug_idx2.count(drug)
    result=qc(drug,denom)
    for i in aes:
        a=len(base_df[(base_df['0']==drug) & (base_df['pt']==i)])
        b=len(base_df[(base_df['0']==drug) & (base_df['pt']!=i)])
        c=len(base_df[(base_df['0']!=drug) & (base_df['pt']==i)])
        d=len(base_df[(base_df['0']!=drug) & (base_df['pt']!=i)])
        result=result+[RR_MGPS(a,b,c,d),RR(a,b,c,d),PRR(a,b,c,d),ROR(a,b,c,d),IC(a,b,c,d)]
    return result


new_df=[]    
for drug in drugs:
    print(drug)
    result=[]
        
    denom=drug_idx2.count(drug)
    print(denom)
    result=qc(drug,denom)
    print(sum(result))
    
    #DISPROPORTIONALITY TESTS AGAINST WHOLE POPULATION (5 COLUMNS)
    for i in aes:
        a=len(base_df[(base_df['0']==drug) & (base_df['pt']==i)])
        b=len(base_df[(base_df['0']==drug) & (base_df['pt']!=i)])
        c=len(base_df[(base_df['0']!=drug) & (base_df['pt']==i)])
        d=len(base_df[(base_df['0']!=drug) & (base_df['pt']!=i)])
        result=result+[RR_MGPS(a,b,c,d),RR(a,b,c,d),PRR(a,b,c,d),ROR(a,b,c,d),IC(a,b,c,d)]
    new_df.append(result)
    sys.exit()
    


cols=['Cardiac','SS','Death',
      'Cardiac_RR_MGPS','Cardiac_RR','Cardiac_PRR','Cardiac_ROR','Cardiac_IC',
      'SS_RR_MGPS','SS_RR','SS_PRR','SS_ROR','SS_IC',
      'Death_RR_MGPS','Death_RR','Death_PRR','Death_ROR','Death_IC']

    
print('Storing data...')
otp_df=pd.DataFrame(new_df,columns=['Cardiac','SS','Death'],index=drugs)
otp_df.to_csv('AE_frequency.csv')
print('Job done. =)')
