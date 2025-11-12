import folium
import webbrowser
from typing import Iterable, Mapping, Optional, Union

PointSpec = Mapping[str, Union[float, str, None]]

def plot_points_on_map(
    points: Iterable[PointSpec],
    *,
    default_radius_m: float = 10.0,
    default_color: str = "#3388ff",
    default_fill_color: Optional[str] = None,
    default_fill_opacity: float = 0.2,
    weight: int = 2,
    tiles: str = "OpenStreetMap",
    outfile: str = "map.html",
    initial_zoom: int = 17,
) -> None:
    """
    Plot only circles (no markers) for a set of coordinates, with per-point radius, colour, and hover text.
    """

    pts = list(points)
    if not pts:
        raise ValueError("`points` must be a non-empty iterable of point specs.")

    # Center map on mean of inputs
    avg_lat = sum(float(p["lat"]) for p in pts) / len(pts)
    avg_lon = sum(float(p["lon"]) for p in pts) / len(pts)
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=initial_zoom, tiles=tiles)

    lats, lons = [], []

    for p in pts:
        lat = float(p["lat"])
        lon = float(p["lon"])
        radius_m = float(p.get("radius_m", default_radius_m))
        color = str(p.get("color", default_color))
        fill_color = str(p.get("fill_color") or p.get("color") or default_fill_color or default_color)
        fill_opacity = float(p.get("fill_opacity", default_fill_opacity))
        tooltip = p.get("tooltip")

        circle = folium.Circle(
            location=[lat, lon],
            radius=radius_m,  # metres
            color=color,
            weight=weight,
            fill=True,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            opacity=1.0,
        )
        if tooltip:
            circle.add_child(folium.Tooltip(str(tooltip)))
        circle.add_to(m)

        lats.append(lat)
        lons.append(lon)

    # Fit bounds if points are spread apart
    if lats and lons:
        sw = [min(lats), min(lons)]
        ne = [max(lats), max(lons)]
        if sw != ne:
            m.fit_bounds([sw, ne], padding=(10, 10))

    m.save(outfile)
    print(f"Map saved to {outfile}")

    # Automatically open the map in your browser
    webbrowser.open(outfile)


if __name__ == "__main__":
    # Your coordinates with optional per-point customisation
    points = [
        {"lat": 51.514469, "lon": -0.133783, "radius_m": 20, "color": "#e63946", "tooltip": "Bonus point for picture evidence of ordering a beverage through a hole…"},
        {"lat": 51.513497, "lon": -0.134019, "radius_m": 20, "color": "#e63946", "tooltip": "What Genius vendor can you find here?"},
        {"lat": 51.513406, "lon": -0.133969, "radius_m": 10, "color": "#e63946", "tooltip": "What musician can you find here with a dark side?"},
        {"lat": 51.512917, "lon": -0.133592, "radius_m": 30, "color": "#e63946", "tooltip": "What colour is the invader from space?"},
        {"lat": 51.513675, "lon": -0.132478, "radius_m": 10, "color": "#fb8500", "tooltip": "What year was the tallest bottle?"},
        {"lat": 51.513872, "lon": -0.132622, "radius_m": 10, "color": "#fb8500", "tooltip": "How many cherubs live in this home for a Monarch?"},
        {"lat": 51.514275, "lon": -0.132964, "radius_m": 10, "color": "#fb8500", "tooltip": "What is the Eurythmics night time snack of choice? "},
        {"lat": 51.514872, "lon": -0.132375, "radius_m": 50, "color": "#fb8500", "tooltip": "Bonus point for the most yellow pigeons photographed"},
        {"lat": 51.515667, "lon": -0.130881, "radius_m": 10, "color": "#8338ec", "tooltip": "Name the Sculptor using Stoneware, Porcelain and Minerals"},
        {"lat": 51.512744, "lon": -0.131711, "radius_m": 20, "color": "#8338ec", "tooltip": "Which Father of computing is in the Maison?"},
        {"lat": 51.511850, "lon": -0.130886, "radius_m": 10, "color": "#8338ec", "tooltip": "What is the Bookmaker ID with 4 Chinese characters?"},
        {"lat": 51.512614, "lon": -0.131756, "radius_m": 30, "color": "#06d6a0", "tooltip": "Which philosopher rose from the ashes here?"},
        {"lat": 51.513094, "lon": -0.131158, "radius_m": 30, "color": "#06d6a0", "tooltip": "How many golden balls does the Antique Dealer have?"},
        {"lat": 51.513644, "lon": -0.131522, "radius_m": 10, "color": "#06d6a0", "tooltip": "Which member of the Fellowship enjoys a custard tart?"},
        {"lat": 51.514703, "lon": -0.132278, "radius_m": 10, "color": "#06d6a0", "tooltip": "What composer enters via the Casino Stage?"},
    ]

    plot_points_on_map(points, outfile="dcp_map.html")