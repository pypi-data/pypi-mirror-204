import pandas as pd
from IPython.core.display import HTML

def correlation(df):
    corr = df.corr()
    corr_stacked = corr.stack().reset_index()
    corr_stacked.columns = ['var1', 'var2', 'corr']
    corr_stacked = corr_stacked[(corr_stacked['corr'] != 1.0) & (corr_stacked['corr'] != -1.0)]
    corr_stacked = corr_stacked[corr_stacked['var1'] < corr_stacked['var2']] # Remove duplicates
    corr_stacked.sort_values(by=['corr'], ascending=False, inplace=True)

    html_table = '<table><thead><tr><th>Variable 1</th><th>Variable 2</th><th>Correlation</th></tr></thead>'
    html_table += '<tbody>'
    for index, row in corr_stacked.iterrows():
        html_table += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(row['var1'], row['var2'], round(row['corr'], 2))
    html_table += '</tbody></table>'

    return HTML('<div style="max-height:300px; overflow-y:auto;">{}</div>'.format(html_table))
