import os
import folium


def create_weather_map(
    latitude,
    longitude,
    location_name,
    forecast_df,
    output_directory
):
    """
    Create an interactive Folium/OpenStreetMap weather map.
    """

    # -------------------------------------------------
    # CREATE MAP
    # -------------------------------------------------

    weather_map = folium.Map(
        location=[latitude, longitude],
        zoom_start=9,
        tiles="OpenStreetMap"
    )

    # -------------------------------------------------
    # GET FIRST FORECAST
    # -------------------------------------------------

    if not forecast_df.empty:

        forecast = forecast_df.iloc[0]

        forecast_hour = int(forecast["forecast_hour"])
        temperature = float(forecast["temperature_c"])
        humidity = float(forecast["humidity"])
        wind_speed = float(forecast["wind_speed_ms"])
        wind_direction = float(
            forecast["wind_direction_deg"]
        )

    else:

        forecast_hour = 0
        temperature = 0
        humidity = 0
        wind_speed = 0
        wind_direction = 0

    # -------------------------------------------------
    # POPUP INFORMATION
    # -------------------------------------------------

    popup_html = f"""
    <div style="font-size:14px">

        <h4>{location_name}</h4>

        <b>GFS Forecast</b><br><br>

        Forecast Hour: F{forecast_hour:03d}<br>
        Temperature: {temperature:.1f} °C<br>
        Humidity: {humidity:.1f}%<br>
        Wind Speed: {wind_speed:.1f} m/s<br>
        Wind Direction: {wind_direction:.1f}°

    </div>
    """

    # -------------------------------------------------
    # CITY MARKER
    # -------------------------------------------------

    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(
            popup_html,
            max_width=300
        ),
        tooltip=f"GFS Weather — {location_name}",
        icon=folium.Icon(
            color="red",
            icon="cloud"
        )
    ).add_to(weather_map)

    # -------------------------------------------------
    # CIRCLE AROUND CITY
    # -------------------------------------------------

    folium.Circle(
        location=[latitude, longitude],
        radius=15000,
        color="red",
        fill=True,
        fill_opacity=0.08
    ).add_to(weather_map)

    # -------------------------------------------------
    # ADD ALL FORECAST POINTS TO POPUP
    # -------------------------------------------------

    forecast_table = ""

    for _, row in forecast_df.iterrows():

        forecast_table += f"""
        <tr>
            <td>F{int(row['forecast_hour']):03d}</td>
            <td>{row['temperature_c']:.1f} °C</td>
            <td>{row['humidity']:.1f}%</td>
            <td>{row['wind_speed_ms']:.1f}</td>
        </tr>
        """

    table_html = f"""
    <div style="font-size:13px">

    <h4>Multi-Forecast — {location_name}</h4>

    <table border="1"
           style="border-collapse:collapse;
                  width:100%;
                  text-align:center">

        <tr>
            <th>Hour</th>
            <th>Temp</th>
            <th>Humidity</th>
            <th>Wind</th>
        </tr>

        {forecast_table}

    </table>

    </div>
    """

    # -------------------------------------------------
    # MULTI-FORECAST MARKER
    # -------------------------------------------------

    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(
            table_html,
            max_width=450
        ),
        tooltip="View Multi-Forecast"
    ).add_to(weather_map)

    # -------------------------------------------------
    # SAVE MAP
    # -------------------------------------------------

    os.makedirs(
        output_directory,
        exist_ok=True
    )

    map_path = os.path.join(
        output_directory,
        "gfs_weather_map.html"
    )

    weather_map.save(map_path)

    print("\n✓ Interactive weather map saved:")
    print(map_path)

    # -------------------------------------------------
    # OPEN MAP IN BROWSER
    # -------------------------------------------------

    import webbrowser

    webbrowser.open(
        "file://" + os.path.abspath(map_path)
    )

    return map_path