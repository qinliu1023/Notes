"""
Table Fiels:
|user_tier|period|bucket_prev|bucket_cur|count_distinct_users|rate_cnt|
​
Values:
1. bucket: 1,2,3,4. Transition direction:
- better if bucket_cur < bucket_prev
- worse if bucket_cur > bucket_prev
- unchange if bucket_cur == bucket_prev
​
2. user_tier: A, B, C
3. period: integers, 1,2,3,...
​
Original Table
| user_tier | period | bucket_prev | bucket_cur | count_distinct_users | rate_cnt |
| A	| 1 | 1| 1 | 38 | 0.81 |
| A	| 1 | 1| 2 | 9 | 0.69 |
| A	| 1 | 1| 3 | 34 | 0.10 |
| A	| 1 | 2| 1 | 76 | 0.39 |
| A	| 1 | 2| 2 | 64 | 0.75 |
| A	| 1 | 2| 3 | 94 | 0.01 |
| A	| 1 | 3| 1 | 106 | 0.49 |
| A	| 1 | 3| 2 | 46 | 0.79 |
| A	| 1 | 3| 3 | 64 | 0.44 |
| A	| 2 | 1| 1 | 75  0.61 |
| A	| 2 | 1| 2 | 16 | 0.93 |
| A	| 2 | 1| 3 | 30 | 0.30 |
| A	| 2 | 2| 1 | 90 | 0.47 |
| A	| 2 | 2| 2 | 74 | 0.51 |
| A	| 2 | 2| 3 | 29 | 0.81 |
| A	| 1 | 3| 1 | 3 | 0.82 |
| A	| 2 | 3| 2 | 37 | 0.16 |
| A	| 2 | 3| 3 | 40 | 0.70 |
| B	| 1 | 1| 1 | 34 | 0.95 |
| B	| 1 | 1| 2 | 20 | 0.51 |
| B	| 1 | 1| 3 | 94 | 0.56 |
| B	| 1 | 2| 1 | 29 | 0.85 |
| B	| 1 | 2| 2 | 97 | 0.51 |
| B	| 1 | 2| 3 | 20 | 0.07 |
| B	| 1 | 3| 1 | 62  0.24 |
| B	| 1 | 3| 2 | 95 | 0.73 |
| B	| 1 | 3| 3 | 12 | 0.41 |
| B	| 2 | 1| 1 | 44 | 0.49 |
| B	| 2 | 1| 2 | 98  0.50 |
| B	| 2 | 1| 3 | 34 | 0.55 |
| B	| 2 | 2| 1 | 10 | 0.85 |
| B	| 2 | 2| 2 | 6 | 0.01 |
| B	| 2 | 2| 3 | 56 | 0.33 |
| B	| 1 | 3| 1 | 9 | 0.94 |
| B	| 2 | 3| 2 | 52 | 0.52 |
| B	| 2 | 3| 3 | 61 | 0.40 |
​
When tracking status transition, we need to remove some records based on total counts:
For example, pivoting above table will get the following
                       
			                       bucket_cur	 All
			                       1	 2	 3	 
user_tier	period	bucket_prev			 	  
A	           1         1	       38	  9	 34	  81  # < 100, no need to show
	           	         2	       76	 64	 94	 234
	           	         3	       106	 46	 64	 216
	           2         1	       75	 16	 30	 121
	           	         2	       90	 74	 29	 193
	           	         3	       	3	 37	 40   80  # < 100, no need to show
B	           1         1	       34	 20	 94	 148
	           	         2	       29	 97	 20	 146
	           	         3	       62	 95	 12	 169
	           2         1	       44	 98	 34	 176
	           	         2	       10	  6	 56	  72  # < 100, no need to show
	           	         3	       	9	 52	 61  122 
All			                      564	537	556	1657
​
Then create multiplier to set those values to be np.nan:
​
                       
			                       bucket_cur	 All
			                       1	 2	 3	 
user_tier	period	bucket_prev			 	  
A	           1         1	       nan  nan nan	 nan  # < 100, set to nan
	           	         2	       1	 1	 1	  1
	           	         3	       1	 1	 1	  1
	           2         1	       1	 1	 1	  1
	           	         2	       1	 1	 1	  1
	           	         3	       nan  nan nan	 nan  # < 100, set to nan
B	           1         1	       1	 1	 1	  1
	           	         2	       1	 1	 1	  1
	           	         3	       1	 1	 1	  1
	           2         1	       1	 1	 1	  1
	           	         2	       nan  nan nan	 nan  # < 100, set to nan
	           	         3	       1	 1	 1    1 
All			                       1	 1	 1    1
​
​
Do multiplier * (pivot rate_cnt) and melt, will get the following:
​
			                          bucket_cur	    All
			                      1	     2	     3	
user_tier	period	bucket_prev				
A	           1	      1	      nan    nan     nan	 nan			
	           1	      2	     0.39	0.75	0.01	1.15
	           1	      3	     0.49	0.79	0.44	1.72
	           2	      1	     0.61	0.93	 0.3    1.84
	           2	      2	     0.47	0.51	0.81	1.79
	           2	      3	      nan    nan     nan	 nan			
B	           1	      1	     0.95	0.51	0.56	2.02
	           1	      2	     0.85	0.51	0.07	1.43
	           1	      3	     0.24	0.73	0.41	1.38
	           2	      1	     0.49	 0.5	0.55	1.54
	           2	      2	      nan    nan     nan	 nan
	           2	      3	     0.94	0.52	0.4	    1.86
All	           		             5.43	5.75	3.55   14.73
​
​
Then melt:
| user_tier | period | bucket_prev | bucket_cur | rate_cnt |
| A	| 1 | 1 | 1 |  |
| A	| 1 | 1 | 2 |  |
| A	| 1 | 1 | 3 |  |
| A	| 1 | 2 | 1 | 0.39 |
| A	| 1 | 2 | 2 | 0.75 |
| A	| 1 | 2 | 3 | 0.01 |
| A	| 1 | 3 | 1 | 0.49 |
| A	| 1 | 3 | 2 | 0.79 |
| A	| 1 | 3 | 3 | 0.44 |
| A	| 2 | 1 | 1 | 0.61 |
| A	| 2 | 1 | 2 | 0.93 |
| A	| 2 | 1 | 3 | 0.3 |
| A	| 2 | 2 | 1 | 0.47 |
| A	| 2 | 2 | 2 | 0.51 |
| A	| 2 | 2 | 3 | 0.81 |
| A	| 2 | 3 | 1 |  |
| A	| 2 | 3 | 2 |  |
| A	| 2 | 3 | 3 |  |
| B	| 1 | 1 | 1 | 0.95 |
| B	| 1 | 1 | 2 | 0.51 |
| B	| 1 | 1 | 3 | 0.56 |
| B	| 1 | 2 | 1 | 0.85 |
| B	| 1 | 2 | 2 | 0.51 |
| B	| 1 | 2 | 3 | 0.07 |
| B	| 1 | 3 | 1 | 0.24 |
| B	| 1 | 3 | 2 | 0.73 |
| B	| 1 | 3 | 3 | 0.41 |
| B	| 2 | 1 | 1 | 0.49 |
| B	| 2 | 1 | 2 | 0.5 |
| B	| 2 | 1 | 3 | 0.55 |
| B	| 2 | 2 | 1 |  |
| B	| 2 | 2 | 2 |  |
| B	| 2 | 2 | 3 |  |
| B	| 2 | 3 | 1 | 0.94 |
| B	| 2 | 3 | 2 | 0.52 |
| B	| 2 | 3 | 3 | 0.4 |
​
"""
​
## Get Transition Direcion Based on Bucket_Prev and Buckt_Cur
df["transition_direction"] = df\
.apply(lambda row: "2. unchange" if int(row["bucket_prev"]) == int(row["bucket_cur"]) else
                   "1. better" if int(row["bucket_prev"]) > int(row["bucket_cur"]) else
                   "3. worse" if int(row["bucket_prev"]) < int(row["bucket_cur"]) else
                   "9. undefined", axis = 1)
