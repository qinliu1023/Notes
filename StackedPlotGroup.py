def stacked_plot_target_segment(df_input, del_bucket):
    fig, ax = plt.subplots(1,2, figsize = (25,10))
    
    mask_bucket = df_input["index_bucket_adjusted"] == del_bucket
    
    segment_list = sorted(df_input[["target_segment"]].dropna(how = "any")["target_segment"].unique())
    bucket_segment_list = sorted(df_input[mask_bucket][["target_segment"]].dropna(how = "any")["target_segment"].unique())
        
    df_input_bucket = df_input[mask_bucket]#.query('target_segment != "Installment"')
    df_input_bucket_amt = df_input_bucket.groupby(["measurement_month", "target_segment"])["sum_amount_dollars"].sum().unstack()
    df_input_bucket_amt_pct = df_input_bucket_amt.div(df_input_bucket_amt.sum(axis = 1), axis = 0)

    df_input_bucket = df_input[mask_bucket]#.query('target_segment != "Installment"')
    df_input_bucket_cnt = df_input_bucket.groupby(["measurement_month", "target_segment"])["count_distinct_targets"].sum().unstack()
    df_input_bucket_cnt_pct = df_input_bucket_cnt.div(df_input_bucket_cnt.sum(axis = 1), axis = 0)

    segment_list_diff = list(set(segment_list)-set(bucket_segment_list))
    if len(segment_list_diff) > 0:
        for value_diff in segment_list_diff:
            df_input_bucket_amt_pct[value_diff] = 0
            df_input_bucket_cnt_pct[value_diff] = 0
    
    df_input_bucket_amt_pct.sort_index(axis = 0, inplace = True)
    df_input_bucket_cnt_pct.sort_index(axis = 0, inplace = True)

    df_input_bucket_amt_pct.plot(kind = "bar", stacked = True, colormap = 'Paired', ax = ax[0]);
    ax[0].set_title("Stacked Percentage of targets Amount by Measurement Month and target segment \n {}".format(del_bucket), fontsize = 12);
    ax[0].set_xlabel("", fontsize = 0);
    ax[0].set_xticklabels("", fontsize = 0);
    ax[0].set_ylabel("Percentage (%)", fontsize = 12);
    ax[0].set_ylim((0,1.02));
    ax[0].legend(" ", fontsize = 12);
    #ax[0].legend("", bbox_to_anchor = (0.5,-0.5,0.8,0.7), fontsize = 0);
    for i in range(len(df_input_bucket_amt_pct.index)):
        index = df_input_bucket_amt_pct.index[i]
        for j in range(len(df_input_bucket_amt_pct.columns)):
            col = df_input_bucket_amt_pct.columns[j]
            y_text = df_input_bucket_amt_pct.fillna(0).loc[index][col]
            y_coord = df_input_bucket_amt_pct.loc[index][:j].sum() + y_text/2
            if (y_text > 0.10) & (i % 2 == 0):
                ax[0].annotate("{:,.0%}".format(y_text), xy = (i-0.1, y_coord), color = "k")   
    ax[0].legend(fontsize = 0);

    
    df_input_bucket_cnt_pct.plot(kind = "bar", stacked = True, colormap = 'Paired', ax = ax[1]);
    ax[1].set_title("Stacked Percentage of targets Counts by Measurement Month and target segment \n {}".format(del_bucket), fontsize = 12);
    ax[1].set_xlabel("Measurement Month", fontsize = 12);
    ax[1].set_ylabel("Percentage (%)");
    ax[1].set_ylim((0,1.02)); 
    #ax[1].legend(bbox_to_anchor = (0.2,-0.2,0.4,-0.1), fontsize = 12);
    ax[1].legend(bbox_to_anchor = (0.55,0,0.8,0.7), fontsize = 12);
    
    for i in range(len(df_input_bucket_cnt_pct.index)):
        index = df_input_bucket_cnt_pct.index[i]
        for j in range(len(df_input_bucket_cnt_pct.columns)):
            col = df_input_bucket_cnt_pct.columns[j]
            y_text = df_input_bucket_cnt_pct.fillna(0).loc[index][col]
            y_coord = df_input_bucket_cnt_pct.loc[index][:j].sum() + y_text/2
            if (y_text > 0.10) & (i % 2 == 0):
                ax[1].annotate("{:,.0%}".format(y_text), xy = (i-0.1, y_coord), color = "k") 
                
                
    output_amt = df_input_bucket_amt   
    for col in output_amt.columns:
        output_amt["{}".format(col)] = output_amt.apply(lambda x: "${:,.0f}".format(x["{}".format(col)]), axis=1) 
    output_amt = output_amt.replace("$nan", " ")
    
    output_cnt = df_input_bucket_cnt   
    for col in output_cnt.columns:
        output_cnt["{}".format(col)] = output_cnt.apply(lambda x: "{:,.0f}".format(x["{}".format(col)]), axis=1)
    output_cnt = output_cnt.replace("nan", " ")    
    
    return multi_table([output_amt, output_cnt])