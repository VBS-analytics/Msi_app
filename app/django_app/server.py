from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc


URL_BASE_PATHNAME = '/msi/'
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
# FA = '/assets/all.css'
# os.path.join(os.path.join(os.path.join(os.getcwd(),"vlstm_crm_django_app_1"),"assets"),"all.css")
# print(f"WWW{os.getcwd()}")

server = Flask(__name__)

app = Dash(
    __name__,
    server = server,
    url_base_pathname = URL_BASE_PATHNAME,
    external_stylesheets=[dbc.themes.BOOTSTRAP,FA],
    # assets_url_path='/static'
    assets_folder='static',
)
app.title = 'ValueStream'

app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True