pd.options.display.float_format = '{:,.2%}'.format

table_a = table_a_num.div(table_a_num.sum(axis = 1), axis = 0)

fig, ax = plt.subplots(1,2,figsize = (25,10))

(table_a_num/1000.0).plot(kind = "bar", stacked = True, colormap = "Set3", ax = ax[0]);
ax[0].set_title("Total Balance", fontsize = 12);
ax[0].set_xlabel("Date", fontsize = 12);
ax[0].set_ylabel("Total Balance (Unit: $1,000)", fontsize = 12);
ax[0].legend(["EvantC Only (Event Age: <= 4 Months)", "EvantC Only (Event Age: 4+ Months)",
              "EvantC and also Filed DMC (Event Age: <= 4 Months)", "EvantC and also Filed DMC (Event Age: 4+ Months)"], 
              bbox_to_anchor = (0.8,-0.6,0.6,0.4), fontsize = 10)
ax[0].patch.set_facecolor('white');
for i in range(len(table_a_num.index)):
    index = table_a_num.index[i]
    for j in range(len(table_a_num.columns)):
        col = table_a_num.columns[j]
        y_text = table_a_num.fillna(0).loc[index][col] /1000.0
        y_coord = table_a_num.loc[index][:j].sum()/1000.0 + y_text/2
        if y_text > 10:
            ax[0].annotate("{:,.0f}".format(y_text), xy = (i-0.2, y_coord+0.005), color = "k")  
            
for i in range(len(table_a_num.index)):
    index = table_a_num.index[i]
    y_coord = table_a_num.loc[index][:].sum()/1000.0 
    if y_coord < 1:
        ax[0].annotate("{:,.2f}".format(y_coord), xy = (i-0.2, y_coord+20), color = "r")           
    else:    
        ax[0].annotate("{:,.0f}".format(y_coord), xy = (i-0.2, y_coord+20), color = "r")   
            
            
            
ax[0].grid(b = False); 

table_a.plot(kind = "bar", stacked = True, colormap = "Set3", ax = ax[1]);
ax[1].set_title("Distribution of Total Balance", fontsize = 12);
ax[1].set_xlabel("Date", fontsize = 12);
ax[1].legend("");
ax[1].patch.set_facecolor('white');
for i in range(len(table_a.index)):
    index = table_a_num.index[i]
    for j in range(len(table_a.columns)):
        col = table_a.columns[j]
        y_text = table_a.fillna(0).loc[index][col]
        y_coord = table_a.loc[index][:j].sum() + y_text/2
        if y_text > 0:
            ax[1].annotate("{:,.0%}".format(y_text), xy = (i-0.2, y_coord+0.005), color = "k")   
ax[1].grid(b = False); 