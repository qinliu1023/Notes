import os
path = get_ipython().magic('pwd')

## Bucket Summary
writer = pd.ExcelWriter(os.path.join(path,r"Overview_{0}.xlsx".format(pd.datetime.today().strftime('%Y-%m-%d').replace('-',''))))
df.to_excel(writer,'Sheet'+str(1), index = True, startcol = (k-1)*10, startrow = 0)
writer.save()


writer = pd.ExcelWriter(os.path.join(path,r"Overview_{0}.xlsx".format(pd.datetime.today().strftime('%Y-%m-%d').replace('-',''))))

#### Count of Each Bucket
for k in range(1,4,1):
    df2.query('index_rank == {0}'.format(k)).groupby("score_tier")["id"].count().to_frame("B"+str(k)).T\
    [["(-inf,0.05)", "[0.05,0.08)", "[0.08,0.11)", "[0.11,0.14)", "[0.14,1.0)", "Undefined"]]\
    .to_excel(writer,'Sheet'+str(k/4+1), index = True, startcol = (k-1)*10, startrow = 0)

#### Bucket Overrall Summary
self_defined_summary_v3(df_group1, "B1", "today", 0, "None")\
.to_excel(writer,'Sheet'+str(1), index = True, startcol = 0*10, startrow = 5)

self_defined_summary_v3(df_group2, "B2", "today", 0, "None")\
.to_excel(writer,'Sheet'+str(1), index = True, startcol = 1*10, startrow = 5)

self_defined_summary_v3(df_group3, "B3", "today", 0, "None")\
.to_excel(writer,'Sheet'+str(1), index = True, startcol = 2*10, startrow = 5)

#### Bucket by Score Tiers Summary
tiers = ["(-inf,0.05)", "[0.05,0.08)", "[0.08,0.11)", "[0.11,0.14)", "[0.14,1.0)"]
for k in range(1,4,1):
    output_start = self_defined_summary_v3(df_group2, "B"+str(k), "today", k, tiers[0])
    for i in range(1,len(tiers)):
        output_new = self_defined_summary_v3(df_group2, "B"+str(k), "today", k, tiers[i])
        output_start = output_start.append(output_new)
    output_start.to_excel(writer,'Sheet'+str(k/4+1), index = True, startcol = (k-1)*10, startrow = 13)

writer.save()
