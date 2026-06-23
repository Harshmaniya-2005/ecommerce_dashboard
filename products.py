import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/products")

# Load Data
df = pd.read_csv("data/clean_sales_data.csv")

# KPIs
total_products = df["Product"].nunique()

product_revenue = (
    df.groupby("Product")["NetSales"]
    .sum()
    .sort_values(ascending=False)
)

top_product = product_revenue.index[0]
top_product_revenue = product_revenue.iloc[0]

avg_product_revenue = product_revenue.mean()

# Charts

# Top Revenue Products
top_products_df = (
    df.groupby("Product")["NetSales"]
    .sum()
    .reset_index()
    .sort_values("NetSales", ascending=False)
    .head(10)
)

fig_revenue = px.bar(
    top_products_df,
    x="Product",
    y="NetSales",
    color="NetSales",
    title="Top 10 Products by Revenue"
)

# Quantity Sold
qty_df = (
    df.groupby("Product")["Quantity"]
    .sum()
    .reset_index()
    .sort_values("Quantity", ascending=False)
    .head(10)
)

fig_quantity = px.bar(
    qty_df,
    x="Product",
    y="Quantity",
    color="Quantity",
    title="Top Products by Quantity Sold"
)

# Revenue Share
fig_donut = px.pie(
    top_products_df,
    names="Product",
    values="NetSales",
    hole=0.55,
    title="Revenue Share by Product"
)

fig_revenue.update_layout(
    height=400,
    template="plotly_white",
    transition_duration=0
)

fig_quantity.update_layout(
    height=400,
    template="plotly_white",
    transition_duration=0
)

fig_donut.update_layout(
    height=400,
    template="plotly_white",
    transition_duration=0
)

# Insights
insights = html.Div([

    html.H2("📊 Product Insights"),

    html.Ul([

        html.Li(
            f"Best Selling Product: {top_product}"
        ),

        html.Li(
            f"Revenue Generated: ${top_product_revenue:,.0f}"
        ),

        html.Li(
            f"Average Product Revenue: ${avg_product_revenue:,.0f}"
        ),

        html.Li(
            "Focus marketing campaigns on top-performing products."
        ),

        html.Li(
            "Consider discounts for low-performing products."
        )

    ])

], className="insight-box")

layout = html.Div([

    # Header
    html.Div([

        html.H1(
            "📦 Product Analytics Dashboard",
            style={
                "color": "#1F4E79",
                "fontWeight": "bold"
            }
        ),

        html.P(
            "Analyze product performance, revenue contribution and sales trends."
        )

    ], className="insight-box"),

    # KPI Cards
    html.Div([

        html.Div([
            html.H3(total_products),
            html.P("Products")
        ], className="card"),

        html.Div([
            html.H3(top_product),
            html.P("Best Product")
        ], className="card"),

        html.Div([
            html.H3(f"${top_product_revenue:,.0f}"),
            html.P("Top Product Revenue")
        ], className="card"),

        html.Div([
            html.H3(f"${avg_product_revenue:,.0f}"),
            html.P("Avg Product Revenue")
        ], className="card")

    ], className="cards"),

    # Row 1
    html.Div([

        html.Div(
            dcc.Graph(
                figure=fig_revenue,
                config={"displayModeBar": False}
            ),
            style={
                "width": "49%",
                "display": "inline-block"
            }
        ),

        html.Div(
            dcc.Graph(
                figure=fig_quantity,
                config={"displayModeBar": False}
            ),
            style={
                "width": "49%",
                "display": "inline-block",
                "float": "right"
            }
        )

    ]),

    html.Br(),

    # Row 2
    html.Div([

        html.Div(
            dcc.Graph(
                figure=fig_donut,
                config={"displayModeBar": False}
            ),
            style={
                "width": "60%",
                "display": "inline-block"
            }
        ),

        html.Div(
            insights,
            style={
                "width": "38%",
                "display": "inline-block",
                "verticalAlign": "top",
                "marginLeft": "2%"
            }
        )

    ])

])