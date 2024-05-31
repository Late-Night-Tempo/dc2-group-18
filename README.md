# dc2-group-18
A school project for data challenge 2, group 18, centered around police trust and confidence.


## File notes
eda.py: Creates cleaned search and street data

main.py: Creates graphs based on PAS data

pas_ward_cleaner.py: Creates concatenated raw pas ward data, and creates TrueFalseSetter excel file

pas_ward_reducer.py: Takes edited TrueFalseSetter excel file (I named it as TrueFalsePasReducer.xlsx) and drops columns 
from raw pas ward data which have been labeled with False, and generates the CleanedPasWardData.csv