​​
## Get transition_matrix
transition_matrix = \
df.groupby(["user_tier", "period", "bucket_prev", "transition_direction"])[["count_distinct_users"]].sum().reset_index()\
.merge(
    df.groupby(["user_tier", "period", "bucket_prev"])[["count_distinct_users"]].sum().reset_index(),
    how = "left", on = ["user_tier", "period", "bucket_prev"],
    suffixes = ("", "_prev")
)
transition_matrix["rate_cnt"] = 1.0 * transition_matrix["count_distinct_users"] / transition_matrix["count_distinct_users_prev"]
​
​
## Get multiplier
multiplier = \
pd.pivot_table(transition_matrix, 
               index = ["user_tier", "period", "bucket_prev"], columns = "transition_direction", 
               values = "count_distinct_users", aggfunc = "sum", margins = True)
​
for col in multiplier.columns:
    multiplier[col] = multiplier.apply(lambda row: 1 if (row["All"] >= 100) & (row[col] > 0) else np.nan, axis = 1)
​
​
## Melt
a = \
(multiplier * \
 pd.pivot_table(transition_matrix, 
               index = ["user_tier", "period", "bucket_prev"], columns = "transition_direction", 
               values = "rate_cnt", aggfunc = "sum", margins = True)).iloc[:-1, :-1]
