df_agg = df.groupby("month")["weighted_score", "amount"].sum()

df_agg["weighted_average_score"] = df_agg["weighted_score"] / df_agg["amount"]

fig, ax = plt.subplots(1,1, figsize = (25,2))

df_agg[["weighted_average_score"]].plot(kind = "line", color = "dodgerblue", marker = "D", ax = ax);
ax.set_title("Amount Weighted Average Score", fontsize = 12);
ax.set_ylabel("Weighted Average \n Score", fontsize = 10);
#ax.set_ylim(0.023,0.03);
ax.set_xlabel("Origination Month", fontsize = 10);
ax.set_xticks(range(len(df_agg.index)));
ax.set_xticklabels(df_agg.index, rotation = 30, fontsize = 9);
ax.legend("", fontsize =12);
ax.patch.set_facecolor('white');
#for k in np.array(range(24,60,2))/1000.0:
#    ax.axhline(y = k, color = "darkgray", linewidth = 0.5);
ax.axhline(y = 24/1000.0, color = "darkgray", linewidth = 0.5);
for i in range(len(df_agg.index)):
    index = df_agg.index[i]
    if i % 2 == 0:
        y_text = df_agg[["weighted_average_score"]].loc[index]["weighted_average_score"]
        ax.annotate("{:,.3f}".format(y_text), xy = (i-0.3, y_text+0.0002), color = "k")    


# Every Other Group
for i in range(len(df_agg.index)):
    index = df_agg.index[i]
    for j in range(len(df_agg.columns)):
        col = df_agg.columns[j]
        y_text = df_agg.loc[index][col] * 100.0
        if (j % 2 == 0) & (i % 2 == 0):
            ax.annotate("{:,.0%}".format(y_text/100.0), xy = (i, y_text), color = "k") 
        if (j % 2 == 1)  & (i % 2 == 1):
            ax.annotate("{:,.0%}".format(y_text/100.0), xy = (i, y_text), color = "k") 
ax.grid(b = False);   
