import os

from geopy.geocoders import Nominatim

from gfs.gfs_download import (
    download_all_gfs
)

from gfs.gfs_model import (
    build_forecast
)

from gfs.gfs_map import (
    create_weather_map
)


# ============================================================
# SETTINGS
# ============================================================

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__),
    "results"
)


# ============================================================
# LOCATION SEARCH
# ============================================================

def search_location():

    location_name = input(
        "\nEnter Indian city/location: "
    )

    geolocator = Nominatim(
        user_agent="weathergpt_gfs"
    )

    location = geolocator.geocode(
        f"{location_name}, India"
    )

    if location is None:

        print(
            "❌ Location not found."
        )

        return None


    latitude = location.latitude
    longitude = location.longitude


    print("\nLocation found")
    print("-" * 40)

    print(
        f"Name      : {location.address}"
    )

    print(
        f"Latitude  : {latitude}"
    )

    print(
        f"Longitude : {longitude}"
    )


    return (
        location_name,
        latitude,
        longitude
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("             WEATHERGPT GFS MODULE")
    print("=" * 60)


    # 1. Location
    location = search_location()

    if location is None:
        return


    location_name, latitude, longitude = (
        location
    )


    # 2. Download GFS
    downloaded_files = download_all_gfs()


    if not downloaded_files:

        print(
            "\n❌ No GFS files downloaded."
        )

        return


    # 3. Generate forecast
    forecast_df = build_forecast(
        downloaded_files,
        latitude,
        longitude,
        location_name
    )


    if forecast_df.empty:

        print(
            "\n❌ Forecast generation failed."
        )

        return


    # 4. Display
    print("\n")
    print("=" * 60)
    print("GFS MULTI-FORECAST")
    print("=" * 60)

    print(
        forecast_df.to_string(
            index=False
        )
    )


    # 5. Save CSV
    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    csv_path = os.path.join(
        RESULTS_DIR,
        "gfs_forecast.csv"
    )

    forecast_df.to_csv(
        csv_path,
        index=False
    )

    print(
        f"\n✓ CSV saved:\n{csv_path}"
    )


    # 6. Create map
    create_weather_map(
        latitude,
        longitude,
        location_name,
        forecast_df,
        RESULTS_DIR
    )


    print("\n")
    print("=" * 60)
    print("             GFS MODULE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()