​
a_melt = \
pd.melt(frame = a.reset_index(),
        id_vars = ["user_tier", "period", "bucket_prev"], 
        value_vars = ["1. better", "2. unchange", "3. worse"], 
        var_name = "transition_direction", 
        value_name = "rate_cnt")
​
a_melt.groupby(["user_tier", "transition_direction", "bucket_prev", "period"])[["rate_cnt"]].mean().fillna(" ").unstack()
​
​
## If Plot at the same time
fig, ax = plt.subplots(3, 5, figsize = (40, 20));
​
directions = sorted(transition_matrix["transition_direction"].unique())
user_tiers = sorted(transition_matrix["user_tier"].unique())
print directions
print user_tiers
​
​
for j in range(3):
    tran_sub = transition_matrix[transition_matrix["user_tier"] == user_tiers[j]]
    ## Build Multiplier
    multiplier = \
    pd.pivot_table(tran_sub, 
                   index = ["period", "bucket_prev"], columns = "transition_direction",
                   values = "count_distinct_loans", aggfunc = "sum", margins = True)
    
    for col in multiplier.columns:
        multiplier[col] = multiplier.apply(lambda row: 1 if (row["All"] >= 100) & (row[col] > 0) else np.nan, axis = 1)
    
    
    ## Pivot Rate_Cnt    
    a = \
    (multiplier * \
     pd.pivot_table(tran_sub, 
                   index = ["period", "bucket_prev"], columns = "transition_direction",
                   values = "rate_cnt", aggfunc = "sum", margins = True)).iloc[:-1, :-1]
    
    
        
    ## Cleaned Pivot Table with Multiplier and Melt    
    a_melt = \
    pd.melt(frame = a.reset_index(),
            id_vars = ["period", "bucket_prev"], 
            value_vars = ["1. better", "2. unchange", "3. worse"], 
            var_name = "transition_direction", 
            value_name = "rate_cnt")
​
​
    for k in range(5):
​
        transition_sub = a_melt[a_melt["transition_direction"] == directions[k]]
        table_plot = pd.pivot_table(transition_sub, columns = "bucket_prev", index = "period", values = "rate_cnt").round(4)
        table_plot.plot(colormap = "Paired", marker = "D", ax = ax[j, k]);
        #print table_plot.round(3)
        plt.sca(ax[j, k]);
        plt.title("{} Rate by Period - Tier {}".format(directions[k], user_tiers[j]));
        plt.xlabel("Period");
        plt.xticks(table_plot.index, table_plot.index);
        plt.legend(loc = "best");
        plt.ylim(0, 1.1); 