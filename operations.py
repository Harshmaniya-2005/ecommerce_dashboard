import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/operations")

df = pd.read_csv("data/clean_sales_data.csv")

avg_delivery = round(
    df["DeliveryDays"].mean(),
    2
)

max_delivery = df["DeliveryDays"].max()

min_delivery = df["DeliveryDays"].min()

returned_orders = (
    df["Returned"]
    .astype(str)
    .str.lower()
    .eq("yes")
    .sum()
)

# Delivery Distribution
fig_delivery = px.histogram(
    df,
    x="DeliveryDays",
    nbins=20,
    title="Delivery Days Distribution"
)

# Region Delivery
region_delivery = (
    df.groupby("Region")["DeliveryDays"]
    .mean()
    .reset_index()
)

fig_region = px.bar(
    region_delivery,
    x="Region",
    y="DeliveryDays",
    color="Region",
    title="Average Delivery Days by Region"
)

# Shipping Cost
shipping = (
    df.groupby("Region")["ShippingCost"]
    .sum()
    .reset_index()
)

fig_shipping = px.bar(
    shipping,
    x="Region",
    y="ShippingCost",
    color="ShippingCost",
    title="Shipping Cost by Region"
)

fig_delivery.update_layout(
    height=400,
    template="plotly_white",
    transition_duration=0
)

fig_region.update_layout(
    height=400,
    template="plotly_white",
    transition_duration=0
)

fig_shipping.update_layout(
    height=400,
    template="plotly_white",
    transition_duration=0
)

insights = html.Div([

    html.H2("📊 Operations Insights"),

    html.Ul([

        html.Li(
            f"Average Delivery Time: {avg_delivery} days"
        ),

        html.Li(
            f"Returned Orders: {returned_orders}"
        ),

        html.Li(
            "Improve delivery performance in slower regions."
        ),

        html.Li(
            "Reduce shipping costs through route optimization."
        ),

        html.Li(
            "Fast delivery increases customer satisfaction."
        )

    ])

], className="insight-box")

layout = html.Div([

    html.Div([

        html.H1(
            "🚚 Operations Dashboard",
            style={
                "color":"#1F4E79",
                "fontWeight":"bold"
            }
        ),

        html.P(
            "Monitor logistics, shipping and delivery performance."
        )

    ], className="insight-box"),

    html.Div([

        html.Div([
            html.H3(avg_delivery),
            html.P("Avg Delivery Days")
        ], className="card"),

        html.Div([
            html.H3(max_delivery),
            html.P("Max Delivery")
        ], className="card"),

        html.Div([
            html.H3(min_delivery),
            html.P("Min Delivery")
        ], className="card"),

        html.Div([
            html.H3(returned_orders),
            html.P("Returned Orders")
        ], className="card")

    ], className="cards"),

    html.Div([

        html.Div(
            dcc.Graph(
                figure=fig_delivery,
                config={"displayModeBar":False}
            ),
            style={"width":"49%","display":"inline-block"}
        ),

        html.Div(
            dcc.Graph(
                figure=fig_region,
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
                figure=fig_shipping,
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