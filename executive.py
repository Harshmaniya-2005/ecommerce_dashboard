import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/")

# Load Data
df = pd.read_csv("data/clean_sales_data.csv")
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# KPIs
total_revenue = df["NetSales"].sum()
total_orders = df["OrderID"].nunique()
total_customers = df["CustomerName"].nunique()
avg_order_value = total_revenue / total_orders

# Filter Values
regions = sorted(df["Region"].dropna().unique())
products = sorted(df["Product"].dropna().unique())

layout = html.Div([

    # Professional Header
    html.Div([

        html.H1(
            "🛒 E-Commerce Sales Analytics Dashboard",
            style={
                "fontWeight": "bold",
                "color": "#1F4E79"
            }
        ),

        html.P(
            "Executive Business Intelligence Dashboard",
            style={
                "fontSize": "20px",
                "color": "#2563EB",
                "fontWeight": "500"
            }
        ),

        html.P(
            "Track revenue, orders, customer engagement, product performance and business growth opportunities through interactive analytics.",
            style={
                "color": "#6B7280",
                "fontSize": "15px"
            }
        )

    ],
    style={
        "background": "linear-gradient(135deg,#ffffff,#f8fafc)",
        "padding": "25px",
        "borderRadius": "15px",
        "boxShadow": "0 4px 15px rgba(0,0,0,0.08)",
        "marginBottom": "25px"
    }),

    # KPI Cards
    html.Div([

        html.Div([
            html.H3(f"${total_revenue:,.0f}"),
            html.P("Total Revenue")
        ], className="card"),

        html.Div([
            html.H3(f"{total_orders:,}"),
            html.P("Total Orders")
        ], className="card"),

        html.Div([
            html.H3(f"{total_customers:,}"),
            html.P("Customers")
        ], className="card"),

        html.Div([
            html.H3(f"${avg_order_value:,.0f}"),
            html.P("Average Order Value")
        ], className="card")

    ], className="cards"),

    # Filters
    html.Div([

        html.H3("Dashboard Filters"),

        html.Br(),

        html.Label("Select Date Range"),

        dcc.DatePickerRange(
            id="date_filter",
            start_date=df["OrderDate"].min(),
            end_date=df["OrderDate"].max()
        ),

        html.Br(),
        html.Br(),

        html.Label("Select Region"),

        dcc.Dropdown(
            id="region_filter",
            options=[
                {"label": r, "value": r}
                for r in regions
            ],
            multi=True,
            placeholder="Choose Region"
        ),

        html.Br(),

        html.Label("Select Product"),

        dcc.Dropdown(
            id="product_filter",
            options=[
                {"label": p, "value": p}
                for p in products
            ],
            multi=True,
            placeholder="Choose Product"
        )

    ],
    style={
        "background": "white",
        "padding": "20px",
        "borderRadius": "15px",
        "boxShadow": "0 4px 15px rgba(0,0,0,0.08)",
        "marginBottom": "25px"
    }),

    # Charts
    dcc.Graph(
        id="sales_chart",
        style={"height": "420px"}
    ),

    dcc.Graph(
        id="region_chart",
        style={"height": "420px"}
    ),

    # Insights
    html.Div(
        id="insights_box",
        className="insight-box"
    )

])


@callback(
    [
        Output("sales_chart", "figure"),
        Output("region_chart", "figure"),
        Output("insights_box", "children")
    ],
    [
        Input("date_filter", "start_date"),
        Input("date_filter", "end_date"),
        Input("region_filter", "value"),
        Input("product_filter", "value")
    ]
)
def update_dashboard(
    start_date,
    end_date,
    selected_regions,
    selected_products
):

    filtered_df = df.copy()

    filtered_df = filtered_df[
        (filtered_df["OrderDate"] >= start_date)
        &
        (filtered_df["OrderDate"] <= end_date)
    ]

    if selected_regions:
        filtered_df = filtered_df[
            filtered_df["Region"].isin(selected_regions)
        ]

    if selected_products:
        filtered_df = filtered_df[
            filtered_df["Product"].isin(selected_products)
        ]

    # Sales Trend Chart
    monthly_sales = (
        filtered_df
        .groupby(
            filtered_df["OrderDate"]
            .dt.strftime("%Y-%m")
        )["NetSales"]
        .sum()
        .reset_index()
    )

    sales_fig = px.line(
        monthly_sales,
        x="OrderDate",
        y="NetSales",
        markers=True,
        title="Sales Trend Over Time",
        color_discrete_sequence=["#2563EB"]
    )
    sales_fig.update_layout(
    height=400,
    autosize=False,
    margin=dict(l=40, r=40, t=50, b=40)
    )

    # Region Revenue Chart
    region_sales = (
        filtered_df
        .groupby("Region")["NetSales"]
        .sum()
        .reset_index()
    )

    region_fig = px.bar(
        region_sales,
        x="Region",
        y="NetSales",
        color="Region",
        title="Revenue by Region"
    )
    region_fig.update_layout(
    height=400,
    autosize=False,
    margin=dict(l=40, r=40, t=50, b=40)
    )

    # Insights
    if len(filtered_df) > 0:

        region_data = (
            filtered_df.groupby("Region")["NetSales"]
            .sum()
        )

        product_data = (
            filtered_df.groupby("Product")["NetSales"]
            .sum()
        )

        top_region = region_data.idxmax()
        top_region_sales = region_data.max()

        lowest_region = region_data.idxmin()

        top_product = product_data.idxmax()
        top_product_sales = product_data.max()

        insights = html.Div([

            html.H2("📊 Business Insights"),

            html.Ul([

                html.Li(
                    f"Highest Revenue Region: {top_region} generated ${top_region_sales:,.0f}"
                ),

                html.Li(
                    f"Best Selling Product: {top_product} generated ${top_product_sales:,.0f}"
                ),

                html.Li(
                    f"Lowest Performing Region: {lowest_region}"
                ),

                html.Li(
                    "Opportunity: Increase marketing efforts in low-performing regions."
                ),

                html.Li(
                    "Recommendation: Maintain inventory levels for top-selling products."
                )

            ])

        ])

    else:

        insights = html.Div([
            html.H3("No data available for selected filters.")
        ])

    return sales_fig, region_fig, insights