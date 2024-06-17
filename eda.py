import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

try:
    df = pd.read_csv('C:/Users/20224257/OneDrive - TU Eindhoven/Documents/Year 2/quartile 4/ward_edu_data.csv', encoding='latin1')
except Exception as e:
    print("An error occurred:", e)


df_filtered = df[['% with Level 4 qualifications and above - 2011', 'Crime rate - 2014/15', 'Violence against the person rate - 2014/15', 'Average GCSE capped point scores - 2014', 'Unauthorised Absence in All Schools (%) - 2013', '% with no qualifications - 2011', '% with Level 4 qualifications and above - 2011', 'A-Level Average Point Score Per Student - 2013/14', 'A-Level Average Point Score Per Entry; 2013/14']]
df.dropna(subset=['% with Level 4 qualifications and above - 2011', 'Crime rate - 2014/15', 'Violence against the person rate - 2014/15'], inplace=True)

rename_dict = {
    '% with Level 4 qualifications and above - 2011': 'Level 4+ Qualifications - 2011',
    'Crime rate - 2014/15': 'Crime Rate - 2014/15',
    'Violence against the person rate - 2014/15': 'Violence Rate - 2014/15',
    'Average GCSE capped point scores - 2014': 'GCSE Scores - 2014',
    'Unauthorised Absence in All Schools (%) - 2013': 'Unauthorised Absence - 2013',
    '% with no qualifications - 2011': 'No Qualifications - 2011',
    'A-Level Average Point Score Per Student - 2013/14': 'A-Level Score Per Student - 2013/14',
    'A-Level Average Point Score Per Entry; 2013/14': 'A-Level Score Per Entry - 2013/14'
}

df_filtered.rename(columns=rename_dict, inplace=True)
correlation_matrix = df_filtered.corr()


plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix.loc[:, ['Crime Rate - 2014/15', 'Violence Rate - 2014/15']], annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap', weight = 'bold', size = 20)
plt.xticks(fontsize=16, weight='bold')
plt.yticks(fontsize=16, weight='bold')
plt.show()

columns_of_interest = ['Unauthorised Absence in All Schools (%) - 2013', 'A-Level Average Point Score Per Student - 2013/14','Average GCSE capped point scores - 2014','% with Level 4 qualifications and above - 2011', 'Crime rate - 2014/15', 'Violence against the person rate - 2014/15']
df = df[columns_of_interest]
df.dropna(inplace=True)

# print(df.describe())

# Linear Regression Analysis
sns.lmplot(x='A-Level Average Point Score Per Student - 2013/14', y='Violence against the person rate - 2014/15', data=df, aspect=1.5, scatter_kws={"s": 2})
plt.title('A-level average vs Violence rate', weight = 'bold', size = 20)
plt.xlabel('A-level average', weight ='bold', size=16)
plt.ylabel('Violence Rate', weight ='bold', size=16)
plt.xticks(fontsize=16, weight='bold')
plt.yticks(fontsize=16, weight='bold')
plt.show()

sns.lmplot(x='Average GCSE capped point scores - 2014', y='Crime rate - 2014/15', data=df, aspect=1.5, scatter_kws={"s": 2})
plt.title('Average GCSE score vs Crime rate ', weight = 'bold', size = 20)
plt.xlabel('Average GCSE score', weight ='bold', size=16)
plt.ylabel('Crime Rate', weight ='bold', size=16)
plt.axis([280, 400, 0, 200])
plt.xticks(fontsize=16, weight='bold')
plt.yticks(fontsize=16, weight='bold')
plt.show()
