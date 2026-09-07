# 🌦️ WeatherGPT — GFS Multi-Forecast Weather System

WeatherGPT is a weather forecasting system that integrates **NOAA GFS (Global Forecast System)** forecast data with location-based weather analysis and interactive map visualization.

The current module focuses on downloading and processing **GFS 0.25° forecast data** for the Indian region and preparing multiple forecast time steps for integration with the WeatherGPT chatbot.

---

## 🚀 Project Overview

WeatherGPT aims to provide users with an easy way to obtain weather forecasts through a conversational interface.

The system combines:

* 🌍 **GFS numerical weather prediction data**
* 📍 **Location-based weather forecasting**
* 🕐 **Multi-hour / multi-day forecasts**
* 🗺️ **Interactive Folium map visualization**
* 🤖 **WeatherGPT conversational interface**
* 🐍 **Python-based backend processing**

### Current Development Pipeline

```text
User Query
    ↓
WeatherGPT
    ↓
Location Detection
    ↓
GFS Forecast Data
    ↓
Forecast Processing
    ↓
Location-wise Weather Data
    ↓
Folium Visualization
    ↓
Weather Response
```

---
Install Dependencies
pip install -r requirements.txt

💻 Usage
To run the project and generate the weather map and forecast, simply execute the main script:
python main.py


## 📌 Current Features

### GFS Data Download

The system automatically searches for the latest available GFS cycle and downloads forecast files for:

```text
F000
F006
F012
F024
F048
F072
F120
```

These represent forecast lead times of:

| Forecast | Meaning          |
| -------- | ---------------- |
| F000     | Initial analysis |
| F006     | +6 hours         |
| F012     | +12 hours        |
| F024     | +24 hours        |
| F048     | +48 hours        |
| F072     | +72 hours        |
| F120     | +120 hours       |

---

## 🌍 Geographic Coverage

The current GFS download is restricted to the Indian region to reduce file size and processing requirements.

```text
Longitude: 68°E – 98°E
Latitude:   6°N – 38°N
```

This covers most of the Indian subcontinent and surrounding areas.

---

## 📡 GFS Dataset

The project currently uses:

**NOAA GFS 0.25° Global Forecast System**

The GFS data contains meteorological variables such as:

* Temperature
* Relative Humidity
* U-component of wind
* V-component of wind
* 2-meter atmospheric variables
* 10-meter wind variables

The data is retrieved through the **NOAA NOMADS GFS GRIB filter**.

---

## 🛠️ Technologies Used

### Programming

* Python

### Data Processing

* NumPy
* Pandas
* Xarray
* cfgrib

### Weather Data

* NOAA GFS
* NOMADS

### Visualization

* Folium

### Networking

* Requests

### Development

* VS Code
* Git
* GitHub
* Python Virtual Environment

---

## 📂 Project Structure

```text
WeatherGPT-GFS-MultiForecast/
│
├── data/
│   └── gfs/
│       └── .gitkeep
│
├── src/
│   └── gfs_downloader.py
│
├── app.py
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
```

> The project structure may change as additional WeatherGPT modules are integrated.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/WeatherGPT-GFS-MultiForecast.git
```

Move into the project directory:

```bash
cd WeatherGPT-GFS-MultiForecast
```

---

## 2. Create a Python Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, your terminal should look similar to:

```text
(.venv) PS C:\Users\...\WeatherGPT-GFS-MultiForecast>
```

---

## 3. Select the Python Interpreter in VS Code

In VS Code:

```text
Ctrl + Shift + P
```

Search:

```text
Python: Select Interpreter
```

Select:

```text
.venv\Scripts\python.exe
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` has not yet been created:

```bash
pip install requests numpy pandas xarray cfgrib folium
```

Then generate it:

```bash
pip freeze > requirements.txt
```

---

# ▶️ Running the GFS Downloader

Run the downloader from the project directory:

```bash
python src/gfs_downloader.py
```

The program will:

1. Check the latest available GFS cycles.
2. Select the most recent available cycle.
3. Generate the NOAA NOMADS download URL.
4. Download the requested forecast hours.
5. Save the GRIB2 files locally.
6. Display the download summary.

Example:

```text
============================================================
GFS DOWNLOAD
============================================================

