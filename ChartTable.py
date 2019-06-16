def vm_upldate_list(updated_list_excel_file, sheet_name):

    df_new_list = pd.read_excel(updated_list_excel_file, sheet = sheet_name)

    table_name = 'list_{}'.format(pd.to_datetime('today').strftime('%Y-%m-%d').replace("-",""))

    table.upload_df(df = df_new_list[["id", "type", "date"]], delim = '|', overwrite = True)

    return table_name


def vm_update(table_name, metric_index):
    query_vm = '''SELECT * FROM tbl1 LEFT JOIN {} AS tbl2 ON tbl1.id = tb2.tbl1_id'''.format(table_name)
    df_copy = pd.read_sql(query_vm, trellis.connect("server_name"))

    df = copy.deepcopy(df_copy)

    df["value_on_date"] = df["value_on_date"].astype(float)
    df["value"] = df["value"].astype(float)

    table_value = \
    df.query('days_since_event == {}'.format(metric_index)).query('index_bucket_on_date == "[1,5]"')\
    .groupby(["index_bucket_on_date", "type"])\
    [["value_on_date", "value"]].sum()\

    table_value["{}_day_metric".format(metric_index)] = \
    1.0 * table_value["value"] / table_value["value_on_date"]

    fig, ax = plt.subplots(figsize = (12,8))

    #ax1 = plt.subplot2grid(shape = (12, 1), loc = (0, 0), rowspan = 8, colspan = 1)
    #ax2 = plt.subplot2grid(shape = (12, 1), loc = (8, 0), rowspan = 4, colspan = 1)

    plot_pivot_table = \
    pd.pivot_table(table_value.reset_index(), 
                   index = "index_bucket_on_date",
                   columns = "placement_type",
                   values = "{}_day_metric".format(metric_index))
    plot_pivot_table.plot(kind = "bar", ax = ax);
    ax.set_title("{} Day Metric by Test Groups".format(metric_index));
    ax.set_xlabel("index_Bucket on Date", fontsize = 12);
    ax.set_xticklabels(plot_pivot_table.index, rotation = 0, fontsize = 12);
    ax.set_ylim((-0.01,1.0));
    ax.legend(loc = "lower right");
    ax.patch.set_facecolor('white');
    for k in np.array(range(0,80,10))/100.0:
        ax.axhline(y = k, color = "darkgray", linewidth = 0.5, linestyle = "-");
    ax.grid(b = None);

    from pandas.plotting import table

    show_table = \
    df.query('days_since_event == {}'.format(metric_index)).query('index_bucket_on_date == "[1,5]"')\
    .groupby(["index_bucket_on_date", "placement_type"])[["id"]].nunique().reset_index()\
    .merge(table_value[["{}_day_metric".format(metric_index)]].reset_index(),
           how = "left", 
           left_on = ["index_bucket_on_date", "placement_type"],
           right_on = ["index_bucket_on_date", "placement_type"])\
    .set_index("index_bucket_on_date").rename(columns = {"id": "count_distinct_loans"})
    #.set_index(["index_bucket_on_date", "placement_type"]).rename(columns = {"id": "count_distinct_loans"})

    show_table["count_distinct_loans"] = show_table.apply(lambda x: "{:,.0f}".format(x["count_distinct_loans"]), axis=1)
    show_table["{}_day_metric".format(metric_index)] = show_table.apply(lambda x: "{:,.2%}".format(x["{}_day_metric".format(metric_index)]), axis=1)

    show_table
    table(ax, show_table, loc = "upper right", colWidths = [0.2,0.2,0.2,0.2],
          rowColours = ["lightgray","lightgray","lightgray","lightgray"],
          colColours = ["lightgray","lightgray","lightgray","lightgray"]);

#updated_table_name = vm_upldate_list("Voicemail Test Adherence Summary by Account 2019-03-18.xlsx", "final_list")
#vm_update(updated_table_name, 30)    