print("\n#### Fix broken links\n\n")

import pandas as pd

def dumper(path, name, frame):
    with open(f'{path}/{name}.csv', 'w') as f:
        frame.to_csv(f, index=False, header=True)

pathos = 'data/register_combined/combined.csv'

old = pd.read_csv(pathos)


to_fix = [('2019/8487','https://epbcpublicportal.awe.gov.au/offsets-register/offset-detail/?id=be67e082-1e82-eb11-80c2-00505684c137'),
          ('2015/7516', 'https://epbcpublicportal.awe.gov.au/offsets-register/offset-detail/?id=9b4bf5ef-20e8-eb11-80c6-00505684c137')]

for thing in to_fix:
    old.loc[old['EPBC Number'] == thing[0], 'Url'] = thing[1]



#### Remove ones that don't work.


to_remove = ['https://epbcpublicportal.awe.gov.au/offsets-register/offset-detail/?id=7f2ac5ce-e927-ec11-80c9-00505684c137', 
             'https://epbcpublicportal.awe.gov.au/offsets-register/offset-detail/?id=9a163abf-75b6-ea11-8731-005056842ad1',
             'https://epbcpublicportal.awe.gov.au/offsets-register/offset-detail/?id=7f2ac5ce-e927-ec11-80c9-00505684c137',
             'https://epbcpublicportal.awe.gov.au/offsets-register/offset-detail/?id=9a163abf-75b6-ea11-8731-005056842ad1',
             'https://epbcpublicportal.awe.gov.au/offsets-register/offset-detail/?id=9a163abf-75b6-ea11-8731-005056842ad1',
             'https://epbcpublicportal.awe.gov.au/offsets-register/offset-detail/?id=55700b2e-ec82-eb11-80c5-00505684c563']

for thing in to_remove:
    old = old.loc[old['Url'] != thing]


dumper('data/register_combined', 'combined', old)