Checking available GFS cycles...

Checking cycle: 2026-09-07 12Z
  Not available.

Checking cycle: 2026-09-07 06Z
✓ Available cycle found: 2026-09-07 06Z

Selected cycle: 2026-09-07 06:00:00 UTC
============================================================

Downloading F000...
✓ Saved: gfs_20260907_06_f000.grib2

Downloading F006...
✓ Saved: gfs_20260907_06_f006.grib2

Downloading F012...
✓ Saved: gfs_20260907_06_f012.grib2
```

---

# 📁 Generated Data

Downloaded GFS files are stored inside:

```text
data/gfs/
```

Example:

```text
data/
└── gfs/
    ├── gfs_20260907_06_f000.grib2
    ├── gfs_20260907_06_f006.grib2
    ├── gfs_20260907_06_f012.grib2
    ├── gfs_20260907_06_f024.grib2
    ├── gfs_20260907_06_f048.grib2
    ├── gfs_20260907_06_f072.grib2
    └── gfs_20260907_06_f120.grib2
```

These generated files are **not committed to GitHub** because GRIB2 weather files can be large.

---

# 🗺️ Planned Map Visualization

The next stage of the project is to process the GFS data and generate location-based weather visualization using **Folium**.

The planned workflow is:

```text
GFS GRIB2
    ↓
xarray / cfgrib
    ↓
Extract Weather Variables
    ↓
Latitude / Longitude Grid
    ↓
Location Selection
    ↓
Folium Map
    ↓
Weather Visualization
```

The map will allow users to visualize forecast information for selected locations.

---

# 🤖 WeatherGPT Integration

The final system will connect the GFS forecasting module to the WeatherGPT chatbot.

Example interaction:

```text
User:
What will the weather be like in Kolkata over the next 3 days?

        ↓

WeatherGPT

        ↓

Identify:
Kolkata

        ↓

Retrieve:
GFS Forecast

        ↓

Process:
Temperature
Humidity
Wind
Rainfall

        ↓

Generate:
Multi-Forecast

        ↓

Display:
Weather Information + Interactive Map
```

---

# 🔮 Future Improvements

The project is currently under development.

Planned features include:

* [ ] Multi-day GFS forecasting
* [ ] Automatic GFS cycle selection
* [ ] City-wise weather extraction
* [ ] Temperature visualization
* [ ] Wind-speed and wind-direction visualization
* [ ] Precipitation visualization
* [ ] Interactive Folium maps
* [ ] Weather forecast markers
* [ ] Location search
* [ ] India-wide weather visualization
* [ ] Integration with WeatherGPT chatbot
* [ ] Automated GFS data updates
* [ ] Forecast comparison between multiple GFS cycles
* [ ] Improved error handling
* [ ] Backend API integration
* [ ] Production deployment

---

# 🧪 Development Status

**Status: 🚧 In Development**

Current implementation:

```text
✅ Python environment
✅ GFS cycle detection
✅ NOAA NOMADS integration
✅ GFS 0.25° data download
✅ India-region subsetting
✅ Multiple forecast-hour downloads
⬜ GRIB2 processing
⬜ City-wise extraction
⬜ Folium visualization
⬜ WeatherGPT integration
⬜ Production deployment
```

---

# 📊 Forecast Configuration

Forecast hours can be modified in:

```python
FORECAST_HOURS = [
    0,
    6,
    12,
    24,
    48,
    72,
    120
]
```

For example, to test forecasts up to 48 hours:

```python
FORECAST_HOURS = [
    0,
    6,
    12,
    24,
    36,
    48
]
```

---

# 🔐 GitHub & Data Policy

The following files should **not** be committed to GitHub:

```text
.venv/
data/gfs/*.grib2
.env
__pycache__/
```

They are excluded through `.gitignore`.

The GFS data is downloaded dynamically by the application.

---

# 👨‍💻 Author

**Mainak Bal**

B.Tech — Electronics & Communication Engineering

Interested in:

* Data Analytics
* Machine Learning
* MLOps
* Remote Sensing
* Weather & Environmental Data
* AI Applications

---

# 📄 License

This project is intended for educational and research purposes.

Weather data is obtained from NOAA's Global Forecast System through the NOMADS service.
