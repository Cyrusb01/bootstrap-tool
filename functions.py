#from pandas._config.config import reset_option
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import bt
from tabulate import tabulate
import plotly.graph_objects as go

# strategy_color = '#A90BFE'
# P6040_color = '#FF7052'
# spy_color = '#66F3EC'
# agg_color = '#67F9AF'
# colors = [strategy_color, P6040_color, spy_color, agg_color, '#EF5BDA', '#3527F5', '#F28585', '#43F22D', '#F1F040']


onramp_colors = {
    "dark_blue" : "#131C4F",
    "seafoam"   : "#00EEAD",
    "gray"      : "#B0B6BD",
    "light_blue": "#2F61D5",
    "pink"      : "#A90BFE",
    "purple"    : "#7540EE",
    "cyan"      : "#3FB6DC",
    "orange"    : "#FF7052",
    "white"     : "white"
}

onramp_title = {"font": {"size": 20, "color": onramp_colors["gray"]}}

onramp_xaxis = {
    "showgrid": False,
    "linecolor": onramp_colors["gray"],
    "color": onramp_colors["gray"],
    "tickangle": 330,
    "titlefont": {"size": 12, "color": onramp_colors["gray"]},
    "tickfont": {"size": 11, "color": onramp_colors["gray"]},
    "zeroline": False,
}

corporate_yaxis = {
    "showgrid": True,
    "color": onramp_colors["gray"],
    "gridwidth": 0.5,
    "gridcolor": onramp_colors["gray"],
    "linecolor": onramp_colors["gray"],
    "titlefont": {"size": 12, "color": onramp_colors["gray"]},
    "tickfont": {"size": 11, "color": onramp_colors["gray"]},
    "zeroline": False,
}
onramp_font_family = "Roboto"

onramp_legend = {
    "orientation": "h",
    "yanchor": "bottom",
    "y": -.3,
    "xanchor": "left",
    "x": 0,
    "font": {"size": 15, "color": onramp_colors["gray"]},
}  # Legend will be on the bottom middle

onramp_margins = {
    "l": 30,
    "r": 10,
    "t": 0,
    "b": 140,
}  # Set top margin to in case there is a legend


onramp_layout = go.Layout(
    colorway= [onramp_colors["seafoam"], onramp_colors["pink"], onramp_colors["orange"], onramp_colors["light_blue"]],
    font = {'family' : onramp_font_family},
    title=onramp_title,
    title_x=0.5, # Align chart title to center
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=onramp_xaxis,
    yaxis=corporate_yaxis,
    height=200,
    legend=onramp_legend,
    margin=onramp_margins,
)

onramp_template = dict(layout=go.Layout(onramp_layout))

def line_chart(results_list):
    result_final = pd.DataFrame()
    for i in range(len(results_list)):

        temp = results_list[i]._get_series(None).rebase()
        result_final = pd.concat([result_final, temp], axis = 1) #result dataframe
        #color_dict[result_final.columns[i]] = colors[i] #colors

    fig = px.line(result_final, labels=dict(index="Click Legend Icons to Toggle Viewing", value="", variable=""),
                    title="",
                    template= onramp_template
                    #height = 350
                    )
    
    fig.update_yaxes( # the y-axis is in dollars
        tickprefix="$"
    )
    fig.update_layout(
        legend = {
            "xanchor": "left",
            "x": .2,
        }  
    )
    return fig

def plotly_pie(stock_list, percent_list):
    
    fig = px.pie( values = percent_list, names = stock_list, color = stock_list, template = onramp_template, hole = .3)
    
    
    #fig.update_traces(marker=dict(line=dict(color='white', width=1.3)))
    

    return fig
    
def results_to_df(results_list):
    df_list = [] #list of completed dataframes
    
    for x in results_list:
        string_res = x.to_csv(sep=',') #This creates string of results stats 
        df = pd.DataFrame([x.split(',') for x in string_res.split('\n')]) # Takes the string and creates a dataframe 
        nan_value = float("NaN") 
        df.replace("", nan_value, inplace=True) #lot of empty collumns in dataframe, this makes the empty go to null("NaN")
        df.dropna(how='all', axis=1, inplace=True) #delete null collumns
        df = df.dropna()

        df_list.append(df)
    
    return df_list

