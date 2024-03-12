from ..production.productionData import prodData
import pandas as pd

def getFPYByDate(initial_date, final_date):

    productionDatabase = prodData()

    df = productionDatabase.queryFpyByDate(initial_date,final_date)
    print(df)
    if df.empty:
        return df
    
    df["OP"] = pd.to_numeric(df["OP"], errors="coerce")

    # Convert "A" to 1 and "R" to 0 for easier calculation
    df["STATUS"] = df["STATUS"].apply(lambda x: 1 if x == "A" else 0)

    # Drop records with invalid serial numbers (less than 10 characters)
    df_valid_serial = df[df["NS"].apply(lambda x: len(str(x)) >= 8)]

    # Drop duplicate serial numbers within each test type
    df_unique = df_valid_serial.drop_duplicates(subset=["PA", "TIPO", "NS"])

    # Group by "PA" and "TIPO" and calculate FPY, number of approved, and number of rejected products
    fpy_df = df_unique.groupby(["PA", "TIPO"]).agg({"STATUS": ["sum", "count"]}).reset_index()

    # Calculate FPY for each type of test
    fpy_df["FPY"] = (fpy_df[("STATUS", "sum")] / fpy_df[("STATUS", "count")])
    print(df_unique)
    # Rename columns for clarity
    fpy_df.columns = ["PA", "TIPO", "Approved", "Total", "FPY"]

    # Group by "PA" and pivot the DataFrame
    pivot_df = fpy_df.pivot_table(index="PA", columns="TIPO", values="FPY").reset_index()

    # Calculate total FPY as the product of FPY values for each row
    pivot_df["Total_FPY"] = pivot_df.drop("PA", axis=1).prod(axis=1)

    # Merge with the original DataFrame on "PA"
    result_df = fpy_df.merge(pivot_df, on="PA")

    result_df = result_df.drop(columns=["FPY"])
    result_df = result_df.drop_duplicates(subset=["PA"])
    result_df["TIPO"] = "Total"
    result_df = result_df.rename(columns={"Total_FPY":"FPY"})
    result_df = result_df[["PA", "TIPO", "FPY"]]
    res = pd.concat([fpy_df, result_df])

    uniquePAs = df.drop_duplicates(subset=["PA"])
    response = res.merge(uniquePAs[["PA","NOME"]], how='left', left_on='PA', right_on='PA')

    return response.sort_values(by=["TIPO"])