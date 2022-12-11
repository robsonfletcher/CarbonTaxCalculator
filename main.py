from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Source of carbon tax amounts per unit of fuel for 2023 ($65/tonne effective April 1):
# https://www.canada.ca/en/department-finance/news/2021/12/fuel-charge-rates-for-listed-provinces-and-territories-for-2023-to-2030.html

# Diesel amount is calculated relative to known previous amounts of gasoline (at $40 or $50 per tonne):
# https://www.nrcan.gc.ca/our-natural-resources/domestic-and-international-markets/transportation-fuel-prices/fuel-consumption-taxes-canada/18885
# Natural gas amounts calculated in GJ from known previous amounts (at $40 and $50 per tonne):
# https://www.directenergy.ca/alberta/federal-carbon-tax


app = Dash(
    title="Federal Carbon Tax Calculator",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

app.layout = html.Div([
    html.H1('Federal Carbon Tax Calculator'),
    html.H5('For the 2023/24 year ($65 per tonne)', style={'font-style': 'italic'}),
    html.Br(),
    html.H5('Household info:',
            style={'text-decoration': 'underline'}),
    html.Div([
        html.Label('Which province do you live in?'),
        dcc.Dropdown(
            id='province-dropdown',
            style={"width": "65%"},
            options=[
                {'label': 'Alberta', 'value': 'ab'},
                {'label': 'Saskatchewan', 'value': 'sk'},
                {'label': 'Manitoba', 'value': 'mb'},
                {'label': 'Ontario', 'value': 'on'}
            ],
            value='ab',
            clearable=False
        )
    ], style={'marginLeft': 15}),
    html.Small(
        'The federal carbon tax currently applies only in Alberta, Saskatchewan, Manitoba and Ontario. (Other provinces have their own carbon-pricing systems.)',
        style={'marginLeft': 15,
               "font-style": "italic"}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Label('Are there one or two adults in your household?'),
        dcc.RadioItems(
            id='num-adults-radio',
            labelStyle={'display': 'block'},
            options=[
                {'label': 'One', 'value': 'one'},
                {'label': 'Two', 'value': 'two'}
            ],
            value='one'
        )
    ], style={'marginLeft': 15}),
    html.Br(),
    html.Div([
        html.Label('How many dependent children do you have?'),
        html.Br(),
        dcc.Input(id='num-children-input', type='number', value=0)
    ], style={'marginLeft': 15}),
    html.Br(),
    html.Div([
        html.Label('Are you a rural resident?'),
        dcc.RadioItems(
            id='rural-radio',
            labelStyle={'display': 'block'},
            options=[
                {'label': 'No', 'value': 'no'},
                {'label': 'Yes', 'value': 'yes'}
            ],
            value='no'
        )
    ], style={'marginLeft': 15}),
    html.Br(),
    html.H5('Estimated fuel usage:',
            style={'text-decoration': 'underline'}),
    html.Div([
        html.Label('Gasoline (L / month):'),
        html.Br(),
        dcc.Input(id='gasoline-input', type='number', value=0),
        html.Br(),
        html.Small('Most vehicles take between 45 and 65 L to fill. A typical fill-up is about 50 L.',
                   style={'font-style': 'italic'}),
        html.Br(),
        html.Br(),
    ], style={'marginLeft': 15}),
    html.Div([
        html.Label('Diesel (L / month):'),
        html.Br(),
        dcc.Input(id='diesel-input', type='number', value=0),
        html.Br(),
        html.Small('Mid-size pickups typically take about 80 L to fill. Full-size pickups, 100 L or more.',
                   style={'font-style': 'italic'}),
        html.Br(),
        html.Br(),
    ], style={'marginLeft': 15}),
    html.Div([
        html.Label('Natural gas (GJ / month):'),
        html.Br(),
        dcc.Input(id='natural-gas-input', type='number', value=0),
        html.Br(),
        html.Small('A typical Canadian household uses about 8 GJ per month, on average, over the course of a year.',
                   style={'font-style': 'italic'}),
        html.Br(),
        html.Br(),
    ], style={'marginLeft': 15}),
    html.Div([
        html.Label('Propane (L / month):'),
        html.Br(),
        dcc.Input(id='propane-input', type='number', value=0),
        html.Br(),
        html.Small('A 20-lb propane tank (BBQ size) holds about 18 L of liquid propane.',
                   style={'font-style': 'italic'}),
        html.Br(),
        html.Br(),
    ], style={'marginLeft': 15}),
    html.Br(),
    html.Div(id='output-div', style={'marginLeft': 15}),
    html.Br(),
    html.H5('Notes:',
            style={'text-decoration': 'underline'}),
    html.Label(
        '• Your household information is used to calculate the rebate you will receive for the 2023/24 year.',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label(
        '• Your monthly fuel usage is used to calculate how much you will pay in carbon tax over that full year.',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label('• Calculations are based on a carbon tax rate of $65 per tonne, which takes effect April 1, 2023.',
               style={'marginLeft': 15}),
    html.Br(),
    html.Label('• Payments are issued quarterly: In April, July & October of 2023 and in January 2024.',
               style={'marginLeft': 15}),
    html.Br(),
    html.Label('• Rural residents receive a 10% supplement:',
               style={'marginLeft': 15}),
    html.Br(),
    html.A('• ', style={'marginLeft': 15}),
    html.A('Find out who qualifies as a rural resident.',
           href='https://www.canada.ca/en/revenue-agency/services/child-family-benefits/cai-payment/qualify-for-the-supplement.html',
           target="_blank"),
    html.Br(),
    html.Br(),
    html.H5('About the Calculator:', style={'text-decoration': 'underline'}),
    html.Br(),
    dcc.Markdown("**• Created by [Robson Fletcher](https://twitter.com/cbcfletch)**", style={'marginLeft': 15}),
    html.A('• ', style={'marginLeft': 15}),
    html.A('Source of rebate data',
           href='https://www.canada.ca/en/department-finance/news/2022/11/climate-action-incentive-payment-amounts-for-2023-24.html',
           target="_blank", style={'font-style': 'italic'}),
    html.Br(),
    html.A('• ', style={'marginLeft': 15}),
    html.A('Source of pricing data',
           href='https://www.canada.ca/en/department-finance/news/2021/12/fuel-charge-rates-for-listed-provinces-and-territories-for-2023-to-2030.html',
           target="_blank", style={'font-style': 'italic'})
], style={'marginLeft': 5,
          'marginBottom': 20})


# ----------------------- CALLBACK FUNCTION BELOW ----------------

@app.callback(
    Output('output-div', 'children'),
    [Input('province-dropdown', 'value'),
     Input('num-children-input', 'value'),
     Input('rural-radio', 'value'),
     Input('num-adults-radio', 'value'),
     Input('gasoline-input', 'value'),
     Input('diesel-input', 'value'),
     Input('natural-gas-input', 'value'),
     Input('propane-input', 'value')
     ])
def update_output_div(province, num_children, rural, num_adults, gasoline, diesel, natural_gas, propane):
    # Calculate the carbon tax rebate

    if province == 'ab':
        rebate = 772 + 193 * num_children
        if num_adults == 'two':
            rebate += 386
        if rural == 'yes':
            rebate *= 1.1
    elif province == 'mb':
        rebate = 528 + 132 * num_children
        if num_adults == 'two':
            rebate += 264
        if rural == 'yes':
            rebate *= 1.1
    elif province == 'on':
        rebate = 488 + 122 * num_children
        if num_adults == 'two':
            rebate += 244
        if rural == 'yes':
            rebate *= 1.1
    elif province == 'sk':
        rebate = 680 + 170 * num_children
        if num_adults == 'two':
            rebate += 340
        if rural == 'yes':
            rebate *= 1.1
    # Calculate the carbon tax paid
    paid = (gasoline * 12 * 0.1431) + (diesel * 12 * 1.21357466 * 0.1431) + (natural_gas * 12 * 3.4177) + (
                propane * 12 * 0.1006)

    # return 'Your carbon tax rebate is: ${:,.2f}'.format(rebate) + '\n\n  Your carbon tax paid is: ${:,.2f}'.format(paid)
    return html.H5('Your carbon tax rebate is: ${:,.2f}'.format(rebate), style={'color': 'green'}), \
           html.H5('Your carbon tax paid is: ${:,.2f}'.format(paid), style={'color': 'red'})


# ------- APP RUNNING / HOSTING INSTRUCTIONS -------------------
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)   # For localhost testing only
    app.run_server()  # For live on web