def display_stats_combined(results_list): #works for list of two results df 
    
    df_list = results_to_df(results_list) #The results arent dataframes, so need to make them dataframes
    
    stats_combined = pd.concat([df_list[0], df_list[1]], axis=1) #this combines them 
    stats_combined.columns = ['Stats', 'Strategy 1', 'Drop', "Strategy 2"]
    stats_combined = stats_combined.drop(['Drop'], axis =1 )

    return stats_combined

def scatter_plot(results_list):
    results_df = results_to_df(results_list)
    xaxis_vol = []
    yaxis_return = []
    for x in results_df: #fill in two lists with the vol and return %s 
        xaxis_vol.append(float(x.iloc[30][1].replace('%', '')))
        yaxis_return.append(float(x.iloc[29][1].replace('%', '')))
    
    size_list =[]
    for i in range(len(xaxis_vol)): #getting errors on the number of sizes
        size_list.append(4)
    
    labels = []
    for i in results_df:
        labels.append(i.iloc[0][1])
    
    fig = px.scatter( x= xaxis_vol, y= yaxis_return, size = size_list, color = labels,
                            labels={
                            "x": "Monthly Vol (ann.) %",
                            "y": "Monthly Mean (ann.) %",
                            "color" : ""
                            },
                            title="", 
                            template= onramp_template,
                            #width = 530, height = 350
                            )
    
    return fig

def balance_table(results, results_con):
    labels = ['<b>Strategy<b>', '<b>Initial Investment<b>', '<b>Final Balance<b>']
    series_res = results._get_series(None).rebase()
    series_con = results_con._get_series(None).rebase()
    final_res = round(series_res.iloc[-1])
    final_con = round(series_con.iloc[-1])
    final_res = '$' + str(int(final_res)) #this line gets the $, but the initial final_res is a dataframe object type so this line is neccesary for the $
    final_con = '$' + str(int(final_con))

    name = series_res.columns[0]
    #st.write(name)
    fig = go.Figure(data=[go.Table(
                                header=dict(values= labels,
                                            line_color= onramp_colors["gray"],
                                            fill_color= onramp_colors['gray'],
                                            align=['center','center'],
                                            font=dict(color='black', size=11)),
                                cells=dict(values=[['60-40 Portfolio', series_res.columns[0]], ["$100", "$100"], [final_con, final_res]],
                                            line_color = onramp_colors["gray"],
                                            font = dict(color = 'white', size = 11),
                                            fill_color = onramp_colors["dark_blue"] )) ])
    fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }
        )
    fig.update_layout(margin = dict(l=1, r=1, t=0, b=0))
    
    return fig

def short_stats_table(results_list):
    stats_0 = results_list[0].display_lookback_returns() #these objects are the dataframes we want, just need to combine them and-
    stats_1 = results_list[1].display_lookback_returns()   #make them into a nice table


    labels= ["<b>Stats<b>", '<b>'+ stats_0.columns[0] + '<b>', "<b>60-40 Portfolio<b>", "<b>Difference<b>"]

    #combining 
    stats_combined = pd.concat([stats_0, stats_1], axis=1)
    stats_combined.columns = ['Your_Strategy', "Portfolio6040"]
    stats_combined = stats_combined.dropna()
    
    #adding new row of differences
    stats_combined['Difference'] = stats_combined.apply(lambda row: 
                                        str(round(float(row.Your_Strategy.replace('%', ''))- float(row.Portfolio6040.replace('%', '')), 2)) + '%', axis = 1)  

    fig = go.Figure(data=[go.Table(
                            header=dict(values= labels,
                                        line_color= onramp_colors["gray"],
                                        fill_color= onramp_colors["gray"],
                                        align=['center','center'],
                                        font=dict(color='black', size=10)),
                            cells=dict(values=[stats_combined.index, stats_combined.Your_Strategy, stats_combined.Portfolio6040, stats_combined.Difference],
                                        line_color = onramp_colors["gray"],
                                        height = 30,
                                        font = dict(color = 'white'),
                                        fill_color = onramp_colors["dark_blue"] )) ])
    fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }
        )
    fig.update_layout(margin = dict(l=2, r=1, t=0, b=0))
    return fig

