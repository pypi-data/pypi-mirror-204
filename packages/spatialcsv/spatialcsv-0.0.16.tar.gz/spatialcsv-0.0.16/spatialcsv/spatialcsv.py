"""Main module."""
import os
import csv
import ipyleaflet
import xyzservices.providers as xyz
import ipywidgets as widgets


class Locations:
    """Inputs a csv with locational data and outputs the proper format to import into a webmap"""

    def __init__(self, csv, lat=None, long=None, **kwargs):
        """
        Keyword arguments:
        csv -- the filepath to the csv file. It is assumed that the delimiter is ','
        lat -- the column header name of the latitude values
        long -- the column header name of the longitude values
        """
        self.csv = csv
        self.lat = lat
        self.long = long
        self.checks()


    def checks(self):
        """
        Checks to make sure file exists, has a header, 
        the lat and long variables exist in the header
        """
        
        if not os.path.isfile(self.csv):
            raise FileNotFoundError("This is not a valid filepath")
        with open(self.csv, 'r') as csvfile:
            head = csv.Sniffer().has_header(csvfile.read(1024))
                
            if head:
                pass
            else:
                print("This csv file does not seem to have a header. Please add column names in the top line of the csv.")
                        
       
        if self.lat in self.header():
            pass
        else:
            print(f"The value '{self.lat}' is not in the header.")
        if self.long in self.header():
            pass
        else:
            print(f"The value '{self.long}' is not in the header.")
        print("done")

    def check_lat_long(self):
        """Checks to make sure latitude and longitude columns are acceptable values"""
        header = self.header()
        lat_pl = header.index(self.lat)
        long_pl = header.index(self.long)
        with open(self.csv, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(file)
            for line in csv_reader:
                for item in [line[lat_pl], line[long_pl]]:
                    try:
                        float(item)
                    except ValueError:
                        print(f"'{item}' on line {line} is not a valid entry")
                    if float(item) > 180 or float(item) < -180:
                        print(f"'{item}' on line {line} is out of range")



    def header(self):
        """Returns header row"""
        with open(self.csv) as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames
            return header




class Map(ipyleaflet.Map):
    
    def __init__(self, center=[20, 0], zoom=2, **kwargs) -> None:

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(center=center, zoom=zoom, **kwargs)

        if "layers_control" not in kwargs:
            kwargs["layers_control"] = True

        if kwargs["layers_control"]:
            self.add_layers_control()

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True
        
        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()

        if "height" in kwargs:
            self.layout.height = kwargs["height"]
        else:
            self.layout.height = "600px"

    def add_search_control(self, position="topleft", **kwargs):
        """Adds a search control to the map.

        Args:
            kwargs: Keyword arguments to pass to the search control.
        """
        if "url" not in kwargs:
            kwargs["url"] = 'https://nominatim.openstreetmap.org/search?format=json&q={s}'
    

        search_control = ipyleaflet.SearchControl(position=position, **kwargs)
        self.add_control(search_control)

    def add_draw_control(self, **kwargs):
        """Adds a draw control to the map.

        Args:
            kwargs: Keyword arguments to pass to the draw control.
        """
        draw_control = ipyleaflet.DrawControl(**kwargs)

        draw_control.polyline =  {
            "shapeOptions": {
                "color": "#6bc2e5",
                "weight": 8,
                "opacity": 1.0
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
                "fillOpacity": 1.0
            },
            "drawError": {
                "color": "#dd253b",
                "message": "Oups!"
            },
            "allowIntersection": False
        }
        draw_control.circle = {
            "shapeOptions": {
                "fillColor": "#efed69",
                "color": "#efed69",
                "fillOpacity": 1.0
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
                "fillOpacity": 1.0
            }
        }

        self.add_control(draw_control)

    def add_layers_control(self, position='topright'):
        """Adds a layers control to the map.

        Args:
            kwargs: Keyword arguments to pass to the layers control.
        """
        layers_control = ipyleaflet.LayersControl(position=position)
        self.add_control(layers_control)

    def add_fullscreen_control(self, position="topleft"):
        """Adds a fullscreen control to the map.

        Args:
            kwargs: Keyword arguments to pass to the fullscreen control.
        """
        fullscreen_control = ipyleaflet.FullScreenControl(position=position)
        self.add_control(fullscreen_control)

    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Adds a tile layer to the map.

        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """
        tile_layer = ipyleaflet.TileLayer(
            url=url,
            name=name,
            attribution=attribution,
            **kwargs
        )
        self.add_layer(tile_layer)


    def add_basemap(self, basemap, **kwargs):

        import xyzservices.providers as xyz

        if basemap.lower() == "roadmap":
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        elif basemap.lower() == "satellite":
            url = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        else:
            try:
                basemap = eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name=basemap.name, attribution=attribution, **kwargs)
            except:
                raise ValueError(f"Basemap '{basemap}' not found.")


    def add_geojson(self, data, name='GeoJSON', **kwargs):
        """Adds a GeoJSON layer to the map.

        Args:
            data (dict): The GeoJSON data.
        """

        if isinstance(data, str):
            import json
            with open(data, "r") as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data=data,name=name, **kwargs)
        self.add_layer(geojson)

    def add_shp(self, data, name='Shapefile', **kwargs):
        """Adds a Shapefile layer to the map.

        Args:
            data (str): The path to the Shapefile.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)


    def add_geodf(self, data, name='GeoDataFrame', **kwargs):
        """Adds a GeoDataFrame to the map
        
        Args:
            data: geodataframe instance
        """
        geodf = ipyleaflet.GeoData(data=data, name=name, **kwargs)
        self.add_layer(geodf)


    def add_vector(self, data, name, **kwarags):
        """Adds a vector layer to the map.
        Can be GeoJson, shapefile, GeoDataFrame, etc

        Args:
            data: the vector data
            name: the type of data. example: 'GeoJson', 'Shapefile', 'GeoDataFrame'
            kwargs: Keyword arguments to pass to the layer.
        """
        if name == "GeoJson":
            self.add_geojson(self, data, name, **kwargs)
        elif name == "Shapefile":
            self.add_shp(self, data, name, **kwargs)
        elif name == "GeoDataFrame":
            self.add_geodf(self, data, name, **kwargs)
        else:
            print("This type of vector is not supported yet.")
        
    def add_raster(self, url, name='Raster', fit_bounds=True, **kwargs):
        """Adds a raster layer to the map.
        Args:
            url (str): The URL of the raster layer.
            name (str, optional): The name of the raster layer. Defaults to 'Raster'.
            fit_bounds (bool, optional): Whether to fit the map bounds to the raster layer. Defaults to True.
        """
        import httpx

        titiler_endpoint = "https://titiler.xyz"

        r = httpx.get(
            f"{titiler_endpoint}/cog/info",
            params = {
                "url": url,
            }
        ).json()

        bounds = r["bounds"]

        r = httpx.get(
            f"{titiler_endpoint}/cog/tilejson.json",
            params = {
                "url": url,
            }
        ).json()

        tile = r["tiles"][0]

        self.add_tile_layer(url=tile, name=name, **kwargs)

        if fit_bounds:
            bbox = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
            self.fit_bounds(bbox)

    def add_image(self, path, w=250, h=250):
        """Adds a small image (like your logo) to the bottom right of the map
        Args:
        file (str): the filepath of the image
        w (int) : width of the image (defaults 250 px)
        h (int) : height of the image (defaults 250 px)
        """

        file = open(path, "rb")
        image = file.read()
        i = widgets.Image(
            value=image,
            format='png',
            width=w,
            height=h,
        )
        
        output_widget = widgets.Output()
        output_control = ipyleaflet.WidgetControl(widget=output_widget, position='bottomright')
        self.add_control(output_control)
        with output_widget:
            display(i)



    self.dropdown = widgets.Dropdown(
        options=["Landsat", "Sentinel", "MODIS"],
        value=None,
        description="Satellite:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="250px")
    )  
    self.btns = widgets.ToggleButtons(
        value=None,
        options=["Apply", "Reset", "Close"],
        button_style="primary",
    )
    self.btns.style.button_width = "80px"

    self.output = widgets.Output()

    self.box = widgets.VBox([dropdown, btns, output])
    



    def dropdown_change(change):
        if change['new']:
            with output:
                output.clear_output()
                print(change['new'])

    

    def button_click(change):
        with output:
            output.clear_output()
            if change['new'] == "Apply":
                if dropdown.value is None:
                    print("Please select a satellite from the dropdown list.")
                else:
                    print(f"You selected {dropdown.value}")
            elif change['new'] == 'Reset':
                dropdown.value = None
            else:
                box.close()

