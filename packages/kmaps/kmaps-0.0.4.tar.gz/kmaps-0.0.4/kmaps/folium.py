"""Folium module."""

import random
import string
import folium


class Map(folium.Map):
    """Class 'Map'.

    Args:
        folium (_type_): Map object from folium.
    """
    def __init__(self, location = [37.5, 127], zoom_start = 8, **kwargs): 
        """Create a Map.

        Args:
            center (list, optional): A coordinate representing the center of the map. Defaults to `[37.5, 127]`
            zoom (int, optional): Zoom level. Defaults to 8
        """            
        if 'scroll_wheel_zoom' not in kwargs:
            kwargs['scroll_wheel_zoom'] = True
        super().__init__(location = location, zoom_start = zoom_start, **kwargs) # inherited from the parent, in this case, ipyleaflet


    def add_layers_control(self, **kwargs):
        """Add a layers control panel to the map.
        """        
        folium.LayerControl(**kwargs).add_to(self)


    def add_geojson(self, data, name = 'GeoJSON', **kwargs):
        """Add a geojson file to the map (folium version).

        Args:
            data (str): A name of the geojson file.
            name (str, optional): A layer name of the geojson file to be displayed on the map. Defaults to 'GeoJSON'.
        """     
        folium.GeoJson(data, name = name).add_to(self)
    
    def add_shp(self, data, name = 'Shapefile', **kwargs):
        """Add a ESRI shape file to the map (folium version).

        Args:
            data (str): A name of the shape file.
            name (str, optional): A layer name of the shape file to be displayed on the map. Defaults to 'Shapefile'.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name = name, **kwargs)