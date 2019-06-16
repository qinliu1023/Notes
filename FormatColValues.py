for col in table_total_amounts.columns:
    plot_table_total_amounts["{}".format(col)] = plot_table_total_amounts.apply(lambda x: "{:,.3f}".format(x["{}".format(col)]), axis=1)

table_total_amounts.plot(kind = "bar", stacked = True, figsize = (15,10), table = plot_table_total_amounts.T);
