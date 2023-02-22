import pandas as pd

def dumper(path, name, frame):
    with open(f'{path}/{name}.csv', 'w') as f:
        frame.to_csv(f, index=False, header=True)

pathos = 'data/register_combined/combined.csv'

old = pd.read_csv(pathos)


to_fix = [('2019/8487','https://epbcpublicportal.awe.gov.au/offsets-register/offset-detail/?id=be67e082-1e82-eb11-80c2-00505684c137')]


for thing in to_fix:
    old.loc[old['EPBC Number'] == thing[0], 'Url'] = thing[1]


dumper('data/register_combined', 'combined', old)