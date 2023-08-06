import fmdt
import pandas as pd

window = fmdt.load_window()

def get_csv_name(w: fmdt.Video, diff: int) -> str:
    pre = w.prefix()
    return pre + f"_50_200_{diff}_data.csv"

def get_df(w: fmdt.Video) -> pd.DataFrame:
    dfs = []
    for d in [1, 2, 4, 8]:
        dfs.append(pd.read_csv(get_csv_name(w, d)))

    df = pd.concat(dfs)
    df = df.drop_duplicates()

    return df

df = get_df(window[0])

print(df.head())

df.groupby(["lmin", "lmax"]).mean()