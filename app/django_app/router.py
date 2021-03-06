from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

from .server import app, server
from . import layouts


pages = (
    ('', layouts.index),
    ('help', layouts.get_help_page),
    # ('fig2', layouts.fig2),
)


routes = {f"{app.config.url_base_pathname}{path}": layout for path, layout in pages}
@app.callback(Output('content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    """A multi-page Dash router"""
    print(f"display_page {pathname}")
    if pathname is None:
        raise PreventUpdate("Ignoring first empty location callback")
    
    page = routes.get(pathname, f"Unknown link '{pathname}'")
    
    if callable(page):
        # can add arguments to layout functions if needed
        layout = page()
    else:
        layout = page

    return layout