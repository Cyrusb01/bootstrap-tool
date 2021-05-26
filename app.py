import dash
from dash_bootstrap_components._components.CardBody import CardBody
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
import bt
from functions import balance_table, monthly_returns_table, monthly_table, onramp_colors, onramp_template, line_chart, scatter_plot, stats_table, short_stats_table
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

server = app.server
# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************


def get_data():
  s_data = bt.get('spy,agg', start = '2017-01-01') #took out gold for now because of error
  #cry_data = bt.get('btc-usd,eth-usd', start = '2017-01-01')
  btc = bt.get('btc-usd', start = '2017-01-01') #had to implement this seperatly because eth data got cut out one day on yahoo finance 
  data_cache = btc.join(s_data, how='outer')
  data_cache = data_cache.dropna()
  return data_cache

data = get_data()


def calculate_controls():
  stock_dic_control = {'spy': float(60)/100, 'agg': float(40)/100, 'vwo': float(0)/100}
  stock_dic_spy = {'spy': float(100)/100, 'agg': float(0)/100, 'vwo': float(0)/100}
  stock_dic_agg = {'spy': float(0)/100, 'agg': float(100)/100, 'vwo': float(0)/100}
                            
  strategy_control = bt.Strategy('60-40 Portfolio', 
                          [bt.algos.RunMonthly(), 
                          bt.algos.SelectAll(), 
                          bt.algos.WeighSpecified(**stock_dic_control),
                          bt.algos.Rebalance()]) #Creating strategy
  strategy_spy = bt.Strategy('SPY', 
                          [bt.algos.RunMonthly(), 
                          bt.algos.SelectAll(), 
                          bt.algos.WeighSpecified(**stock_dic_spy),
                          bt.algos.Rebalance()]) #Creating strategy
  strategy_agg = bt.Strategy('AGG', 
                          [bt.algos.RunMonthly(), 
                          bt.algos.SelectAll(), 
                          bt.algos.WeighSpecified(**stock_dic_agg),
                          bt.algos.Rebalance()]) #Creating strategy
  test_control = bt.Backtest(strategy_control, data)
  results_control = bt.run(test_control)
  
  test_spy = bt.Backtest(strategy_spy, data)
  results_spy = bt.run(test_spy)
  
  test_agg = bt.Backtest(strategy_agg, data)
  results_agg = bt.run(test_agg)

  results_return = [results_control, results_spy, results_agg]

  return results_return 

returns = calculate_controls()

results_control = returns[0]
results_spy = returns[1]
results_agg = returns[2]




def drawFigure():
    return  dbc.Container([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])

def Inputs():

    inputs_ = dbc.Card(
            dbc.CardBody([
                #Inputs 1 
                dbc.Row([
                    dbc.Col(
                        dcc.Input(
                            id = "Ticker1",
                            type= 'text',
                            value = "spy",
                            placeholder= "Enter Ticker",
                            size = "10"

                        ),
                    width={'size':1}, className= "mr-5 mb-4"
                    ), 

                    dbc.Col(
                        dcc.Input(
                            id = "Allocation1",
                            value = "40",
                            type= 'text',
                            placeholder= "Enter Allocation %"

                        ), width={'size':1, 'offset':2},
                    ),
                ]),

                #Inputs 2 
                dbc.Row([
                    dbc.Col(
                        dcc.Input(
                            id = "Ticker2",
                            type= 'text',
                            value = 'agg',
                            placeholder= "Enter Ticker",
                            size = "10"

                        ),
                    width={'size':1}, className= "mr-5 mb-4"
                    ), 

                    dbc.Col(
                        dcc.Input(
                            id = "Allocation2",
                            type= 'text',
                            value = "20",
                            placeholder= "Enter Allocation %"

                        ), width={'size':1, 'offset':2},
                    ),
                ]),

                #Inputs 3 
                dbc.Row([
                    dbc.Col(
                        dcc.Input(
                            id = "Ticker3",
                            type= 'text',
                            value = 'btc-usd',
                            placeholder= "Enter Ticker",
                            size = "10"

                        ),
                    width={'size':1}, className= "mr-5 mb-4"
                    ), 

                    dbc.Col(
                        dcc.Input(
                            id = "Allocation3",
                            type= 'text',
                            value = '20',
                            placeholder= "Enter Allocation %"

                        ), width={'size':1, 'offset':2},
                    ),
                ]),

                #Inputs 4 
                dbc.Row([
                    dbc.Col(
                        dcc.Input(
                            id = "Ticker4",
                            type= 'text',
                            placeholder= "Enter Ticker",
                            size = "10"

                        ),
                    width={'size':1}, className= "mr-5 mb-4"
                    ), 

                    dbc.Col(
                        dcc.Input(
                            id = "Allocation4",
                            type= 'text',
                            placeholder= "Enter Allocation %"

                        ), width={'size':1, 'offset':2},
                    ),
                ]),

                #Inputs 5 
                dbc.Row([
                    dbc.Col(
                    width={'size':1}, className= "mr-5 mb-4" #Empty Col for Rebalance 
                    ), 

                    dbc.Col(
                        dcc.Input(
                            id = "Rebalance",
                            type= 'text',
                            placeholder= "Rebalance Threshold %"

                        ), width={'size':1, 'offset':2},
                    ),
                ]),
                
            ]), className= "text-center mr-4 mb-4", style= {"height": "22rem"}
        )

    return inputs_

