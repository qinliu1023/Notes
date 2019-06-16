table_aggregated = \
pd.concat([active_value, 
           weighted_score_C[["date", "Bal Weighted Avg Score"]].set_index("date").T,
           pd.DataFrame([[np.nan] * active_value.shape[1]], columns = active_value.columns, index = ["Bucket"]), 
           pivot_table.div(pivot_table.sum(axis = 0), axis = 1).fillna(0).sort_index(axis = 1, ascending = True), 
           pd.DataFrame([[np.nan] * active_value.shape[1]], columns = active_value.columns, index = ["GroupD"]),
           pivot_table_GroupD.sort_index(axis = 1, ascending = True),
           pd.DataFrame([[np.nan] * active_value.shape[1]], columns = active_value.columns, index = ["Marginal Bal"]),
           table_marginal]).T.dropna(axis = 0, thresh = 2)

#table_aggregated.insert(loc = 13, column = "GroupB Bal%", value = table_aggregated["GroupB Bal Bal"]/table_aggregated["Bal Bal"], allow_duplicates = False)
table_aggregated.insert(loc = 13, column = "% Bal in GroupD", value = table_aggregated["Bal in GroupD"]/table_aggregated["Bal"], allow_duplicates = False)

for col in table_aggregated.columns:
    if col in ("Bal", "Bal in GroupD", "Marginal Bal"):
        table_aggregated["{}".format(col)] = table_aggregated.apply(lambda x: "${:,.0f}".format(x["{}".format(col)]), axis=1)
    elif col in ("Bal Weighted Avg Score"):
        table_aggregated["{}".format(col)] = table_aggregated.apply(lambda x: "{:,.0f}".format(x["{}".format(col)]), axis=1)
    elif col in ("Bucket", "GroupB", "GroupD"):
        continue
    else:
        table_aggregated["{}".format(col)] = table_aggregated.apply(lambda x: "{:,.2%}".format(x["{}".format(col)]), axis=1)
        
table_aggregated.fillna(" ").replace("nan", " ").replace("$nan", " ").replace("nan%", " ").T