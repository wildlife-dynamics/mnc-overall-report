# MNC Overall Report — User Guide

This guide walks you through configuring and running the MNC Overall Report workflow, which consolidates weather observations, logistics events, wildlife sightings, livestock events, and patrol data from EarthRanger into a single comprehensive monthly report and dashboard for Mara North Conservancy.

---

## Overview

The workflow delivers, for each run:

- **7 weather charts** (HTML + PNG) — daily precipitation, temperature, wind speed, wind gusts, soil temperature, relative humidity, and atmospheric pressure per station
- **Logistics tables** — balloon landing summary, airstrip operations (pivoted by arrival/departure), and airstrip maintenance log
- **Livestock reports** — mobile boma movement map and summary, cattle count table, livestock predation map and summary, illegal grazing map
- **Wildlife reports** — a wildlife incident map, and for all 8 species (elephant, buffalo, rhino, lion, leopard, cheetah, giraffe, hartebeest): a sightings map and a summary table, with elephant and buffalo additionally getting a herd-composition map, a herd-size bubble map, and a herd-size bar chart
- **Events overview** — total events recorded by date and by type, with a line chart
- **Patrol reports** — foot, vehicle, motorbike, and overall patrol coverage maps, per-mode effort summaries, overall per-ranger effort, and conservancy patrol occupancy
- **Results dashboard** — all 44 map, chart, and table widgets above assembled into a single dashboard view
- **1 Word report** (`overall_report.docx`) — generated from a Dropbox-hosted report template

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with the following recorded for the analysis period:
  - Weather station observations under the `ER2ER - From GMMF` subject group
  - Logistics events: `balloon_landing`, `airstrip_operations`, `airstrip_maintenance`
  - Livestock events: `mobile_boma_rep`, `cattle_count`, `livestock_predation_rep`, `illegal_grazing_rep`
  - Wildlife incident events: `snare_rep`, `fire_rep`, `wildlife_injury_rep`, `wildlife_treatment_rep`, `wildlife_carcass_rep`
  - Wildlife sighting events: `elephant_sighting_rep`, `buffalo_sighting_rep`, `rhino_sighting_rep`, `lion_sighting_rep`, `leopardsightingrep`, `cheetah_sighting_rep`, `giraffe_sighting`, `hartebeest_sighting`
  - `patrol_info` events and associated patrol observations
- Network access to **Dropbox**, so the workflow can download the MNC conservancy boundary, parcels, and Word report template files at runtime

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste the GitHub repository URL into the **Github Link** field:

```
https://github.com/wildlife-dynamics/mnc-overall-report.git
```

Then click **Add Template**.

![Add Workflow Template](data/screenshots/add_workflow.png)

---

### Step 2 — Configure the EarthRanger Connection

Navigate to **Data Sources** and click **Connect**, then select **EarthRanger**. Fill in the connection form:

| Field | Description |
|-------|-------------|
| Data Source Name | A label to identify this connection (e.g. `Mara North Conservancy`) |
| EarthRanger URL | Your instance URL (e.g. `your-site.pamdas.org`) |
| EarthRanger Username | Your EarthRanger username |
| EarthRanger Password | Your EarthRanger password |

> Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs.

Click **Connect** to save.

![EarthRanger Connection](data/screenshots/er_connection.png)

---

### Step 3 — Select the Workflow

After the template is added, it appears in the **Workflow Templates** list as **mnc-overall-report**. Click the card to open the workflow configuration form.

![Select Workflow Template](data/screenshots/select_workflow.png)

---

### Step 4 — Configure Workflow Details, Time Range, and EarthRanger Connection

The configuration form has three sections on a single page.

**Set workflow details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes (e.g. reporting month or site) |

**Time range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time — all data from this point is fetched |
| Until | End date and time of the analysis window |

**Connect to ER**

Select the EarthRanger data source configured in Step 2 from the **Data Source** dropdown (e.g. `Mara North Conservancy`).

Once all three sections are filled, click **Submit**.

![Configure Workflow Details, Time Range, and Connect to ER](data/screenshots/configure_workflow.png)

---

## Running the Workflow

Once submitted, the runner will:

1. Download the MNC community conservancy boundary and parcels GeoPackage files from Dropbox; repair invalid geometries; derive the conservancy AOI (`grazing_zone == Conservancy`), the non-conservancy grazing zones (colored individually), and the Mara North Conservancy extent (used to compute the shared map zoom/center); build reusable conservancy, grazing-zone, and parcels map layers.
2. Fetch weather station observations from the `ER2ER - From GMMF` subject group; extract seven meteorological variables from each observation; compute daily per-station aggregates; draw one line chart per variable.
3. Fetch all events once; split off balloon landing, airstrip operations, and airstrip maintenance events; clean and summarise each into a table.
4. Split off mobile boma, cattle count, livestock predation, and illegal grazing events; generate maps and summary tables (livestock maps additionally show the grazing-zone layer).
5. Split off wildlife incident events (snares, fires, carcasses, injuries, veterinary treatments); generate an incident map and summary tables.
6. Split off each of the 8 wildlife species' sighting events; generate a sightings map and summary table for each; elephant and buffalo additionally get herd-composition classification, a herd-size bar chart, and a herd-size bubble map.
7. Summarise all events by date and by type (excluding distance-count and airstrip-operations event types); draw a total-events line chart.
8. Fetch `patrol_info` events and associated patrol observations; convert to relocations; split into Foot, Vehicle, and Motorbike branches and convert each to trajectories using mode-appropriate segment filters; build a coverage grid and map for each mode and for the combined (overall) dataset; compute per-mode and per-ranger effort summaries and conservancy patrol occupancy.
9. Download the Word report template from Dropbox and assemble **overall_report.docx** from the outputs above.
10. Assemble all 44 widgets into the **MNC Overall Report dashboard**.
11. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

> **Note:** Every task is automatically skipped if its input data is empty or an upstream step was skipped, so a run with no events of a given type simply omits that branch's outputs rather than failing. Widget-creation steps are the exception — they always run so that a placeholder widget still appears on the dashboard even if the branch behind it was skipped.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`.

### Weather
| File | Description |
|------|-------------|
| `weather_summary_table.csv` | Daily per-station summary of all 7 weather variables |
| `precipitation_readings_over_time.html` / `.png` | Daily total precipitation |
| `temperature_readings_over_time.html` / `.png` | Daily mean surface air temperature |
| `wind_speed_readings_over_time.html` / `.png` | Daily mean wind speed |
| `wind_gusts_readings_over_time.html` / `.png` | Daily maximum wind gusts |
| `soil_temperature_readings_over_time.html` / `.png` | Daily mean soil temperature |
| `relative_humidity_readings_over_time.html` / `.png` | Daily mean relative humidity |
| `atmospheric_pressure_readings_over_time.html` / `.png` | Daily mean atmospheric pressure |

### Logistics
| File | Description |
|------|-------------|
| `balloon_landing_summary_table.csv` (+ HTML) | Passenger records by balloon company and lodge |
| `airstrip_operations_summary_table.csv` (+ HTML) | Client counts pivoted by camp/lodge and arrival/departure |
| `airstrip_maintenance_summary_table.csv` (+ HTML) | Dated log of airstrip maintenance activities |

### Livestock
| File | Description |
|------|-------------|
| `mobile_boma_movement_summary_table.csv` | Daily count of boma movement events |
| `boma_movement_map.html` / `.png` | Boma movement locations map |
| `total_cattle_count_summary_table.csv` (+ HTML) | Cattle counts by zone, with total |
| `total_livestock_predation_summary_table.csv` | Daily count of livestock predation events |
| `livestock_predation_summary_table.html` | Rendered HTML of the daily predation count table (dashboard widget) |
| `livestock_predation_summary_table.csv` | Detailed per-event predation table (species, predator, total affected) |
| `livestock_predation_events.html` / `.png` | Predation events map, coloured by species |
| `illegal_grazing_map.html` / `.png` | Illegal grazing locations map |

### Wildlife Incidents
| File | Description |
|------|-------------|
| `wildlife_events_recorded.csv` | Raw wildlife incident records (snares, fires, carcasses, injuries, veterinary treatments) |
| `wildlife_incidents_summary_table.csv` | Pivot table of incidents by type |
| `wildlife_incidents_recorded_by_date.csv` | Daily count of unique incidents |
| `wildlife_incidents_map.html` / `.png` | Incident locations map, coloured by incident type |

