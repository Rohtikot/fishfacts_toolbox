import pandas as pd
import os

path = 'harbors'

folder = os.listdir(path)

joined_df = pd.DataFrame()

for n, file in enumerate(folder, start=1):
    if file.endswith('.csv') and file[0:3] == 'fo_':
        file_path = os.path.join(path, file)
        filename, extension = os.path.splitext(file)
        country_code = filename.split('_')[0]
        filename = filename.split('_')[1]

        _df = pd.read_csv(file_path)
        _df['harbor'] = filename
        _df['country_code'] = country_code

        joined_df = pd.concat([joined_df, _df])

joined_df.to_csv('harbors/one_file_zones/fo_harbors.csv', index=False)
print(joined_df)
