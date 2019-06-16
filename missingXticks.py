table_final_pct = \
table_final.set_index(["quarter_starts", "period"])\
[["cum_1_term", "cum_2_term", "cum_3_term", "cum_4_term", "cum_5_term", "cum_charge_off"]]\
.div(table_final.set_index(["quarter_starts", "period"]).count_issued, axis = 0)


pd.options.display.float_format = '{:,.2%}'.format

pivot_values = table_final_pct.columns

fig, ax = plt.subplots(2,3,figsize = (40,18))

for k in range(len(pivot_values)):
    pivot_value = pivot_values[k]
    ax_row, ax_col = k // 3, k % 3

    plot_cum = pd.pivot_table(table_final_pct[[pivot_value]].reset_index(), 
                                      columns = "quarter_starts", index = "period", values = pivot_value)

    # Remove Partial Months
    plot_cum.rename(columns = lambda x: x.replace("-01", "-Q1").replace("-04", "-Q2")\
                       .replace("-07", "-Q3").replace("-10", "-Q4"), inplace = True)
    for col in plot_cum.columns:
        max_notnull_index = plot_cum[plot_cum[col].notnull() == True].index.max()
        plot_cum.iloc[max_notnull_index-2:][col] = np.nan 
    plot_cum.dropna(thresh = 1, inplace = True)        

    
    ylim_max = (plot_cum* 100.0).max().max() + float(5)
    hline_step = int(ylim_max)/10
    
    (plot_cum* 100.0).plot(ax = ax[ax_row, ax_col], colormap = "tab20c", marker = "D");
    ax[ax_row, ax_col].set_title("{} Percentage by Starting Quarter".format(pivot_value.replace("_", " ").title()), fontsize = 14);
    ax[ax_row, ax_col].set_ylabel("Percentage (%)", fontsize = 12);
    ax[ax_row, ax_col].set_ylim(-0.1, ylim_max);
    ax[ax_row, ax_col].set_xlabel("Period", fontsize = 12);
    ax[ax_row, ax_col].set_xticks(plot_cum.index);
    ax[ax_row, ax_col].set_xticklabels(plot_cum.index, rotation = 0, fontsize = 12);
    ax[ax_row, ax_col].legend(loc = "upper left", fontsize = 12);
    ax[ax_row, ax_col].patch.set_facecolor('white');
    for k in np.array(range(0,int(ylim_max),hline_step)):
        ax[ax_row, ax_col].axhline(y = k, color = "darkgray", linewidth = 0.5);
    #for i in range(len(plot_cum.index)):
    #    index = plot_cum.index[i]
    #    for j in range(len(plot_cum.columns)):
    #        col = plot_cum.columns[j]
    #        if i % 5 == 0:
    #            y_text = plot_cum.loc[index][col] * 100.0
    #            ax[ax_row, ax_col].annotate("{:,.2%}".format(y_text/100.0), xy = (i, y_text), color = "k")   
    ax[ax_row, ax_col].grid(b = False);  
    
#ax[1, 2].patch.set_facecolor('white'); 
#ax[1, 2].set_yticklabels("");
#ax[1, 2].set_xticklabels("");