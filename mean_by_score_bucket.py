def mean_by_score_bucket(df, score_col, indicator, indicator_detail, num_bins):
    """
    This function is meant to plot the mean indicator by predicted score bucket. 
    
    Inputs:
    - df: dataframe
    - score_col: float, predicted score
    - indicator: boolean, response variable
    - indicator_detail: string, How do we want indicator to be displayed in plot title and y-label.
    - num_bins: integer, number of bins want score to be cut into, is an arg for with pandas quantile
    
    
    Outputs:
    - Line Chart
    """
    df_input = df[[score_col, indicator]].copy(deep = True)
    
    score_bins = df_input[score_col].quantile(q = np.array(range(0,101, num_bins))/100.0).values.round(3)
    score_bins[0], score_bins[-1] = score_bins[0] - 0.002, score_bins[-1] + 0.002
    
    df_input["{}_bucket".format(score_col)] = pd.cut(df_input[score_col], bins = score_bins, 
                                                     include_lowest = True, right = False,
                                                     duplicates = "drop")
    
    
    a = df_input.groupby("{}_bucket".format(score_col))[indicator].mean()
    a.plot(figsize = (15,8));
    plt.title("Average Number of {} by Predicted Model Score Bucket".format(indicator_detail), fontsize = 12);
    plt.ylabel("Average Number of {}".format(indicator_detail), fontsize = 12);
    plt.xlabel("Predicted Model Score Bucket", fontsize = 12);
    plt.xticks(range(len(a.index)), a.index);    
