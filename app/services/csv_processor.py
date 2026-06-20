import pandas as pd

def clean_csv(file_path: str):
    df = pd.read_csv(file_path)

    row_count_raw = len(df)

    df = df.drop_duplicates()

    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True).dt.strftime("%Y-%m-%d")

    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["currency"] = df["currency"].astype(str).str.upper().str.strip()
    df["status"] = df["status"].astype(str).str.upper().str.strip()

    missing_category_mask = df["category"].isna() | (df["category"].astype(str).str.strip() == "")

    df["category"] = df["category"].fillna("Uncategorised")
    df.loc[df["category"].astype(str).str.strip() == "", "category"] = "Uncategorised"

    df["merchant"] = df["merchant"].astype(str).str.strip()
    df["account_id"] = df["account_id"].astype(str).str.strip()

    row_count_clean = len(df)

    return df, row_count_raw, row_count_clean, missing_category_mask