def Description():

    descript = dbc.Card(
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.P(children= "Commerce on the Internet has come to rely almost exclusively on financial institutions serving as trusted third parties to process electronic payments. While the system works well enough for most transactions, it still suffers from the inherent weaknesses of the trust based model. Completely non-reversible transactions are not really possible, since financial institutions cannotavoid mediating disputes."),
                            
                            html.P(children= "Commerce on the Internet has come to rely almost exclusively on financial institutions serving as trusted third parties to process electronic payments. While the system works well enough for most transactions, it still suffers from the inherent weaknesses of the trust based model. Completely non-reversible transactions are not really possible, since financial institutions cannotavoid mediating disputes.")
                            
                            #className= "text-center")
                            
                        ])

                    ])
                
                ]), className= "text-center mr-4 mb-4", style= {"height": "22rem"}
    )

    return descript

def DisplayPie():
    pie = dbc.Card(
        dbc.CardBody([
            dcc.Graph(
                id = "pie_chart"
            )
        ]), style= {"height": "22rem"}
    )

    return pie
           
def DisplayLineChart():
    line = dbc.Card(
        dbc.CardBody([
            dcc.Graph(
                id = "line_chart",
                style= {"responsive": True}
            )
        ]),  className= "mr-4 mb-4", style= {"max-width" : "100%", "margin": "auto", "height": "24rem"}
    )

    return line        

def DisplayScatter():
    scat = dbc.Card(
        dbc.CardBody([
            dcc.Graph(
                id = "scatter_plot",
                style= {"responsive": True}
            )
        ]),  className= "mr-4 mb-4", style= {"max-width" : "100%", "margin": "auto", "height": "24rem"}
    )

    return scat        

def DisplayStats():
    stats = dbc.Card(
        dbc.CardBody([
            dcc.Graph(
                id = "stats_table",
                style= {"responsive": True}
            )
        ]),  className= "mb-4", style= {"max-width" : "100%", "margin": "auto", "height": "24rem"}
    )

    return stats        

def DisplayReturnStats():
    stats = dbc.Card(
        dbc.CardBody([
                dcc.Graph(
                id = "balance_table",
                style= {"responsive": True}
                ),
                dcc.Graph(
                id = "return_stats",
                style= {"responsive": True}
                )
                            
        ]),  className= "mb-4", style= {"max-width" : "100%", "margin": "auto", "height": "24rem"}
    )

    return stats      

def DisplayMonthTable():
    stats = dbc.Card(
        dbc.CardBody([
            dcc.Graph(
                id = "month_table",
                style= {"responsive": True}
            )
        ]),  className= "mr-4 mb-4", style= {"max-width" : "100%", "margin": "auto", "height": "50rem"}
    )

    return stats        




