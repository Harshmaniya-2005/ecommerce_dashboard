from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ]
)

# Sidebar
sidebar = html.Div(

    [

        html.H2(
            "🛒 E-Commerce",
            style={
                "color": "white",
                "textAlign": "center",
                "marginBottom": "30px"
            }
        ),

        dbc.Nav(

            [

                dbc.NavLink(
                    "📊 Executive Overview",
                    href="/",
                    active="exact"
                ),

                dbc.NavLink(
                    "📈 Sales Analytics",
                    href="/sales",
                    active="exact"
                ),

                dbc.NavLink(
                    "📦 Product Analytics",
                    href="/products",
                    active="exact"
                ),

                dbc.NavLink(
                    "👥 Customer Analytics",
                    href="/customers",
                    active="exact"
                ),

                dbc.NavLink(
                    "🚚 Operations",
                    href="/operations",
                    active="exact"
                ),

            ],

            vertical=True,
            pills=True

        )

    ],

    style={

        "backgroundColor": "#111827",
        "height": "100vh",
        "padding": "20px",
        "position": "fixed",
        "width": "250px",
        "left": "0",
        "top": "0"

    }

)

# Main Content
content = html.Div(

    page_container,

    style={
        "marginLeft": "270px",
        "padding": "20px"
    }

)

# Layout
app.layout = html.Div(
    [
        sidebar,
        content
    ]
)

if __name__ == "__main__":
    app.run(debug=True)