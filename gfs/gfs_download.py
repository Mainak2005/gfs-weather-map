import os
import requests
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode


# ============================================================
# SETTINGS
# ============================================================

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "gfs"
)

os.makedirs(DATA_DIR, exist_ok=True)


# ============================================================
# INDIA REGION
# ============================================================

LEFT_LON = 68
RIGHT_LON = 98
TOP_LAT = 38
BOTTOM_LAT = 6


# ============================================================
# FORECAST HOURS
# ============================================================

FORECAST_HOURS = [
    0,
    6,
    12,
    24,
    48,
    72,
    120
]


# ============================================================
# NOMADS BASE URL
# ============================================================

NOMADS_URL = (
    "https://nomads.ncep.noaa.gov/cgi-bin/"
    "filter_gfs_0p25.pl"
)


# ============================================================
# BUILD URL
# ============================================================

def build_url(cycle, forecast_hour):

    date_str = cycle.strftime("%Y%m%d")
    cycle_hour = cycle.strftime("%H")

    file_name = (
        f"gfs.t{cycle_hour}z."
        f"pgrb2.0p25."
        f"f{forecast_hour:03d}"
    )

    params = {
        "file": file_name,

        # Variables
        "var_TMP": "on",
        "var_RH": "on",
        "var_UGRD": "on",
        "var_VGRD": "on",

        # Levels
        "lev_2_m_above_ground": "on",
        "lev_10_m_above_ground": "on",

        # Region
        "subregion": "",
        "leftlon": LEFT_LON,
        "rightlon": RIGHT_LON,
        "toplat": TOP_LAT,
        "bottomlat": BOTTOM_LAT,

        # GFS directory
        "dir": f"/gfs.{date_str}/{cycle_hour}/atmos"
    }

    return NOMADS_URL + "?" + urlencode(params)


# ============================================================
# CHECK IF A GFS CYCLE EXISTS
# ============================================================

def cycle_available(cycle):

    date_str = cycle.strftime("%Y%m%d")
    cycle_hour = cycle.strftime("%H")

    # Test F000 first
    file_name = (
        f"gfs.t{cycle_hour}z."
        f"pgrb2.0p25.f000"
    )

    params = {
        "file": file_name,

        "var_TMP": "on",
        "lev_2_m_above_ground": "on",

        "subregion": "",

        "leftlon": LEFT_LON,
        "rightlon": RIGHT_LON,
        "toplat": TOP_LAT,
        "bottomlat": BOTTOM_LAT,

        "dir": f"/gfs.{date_str}/{cycle_hour}/atmos"
    }

    url = NOMADS_URL + "?" + urlencode(params)

    try:

        response = requests.get(
            url,
            timeout=30
        )

        if response.status_code == 200:

            content_type = response.headers.get(
                "Content-Type",
                ""
            ).lower()

            if "text/html" not in content_type:

                return True

    except requests.RequestException:

        pass

    return False


# ============================================================
# FIND LATEST AVAILABLE GFS CYCLE
# ============================================================

def get_latest_cycle():

    now = datetime.now(timezone.utc)

    cycle_hours = [
        18,
        12,
        6,
        0
    ]

    print("\nChecking available GFS cycles...\n")

    # Check today and yesterday
    for days_back in range(2):

        date = now - timedelta(days=days_back)

        for hour in cycle_hours:

            cycle = date.replace(
                hour=hour,
                minute=0,
                second=0,
                microsecond=0
            )

            # Do not check future cycle
            if cycle > now:
                continue

            print(
                f"Checking cycle: "
                f"{cycle.strftime('%Y-%m-%d %HZ')}"
            )

            if cycle_available(cycle):

                print(
                    f"✓ Available cycle found: "
                    f"{cycle.strftime('%Y-%m-%d %HZ')}"
                )

                return cycle

            print("  Not available.")

    return None


# ============================================================
# DOWNLOAD ONE GFS FILE
# ============================================================

def download_gfs_file(cycle, forecast_hour):

    url = build_url(
        cycle,
        forecast_hour
    )

    filename = (
        f"gfs_{cycle.strftime('%Y%m%d_%H')}"
        f"_f{forecast_hour:03d}.grib2"
    )

    output_path = os.path.join(
        DATA_DIR,
        filename
    )

    print(
        f"\nDownloading F{forecast_hour:03d}..."
    )

    try:

        response = requests.get(
            url,
            timeout=180
        )

        # ----------------------------------------------------
        # HTTP ERROR
        # ----------------------------------------------------

        if response.status_code != 200:

            print(
                f"❌ Download failed: "
                f"HTTP {response.status_code}"
            )

            return None

        # ----------------------------------------------------
        # CHECK CONTENT
        # ----------------------------------------------------

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if "text/html" in content_type:

            print(
                "❌ NOMADS returned an HTML error page."
            )

            return None

        # ----------------------------------------------------
        # CHECK SIZE
        # ----------------------------------------------------

        if len(response.content) < 1000:

            print(
                "❌ Downloaded file is too small."
            )

            return None

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        with open(
            output_path,
            "wb"
        ) as file:

            file.write(
                response.content
            )

        size_mb = (
            os.path.getsize(output_path)
            / (1024 * 1024)
        )

        print(
            f"✓ Saved: {filename}"
        )

        print(
            f"  Size: {size_mb:.2f} MB"
        )

        return output_path

    except requests.RequestException as e:

        print(
            f"❌ Request error: {e}"
        )

        return None

    except Exception as e:

        print(
            f"❌ Unexpected error: {e}"
        )

        return None


# ============================================================
# DOWNLOAD ALL FORECASTS
# ============================================================

def download_all_gfs():

    print("\n")
    print("=" * 60)
    print("GFS DOWNLOAD")
    print("=" * 60)

    # --------------------------------------------------------
    # FIND AVAILABLE CYCLE
    # --------------------------------------------------------

    cycle = get_latest_cycle()

    if cycle is None:

        print("\n❌ No available GFS cycle found.")

        return []

    print("\n")
    print(
        f"Selected cycle: "
        f"{cycle.strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # DOWNLOAD FORECASTS
    # --------------------------------------------------------

    downloaded = []

    for forecast_hour in FORECAST_HOURS:

        file_path = download_gfs_file(
            cycle,
            forecast_hour
        )

        if file_path:

            downloaded.append(
                (
                    forecast_hour,
                    file_path
                )
            )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)

    print(
        f"Downloaded "
        f"{len(downloaded)} "
        f"of "
        f"{len(FORECAST_HOURS)} "
        f"forecasts."
    )

    print("=" * 60)

    if downloaded:

        print("\nDownloaded files:")

        for hour, path in downloaded:

            print(
                f"  F{hour:03d} → {path}"
            )

    else:

        print(
            "\n❌ No GFS files downloaded."
        )

    return downloaded


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    download_all_gfs()