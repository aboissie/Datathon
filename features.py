import numpy as np
import pandas as pd

def get_coord_mask_params(df):
    lat_min = df['lat'].min()
    lat_max = df['lat'].max()
    lng_min = df['lng'].min()
    lng_max = df['lng'].max()
    # lat_window, lng_window = 0.1, 0.1
    lat_window = (lat_max - lat_min) / 30
    lng_window = (lng_max - lng_min) / 30
    return lat_min, lng_min, lat_window, lng_window

def get_coord_mask(df, lat_min, lng_min, lat_window, lng_window):
    df_np = df[['lat', 'lng']].to_numpy()
    uniq_coords = np.unique(df_np, axis=0)
    # copy np array
    mean_coords = np.copy(uniq_coords)

    def mask_coord(lat, lng):    
        # Round lat down to closest lat step starting from lat_min with step size lat_window
        mean_lat = lat_min + ((lat - lat_min) // lat_window) * lat_window
        mean_lng = lng_min + ((lng - lng_min) // lng_window) * lng_window    
        return mean_lat, mean_lng

    for i, coord in enumerate(mean_coords):
        mean_coords[i] = mask_coord(mean_coords[i][0], mean_coords[i][1])

    # convert np array to pandas df
    mean_coords = pd.DataFrame(mean_coords, columns=['mean_lat', 'mean_lng'])
    # horizontally stack dataframes
    coord_map = pd.concat([pd.DataFrame(uniq_coords, columns=['lat', 'lng']), mean_coords], axis=1)

    return coord_map

import math
def get_closest_station(coords):

  closest = float('inf')
  closestLoc = ""

  police_locations = [
  ["Bustleton Ave & Bowler St", 40.09103,-75.03268],
  ["Haines St & Germantown Ave",40.0384247,-75.1769416],
  ["Academy Rd & Red Lion Rd",40.0817603,-74.9944522],
  ["N Broad St & Champlost St",40.0444281,-75.143506],
  ["Harbison Ave & Levick St",40.0315624,-75.063272],
  ["Ridge Ave & Cinnaminson St",40.0402284,-75.2243751],
  ["22nd St & Hunting Park Ave",40.0132925,-75.1229354],
  ["Whitaker Ave",40.0090593,-75.1209234],
  ["17th St & Montgomery Ave",39.9808387,-75.1623664],
  ["3901 Whitaker Ave",40.0090593,-75.1209234],
  ["E Girard Ave & Montgomery Ave",39.9713591,-75.1271037],
  ["61st  St & Thompson St",39.9713663,-75.2409754],
  ["39th St & Lancaster Ave",39.9615549,-75.1993538],
  ["20th St & Pennsylvania Ave",39.9608066,-75.1715922],
  ["11th St & Winter St",39.9568113,-75.1572059],
  ["55th St & Pine St",39.9542633,-75.2321515],
  ["20th St & Federal St",39.9372741,-75.1767054],
  ["11th St & Wharton St",39.9334602,-75.1623016],
  ["65th St & Woodland Ave",39.9255738,-75.234328],
  ["24th St & Wolf St",39.9240387,-75.1868881],
  ["Police Headquarters",39.9546382,-75.1526274]
  ]

  for station in police_locations:
    station_coords = [station[1],station[2]]
    distance = math.dist(coords, station_coords)

    if (distance < closest):
      closest = distance
      closestLoc = station[0]

  return (closest, closestLoc)

