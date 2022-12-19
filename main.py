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
        dcc.Input(id='num-children-input', type='number', value=0, min=0)
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
    html.Div([
        html.Label('What is your annual household income?'),
        html.Br(),
        html.Label('$'),
        dcc.Input(id='income-input', type='number', value=0, min=0, max=10000000)
    ], style={'marginLeft': 15}),
    html.Br(),
    html.H5('Fuel usage:',
            style={'text-decoration': 'underline'}),
    html.Div([
        html.Label('Gasoline (L / month):'),
        html.Br(),
        dcc.Input(id='gasoline-input', type='number', value=0, min=0),
        html.Br(),
        html.Small('Most vehicles take between 45 and 65 L to fill. A typical fill-up is about 50 L.',
                   style={'font-style': 'italic'}),
        html.Br(),
        html.Br(),
    ], style={'marginLeft': 15}),
    html.Div([
        html.Label('Diesel (L / month):'),
        html.Br(),
        dcc.Input(id='diesel-input', type='number', value=0, min=0),
        html.Br(),
        html.Small('Mid-size pickups typically take about 80 L to fill. Full-size pickups, 100 L or more.',
                   style={'font-style': 'italic'}),
        html.Br(),
        html.Br(),
    ], style={'marginLeft': 15}),
    html.Div([
        html.Label('Natural gas (GJ / month):'),
        html.Br(),
        dcc.Input(id='natural-gas-input', type='number', value=0, min=0),
        html.Br(),
        html.Small('A typical Canadian household uses about 8 GJ per month, on average, over the course of a year.',
                   style={'font-style': 'italic'}),
        html.Br(),
        html.Br(),
    ], style={'marginLeft': 15}),
    html.Div([
        html.Label('Propane (L / month):'),
        html.Br(),
        dcc.Input(id='propane-input', type='number', value=0, min=0),
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
        '• The province you live in and the number of people in your household are used to calculate the rebate you'
        ' will receive for the 2023/24 year.',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label(
        '• Your monthly fuel usage is used to calculate how much you will pay in carbon tax over that full year.',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label(
        '• Your household income is used to ESTIMATE your annual indirect carbon-tax costs in the things you buy.',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label(
        '• The estimate is of the "worst-case" variety and assumes "full pass-through of carbon pricing costs from'
        ' businesses to households," according to the economists who developed the estimates.',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label(
        '• For more on the methodology of these estimates, see the source links and additional notes below.',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label('• All calculations are based on a carbon tax rate of $65 per tonne, which takes effect April 1, 2023.',
               style={'marginLeft': 15}),
    html.Br(),
    html.Label('• Rebates are issued quarterly: In April, July & October of 2023 and in January 2024.',
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
    dcc.Markdown("**• Created by [Robson Fletcher](https://mas.to/@robsonfletcher)**", style={'marginLeft': 15}),
    html.A('• ', style={'marginLeft': 15}),
    html.A('Source of rebate data',
           href='https://www.canada.ca/en/department-finance/news/2022/11/climate-action-incentive-payment-amounts-for-2023-24.html',
           target="_blank", style={'font-style': 'italic'}),
    html.Br(),
    html.A('• ', style={'marginLeft': 15}),
    html.A('Source of pricing data',
           href='https://www.canada.ca/en/department-finance/news/2021/12/fuel-charge-rates-for-listed-provinces-and-territories-for-2023-to-2030.html',
           target="_blank", style={'font-style': 'italic'}),
    html.Br(),
    html.A('• ', style={'marginLeft': 15}),
    html.A('Source of indirect-cost estimates',
           href='https://jenniferwinter.github.io/website/WinterDolterFellows_latest.pdf',
           target="_blank", style={'font-style': 'italic'}),
    html.Br(),
    html.Br(),
    html.H5('More about the indirect-cost estimates:', style={'text-decoration': 'underline'}),
    html.Label(
        '• The estimates come from a paper written by economists Jennifer Winter, Brett Dolter and G. Kent Fellows.',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label(
        '• Their analysis is based on Statistic’s Canada’s Social Policy Simulation Database and Model version 28.0.',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label(
        '• The calculations in their paper were originally done in 2020 dollars and based on $50 per tonne.',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label(
        '• Jennifer Winter kindly shared her data and advice in adapting it for the purpose of this calculator.',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label(
        '• The values have been adjusted for a rate of $65 per tonne and for inflation (to 2022 dollars) for the '
        'purpose of this calculator.',
        style={'marginLeft': 15}),
    html.Br(),

    html.Label(
        '• The estimates do not scale directly with the income you input, but rather are based on income decile'
        ' (i.e. there are 10 discrete ranges of income for each province.)',
        style={'marginLeft': 15}),
    html.Br(),
    html.Label(
        '• The estimates DO account for the output-based pricing system (OBPS) on large emitters.',
        style={'marginLeft': 15}),
    html.Br(),
], style={'marginLeft': 5,
          'marginBottom': 20})

# ----------- NOTES FROM JEN'S PAPER TO INCLUDE IN THE HTML SOMEWHERE: --------------

# https://jenniferwinter.github.io/website/WinterDolterFellows_latest.pdf

# our indirect carbon cost estimates are of the ‘worst-case’ variety since
# we assume full pass-through of carbon pricing costs from businesses to households. This means
# that our indirect costs are an upper bound on potential household indirect carbon costs.


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
     Input('propane-input', 'value'),
     Input('income-input', 'value')
     ])
def update_output_div(province, num_children, rural, num_adults, gasoline, diesel, natural_gas, propane, income):
    # Calculate the carbon tax rebate

    if province == 'ab':
        rebate = 772 + 193 * num_children
        income_min = [0, 38991, 61385, 87285, 116467, 146254, 173859, 207437, 250156, 341880]
        income_max = [38990, 61384, 87284, 116466, 146253, 173858, 207436, 250155, 341879, 10000000]
        indirect_costs = [260.27, 261.73, 351.88, 402.77, 474.02, 542.36, 716.85, 754.65, 735.75, 913.14]
        if num_adults == 'two':
            rebate += 386
        if rural == 'yes':
            rebate *= 1.1
    elif province == 'mb':
        rebate = 528 + 132 * num_children
        income_min = [0, 31455, 48466, 68112, 87372, 109806, 131962, 159829, 199344, 259840]
        income_max = [31454, 48465, 68111, 87371, 109805, 131961, 159828, 199343, 259839, 10000000]
        indirect_costs = [226.83, 222.47, 279.18, 295.17, 287.9, 343.16, 398.41, 485.65, 658.68, 766.28]
        if num_adults == 'two':
            rebate += 264
        if rural == 'yes':
            rebate *= 1.1
    elif province == 'on':
        rebate = 488 + 122 * num_children
        income_min = [0, 29659, 47327, 67120, 90907, 115284, 143110, 174349, 218431, 297904]
        income_max = [29658, 47326, 67119, 90906, 115283, 143109, 174348, 218430, 297903, 10000000]
        indirect_costs = [157.04, 159.95, 206.48, 216.65, 247.19, 274.82, 309.71, 366.42, 442.03, 568.53]
        if num_adults == 'two':
            rebate += 244
        if rural == 'yes':
            rebate *= 1.1
    elif province == 'sk':
        rebate = 680 + 170 * num_children
        income_min = [0, 32013, 48264, 72404, 95820, 119502, 147543, 180020, 224448, 285422]
        income_max = [32012, 48263, 72403, 95819, 119501, 147542, 180019, 224447, 285421, 10000000]
        indirect_costs = [404.23, 463.84, 494.38, 533.64, 548.18, 663.05, 770.65, 994.57, 1224.31, 1494.76]
        if num_adults == 'two':
            rebate += 340
        if rural == 'yes':
            rebate *= 1.1
    # Calculate the carbon tax paid
    paid = (gasoline * 12 * 0.1431) + (diesel * 12 * 1.21357466 * 0.1431) + (natural_gas * 12 * 3.4177) + (
                propane * 12 * 0.1006)
    # Estimate the indirect carbon tax cost
    for i in range(10):
        if income >= income_min[i] and income <= income_max[i]:
            indirect_cost = indirect_costs[i]
            break

    # return 'Your carbon tax rebate is: ${:,.2f}'.format(rebate) + '\n\n  Your carbon tax paid is: ${:,.2f}'.format(paid)
    return html.H5('Your carbon tax rebate is: ${:,.2f}'.format(rebate), style={'color': 'green'}), \
           html.H5('Your carbon tax paid is: ${:,.2f}'.format(paid), style={'color': 'red'}), \
           html.H5('Your *estimated* indirect costs are: ${:,.2f}'.format(indirect_cost), style={'color': 'orange'})


# ------- APP RUNNING / HOSTING INSTRUCTIONS -------------------
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)   # For localhost testing only
    app.run_server()  # For live on web

