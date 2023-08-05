# to add a shiny app to public dir:
# shinylive export shinyapps/basic public/dashboard --subdir basic
from shiny import App, reactive, render, ui

import ipyleaflet as L
from shinywidgets import output_widget, reactive_read, register_widget


# Import modules for plot rendering
import numpy as np
import matplotlib.pyplot as plt

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider("n", "N", 0, 100, 20),
            ui.input_slider("zoom", "Map zoom level", value=12, min=1, max=18),
        ),
        ui.panel_main(
            ui.output_plot("histogram"),
            output_widget("map"),
            ui.output_ui("map_bounds"),
        ),
    ),
)


def server(input, output, session):
    map = L.Map(center=(51.476852, -0.000500), zoom=12, scroll_wheel_zoom=True)
    # Add a distance scale
    map.add_control(L.leaflet.ScaleControl(position="bottomleft"))
    register_widget("map", map)

    # When the slider changes, update the map's zoom attribute (2)
    @reactive.Effect
    def _():
        map.zoom = input.zoom()

    @reactive.Effect
    def _():
        ui.update_slider("zoom", value=reactive_read(map, "zoom"))

    @output
    @render.ui
    def map_bounds():
        center = reactive_read(map, "center")
        if len(center) == 0:
            return

        lat = round(center[0], 4)
        lon = (center[1] + 180) % 360 - 180
        lon = round(lon, 4)

        return ui.p(f"Latitude: {lat}", ui.br(), f"Longitude: {lon}")

    @output
    @render.plot(alt="A histogram")
    def histogram():
        np.random.seed(19680801)
        x = 100 + 15 * np.random.randn(437)
        plt.hist(x, input.n(), density=True)


app = App(app_ui, server, debug=True)
