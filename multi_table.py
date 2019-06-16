# https://github.com/epmoyer/ipy_table/issues/24   

from IPython.core.display import HTML

def multi_table(table_list):
    ''' Acceps a list of IpyTable objects and returns a table which contains each IpyTable in a cell
    '''
    return HTML(
        '<table><tr style="background-color:white;">' + 
        ''.join(['<td>' + table._repr_html_() + '</td>' for table in table_list]) +
        '</tr></table>'
    )


## A more basic way
df1_styler = result1.style.\
                set_table_attributes("style='display:inline-block'").\
                set_caption('Cure Rate of Old Strategy')
df2_styler = result2.style.\
                set_table_attributes("style='display:inline-block'").\
                set_caption('Cure Rate of Hold Out Strategy')
df3_styler = result3.style.\
                set_table_attributes("style='display:inline-block'").\
                set_caption('Cure Rate of New Strategy')
display_html(df1_styler._repr_html_()+df2_styler._repr_html_()+df3_styler._repr_html_(), raw=True)