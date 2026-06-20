DOMESTIC_ONLY_BRANDS = ["SWIGGY", "OLA", "IRCTC"]

def detect_anomalies(df):
    df["is_anomaly"] = False
    df["anomaly_reason"] = None

    for account_id, group in df.groupby("account_id"):
        median_amount = group["amount"].median()

        for index, row in group.iterrows():
            reasons = []

            if median_amount > 0 and row["amount"] > 3 * median_amount:
                reasons.append("Amount exceeds 3x account median")

            merchant_upper = str(row["merchant"]).upper()

            if row["currency"] == "USD" and merchant_upper in DOMESTIC_ONLY_BRANDS:
                reasons.append("USD used for domestic-only merchant")

            if reasons:
                df.at[index, "is_anomaly"] = True
                df.at[index, "anomaly_reason"] = "; ".join(reasons)

    return df