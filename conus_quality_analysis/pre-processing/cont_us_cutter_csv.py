# cuts the data in a csv file to only the continental USA
# csv needs to have lat, lon
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path

p = Path(
    "C:/Users/noodl/Desktop/conus_git/conus_snodas_comparison/web_scrape/resort_data_coords_altitude_terrain.csv"
)

df = resorts = pd.read_csv(p)

geometry = [Point(xy) for xy in zip(df["lon"], df["lat"])]
gdf_resorts = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# create shapefile of continentla USA
states = gpd.read_file(
    "C:/Users/noodl/Desktop/conus_git/conus_quality_analysis/pre-processing/usa_shapefiles/cb_2018_us_state_20m.shp"
)
continental_states = states[~states["STUSPS"].isin(["AK", "HI", "PR"])]
continental_us = continental_states.dissolve()


gdf_resorts = gdf_resorts.to_crs(continental_us.crs)
# Use spatial join or point-in-polygon test
within_us_mask = gdf_resorts.within(continental_us.geometry.iloc[0])
gdf_resorts_continental = gdf_resorts[within_us_mask].copy()

gdf_resorts_continental.to_csv(
    "C:/Users/noodl/Desktop/conus_git/conus_snodas_comparison/web_scrape/resort_data_coords_altitude_terrain_contUS.csv",
    index=False,
)
