import os
import laspy
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np

def convert_pointcloud_to_shapefile(input_file, output_file):
    # Kontrola přípony souboru
    ext = os.path.splitext(input_file)[1].lower()
    
    if ext == ".las":
        # Načtení LAS souboru
        with laspy.open(input_file) as las:
            point_data = las.read()
            mask = point_data.classification == 2   #klasifikace pouze ground bodů
            x = point_data.x[mask]
            y = point_data.y[mask]
            z = point_data.z[mask]

            # Kontrola, zda nejsou pole prázdná
            if len(x) == 0 or len(y) == 0 or len(z) == 0:
                raise ValueError("The LAS file contains no point data.")

            # Vytvoření DataFrame
            data = pd.DataFrame({
        "X": np.array(x),
        "Y": np.array(y),
        "Elevation": np.array(z)
    })
    elif ext == ".txt":
        # Načtení TXT souboru (předpokládá se, že obsahuje sloupce X, Y, Z oddělené mezerami)
        data = pd.read_csv(input_file, delim_whitespace=True, header=None, names=["X", "Y", "Elevation"])
    else:
        raise ValueError("Unsupported file format. Please provide a .las or .txt file.")

    # Zajištění správného formátu X a Y
    data["X"] = pd.to_numeric(data["X"], errors="coerce")
    data["Y"] = pd.to_numeric(data["Y"], errors="coerce")

    # Převod DataFrame na GeoDataFrame
    geometry = [Point(x, y) for x, y in zip(data["X"].tolist(), data["Y"].tolist())]
    gdf = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:32633")  # UMT 33N

    # Uložení do Shapefile
    gdf.to_file(output_file, driver="ESRI Shapefile")
    print(f"Shapefile saved to {output_file}")

if __name__ == "__main__":
    input_file = "D:\\Mgr\\diplomka\\data_dp\\data_LAS\\input.las"  
    output_file = "D:\\Mgr\\diplomka\\data_dp\\data_LAS\\output.shp"  

    convert_pointcloud_to_shapefile(input_file, output_file)
