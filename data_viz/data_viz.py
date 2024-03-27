from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from df import taste_hist_df, abv_price_df, production_by_nation_df, most_sold_products_df, wine_type_count_df, by_year_price_df

# taste_hist_df is :

app = Dash(__name__)

df = taste_hist_df
# Now, let's melt this DataFrame into a long format
df_long = df.melt(id_vars=['sweet', 'acidity', 'body', 'tannin'], 
                  value_vars=['count_sweet', 'count_acidity', 'count_body', 'count_tannin'],
                  var_name='Attribute', value_name='Count')

# Map the original attributes to a simpler form (e.g., sweet -> Sweetness) for clarity in the chart
attribute_mapping = {
    'count_sweet': 'Sweetness',
    'count_acidity': 'Acidity',
    'count_body': 'Body',
    'count_tannin': 'Tannin'
}

df_long['Attribute'] = df_long['Attribute'].map(attribute_mapping)

# Create a new column 'Level' for grouping in the plot
level_mapping = {name: f"Level {i+1}" for i, name in enumerate(df['sweet'])}
df_long['Level'] = df_long['sweet'].map(level_mapping)

# Creating a grouped bar chart with Plotly Express
fig_taste_hist = px.bar(df_long, x='Level', y='Count', color='Attribute', barmode='group',
             title="Comparison of Sweetness, Acidity, Body, and Tannin Counts")

# Creating the alcool by volume (abv) and average price graph

fig_abv_price = px.scatter(abv_price_df, x='abv', y='avg_price', title="Average Price by Alcohol by Volume (ABV)")
fig_abv_price.update_traces(mode='markers+lines')

fig_by_year_price = px.line(by_year_price_df, x='year', y='avg_price', title="Average Price by Year")
fig_by_year_price.update_traces(mode='lines')

fig_production_by_nation = px.bar(production_by_nation_df, x='nation', y='production_count', title="Production Count by Nation")
fig_production_by_nation.update_xaxes(categoryorder='total descending')

fig_most_sold_products = px.bar(most_sold_products_df, x='name', y='total_sales', title="Total Sales by Product")
fig_most_sold_products.update_xaxes(categoryorder='total descending')

fig_wine_type_count = px.pie(wine_type_count_df, names='type', values='count_type', title="Wine Type Count")


graphs = [fig_taste_hist, fig_abv_price, fig_production_by_nation, 
          fig_most_sold_products, fig_wine_type_count, fig_by_year_price]


app.layout = html.Div([
    html.H1("Wine Characteristics"),
    html.Div([
        dcc.Graph(figure=fig) for fig in graphs
    ])
])

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig_taste_hist
#     )
    
# ])


if __name__ == '__main__':
    app.run(debug=True)
