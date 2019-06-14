fig, ax = plt.subplots(2,3,figsize = (40,18))

Targets = ["initla_pct", "initial_to_1st", "1st_to_2nd", "2nd_to_3rd", "3rd_to_4th"]

pivot_value_col_dict = {
"initla_pct": ["T0 Score", "T1 Score", "T2 Score", "T3 Score", "T4 Undefined"],
"initial_to_1st": ["T0 Score", "T1 Score", "T2 Score", "T3 Score", "T4 Undefined"],
"1st_to_2nd": ["T0 Score", "T1 Score", "T2 Score", "T4 Undefined"],
"2nd_to_3rd": ["T0 Score", "T1 Score", "T4 Undefined"],
"3rd_to_4th": ["T0 Score", "T1 Score", "T4 Undefined"]}


for k in range(len(Targets)):
    ax_row, ax_col = k // 3, k % 3
    
    pivot_value = Targets[k]
    pivot_value_col = pivot_value_col_dict[pivot_value]

    plot_target = pd.pivot_table(df_target,
                                   index = "month", columns = "fico_tiers", 
                                   values = pivot_value)
    
    for col in plot_target.columns:
        if col in pivot_value_col:
            continue
        else:
            plot_target[col] = np.nan
    
    ylim_min = int(max(0.0, plot_target.min().min() - float(0.2)) * 100)
    ylim_max = int(min(1.0, plot_target.max().max() + float(0.1)) * 100)
    hline_step = (ylim_max - ylim_min) / 10

    
    (plot_target * 100.0).plot(ax = ax[ax_row,ax_col], colormap = "Paired", marker = "D");
    ax[ax_row, ax_col].set_title("Target: {}".format(pivot_value.replace("Target_", "").replace("_", " ").title()), fontsize = 16);
    ax[ax_row, ax_col].set_ylabel("Target (%)", fontsize = 12);
    ax[ax_row, ax_col].set_ylim(ylim_min, ylim_max);
    ax[ax_row, ax_col].set_xlabel("Month", fontsize = 10);
    ax[ax_row, ax_col].set_xticks(range(len(plot_target.index)));
    ax[ax_row, ax_col].set_xticklabels(plot_target.index);
    if (ax_row == 0) & (ax_col == 0):
        ax[ax_row, ax_col].legend(loc = "upper right", fontsize = 12);
    else:
        ax[ax_row, ax_col].legend(loc = "lower right", fontsize = 12);        
    ax[ax_row, ax_col].patch.set_facecolor('white');
    for k in np.array(range(ylim_min-1, ylim_max+1, hline_step)):
        ax[ax_row, ax_col].axhline(y = k, color = "darkgray", linewidth = 0.5);
    for i in range(len(plot_target.index)):
        index = plot_target.index[i]
        for j in range(len(plot_target.columns)):
            col = plot_target.columns[j]
            if j % 3 == 0:
                y_text = plot_target.fillna(0).loc[index][col] * 100.0
                if y_text > 0:
                    ax[ax_row, ax_col].annotate("{:,.0%}".format(y_text/100.0), xy = (i, y_text), color = "k")   
    ax[ax_row, ax_col].grid(b = False);
   
    ax_twin = ax[ax_row, ax_col].twinx()
    pivot_value_overall = pivot_value + "_overall"
    
    plot_target_overall = \
    df_target_overall[["month", pivot_value_overall]].set_index("month")\
    .rename(columns = {pivot_value_overall: "{}".format("Overall" + pivot_value.replace("_", " ").title())})\
    .loc[plot_target.index]
    
    (plot_target_overall * 100.0).plot(ax = ax_twin, color = "black", marker = "D", linewidth = 3);
    ax_twin.set_ylim(ylim_min, ylim_max);
    ax_twin.legend("", fontsize = 0);
    ax_twin.set_yticklabels("", fontsize = 0);
    ax_twin.grid(b = False);

    
for k in range(len(Targets)):
    ax_row, ax_col = k // 3, k % 3
    ax[ax_row, ax_col].tick_params(axis='both', which='both', labelsize = 10)
    
    # set ticks visible, if using sharex = True. Not needed otherwise
    for tick in ax[ax_row, ax_col].get_xticklabels():
        tick.set_visible(True) 
 
ax[1, 2].patch.set_facecolor('white'); 
ax[1, 2].set_yticklabels("");
ax[1, 2].set_xticklabels(""); 
