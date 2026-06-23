import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/customers")

df = pd.read_csv("data/clean_sales_data.csv")

customer_spend = (
    df.groupby("CustomerName")["NetSales"]
    .sum()
    .reset_index()
)

total_customers = customer_spend.shape[0]

avg_spend = customer_spend["NetSales"].mean()

top_customer = (
    customer_spend
    .sort_values("NetSales", ascending=False)
    .iloc[0]["CustomerName"]
)

top_customer_sales = (
    customer_spend
    .sort_values("NetSales", ascending=False)
    .iloc[0]["NetSales"]
)

# Top Customers
top_customers = (
    customer_spend
    .sort_values("NetSales", ascending=False)
    .head(10)
)

fig_top = px.bar(
    top_customers,
    x="CustomerName",
    y="NetSales",
    color="NetSales",
    title="Top 10 Customers by Revenue"
)

# Customer Type Revenue
customer_type = (
    df.groupby("CustomerType")["NetSales"]
    .sum()
    .reset_index()
)

fig_type = px.pie(
    customer_type,
    names="CustomerType",
    values="NetSales",
    hole=0.55,
    title="Revenue by Customer Type"
)

# Spend Distribution
fig_scatter = px.scatter(
    customer_spend,
    x="CustomerName",
    y="NetSales",
    title="Customer Spending Distribution"
)

fig_top.update_layout(
    height=400,
    template="plotly_white",
    transition_duration=0
)

fig_type.update_layout(
    height=400,
    template="plotly_white",
    transition_duration=0
)

fig_scatter.update_layout(
    height=400,
    template="plotly_white",
    transition_duration=0
)

insights = html.Div([

    html.H2("📊 Customer Insights"),

    html.Ul([

        html.Li(f"Top Customer: {top_customer}"),

        html.Li(
            f"Revenue Generated: ${top_customer_sales:,.0f}"
        ),

        html.Li(
            f"Average Customer Spend: ${avg_spend:,.0f}"
        ),

        html.Li(
            "High-value customers contribute significantly to revenue."
        ),

        html.Li(
            "Customer retention programs can improve repeat purchases."
        )

    ])

], className="insight-box")

layout = html.Div([

    html.Div([

        html.H1(
            "👥 Customer Analytics Dashboard",
            style={
                "color":"#1F4E79",
                "fontWeight":"bold"
            }
        ),

        html.P(
            "Analyze customer behavior and spending patterns."
        )

    ], className="insight-box"),

    html.Div([

        html.Div([
            html.H3(total_customers),
            html.P("Customers")
        ], className="card"),

        html.Div([
            html.H3(top_customer),
            html.P("Top Customer")
        ], className="card"),

        html.Div([
            html.H3(f"${avg_spend:,.0f}"),
            html.P("Avg Spend")
        ], className="card"),

        html.Div([
            html.H3(f"${top_customer_sales:,.0f}"),
            html.P("Top Customer Revenue")
        ], className="card")

    ], className="cards"),

    html.Div([

        html.Div(
            dcc.Graph(
                figure=fig_top,
                config={"displayModeBar":False}
            ),
            style={"width":"49%","display":"inline-block"}
        ),

        html.Div(
            dcc.Graph(
                figure=fig_type,
                config={"displayModeBar":False}
            ),
            style={
                "width":"49%",
                "display":"inline-block",
                "float":"right"
            }
        )

    ]),

    html.Br(),

    html.Div([

        html.Div(
            dcc.Graph(
                figure=fig_scatter,
                config={"displayModeBar":False}
            ),
            style={
                "width":"60%",
                "display":"inline-block"
            }
        ),

        html.Div(
            insights,
            style={
                "width":"38%",
                "display":"inline-block",
                "verticalAlign":"top",
                "marginLeft":"2%"
            }
        )

    ])

])