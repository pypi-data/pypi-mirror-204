"""Main module."""

import random
import string
import ipyleaflet


class Map(ipyleaflet.Map):
    """Class 'Map'

    Args:
        ipyleaflet (_type_): _description_
    """
    def __init__(self, center = [37.5, 127], zoom = 8, **kwargs):
        """Create a Map.

        Args:
            center (list, optional): A coordinate representing the center of the map. Defaults to `[37.5, 127]`
            zoom (int, optional): Zoom level. Defaults to 8
        """        
        if 'scroll_wheel_zoom' not in kwargs:
            kwargs['scroll_wheel_zoom'] = True
        super().__init__(center = center, zoom = zoom, **kwargs) # inherited from the parent, in this case, ipyleaflet
        
        if 'layers_control' not in kwargs:
            kwargs['layers_control'] = True
        
        if kwargs['layers_control']:
            self.add_layers_control()

        self.add_search_control()
    


    def add_search_control(self, position = 'topleft', **kwargs):
        """Add a search control panel to the map.

        Args:
            position (str, optional): The location of the search control panel. Defaults to 'topleft'.
        """        
        if 'url' not in kwargs:
            kwargs['url'] = 'https://nominatim.openstreetmap.org/search?format=json&q={s}'
        
        search_control = ipyleaflet.SearchControl(position = position, **kwargs)
        self.add_control(search_control)


    def add_draw_control(self, position = 'topleft', **kwargs):
        """Add a draw control panel to the map.

        Args:
            position (str, optional): The location of the draw control panel. Defaults to 'topleft'.
        """        
        draw_control = ipyleaflet.DrawControl(position = position, **kwargs)
        self.add_control(draw_control)


    def add_layers_control(self, position = 'topright', **kwargs):
        """Add a layers control panel to the map.

        Args:
            position (str, optional): The location of the layers control panel. Defaults to 'topright'.
        """        
        layers_control = ipyleaflet.LayersControl(position = position, **kwargs)
        self.add_control(layers_control)


    def add_tile_layer(self, url, name, attribution = '', **kwargs):
        """Add a tile layer to the map.

        Args:
            url (str): xyz url of the tile layer.
            name (str): A name of the layer that would be displayed on the map.
            attribution (str, optional): A name of the attribution. Defaults to ''.
        """        
        tile_layer = ipyleaflet.TileLayer(
            url = url,
            name = name,
            attribution = attribution,
            **kwargs
        )
        self.add_layer(tile_layer)
    

    def add_basemap(self, basemap, **kwargs):
        """Add a base map to the map.

        Args:
            basemap (str): xyz url of the base map.

        Raises:
            ValueError: Error message will be raised if the url is not available.
        """
        import xyzservices.providers as xyz

        if basemap.lower() == 'roadmap':
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name = basemap, **kwargs)
        elif basemap.lower() == 'satellite':
            url = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name = basemap, **kwargs)
        else:
            try:
                basemap = eval(f'xyz.{basemap}')
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name = basemap, attribution = attribution, **kwargs)
            except:
                raise ValueError(f'{basemap} is not found')


    def add_geojson(self, data, name = 'GeoJSON', **kwargs):
        """Add a geojson file to the map.

        Args:
            data (str): A name of the geojson file.
            name (str, optional): A layer name of the geojson file to be displayed on the map. Defaults to 'GeoJSON'.
        """        
        if isinstance(data, str):
            import json
            with open(data, 'r') as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data = data, name = name, **kwargs)
        self.add_layer(geojson)
    
    def add_shp(self, data, name = 'Shapefile', **kwargs):
        """Add a ESRI shape file to the map.

        Args:
            data (str): A name of the shape file.
            name (str, optional): A layer name of the shape file to be displayed on the map. Defaults to 'Shapefile'.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name = name, **kwargs)

    def add_raster(self, url, name = 'Raster', fit_bounds = True, **kwargs):
        """_summary_

        Args:
            url (str): _description_
            name (str, optional): _description_. Defaults to 'Raster'.
            fit_bounds (bool, optional): _description_. Defaults to True.
        """        
        import httpx

        titiler_endpoint = 'https://titiler.xyz'
        
        # get a bbox
        r = httpx.get(
            f"{titiler_endpoint}/cog/info",
            params = {
                "url": url,
            }
        ).json()

        bounds = r["bounds"]

        # get a url
        r = httpx.get(
            f"{titiler_endpoint}/cog/tilejson.json",
            params = {
                "url": url,
            }
        ).json()

        tile = r['tiles'][0]

        self.add_tile_layer(url = tile, name = name, **kwargs)

        if fit_bounds:
            bbox = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
            self.fit_bounds(bbox)
        
    def add_local_raster(self, filename, name = 'local raster', **kwargs):
        try:
            import localtileserver
        except ImportError:
            raise ImportError('')
    


    def add_vector(
        self,
        filename,
        layer_name = 'Vector',
        **kwargs,
    ):
        import os
        if not filename.startswith('http'):
            filename = os.path.abspath(filename)
        else:
            filename = github_raw_url(filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.shp':
            self.add_shp(
                filename,
                layer_name
            )
        elif ext in ['.json', '.geojson']:
            self.add_geojson(
                filename,
                layer_name
            )
        else:
            geojson = vector_to_geojson(
                filename,
                bbox = bbox,
                mask = mask,
                rows = rows,
                epsg = '4326',
                **kwargs,
            )

            self.add_geojson(
                geojson,
                layer_name
            )
        


def generate_random_string(length, upper = False, digit = False, punc = False):
    """Generates a random string of a given length.

    Args:
        length (int): A length of the string.
        upper (bool, optional): Whether you would like to contain upper case alphabets in your string pool or not. Defaults to False.
        digit (bool, optional): Whether you would like to contain digits in your string pool or not. Defaults to False.
        punc (bool, optional): Whether you would like to contain punctuations in your string pool or not. Defaults to False.

    Returns:
        str: Generated random string.
    """
    chars = string.ascii_lowercase
    if upper:
        chars += string.ascii_uppercase
    if digit:
        chars += string.digits
    if punc:
        chars += string.punctuation
    
    result_str = ''.join(random.choice(chars) for i in range(length))
    return result_str


def generate_lucky_number(length = 2):
    """Generates a random number of a given length.

    Args:
        length (int, optional): A length of the number. Defaults to 2.

    Returns:
        int: Generated random number.
    """    
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    result_str = int(result_str)
    return result_str


def euclidean_dist(first_coord, second_coord):
    """Calculates an Euclidean distance between two coordinates.

    Args:
        first_coord (list): A coordinate of the first point. Should have 2 length. 
        second_coord (list): A coordinate of the second point. Should have 2 length. 

    Returns:
        int: Calculated Euclidean distance.
    """
    if len(first_coord) != 2:
        print('1')
    elif len(second_coord) != 2:
        print('2')
    else:
        x_diff = first_coord[0] - second_coord[0]
        y_diff = first_coord[1] - second_coord[1]
        dist = ((x_diff) ** 2 + (y_diff) ** 2) ** (1 / 2)
        return dist