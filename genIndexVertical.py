import pandas as pd
import json

csv_file = "./vocabulary.csv"
df = pd.read_csv(csv_file)
drop_col = set(df.columns) - set(["Index", "Vertical1"])
df = df.drop(drop_col, axis=1)
# print(df.columns)

verticals = df["Vertical1"].unique()
idx2vertical = dict(enumerate(verticals))
vertical2idx = {x:y for y, x in idx2vertical.items()}
# print(idx2vertical)
# print(vertical2idx)

df_dict = {}
# df_dict = df["Vertical1"].map(vertical2idx)
for i in range(len(df)):
	df_dict[i] = vertical2idx[df.iloc[i, -1]]

with open("idx2verticalidx.json", 'w') as f:
	json.dump(df_dict, f)

with open("verticalidx2vertical.json", 'w') as f:
	json.dump(idx2vertical, f)
# print(df_dict)