def monthly_table(results_list):

    

    key = results_list[0]._get_backtest(0) #syntax for getting the monthly returns data frame 
    res_mon = results_list[0][key].return_table
    df_r = pd.DataFrame(res_mon)

    keyc = results_list[1]._get_backtest(0)  
    res_con = results_list[1][keyc].return_table
    df_c = pd.DataFrame(res_con)

    keys = results_list[2]._get_backtest(0) #syntax for getting the monthly returns data frame 
    res_spy = results_list[2][keys].return_table
    df_s = pd.DataFrame(res_spy)

    keya = results_list[3]._get_backtest(0)  
    res_agg = results_list[3][keya].return_table
    df_a = pd.DataFrame(res_agg)

    strategy_color = '#A90BFE'
    P6040_color = '#FF7052'
    spy_color = '#66F3EC'
    agg_color = '#67F9AF'
    label_color = '#131c4f'

    #hard part of this is combining
    index = res_mon.index
    index = index.tolist()
    
    
    year_rows =[] #create a list of the rows of year month month YTD
    for i in range(len(res_mon.index)):
        temp = []
        temp.append(index[i])
        temp.append("Jan")
        temp.append("Feb")
        temp.append("Mar")
        temp.append("Apr")
        temp.append("May")
        temp.append("Jun")
        temp.append("Jul")
        temp.append("Aug")
        temp.append("Sep")
        temp.append("Oct")
        temp.append("Nov")
        temp.append("Dec")
        temp.append("YTD")
        year_rows.append(temp)


    df_results = results_to_df(results_list) #doing this because we need to get the correct name of the strategy
    res_rows = [] #this creates the list of the "Your Strategy" then all the numbers
    for i in range(len(res_mon.index)):
        temp = []
        temp += [df_results[0].iloc[0][1]]
        for j in range(len(res_mon.columns)):
            temp += [str(round(df_r.iloc[i][j]*100, 2)) + '%']
        res_rows.append(temp)
    
    con_rows = [] #this creates the list of the "60-40 Portfolio " then all the numbers
    for i in range(len(res_con.index)):
        temp = []
        temp += ["60-40 Portfolio"]
        for j in range(len(res_con.columns)):
            temp += [str((round(df_c.iloc[i][j] *100, 2))) + '%'] #this takes the value in, round to 2 decimal places, and adds the percent sign
        con_rows.append(temp)

    spy_rows = [] #this creates the list of the "60-40 Portfolio " then all the numbers
    for i in range(len(res_spy.index)):
        temp = []
        temp += ["SPY"]
        for j in range(len(res_spy.columns)):
            temp += [str((round(df_s.iloc[i][j] *100, 2))) + '%'] #this takes the value in, round to 2 decimal places, and adds the percent sign
        spy_rows.append(temp)
    
    agg_rows = [] #this creates the list of the "60-40 Portfolio " then all the numbers
    for i in range(len(res_agg.index)):
        temp = []
        temp += ["AGG"]
        for j in range(len(res_agg.columns)):
            temp += [str((round(df_a.iloc[i][j] *100, 2))) + '%'] #this takes the value in, round to 2 decimal places, and adds the percent sign
        agg_rows.append(temp)

    length = len(year_rows)

    
    list_4_df = [] #appends the rows in the correct order
    for i in range(length):
        list_4_df.append(year_rows[(length-1)-i])
        list_4_df.append(res_rows[(length-1)-i])
        list_4_df.append(con_rows[(length-1)-i])
        list_4_df.append(spy_rows[(length-1)-i])
        list_4_df.append(agg_rows[(length-1)-i])
    
    label_row = year_rows[length-1] #grabs the label row
    for i in range (len(year_rows)): # this loop is to make all the labels bold
        for j in range(len(year_rows[0])):
            label_row[j] = str(label_row[j])
            label_row[j] = '<b>' + label_row[j] + '<b>'

            year_rows[i][j] = str(year_rows[i][j])
            year_rows[i][j] = '<b>' + year_rows[i][j] + '<b>'

    for i in range (len(res_rows)): # this loop is to make all the strategy titles bold 

        res_rows[i][0] = str(res_rows[i][0])
        res_rows[i][0] = '<b>' + res_rows[i][0] + '<b>'  

        con_rows[i][0] = str(con_rows[i][0])
        con_rows[i][0] = '<b>' + con_rows[i][0] + '<b>'   

        spy_rows[i][0] = str(spy_rows[i][0])
        spy_rows[i][0] = '<b>' + spy_rows[i][0] + '<b>'

        agg_rows[i][0] = str(agg_rows[i][0])
        agg_rows[i][0] = '<b>' + agg_rows[i][0] + '<b>'

    df = pd.DataFrame(list_4_df) #creates a dataframe of the lists
    df = df.drop(df.index[0]) #drops the label row, this is for creating a plotly table better 
    
    color_list = []
    font_color_list = []
    color_list += [strategy_color]
    color_list += [P6040_color]
    color_list += [spy_color]
    color_list += [agg_color]
    color_list += [label_color]
    font_color_list += ['black']
    font_color_list += ['black']
    font_color_list += ['black']
    font_color_list += ['black']
    font_color_list += ['white']
    for i in range(length-1):
        color_list += [strategy_color]
        color_list += [P6040_color]
        color_list += [spy_color]
        color_list += [agg_color]
        color_list += [label_color]
        font_color_list += ['black']
        font_color_list += ['black']
        font_color_list += ['black']
        font_color_list += ['black']
        font_color_list += ['white']
    
    color_list2 = []
    for i in range(length):
        color_list2 += ['#f7f7f7']
        color_list2 += ['#f7f7f7']
        color_list2 += ['#f7f7f7']
        color_list2 += ['#f7f7f7']
        color_list2 += [label_color]

    df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
    #making the table 
    date_color = '#131c4f'
    fig = go.Figure(data=[go.Table(
                            #columnorder = [1,2,1,1,1,1,1,1,1,1,1,1,1,1],
                            columnwidth = [200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                            header=dict(values= label_row,
                                        line_color= '#dbdbdb',
                                        height = 30,
                                        fill_color= '#131c4f',
                                        align=['center','center'],
                                        font=dict(color='white', size=12)),
                            cells=dict(values=[df.a, df.b, df.c, df.d, df.e, df.f, df.g, df.h, df.i, df.j, df.k, df.l, df.m, df.n],
                                        line_color = '#dbdbdb',
                                        height = 30,
                                        font = dict(color = [font_color_list*14]),
                                        fill_color = [color_list] )) ])
    fig.update_layout(margin = dict(l=0, r=0, t=1, b=0))


    return fig
    #['#A90BFE', '#FF7052', date_color, '#A90BFE','#FF7052', date_color, '#A90BFE', '#FF7052', date_color, '#A90BFE', '#FF7052', date_color, '#A90BFE', '#FF7052']
    #['black', 'black', 'white', 'black','black', 'white', 'black', 'black', 'white', 'black', 'black', 'white', 'black', 'black']

def optomize_table(df):
    df = pd.DataFrame(df)
    
    #combining 
    labels = ['<b>Tickers<b>', '<b>Allocation<b>']

    df.columns = ["Allocation"]
    df = df.dropna()
    
    fig = go.Figure(data=[go.Table(
                            header=dict(values= labels,
                                        line_color= 'black',
                                        fill_color= '#131c4f',
                                        align=['center','center'],
                                        font=dict(color='white', size=10)),
                            cells=dict(values=[df.index, df.Allocation],
                                        line_color = 'black',
                                        height = 30,
                                        font = dict(color = 'black'),
                                        fill_color = '#f7f7f7' )) ])
    fig.update_layout(margin = dict(l=1, r=0, t=0, b=0))
    return fig

def optomize_table_combine(df):
    
    #combining 
    labels = ['<b>Tickers<b>', '<b>Daily<b>', '<b>Monthly<b>', '<b>Quarterly<b>', '<b>Yearly<b>']

    fig = go.Figure(data=[go.Table(
                            header=dict(values= labels,
                                        line_color= 'black',
                                        fill_color= '#131c4f',
                                        align=['center','center'],
                                        font=dict(color='white', size=10)),
                            cells=dict(values=[df.index, df.Daily, df.Monthly, df.Quarterly, df.Yearly],
                                        line_color = 'black',
                                        height = 30,
                                        font = dict(color = 'black'),
                                        fill_color = '#f7f7f7' )) ])
    fig.update_layout(margin = dict(l=1, r=0, t=0, b=0))
    return fig

def stats_table(results_list):

    df_list = results_to_df(results_list) #The results arent dataframes, so need to make them dataframes

    stats_combined = pd.concat([df_list[0], df_list[1]], axis=1) #this combines them 
    stats_combined.columns = ['Stats', 'Your Strategy', 'Drop', "60-40 Portfolio"]
    stats_combined = stats_combined.drop(['Drop'], axis =1 )

    stats_col = []
    stats_col.append(stats_combined.iloc[1][0])
    stats_col.append(stats_combined.iloc[2][0])
    stats_col.append(stats_combined.iloc[4][0])
    stats_col.append(stats_combined.iloc[8][0])
    stats_col.append(stats_combined.iloc[27][0])
    stats_col.append(stats_combined.iloc[28][0])
    stats_col.append(stats_combined.iloc[29][0])
    stats_col.append(stats_combined.iloc[30][0])
    stats_col.append(stats_combined.iloc[33][0])
    stats_col.append(stats_combined.iloc[34][0])
    
    strat1_col = []
    strat1_col.append(stats_combined.iloc[1][1])
    strat1_col.append(stats_combined.iloc[2][1])
    strat1_col.append(stats_combined.iloc[4][1])
    strat1_col.append(stats_combined.iloc[8][1])
    strat1_col.append(stats_combined.iloc[27][1])
    strat1_col.append(stats_combined.iloc[28][1])
    strat1_col.append(stats_combined.iloc[29][1])
    strat1_col.append(stats_combined.iloc[30][1])
    strat1_col.append(stats_combined.iloc[33][1])
    strat1_col.append(stats_combined.iloc[34][1])

    strat2_col = []
    strat2_col.append(stats_combined.iloc[1][2])
    strat2_col.append(stats_combined.iloc[2][2])
    strat2_col.append(stats_combined.iloc[4][2])
    strat2_col.append(stats_combined.iloc[8][2])
    strat2_col.append(stats_combined.iloc[27][2])
    strat2_col.append(stats_combined.iloc[28][2])
    strat2_col.append(stats_combined.iloc[29][2])
    strat2_col.append(stats_combined.iloc[30][2])
    strat2_col.append(stats_combined.iloc[33][2])
    strat2_col.append(stats_combined.iloc[34][2])

    #creates a datframe with exactly what we need
    df = pd.DataFrame(list(zip(stats_col, strat1_col, strat2_col)), 
               columns =['Stats', 'Your_Strategy', 'Portfolio6040'])
    labels = ['<b>Stats<b>', '<b>' +stats_combined.iloc[0][1] + '<b>', "<b>60-40 Portfolio<b>"]
    
    fig = go.Figure(data=[go.Table(
                            header=dict(values= labels,
                                        line_color= onramp_colors["gray"],
                                        fill_color= onramp_colors["gray"],
                                        align=['center','center'],
                                        font=dict(color='black', size=11)),
                            cells=dict(values=[df.Stats, df.Your_Strategy, df.Portfolio6040],
                                        line_color = onramp_colors["gray"],
                                        height = 30,
                                        font = dict(color = 'white'),
                                        fill_color =  onramp_colors["dark_blue"])) ])
    fig.update_layout(margin = dict(l=2, r=1, t=0, b=10), 
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",)

    return fig






