import numpy as np
import pandas as pd
import xarray as xr


# ============================================================
# OPEN GRIB VARIABLE
# ============================================================

def open_variable(
    file_path,
    short_name,
    level
):

    ds = xr.open_dataset(
        file_path,
        engine="cfgrib",
        backend_kwargs={
            "filter_by_keys": {
                "typeOfLevel":
                    "heightAboveGround",

                "level":
                    level,

                "shortName":
                    short_name
            }
        }
    )

    return ds


# ============================================================
# PROCESS ONE GFS FILE
# ============================================================

def process_gfs_file(file_path):

    # --------------------------------------------------------
    # 2 METRE TEMPERATURE
    # --------------------------------------------------------

    ds_temp = open_variable(
        file_path,
        "2t",
        2
    )

    temperature = (
        ds_temp["t2m"] - 273.15
    )

    temperature = temperature.drop_vars(
        "heightAboveGround",
        errors="ignore"
    )


    # --------------------------------------------------------
    # 2 METRE RELATIVE HUMIDITY
    # --------------------------------------------------------

    ds_rh = open_variable(
        file_path,
        "2r",
        2
    )

    humidity = ds_rh["r2"]

    humidity = humidity.drop_vars(
        "heightAboveGround",
        errors="ignore"
    )


    # --------------------------------------------------------
    # 10 METRE U WIND
    # --------------------------------------------------------

    ds_u = open_variable(
        file_path,
        "10u",
        10
    )

    u10 = ds_u["u10"]

    u10 = u10.drop_vars(
        "heightAboveGround",
        errors="ignore"
    )


    # --------------------------------------------------------
    # 10 METRE V WIND
    # --------------------------------------------------------

    ds_v = open_variable(
        file_path,
        "10v",
        10
    )

    v10 = ds_v["v10"]

    v10 = v10.drop_vars(
        "heightAboveGround",
        errors="ignore"
    )


    # --------------------------------------------------------
    # WIND SPEED
    # --------------------------------------------------------

    wind_speed = np.sqrt(
        u10 ** 2 +
        v10 ** 2
    )


    # --------------------------------------------------------
    # WIND DIRECTION
    # --------------------------------------------------------

    wind_direction = (
        180
        +
        np.degrees(
            np.arctan2(
                u10,
                v10
            )
        )
    ) % 360


    # --------------------------------------------------------
    # CREATE WEATHER DATASET
    # --------------------------------------------------------

    weather = xr.Dataset({

        "temperature_c":
            temperature,

        "relative_humidity":
            humidity,

        "wind_speed_ms":
            wind_speed,

        "wind_direction_deg":
            wind_direction
    })


    return weather


# ============================================================
# GET WEATHER AT LOCATION
# ============================================================

def get_location_weather(
    weather,
    latitude,
    longitude
):

    temperature = weather[
        "temperature_c"
    ].sel(
        latitude=latitude,
        longitude=longitude,
        method="nearest"
    ).values.item()


    humidity = weather[
        "relative_humidity"
    ].sel(
        latitude=latitude,
        longitude=longitude,
        method="nearest"
    ).values.item()


    wind_speed = weather[
        "wind_speed_ms"
    ].sel(
        latitude=latitude,
        longitude=longitude,
        method="nearest"
    ).values.item()


    wind_direction = weather[
        "wind_direction_deg"
    ].sel(
        latitude=latitude,
        longitude=longitude,
        method="nearest"
    ).values.item()


    return {
        "temperature_c":
            round(float(temperature), 2),

        "humidity":
            round(float(humidity), 2),

        "wind_speed_ms":
            round(float(wind_speed), 2),

        "wind_direction_deg":
            round(float(wind_direction), 2)
    }


# ============================================================
# BUILD MULTI-FORECAST
# ============================================================

def build_forecast(
    downloaded_files,
    latitude,
    longitude,
    location_name
):

    results = []

    for forecast_hour, file_path in downloaded_files:

        print(
            f"\nProcessing F{forecast_hour:03d}"
        )

        try:

            weather = process_gfs_file(
                file_path
            )

            values = get_location_weather(
                weather,
                latitude,
                longitude
            )

            values["location"] = location_name

            values["latitude"] = latitude

            values["longitude"] = longitude

            values["forecast_hour"] = (
                forecast_hour
            )

            results.append(values)

            print("✓ Processed")

        except Exception as e:

            print(
                f"❌ Processing error: {e}"
            )


    # Create DataFrame
    df = pd.DataFrame(results)


    # Reorder columns
    if not df.empty:

        df = df[
            [
                "location",
                "latitude",
                "longitude",
                "forecast_hour",
                "temperature_c",
                "humidity",
                "wind_speed_ms",
                "wind_direction_deg"
            ]
        ]


    return df