### Wildlife Sightings
| File | Description |
|------|-------------|
| `elephant_sightings_events.html` / `.png` | Elephant herd-composition sightings map |
| `elephant_herd_types_map.html` / `.png` | Elephant herd-size bubble map |
| `elephant_herd_size_bar_chart.html` / `.png` | Elephant herd-size distribution (5 bins) |
| `overall_elephant_summary_table.csv` (+ HTML) | Elephant sightings summary by herd type |
| `buffalo_sightings_events.html` / `.png` | Buffalo herd-composition sightings map |
| `buffalo_herd_types_map.html` / `.png` | Buffalo herd-size bubble map |
| `buffalo_herd_size_bar_chart.html` / `.png` | Buffalo herd-size distribution (5 bins) |
| `overall_buffalo_summary_table.csv` (+ HTML) | Buffalo sightings summary by herd type |
| `lion_pride_sightings_map.html` / `.png` | Lion sightings map, coloured by pride |
| `overall_lion_summary_table.csv` (+ HTML) | Lion sightings summary by pride |
| `leopard_sightings_map.html` / `.png` | Leopard sightings map, coloured by individuals present |
| `overall_leopard_summary_table.csv` (+ HTML) | Leopard sightings summary |
| `cheetah_sightings_map.html` / `.png` | Cheetah sightings map, coloured by individuals present |
| `overall_cheetah_summary_table.csv` (+ HTML) | Cheetah sightings summary |
| `giraffe_sightings_map.html` / `.png` | Giraffe sightings map |
| `overall_giraffe_summary_table.csv` (+ HTML) | Giraffe daily sightings summary |
| `rhino_sightings_map.html` / `.png` | Rhino sightings map |
| `overall_rhino_summary_table.csv` (+ HTML) | Rhino daily sightings summary |
| `hartebeest_sightings_map.html` / `.png` | Hartebeest sightings map |
| `overall_hart_summary_table.csv` (+ HTML) | Hartebeest daily sightings summary |

### Events Overview
| File | Description |
|------|-------------|
| `total_events_recorded_by_date.csv` | All events recorded by date |
| `total_events_recorded_by_type.csv` | All events recorded by type |
| `total_events_recorded.html` / `.png` | All-events line chart |

### Patrols
| File | Description |
|------|-------------|
| `patrol_events.csv` | Flattened `patrol_info` event details |
| `patrol_purpose_summary.csv` (+ HTML) | Patrol count by patrol purpose |
| `patrol_relocations.geoparquet` | Combined patrol observation dataset with patrol metadata |
| `foot_patrol_efforts.csv` | Foot patrol effort summary (count, distance, duration, speed) |
| `foot_patrol_map.html` / `.png` | Foot patrol coverage grid map |
| `vehicle_patrol_efforts.csv` | Vehicle patrol effort summary |
| `vehicle_patrol_map.html` / `.png` | Vehicle patrol coverage grid map |
| `motorbike_patrol_efforts.csv` | Motorbike patrol effort summary |
| `motor_patrol_map.html` / `.png` | Motorbike patrol coverage grid map |
| `overall_patrol_map.html` / `.png` | Combined (foot + vehicle + motorbike) patrol coverage grid map |
| `patrol_trajectories.geoparquet` | Reprojected overall patrol coverage grid |
| `overall_patrol_efforts.csv` (+ HTML) | Per-ranger summary of patrols, distance, and duration |
| `patrol_coverage.csv` (+ HTML) | Conservancy patrol occupancy percentage |

### Report
| File | Description |
|------|-------------|
| `overall_report.docx` | Final Word report, assembled from the Dropbox-hosted template and all outputs above |

---

## Dashboard

The workflow run also produces the **MNC Overall Report dashboard**, viewable in the workflow runner, with 44 widgets:

- **Weather (7):** Precipitation, Temperature, Wind Speed, Wind Gusts, Soil Temperature, Relative Humidity, Atmospheric Pressure
- **Logistics (3):** Balloon Landing Summary, Airstrip Operations Summary, Airstrip Maintenance Summary
- **Livestock (5):** Mobile Boma Movement Map, Livestock Predation Events Map, Illegal Grazing Events Map, Total Cattle Count Summary, Livestock Predation Summary
- **Wildlife (21):** Wildlife Incident Map, Elephant Herd Size Map, Elephant Herd Composition Map, Elephant Herd Size Distribution, Elephant Herd Composition Summary, Buffalo Herd Size Map, Buffalo Herd Composition Map, Buffalo Herd Size Distribution, Buffalo Herd Composition Summary, Lion Sightings Map, Lion Sightings Summary, Leopard Sightings Map, Leopard Sightings Summary, Cheetah Sightings Map, Cheetah Sightings Summary, Giraffe Sightings Map, Giraffe Sightings Summary, Hartebeest Sightings Map, Hartebeest Sightings Summary, Rhino Sightings Map, Rhino Sightings Summary
- **Patrol (8):** Foot Patrol Coverage Map, Vehicle Patrol Coverage Map, Motorbike Patrol Coverage Map, Overall Patrol Coverage Map, Total Events Recorded, Patrol Purpose Summary, Overall Patrol Efforts, Conservancy Patrol Occupancy

> **Note:** Each table widget is sortable and filterable in place; downloading directly from the widget is disabled — use the corresponding CSV output file for that.
