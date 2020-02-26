import pandas as pd
import os,re

#3

#each drug class/group of drugs that are known to cause their variable name
#(ie. drugs with a 1 in death variable are known to cause death, and drugs in
#ss with a 1 are known to cause serotonin syndrome)
#TableA is a merged version of all 3 together in a single DF (used as training data as the outcome variable Y=b0+b1x1+b2x2+b3x3)

def qc(d,denom):
    '''drug use with adverse event / total drug use for each element of X
        This creates an adverse event frequency matrix'''
    dff=base_df[base_df[0]==d]
    return [len(dff[dff['pt']==event])/denom for event in ae]

def drug_n_event(d,denom):
    '''drug use with adverse event / total drug use for each element of X
        This creates an adverse event frequency matrix'''
    dff=df[df['0']==d]
    return [len(dff[dff['pt']==event])/denom for event in ae]

data={i:pd.read_csv(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output\\'+i) for i in os.listdir(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output') if i[-4:]=='.csv'}
df=pd.read_csv('faers_ae_grouping.csv').drop('Unnamed: 0',axis=1)
df1=pd.read_csv(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output\drug_data\drug_var.csv').drop('Unnamed: 0',axis=1)
base_df=pd.read_csv(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\faers_ALL_ae_grouping.csv').drop('Unnamed: 0',axis=1)

keys=list(data.keys())



drugs2=base_df[['prod_ai','drugname']]
drugs2=drugs2.values

drug_idx2=[]
for i in drugs2:
    if i[0]!=i[0]:
        i[0]=i[1]
    drug_idx2.append(i[0])

#dataframe of only 3 AE groups: Cardiac, SS, death, and is used only to increase speed of this script in func
df.drop(['prod_ai','drugname'],inplace=True,axis=1)
df=df.join(df1['0'])

#dataframe of all adverse effects: n=1.04million
base_df.drop(['prod_ai','drugname'],inplace=True,axis=1)
base_df=base_df.join(pd.DataFrame(drug_idx2))

#all drugs list, deduplicated, to be used to iterate over for primary loop
drugs=list(data[keys[0]]['Unnamed: 0'])
ae=set(pd.read_csv('faers_ae_grouping.csv')['pt'])

sys.exit()
#Primary Loop
new_df=[]    
for drug in drugs:
    print(drug)
    denom=drug_idx2.count(drug)
    print(denom)
    result=drug_n_event(drug,denom)
    print(sum(result))
    new_df.append(result)

otp_df=pd.DataFrame(new_df,columns=['Cardiac','SS','Death'],index=drugs)
otp_df.to_csv('AE_frequency.csv')
