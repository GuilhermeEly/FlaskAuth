from ..production.productionData import prodData
import pandas as pd

def getFPYByDate(initial_date, final_date):

    productionDatabase = prodData()

    df = productionDatabase.queryFpyByDate(initial_date,final_date)

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
    response = res.merge(uniquePAs[["PA","NOME"]], how="left", left_on="PA", right_on="PA")

    return response.sort_values(by=["TIPO"])

def getOverallFPY(initial_date, final_date):
    productionDatabase = prodData()

    df_update_data = productionDatabase.queryFpyByDate(initial_date,final_date)

    df_products = df_update_data.drop_duplicates(subset = ["PA"])

    df_products = df_products.set_index("PA")

    dfrep = df_update_data.loc[(df_update_data["STATUS"] == "R")].drop_duplicates(subset = ["NS"])

    SNRep = dfrep.filter(["NS"], axis=1)

    dfRlyApproved = df_update_data[~df_update_data.NS.isin(SNRep.NS)].drop_duplicates(subset = ["NS"])

    dftest = dfrep.groupby(["PA"]).size().reset_index(name="counts")

    dfApprTest = dfRlyApproved.groupby(["PA"]).size().reset_index(name="counts")

    dfFinal = pd.merge(dftest, dfApprTest, how="outer", on="PA").fillna(0)

    dfFinal["fpy"] = dfFinal["counts_y"] /( dfFinal["counts_y"] + dfFinal["counts_x"])

    dfFinal["Produzido"] = dfFinal["counts_y"] + dfFinal["counts_x"]

    dfFinal.rename(columns={"counts_y": "Aprovadas", "counts_x": "Reprovadas"}, inplace=True)

    dfFinal[["PA", "fpy"]].fillna(0)

    dfFinal = dfFinal.sort_values(by=["fpy"])

    dfFinal.loc[(dfFinal["fpy"] == 0), "fpy"] = 0.005

    dfFinal = dfFinal[(dfFinal["fpy"] >= float(0)/100.0) & (dfFinal["fpy"] <= float(100)/100.0)]

    dfFinal["PA"] = dfFinal["PA"].map(str)

    dfFinal["fpy"] = dfFinal["fpy"].astype(float).map("{:.2%}".format)

    dfFinal = dfFinal.join(df_products, on="PA")

    dfFinal = dfFinal[dfFinal["Produzido"]>10]

    FPY_Total = (dfFinal["Aprovadas"].sum() /( dfFinal["Aprovadas"].sum() + dfFinal["Reprovadas"].sum()))*100

    return FPY_Total

def getNewOverallFPY(initial_date, final_date):

    df = getFPYByDate(initial_date=initial_date, final_date=final_date)

    approved = df.loc[df["TIPO"] == "1", "Approved"].sum()
    total = df.loc[df["TIPO"] == "1", "Total"].sum()
    fpy1 = approved/total

    approved = df.loc[df["TIPO"] == "2", "Approved"].sum()
    total = df.loc[df["TIPO"] == "2", "Total"].sum()
    fpy2 = approved/total

    if (df.loc[df["TIPO"] == "3"]).empty:
        fpy = fpy1*fpy2
        pass
    else:
        approved = df.loc[df["TIPO"] == "3", "Approved"].sum()
        total = df.loc[df["TIPO"] == "3", "Total"].sum()
        fpy3 = approved/total
        fpy = fpy1*fpy2*fpy3

    return fpy

def get_causes_by_PA(start_date, end_date, PA):

    fetch = prodData()

    start_date = start_date.replace("-", "")
    end_date = end_date.replace("-", "")

    df_update_data = fetch.queryFailCauses(startDate=start_date, endDate=end_date, PASelected=PA)

    dfREP = df_update_data[df_update_data.STATUS != "A"]

    dfttREP = dfREP.drop_duplicates(subset=["NS"], keep="first")

    #apenas a primeira reprovação em cada tentativa
    dfReprovations = dfREP.drop_duplicates(subset=["NS","DATA","HORA"], keep="first")

    dftest = dfttREP.groupby(["STEP","STATUS"]).size().reset_index(name="Reprovações")

    dfFinal = dftest.sort_values(by=["Reprovações"], ascending=False)

    return dfFinal, dfReprovations