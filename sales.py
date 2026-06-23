import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/sales")

# Load Data
df = pd.read_csv("data/clean_sales_data.csv")

# Convert Date
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# KPIs
total_sales = df["NetSales"].sum()
total_orders = df["OrderID"].nunique()
avg_sale = total_sales / total_orders

top_region = (
    df.groupby("Region")["NetSales"]
    .sum()
    .idxmax()
)

# Revenue by Region
region_sales = (
    df.groupby("Region")["NetSales"]
    .sum()
    .reset_index()
)

fig_region = px.bar(
    region_sales,
    x="Region",
    y="NetSales",
    color="Region",
    title="Revenue by Region"
)

fig_region.update_layout(
    height=400,
    template="plotly_white"
)

# Top Salespersons
salesperson_sales = (
    df.groupby("Salesperson")["NetSales"]
    .sum()
    .reset_index()
    .sort_values("NetSales", ascending=False)
    .head(10)
)

fig_salesperson = px.bar(
    salesperson_sales,
    x="Salesperson",
    y="NetSales",
    color="NetSales",
    title="Top 10 Salespersons"
)

fig_salesperson.update_layout(
    height=400,
    template="plotly_white",
    transition_duration=0
)
# Monthly Trend
monthly_sales = (
    df.groupby(
        df["OrderDate"].dt.strftime("%Y-%m")
    )["NetSales"]
    .sum()
    .reset_index()
)

fig_trend = px.line(
    monthly_sales,
    x="OrderDate",
    y="NetSales",
    markers=True,
    title="Monthly Sales Trend"
)

fig_trend.update_layout(
    height=400,
    template="plotly_white",
    transition_duration=0
)

# Insights Card
insights = html.Div([

    html.H2("📊 Sales Insights"),

    html.Ul([

        html.Li(
            f"Highest Revenue Region: {top_region}"
        ),

        html.Li(
            f"Total Revenue Generated: ${total_sales:,.0f}"
        ),

        html.Li(
            f"Average Sale Value: ${avg_sale:,.0f}"
        ),

        html.Li(
            "Top salespersons drive a major portion of revenue."
        ),

        html.Li(
            "Growth opportunities exist in lower-performing regions."
        )

    ])

], className="insight-box")

# Layout
layout = html.Div([

    # Header
    html.Div([

        html.H1(
            "📈 Sales Analytics Dashboard",
            style={
                "color": "#1F4E79",
                "fontWeight": "bold"
            }
        ),

        html.P(
            "Monitor revenue performance, regional sales trends and salesperson effectiveness."
        )

    ], className="insight-box"),

    # KPI Cards
    html.Div([

        html.Div([
            html.H3(f"${total_sales:,.0f}"),
            html.P("Total Revenue")
        ], className="card"),

        html.Div([
            html.H3(f"{total_orders:,}"),
            html.P("Total Orders")
        ], className="card"),

        html.Div([
            html.H3(f"${avg_sale:,.0f}"),
            html.P("Average Sale")
        ], className="card"),

        html.Div([
            html.H3(top_region),
            html.P("Top Region")
        ], className="card")

    ], className="cards"),

    # Row 1
    html.Div([

        html.Div(
            dcc.Graph(
                figure=fig_trend,
                config={"displayModeBar": False}
            ),
            style={
                "width": "49%",
                "display": "inline-block"
            }
        ),

        html.Div(
            dcc.Graph(
                figure=fig_region,
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
                figure=fig_salesperson,
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