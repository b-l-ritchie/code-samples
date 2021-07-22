# custom function to create chart visualization plotting price, the algorithm's score, and slope of score line
# inputs required are individual company ticker, the dataframe created by the algorithm, and choice of score indicator produced by the algorithm

def main_chart(ticker, df, indicator):
    df_plot = df
    score_color = 'cyan'
    price_color = '#00ff88'
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=df_plot['obs_date'], 
            y=df_plot['price'], 
            name='price', 
            line=dict(
                color=price_color
            )
        ),
        secondary_y=False,
    )
    # -- Add functionality to toggle the trends
    fig.add_trace(
        go.Scatter(
            x=df_plot['obs_date'], 
            y=df_plot['bestfit'], 
            name='Score Trend', 
            line=dict(
                color=score_color
            )
        ),
        secondary_y=True,
    )
    
    fig.add_trace(
        go.Scatter(
            x=df_plot['obs_date'], 
            y=df_plot[indicator], 
            name='Score', 
            line=dict(
                color=score_color
            )
        ),
        secondary_y=True,
    )
    
    fig.update_layout(
        xaxis_rangeslider_visible = False,
        width = 900,
        height = 400,
        margin = dict(t=50, r=5, l=5, b=5),
        # paper_bgcolor = '#090909',
        paper_bgcolor = '#1B1B1B',
        plot_bgcolor = '#1B1B1B',
        font = dict(
            color='white',
            family='arial'
        ),
        # font_family='Arial',
        xaxis = dict(
            showgrid=False, 
            zeroline=False
        ),
        yaxis = dict(
            showgrid=False, 
            zeroline=False, 
            ticks='inside'
        ),
        yaxis2 = dict(
            showgrid=False, 
            zeroline=False, 
            ticks='inside'
        ),
        showlegend = False,
        title = dict(
            text=ticker,
            font=dict(
                size=24
            )
        ),
        # annotations for future buy/sell signals. x/y location to be dynamic based on signal output
        # annotations=[
        #     dict(text='BUY', x='2020-03-23', y=212.59),
        #     dict(text='SELL', x='2020-02-19', y=314.37)
        # ]
    )
    # fig.update_xaxes(title_text='Date')
    fig.update_yaxes(
        title=dict(
            text='Price', 
            font=dict(
                size=16
            )
        ), 
        secondary_y=False, 
        color=price_color
    )
    fig.update_yaxes(
        title=dict(
            text='Score', 
            font=dict(
                size=16
            )
        ), 
        secondary_y=True, 
        color=score_color
    )
    chart = plot(fig, output_type='div')
    fig.show()
    # return chart