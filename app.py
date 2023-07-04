import dash
import dash_bootstrap_components as dbc
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
standard_BS = dbc.themes.BOOTSTRAP
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[standard_BS])
#app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[BS])
server = app.server
colors = ['#ffcc00', 
          '#f5f2e8', 
          '#f8f3e3',
          '#ffffff', 
          ]