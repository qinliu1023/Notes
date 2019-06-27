def ratio_early_to_all(df, message):
    print message
    
    pivot_early = pd.pivot_table(df.query('is_MOB_Early == True'), columns = "pp_created_yearHalf", 
                                 index = "structure_general",  values = "pp_id", aggfunc = "count", margins = True, fill_value = 0, dropna = False, margins_name = "Total")
    
    pivot_total = pd.pivot_table(df, columns = "pp_created_yearHalf", 
                                 index = "structure_general",  values = "pp_id", aggfunc = "count", margins = True, fill_value = 0, dropna = False, margins_name = "Total")
    
    
    early_ratio = (pivot_early / pivot_total).round(4).fillna(" ")
​
    def highlight_max(s):
        '''
        highlight the maximum in a Series green.
        '''
        s1 = s[:-1].replace(" ", 0)
        is_max = s == max(s1)
        is_max[-1] = False # set Total Row to False
        return ['background-color: green' if v else '' for v in is_max]
​
    return multi_table([pivot_total, 
                       early_ratio.style.apply(highlight_max, subset = early_ratio.columns[:-1], axis = 0)])
​
​
​
​
​
# All Plans
​
def highlight_max(s):
    '''
    highlight the maximum in a Series green.
    '''
    num = len(s) - 1
    s1, s2 = s[:num/2], s[num/2:-1]
    is_max = (s == max(s1)) | (s == max(s2))
    return ['background-color: green' if v else '' for v in is_max]
​
​
b = pd.pivot_table(plans_all_final, columns = "pp_created_yearHalf", index = ["is_MOB_Early", "structure_general"],  values = "pp_id", aggfunc = "count", margins = True, fill_value = 0, dropna = False, margins_name = "Total")
​
multi_table([b, 
             (b.div(b.iloc[-1, :], axis = 1) * 100).round(2).style.apply(highlight_max, subset = b.columns[:-1], axis = 0)])
