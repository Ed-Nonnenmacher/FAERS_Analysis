import os,sys,re
import pandas as pd
#0


def from_dat(file):
    file=open(data_dir+'\\'+file)
    dat=[i.split('$') for i in file.read().split('\n')]
    return pd.DataFrame(data=dat[1:],columns=dat[0])

def file_finder(listdir):
    files=[]
    for i in listdir:
        if drug_reg.search(i):
            files.append(i)
        if demo_reg.search(i):
            files.append(i)
        if reac_reg.search(i):
            files.append(i)
    return files

keep_cols=['primaryid', 'caseid', 'age',
           'occr_country','pt','drugname']
try_cols=['sex','prod_ai','primaryid', 'caseid', 'age',
           'occr_country','pt','drugname']


base='C:\\Users\\enonnenmacher\\AppData\\Local\\Programs\\Python\\Python37\\faers_data\\data\\'
all_=os.listdir(base)
#file order is important to start with demo, merge reac into it, then merge that output with drug file

#regex for identifying dfs of interest
drug_reg=re.compile('drug.*\.txt',re.IGNORECASE)
demo_reg=re.compile('demo.*\.txt',re.IGNORECASE)
reac_reg=re.compile('reac.*\.txt',re.IGNORECASE)


storage_dir=r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output\data\\'



for i in os.listdir(base):
    print('Working on '+i)
    file=os.listdir(base+i)
    data_dir=base+i+'\\'+file[0]
    files=os.listdir(data_dir)
    data=file_finder(files)
    print('Extracting data',end='')
    print('.',end='')
    d=from_dat(data[0])
    print('..',end='')
    d1=from_dat(data[1])
    print('..',end='')
    d2=from_dat(data[2])
    print('..',end='')
    print('Data in '+i+' extracted succesfully.')
    print(len(d),len(d1),len(d2))
    print('Merging',end='')
    print('.',end='')
    df=pd.merge(d,d1,how='inner',on='caseid')
    print('..',end='')
    df=pd.merge(df,d2,how='inner',on='caseid')
    print('...',end='')
    print(len(df))
    print('Final cleanup...')
    df=df[df['age']!='']
    df=df[df['age'].astype(str)!='None']
    df=df[df['age']!='FEW']
    df=df[df['age']!='U']
    df=df.dropna(subset=['age'])
    #df=df[df['age'].astype(int)<18]
    try:
        df=df[try_cols]
        print('----\n----')
        print(try_cols)
        print('----\n----')
    except KeyError:
        print('----\n----')
        print(keep_cols)
        print('----\n----')
        df=df[keep_cols]
    
    print('Done.  Final size of data in '+i+' is:  '+str(len(df)))
    print(r'Storing data in: C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output\data\n\n\n')
    df.to_csv(storage_dir+i+'.csv')
    
base=r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output\data\\'
files=os.listdir(r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\faers_data\output\data')
df=pd.read_csv(base+files[0])
sys.exit()

for i in files[1:]:
    print(len(df))
    df=pd.concat([df,pd.read_csv(base+i)],ignore_index=True)
    print(len(df))
df.to_csv('faers_base.csv')
import faers_grouping_AE_1
