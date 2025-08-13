import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Calculate differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = (math.sin(dlat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def calculate_bearing(lat1, lon1, lat2, lon2):
    """Calculate bearing from point 1 to point 2"""
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlon_rad = math.radians(lon2 - lon1)
    
    y = math.sin(dlon_rad) * math.cos(lat2_rad)
    x = (math.cos(lat1_rad) * math.sin(lat2_rad) - 
         math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon_rad))
    
    bearing = math.atan2(y, x)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360
    
    return bearing

def calculate_polar_distances(lat, lon):
    """Calculate distances from North and South poles"""
    # North Pole coordinates: 90°N, any longitude
    north_pole_distance = calculate_distance(lat, lon, 90, 0)
    
    # South Pole coordinates: 90°S, any longitude  
    south_pole_distance = calculate_distance(lat, lon, -90, 0)
    
    return north_pole_distance, south_pole_distance

def format_coordinates(lat, lon):
    """Format coordinates with directional indicators"""
    lat_dir = 'N' if lat >= 0 else 'S'
    lon_dir = 'E' if lon >= 0 else 'W'
    
    return f"{abs(lat):.4f}°{lat_dir}, {abs(lon):.4f}°{lon_dir}"

def format_bearing(bearing):
    """Format bearing with cardinal directions"""
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    
    index = round(bearing / 22.5) % 16
    return f"{bearing:.1f}° ({directions[index]})"