app.layout = dbc.Container([
   
    #Title 
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody("Custom Strategy Dashboard"), 
            className="text-center mb-4"), 
        width = 12)
    ),

    #Column Headers Input Dashboard Description Portfolio Allocaiton
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody("Inputs"), 
                className= "text-center mr-4 mb-4"),
        width = 3
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody("Dashboard Description"), 
                className= "text-center mr-4 mb-4"),
        width = 6
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody("Portfolio Allocation"), 
                className= "text-center mb-4"),
        width = 3
        ),
    ]), 
    
    # Actually Inputs Descriptions Pie 
    dbc.Row([
        dbc.Col([
            Inputs()
        ], width = 3),
        
        dbc.Col([
            Description()
        ], width = 6),

        dbc.Col([
            DisplayPie()
        ], width = 3),
    ]),

    #Column Headers Porfolio Performance Risk Vs. Return Performance Statistics
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody("Portfolio Performance"), 
                className= "text-center mr-4 mb-4"),
        width = 5
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody("Risk Vs. Return"), 
                className= "text-center mr-4 mb-4"),
        width = 4
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody("Performance Statistics"), 
                className= "text-center mb-4"),
        width = 3
        ),
    ]), 

    #Line chart Scatter 
    dbc.Row([
        dbc.Col([
            DisplayLineChart()
        ], width = 5),
        
        dbc.Col([
            DisplayScatter()
        ], width = 4),

        dbc.Col([
            DisplayStats()
        ], width = 3),
    ]),

    #Column Headers Returns Breakdown Returns Recap 
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody("Returns Breakdown"), 
                className= "text-center mr-4 mb-4"),
        width = 9
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody("Returns Recap"), 
                className= "text-center mr-4 mb-4"),
        width = 3
        ),
    ]), 

    dbc.Row([
        dbc.Col([
            DisplayMonthTable()
        ], width = 9),
        
        dbc.Col([
            DisplayReturnStats()
        ], width = 3),

    ]),
], fluid=True)


@app.callback(
    [Output('pie_chart', 'figure'),
    Output('line_chart', 'figure'),
    Output('scatter_plot', 'figure'),
    Output("stats_table", "figure"),
    Output("month_table", "figure"),
    Output("balance_table", "figure"),
    Output("return_stats", "figure")
    ],
    
    
    [Input('Ticker1', 'value'),
    Input('Allocation1', 'value'),
    Input('Ticker2', 'value'),
    Input('Allocation2', 'value'),
    Input('Ticker3', 'value'),
    Input('Allocation3', 'value')
    ]
)
def update_graph(stock_choice_1, alloc1, stock_choice_2, alloc2, stock_choice_3, alloc3):

    ####################################################### PIE CHART ##########################################################################################
    stock_list = [stock_choice_1, stock_choice_2, stock_choice_3]
    percent_list = [float(alloc1)/100, float(alloc2)/100, float(alloc3)/100]

    fig = px.pie( values = percent_list, names = stock_list, color = stock_list, title="Portfolio Allocation", template= onramp_template, hole = .3, height = 300)
    
    ##################################################### SETTING UP DATA #############################################################################################
    stock_choice_1 = stock_choice_1.lower()
    stock_choice_2 = stock_choice_2.lower()
    stock_choice_3 = stock_choice_3.lower()

    stock_list = stock_choice_1 +',' + stock_choice_2 + ',' + stock_choice_3
    
    data = bt.get(stock_list, start = '2017-01-01') 

    #need the '-' in cryptos to get the data, but bt needs it gone to work
    stock_choice_1 = stock_choice_1.replace('-', '')
    stock_choice_2 = stock_choice_2.replace('-', '')
    stock_choice_3 = stock_choice_3.replace('-', '')

    your_strategy = stock_choice_1.upper()  + '-' +  stock_choice_2.upper() +  '-' + stock_choice_3.upper()

    stock_dic = {stock_choice_1: float(alloc1)/100, stock_choice_2: float(alloc2)/100, stock_choice_3: float(alloc3)/100} #dictonary for strat
    
    strategy_ = bt.Strategy(your_strategy, 
                              [ 
                              bt.algos.RunDaily(),
                              bt.algos.SelectAll(), 
                              bt.algos.WeighSpecified(**stock_dic),
                              bt.algos.RunMonthly(),
                              bt.algos.Rebalance()]) #Creating strategy

    test = bt.Backtest(strategy_, data)
    results = bt.run(test)
    
    results_list = [results, results_control, results_spy, results_agg]

    ################################################### LINE CHART ########################################################################################################
    fig_line = line_chart(results_list)

    fig_scat = scatter_plot(results_list)

    fig_stats = stats_table(results_list)

    fig_month_table = monthly_table(results_list)

    fig_month_table.update_layout(height = 760)

    fig_balance_table = balance_table(results, results_control)

    fig_balance_table.update_layout(height = 100)

    fig_returns_stats = short_stats_table(results_list)

    return fig, fig_line, fig_scat, fig_stats, fig_month_table, fig_balance_table, fig_returns_stats

   




if __name__=='__main__':
    app.run_server(debug=True)