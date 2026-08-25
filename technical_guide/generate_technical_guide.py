"""
Generate the MNC Overall Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: mnc_overall_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "mnc_overall_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"MNC Overall Report — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("MNC Overall Report", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Weather, logistics, livestock, wildlife, and patrol reporting for "
      "Mara North Conservancy", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>mara_north_event_report</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>mara_north_event_report</b> workflow (repository "
      "<b>mnc-overall-report</b>) is a comprehensive, multi-pipeline report for "
      "Mara North Conservancy. It pulls data from two independent sources "
      "— EarthRanger weather station observations and EarthRanger event records — "
      "and routes them through five reporting sections plus a cross-cutting "
      "events overview:"),
    bullet("<b>Section 1 — Weather:</b> Observations from the "
           "'ER2ER - From GMMF' subject group; produces a daily summary CSV and "
           "7 line charts (one per meteorological variable)."),
    bullet("<b>Section 2 — Logistics:</b> Balloon landings, airstrip operations, "
           "and airstrip maintenance events produce summary tables. A fourth "
           "event type, airline complaints, is fetched and normalised but "
           "produces no output (see Section 6.4)."),
    bullet("<b>Section 3 — Livestock:</b> Mobile boma movements, cattle counts, "
           "livestock predation, and illegal grazing events; produces summary "
           "CSVs/tables and maps that additionally show a grazing-zone layer "
           "not used elsewhere in the workflow."),
    bullet("<b>Section 4 — Wildlife:</b> Five wildlife incident types and eight "
           "wildlife sighting species; produces CSVs, maps, bar charts, and "
           "summary tables, with elephant and buffalo receiving the richest "
           "treatment (herd composition + herd size)."),
    bullet("<b>Events overview:</b> A cross-section daily/typed event count and "
           "a total-events line chart, independent of the five sections above."),
    bullet("<b>Section 5 — Patrol:</b> Foot, vehicle, and motorbike patrol "
           "trajectories derived from patrol_info events; produces patrol effort "
           "CSVs, a raw relocations file, three per-mode coverage maps, an "
           "overall coverage map, overall per-ranger efforts, and conservancy "
           "patrol occupancy."),
    sp(4),
    p("Logistics, Livestock, Wildlife, and Patrol all share a single "
      "<b>events_temporal</b> DataFrame built from one <b>get_events</b> call "
      "(no filters applied at fetch time — each branch performs its own "
      "downstream filter_df on event_type). Weather uses a separate "
      "<b>get_subjectgroup_observations</b> call. The workflow concludes by "
      "generating a Word report from a Dropbox-hosted template and assembling "
      "a 44-widget results dashboard."),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Section", "Output type", "Key files"],
            ["Weather",    "CSV + HTML/PNG charts",
             "weather_summary_table.csv, 7 × *_readings_over_time.html/.png"],
            ["Logistics",  "CSV (+ HTML)",
             "balloon_landing_summary_table, airstrip_operations_summary_table, "
             "airstrip_maintenance_summary_table (no output for airline complaints)"],
            ["Livestock",  "CSV/HTML + Map",
             "mobile_boma_movement_summary_table.csv, total_cattle_count_summary_table, "
             "total_livestock_predation_summary_table.csv + livestock_predation_summary_table "
             "(csv/html pair with overlapping names, see 7.3), "
             "boma_movement_map, livestock_predation_events, illegal_grazing_map"],
            ["Wildlife",   "CSV/HTML + Map + Chart",
             "wildlife_events_recorded.csv, wildlife_incidents_* CSVs, wildlife_incidents_map, "
             "8 species × (sightings map + overall_<species>_summary_table), elephant/buffalo "
             "additionally get a herd-size bar chart and a herd-types bubble map"],
            ["Events overview", "CSV + Chart",
             "total_events_recorded_by_date.csv, total_events_recorded_by_type.csv, "
             "total_events_recorded.html/.png"],
            ["Patrol",     "CSV + GeoParquet + Map",
             "patrol_events.csv, patrol_purpose_summary.csv, patrol_relocations.geoparquet, "
             "foot/vehicle/motorbike_patrol_efforts.csv, foot/vehicle/motor_patrol_map, "
             "overall_patrol_map, patrol_trajectories.geoparquet, overall_patrol_efforts.csv, "
             "patrol_coverage.csv"],
            ["Report",     "Word document",
             "overall_report.docx"],
        ],
        [2.5*cm, 3*cm, W - 5.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-platform",               ">=2.15.0, <2.16.0", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",    "0.1.0rc14.*",       "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",       "0.0.0rc1.*",        "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-wwf-virunga","0.0.0rc9.*",       "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-big-life",  "1.0.1.*",           "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",       "1.0.3.*",           "ecoscope-workflows-custom"],
            ["pydeck",                           "0.9.2",             "conda-forge"],
            ["opentelemetry-sdk",                ">=1.20.0,<2.0.0",   "conda-forge"],
        ],
        [6.5*cm, 4*cm, W - 10.5*cm],
    ),
    sp(6),
    p("Several tasks in this spec call into the "
      "<b>ecoscope_workflows_ext_mnc.tasks.*</b> namespace: "
      "fix_invalid_geometries, build_legend_values_from_column, "
      "remove_brackets_from_column, convert_columns_to_int, and "
      "apply_arithmetic_operation_over_rows. The requirements list above pins "
      "<b>ecoscope-workflows-ext-mnc 1.0.3.*</b>, which supplies these tasks — "
      "the package is present and correctly versioned in the current spec."),
    sp(6),
    h2("2.2  Connections and external assets"),
    make_table(
        [
            ["Asset", "Task / Source", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch all event records and subject group observations; "
             "also used by process_events_details calls to resolve display titles "
             "and by get_patrol_values / patrol observation fetches."],
            ["mnc_conservancy.gpkg", "fetch_and_persist_file (Dropbox)",
             "MNC community conservancy boundaries, one polygon per grazing_zone "
             "value. Fixed with fix_invalid_geometries, then split into the "
             "conservancy AOI, the Mara North extent, and the non-conservancy "
             "grazing zones (see Section 3)."],
            ["mnc_across_the_river_parcels.gpkg", "fetch_and_persist_file (Dropbox)",
             "MNC across-the-river land parcels. Used as an additional polygon "
             "layer on every map in the workflow."],
            ["mara_north_event_template.docx", "fetch_mnc_template / fetch_and_persist_file (Dropbox)",
             "Word report template. Populated by generate_mnc_report at the "
             "end of the workflow to produce overall_report.docx."],
        ],
        [3.5*cm, 4.5*cm, W - 8*cm],
    ),
    note("All Dropbox files are downloaded with overwrite_existing: false and "
         "retries: 3. If a file already exists in ECOSCOPE_WORKFLOWS_RESULTS "
         "from a prior run the download is skipped."),
    sp(6),
    h2("2.3  Grouper"),
    p("The workflow uses an <b>empty grouper list</b> (groupers: [], set once "
      "by the set_groupers task and referenced via "
      "<b>${{ workflow.groupers.return }}</b> everywhere a grouper is needed, "
      "including add_temporal_index calls and the final dashboard). "
      "All records are processed as a single undivided dataset — no fan-out or "
      "per-group branching is applied anywhere in the spec."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. GEOSPATIAL ASSET PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Geospatial Asset Pipeline"),
    hr(),
    p("Before the reporting sections run, the workflow downloads and prepares "
      "all shared geospatial base layers: two ArcGIS raster basemap tiles, the "
      "conservancy boundary / grazing-zone / parcels vector layers, and a single "
      "shared map zoom and view state. These are reused across every map drawn "
      "later in the workflow."),
    sp(6),
    h2("3.1  Conservancy boundaries"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download <b>mnc_conservancy.gpkg</b> from Dropbox "
             "(overwrite_existing: false, retries: 3)."],
            ["2", "load_df",
             "Load the gpkg into a GeoDataFrame."],
            ["3", "fix_invalid_geometries",
             "Repair invalid geometries (ecoscope_workflows_ext_mnc task). "
             "All three derived views below are built from this fixed layer."],
            ["4", "filter_df — Conservancy AOI",
             "grazing_zone == 'Conservancy' → the coverage/report area of "
             "interest, used as the base polygon for the patrol coverage grid "
             "and as one of the two/three layers combined on every map."],
            ["5", "filter_df — Mara North extent",
             "name == 'Mara North Conservancy' → used only to compute the "
             "shared map zoom/centre (Section 3.5), not drawn on any map."],
            ["6", "filter_df — Grazing zones",
             "grazing_zone != 'Conservancy' → the individual grazing zones, "
             "coloured with a GnBu colormap and a generated legend "
             "(build_legend_values_from_column, ecoscope_workflows_ext_mnc)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.2  Styled zone layers"),
    p("Three reusable static DeckGL layers are built, one per derived view "
      "above:"),
    make_table(
        [
            ["Layer", "Task", "Style", "Legend"],
            ["create_conservancy_layer",
             "create_deckgl_layer_from_gdf (or equivalent)",
             "Grey outline, unfilled",
             "'Conservancy Boundary'"],
            ["create_grazing_zones_layer",
             "create_deckgl_layer_from_gdf",
             "Filled per-zone colour from the GnBu legend",
             "grazing_zone_legend_values"],
            ["create_parcels_layer",
             "create_deckgl_layer_from_gdf",
             "Tan / khaki fill, stroked",
             "'Parcels' (legend title: 'Map Layers')"],
        ],
        [4*cm, 4.5*cm, 4*cm, W - 12.5*cm],
    ),
    note("Layering rule: the three Livestock-branch maps (mobile boma "
         "movement, livestock predation, illegal grazing) combine <b>all "
         "three</b> static layers — parcels + grazing zones + conservancy. "
         "Every other map in the workflow (all wildlife sighting/incident maps "
         "and all patrol maps) combines only <b>two</b> layers — parcels + "
         "conservancy — the grazing-zone layer is intentionally omitted outside "
         "the Livestock section. This is a real, deliberate behavioural "
         "distinction and did not exist in the previous version of this spec."),
    sp(6),
    h2("3.3  Conservancy GDFs and text labels"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "create_gdf_from_dict / filter_df",
             "Build <b>conservancy_gdf</b> (Conservancy AOI) and "
             "<b>envelope_gdf</b> (Mara North extent) for downstream use."],
            ["2", "create_custom_text_layer",
             "Render conservancy / zone name labels for placement on the maps."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.4  Parcels layer"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download <b>mnc_across_the_river_parcels.gpkg</b> from Dropbox."],
            ["2", "load_df",
             "Load the parcels gpkg into a GeoDataFrame."],
            ["3", "create_parcels_layer",
             "Render as a filled polygon layer (tan fill). Legend entry: "
             "'Parcels', legend title 'Map Layers'."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.5  Base tiles and shared view state"),
    make_table(
        [
            ["Item", "Detail"],
            ["Basemap tile layers",
             "Two ArcGIS raster layers reused as tile_layers on every "
             "draw_map call: Elevation/World_Hillshade (opacity 0.80, "
             "max_zoom 20) and Reference/World_Boundaries_and_Places_Alternate "
             "(opacity 0.35, max_zoom 20)."],
            ["Map Zoom & Extent task-group",
             "compute_view_state_from_gdf on the Mara North extent "
             "(envelope_gdf) with pitch 0, bearing 0, max_zoom 15 → "
             "gdf_image_extent."],
        ],
        [4.5*cm, W - 4.5*cm],
    ),
    note("gdf_image_extent is the single view_state reused on every draw_map "
         "call in the entire workflow — Livestock, Wildlife, and Patrol maps "
         "alike share one zoom/centre, computed once."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. SHARED EVENT INGESTION PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Shared Event Ingestion Pipeline"),
    hr(),
    p("Logistics, Livestock, Wildlife, and Patrol all share a single event "
      "retrieval call. Weather data uses a separate subject-group observation "
      "fetch (Section 5.1)."),
    sp(6),
    h2("4.1  Event retrieval"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",                      "get_events"],
            ["event_types",               "[] (fetch all event types — no filter at fetch time)"],
            ["Downstream filtering",      "Each of Logistics, Livestock, Wildlife Incidents, "
                                          "Wildlife Sightings, Events Overview, and Patrol performs "
                                          "its own filter_df / exclude_row_values on event_type "
                                          "against the shared events_temporal DataFrame."],
            ["include_details",           "true"],
            ["raise_on_empty",            "true"],
            ["include_null_geometry",     "false"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("4.2  Date extraction and temporal indexing"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "extract_column_as_type",
             "Extract the <b>time</b> column as <b>output_type: date</b> "
             "into a new column named <b>date</b>."],
            ["2", "add_temporal_index",
             "Add temporal index using the shared <b>groupers</b> "
             "(${{ workflow.groupers.return }}, i.e. []). "
             "Produces the shared <b>events_temporal</b> DataFrame consumed "
             "by every downstream section."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("4.3  Common event detail normalisation pattern"),
    p("Every event branch applies the same three-step normalisation after "
      "filtering events_temporal by event_type:"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "process_events_details",
             "Resolve event detail field IDs to display titles "
             "(map_to_titles: true). Requires the ER connection."],
            ["2", "normalize_json_column",
             "Flatten the <b>event_details</b> JSON column."],
            ["3", "drop_column_prefix",
             "Remove the <b>event_details__</b> prefix from all flattened "
             "columns."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    note("Because map_to_titles is true, flattened column names are "
         "human-readable display titles from EarthRanger (e.g. 'Balloon "
         "Company', 'Livestock Species'). All downstream map_columns steps "
         "reference these titles directly."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. SECTION 1 — WEATHER PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Section 1 — Weather Pipeline"),
    hr(),
    p("The weather pipeline runs independently from the shared event pipeline. "
      "It fetches sensor observations from the <b>ER2ER - From GMMF</b> "
      "subject group and extracts seven meteorological fields sequentially "
      "from the <b>extra__observation_details</b> JSON column."),
    sp(6),
    h2("5.1  Observation retrieval"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",                "get_subjectgroup_observations"],
            ["subject_group_name",  "ER2ER - From GMMF"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("5.2  Field extraction chain"),
    p("Seven sequential <b>extract_value_from_json_column</b> tasks are "
      "chained, each reading from the previous task's output, all extracting "
      "from <b>extra__observation_details</b>:"),
    make_table(
        [
            ["Output column", "Field"],
            ["precipitation",        "precipitation"],
            ["temperature",          "temperature"],
            ["wind_speed",           "wind_speed"],
            ["wind_gusts",           "wind_gusts"],
            ["soil_temperature",     "soil_temperature"],
            ["relative_humidity",    "relative_humidity"],
            ["atmospheric_pressure", "atmospheric_pressure"],
        ],
        [6*cm, W - 6*cm],
    ),
    sp(6),
    h2("5.3  Date extraction, renaming, and temporal index"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "extract_column_as_type",
             "Extract the observation time column as <b>output_type: date</b> "
             "→ new column <b>date</b>."],
            ["2", "map_columns",
             "Rename <b>extra__subject__name</b> → <b>weather_station</b>."],
            ["3", "add_temporal_index",
             "Add temporal index (groupers: [])."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("5.4  Daily weather summary"),
    p("Task: <b>summarize_df</b>. Groups by <b>weather_station</b> and "
      "<b>date</b>. Aggregations:"),
    make_table(
        [
            ["Column", "Aggregator", "Description"],
            ["precipitation",       "sum",  "Total daily rainfall"],
            ["temperature",         "mean", "Daily average temperature"],
            ["wind_speed",          "mean", "Daily average wind speed"],
            ["wind_gusts",          "max",  "Daily maximum wind gust"],
            ["soil_temperature",    "mean", "Daily average soil temperature"],
            ["relative_humidity",   "mean", "Daily average relative humidity"],
            ["atmospheric_pressure","mean", "Daily average atmospheric pressure"],
        ],
        [4*cm, 2.5*cm, W - 6.5*cm],
    ),
    p("Output saved as <b>weather_summary_table.csv</b>. No dashboard widget "
      "is created for this table — it persists as a downloadable file only."),
    sp(6),
    h2("5.5  Line charts"),
    p("One <b>draw_line_chart</b> task per metric reads from the daily "
      "weather summary (x_column: date, category_column: weather_station), "
      "each persisted as HTML then converted to PNG:"),
    make_table(
        [
            ["HTML filename", "Widget"],
            ["precipitation_readings_over_time.html",        "Precipitation"],
            ["temperature_readings_over_time.html",          "Temperature"],
            ["wind_speed_readings_over_time.html",            "Wind Speed"],
            ["wind_gusts_readings_over_time.html",            "Wind Gusts"],
            ["soil_temperature_readings_over_time.html",      "Soil Temperature"],
            ["relative_humidity_readings_over_time.html",     "Relative Humidity"],
            ["atmospheric_pressure_readings_over_time.html",  "Atmospheric Pressure"],
        ],
        [8*cm, W - 8*cm],
    ),
    note("All 7 weather widgets are plot widgets on the dashboard (see "
         "Section 12), and all are widget-creation steps — they use "
         "skipif.conditions: [never], so a placeholder still renders even if "
         "the weather observation fetch returned no data."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. SECTION 2 — LOGISTICS REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Section 2 — Logistics Report"),
    hr(),
    p("Four event types are filtered from <b>events_temporal</b> and "
      "normalised using the common three-step pattern (Section 4.3): "
      "balloon_landing, airstrip_operations, airstrip_maintenance, and "
      "airline_complaint."),
    sp(6),
    h2("6.1  Branch 1 — Balloon Landings"),
    p("Filter: event_type == <b>balloon_landing</b>"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_column_prefix."],
            ["4", "map_columns",
             "Retain date, Balloon Company, Where are clients staying?, "
             "# of passengers; rename for display."],
            ["5", "remove_brackets_from_column",
             "Strip list-bracket characters from the retained text columns "
             "(ecoscope_workflows_ext_mnc task)."],
            ["6", "persist_df",
             "Save as <b>balloon_landing_summary_table.csv</b>."],
            ["7", "draw_table + persist_text",
             "Render an HTML table; persisted with a runtime-computed "
             "filename_suffix of 'balloon_landing_summary_table.html' "
             "(there is no explicit `filename:` for the HTML output — the "
             "name is derived at run time from the suffix)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    p("Widget: <b>'Balloon Landing Summary'</b> (table)."),
    sp(6),
    h2("6.2  Branch 2 — Airstrip Operations"),
    p("Filter: event_type == <b>airstrip_operations</b>"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_column_prefix."],
            ["4", "summarize_df",
             "Group by camp/lodge × arrival/departure; count clients."],
            ["5", "pivot_df",
             "Pivot the grouped counts into Arrival / Departure columns, one "
             "row per Camp/Lodge."],
            ["6", "persist_df",
             "Save as <b>airstrip_operations_summary_table.csv</b>."],
            ["7", "draw_table + persist_text",
             "Render an HTML table; persisted with a runtime-computed "
             "filename_suffix of 'airstrip_operations_summary_table.html'."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    p("Widget: <b>'Airstrip Operations Summary'</b> (table)."),
    sp(6),
    h2("6.3  Branch 3 — Airstrip Maintenance"),
    p("Filter: event_type == <b>airstrip_maintenance</b>"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_column_prefix."],
            ["4", "map_columns",
             "Retain date and Maintenance type."],
            ["5", "persist_df",
             "Save as <b>airstrip_maintenance_summary_table.csv</b>."],
            ["6", "draw_table + persist_text",
             "Render an HTML table; persisted with a runtime-computed "
             "filename_suffix of 'airstrip_maintenance_summary_table.html'."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    p("Widget: <b>'Airstrip Maintenance Summary'</b> (table)."),
    sp(6),
    h2("6.4  Branch 4 — Airline Complaints"),
    p("Filter: event_type == <b>airline_complaint</b>."),
    note("This branch is fetched, filtered, and normalised "
         "(process_events_details → normalize_json_column → "
         "drop_column_prefix) exactly like the other three, but the "
         "pipeline <b>dead-ends there</b>: there is no map_columns, "
         "persist_df, draw_table, or widget-creation step downstream of the "
         "normalisation for airline complaints anywhere in the spec. "
         "<b>No file and no dashboard widget are produced for airline "
         "complaints</b> in the current version of this workflow. This is a "
         "real behavioural difference from earlier versions and is worth "
         "flagging explicitly to anyone expecting an airline-complaints "
         "output."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. SECTION 3 — LIVESTOCK REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Section 3 — Livestock Report"),
    hr(),
    p("Four livestock event types are filtered from <b>events_temporal</b> "
      "and each normalised using the common pattern (Section 4.3). All "
      "Livestock maps use the 3-layer map style (parcels + grazing zones + "
      "conservancy) described in Section 3.2 — the only maps in the workflow "
      "that include the grazing-zone layer."),
    sp(6),
    h2("7.1  Branch 1 — Mobile Boma Movements"),
    p("Filter: event_type == <b>mobile_boma_rep</b>"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_column_prefix."],
            ["4", "map_columns",
             "Retain id, date, event_type, geometry, Date of Relocation, "
             "Electric Boma Status, Mobile Boma Zone, Nature of the Site, "
             "Reason for relocation."],
            ["5", "summarize_df",
             "Group by date; count nunique(id) boma events."],
            ["6", "persist_df",
             "Save as <b>mobile_boma_movement_summary_table.csv</b>."],
            ["7", "draw_map",
             "Point map, coloured layer combined with the 3-layer livestock "
             "map style; persisted as <b>boma_movement_map.html/.png</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    p("Widget: <b>'Mobile Boma Movement Map'</b> (map)."),
    sp(6),
    h2("7.2  Branch 2 — Total Cattle Count"),
    p("Filter: event_type == <b>cattle_count</b>. No map produced."),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_column_prefix."],
            ["4", "map_columns",
             "Rename '# cattle in Zone 1 mobile boma' → zone_1, "
             "'# cattle in Zone 2/3 mobile boma' → zone_2_3, "
             "'# cattle in Zone 4' → zone_4."],
            ["5", "apply_arithmetic_operation_over_rows",
             "Sum zone_1 + zone_2_3 + zone_4 into a new <b>total</b> column "
             "(ecoscope_workflows_ext_mnc task)."],
            ["6", "persist_df",
             "Save as <b>total_cattle_count_summary_table.csv</b>."],
            ["7", "draw_table + persist_text",
             "Save the rendered HTML with an <b>explicit</b> filename "
             "<b>total_cattle_count_summary_table.html</b> "
             "(filename_suffix: null — unlike the Logistics branches, this "
             "one names its HTML output directly)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    p("Widget: <b>'Total Cattle Count Summary'</b> (table)."),
    sp(6),
    h2("7.3  Branch 3 — Livestock Predation"),
    p("Filter: event_type == <b>livestock_predation_rep</b>. This branch "
      "builds two genuinely different output tables that share an "
      "overlapping naming scheme — read carefully:"),
    make_table(
        [
            ["Output file", "Content", "Backs a widget?"],
            ["total_livestock_predation_summary_table.csv",
             "Daily nunique-id predation event counts. Columns: 'Date', "
             "'Livestock Predation Events'.",
             "No (CSV only)"],
            ["livestock_predation_summary_table.html",
             "The rendered HTML of that <b>same</b> daily-count table above "
             "(not a different dataset).",
             "Yes — 'Livestock Predation Summary'"],
            ["livestock_predation_summary_table.csv",
             "A <b>second, different</b> table: the detailed per-event "
             "records (Livestock Species, Suspected Predator, Total "
             "livestock affected), with nulls filled 'Unknown'.",
             "No (CSV only, no HTML/widget)"],
            ["livestock_predation_events.html/.png",
             "Point map of predation incidents, coloured by species "
             "(tab10 colormap).",
             "Yes — 'Livestock Predation Events Map'"],
        ],
        [4.5*cm, 6*cm, W - 10.5*cm],
    ),
    note("The daily-count CSV (total_livestock_predation_summary_table.csv) "
         "and the detailed per-event CSV (livestock_predation_summary_table.csv) "
         "have similar but distinct names and different columns entirely. "
         "The 'Livestock Predation Summary' dashboard widget is backed by the "
         "HTML of the <b>daily-count</b> table, not the detailed per-event "
         "table — the detailed CSV has no widget at all."),
    sp(6),
    h2("7.4  Branch 4 — Illegal Grazing"),
    p("Filter: event_type == <b>illegal_grazing_rep</b>. Only a map is "
      "produced — no summary CSV or table exists for this branch."),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_column_prefix."],
            ["4", "map_columns",
             "Retain date, event_type, geometry, Herd Zone, Landowner name, "
             "action taken."],
            ["5", "draw_map",
             "Point map on the 3-layer livestock map style; persisted as "
             "<b>illegal_grazing_map.html/.png</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    p("Widget: <b>'Illegal Grazing Events Map'</b> (map)."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. SECTION 4 — WILDLIFE REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Section 4 — Wildlife Report"),
    hr(),
    p("This section covers five wildlife incident types (fetched together as "
      "one branch) and eight wildlife sighting species (each its own branch). "
      "All Wildlife maps use the 2-layer map style (parcels + conservancy "
      "only) described in Section 3.2 — the grazing-zone layer used in "
      "Livestock maps is intentionally absent here."),
    sp(6),
    h2("8.1  Common wildlife sighting pattern"),
    p("Every one of the 8 sighting branches follows the same skeleton:"),
    make_table(
        [
            ["Step", "Detail"],
            ["1", "filter_df events_temporal by event_type"],
            ["2–4", "process_events_details → normalize_json_column → drop_column_prefix"],
            ["5", "map_columns to rename species-specific fields to snake_case"],
            ["6", "exclude_geom_outliers → drop_null_geometry"],
            ["7", "draw_map on the shared parcels + conservancy (2-layer) map style"],
        ],
        [1.5*cm, W - 1.5*cm],
    ),
    p("Branches differ in sophistication across three tiers, described in "
      "the branch list below (Section 8.2) and detailed further in "
      "Sections 8.3–8.4."),
    sp(6),
    h2("8.2  Sighting branches and daily count / summary CSV outputs"),
    make_table(
        [
            ["Species", "event_type value", "Tier"],
            ["Elephant",   "elephant_sighting_rep", "Full (herd composition + herd size)"],
            ["Buffalo",    "buffalo_sighting_rep",  "Full (herd composition + herd size)"],
            ["Lion",       "lion_sighting_rep",     "Mid (pride, map + summary)"],
            ["Leopard",    "leopardsightingrep",    "Mid — NOTE: event_type has no underscores"],
            ["Cheetah",    "cheetah_sighting_rep",  "Mid (map + summary)"],
            ["Giraffe",    "giraffe_sighting",      "Simplest — NOTE: no '_rep' suffix"],
            ["Rhino",      "rhino_sighting_rep",    "Simplest (map + summary)"],
            ["Hartebeest", "hartebeest_sighting",   "Simplest — NOTE: no '_rep' suffix"],
        ],
        [3*cm, 5*cm, W - 8*cm],
    ),
    note("Leopard's event_type is written verbatim as 'leopardsightingrep' "
         "(no underscores at all), while Giraffe and Hartebeest use "
         "'giraffe_sighting' / 'hartebeest_sighting' (underscored, but "
         "missing the '_rep' suffix that every other species carries). "
         "These are exact values from the spec, not typos to correct."),
    sp(6),
    h2("8.3  Individual / pride summary CSVs"),
    make_table(
        [
            ["Species", "Outputs (CSV + HTML)", "Widgets"],
            ["Elephant",
             "elephant_herd_size_bar_chart.html/.png, elephant_herd_types_map.html/.png, "
             "elephant_sightings_events.html/.png, overall_elephant_summary_table.csv + .html",
             "Elephant Herd Size Map, Elephant Herd Composition Map, "
             "Elephant Herd Size Distribution, Elephant Herd Composition Summary"],
            ["Buffalo",
             "buffalo_herd_size_bar_chart.html/.png, buffalo_herd_types_map.html/.png, "
             "buffalo_sightings_events.html/.png, overall_buffalo_summary_table.csv + .html",
             "Buffalo Herd Size Map, Buffalo Herd Composition Map, "
             "Buffalo Herd Size Distribution, Buffalo Herd Composition Summary"],
            ["Lion",
             "lion_pride_sightings_map.html/.png, overall_lion_summary_table.csv + .html",
             "Lion Sightings Map, Lion Sightings Summary"],
            ["Leopard",
             "leopard_sightings_map.html/.png, overall_leopard_summary_table.csv + .html",
             "Leopard Sightings Map, Leopard Sightings Summary"],
            ["Cheetah",
             "cheetah_sightings_map.html/.png, overall_cheetah_summary_table.csv + .html",
             "Cheetah Sightings Map, Cheetah Sightings Summary"],
            ["Giraffe",
             "giraffe_sightings_map.html/.png, overall_giraffe_summary_table.csv + .html",
             "Giraffe Sightings Map, Giraffe Sightings Summary"],
            ["Rhino",
             "rhino_sightings_map.html/.png, overall_rhino_summary_table.csv + .html",
             "Rhino Sightings Map, Rhino Sightings Summary"],
            ["Hartebeest",
             "hartebeest_sightings_map.html/.png, overall_hart_summary_table.csv + .html",
             "Hartebeest Sightings Map, Hartebeest Sightings Summary"],
        ],
        [2.2*cm, 8*cm, W - 10.2*cm],
    ),
    note("Hartebeest's summary CSV/HTML filenames use the abbreviation "
         "'hart' — <b>overall_hart_summary_table.csv/.html</b> — not "
         "'hartebeest'. This is inconsistent with the map filename "
         "(hartebeest_sightings_map.html) and with the widget titles "
         "('Hartebeest Sightings Map/Summary'), but is the exact filename "
         "produced by the spec."),
    sp(6),
    h2("8.4  Sighting maps"),
    p("Elephant and Buffalo (full tier): herd_composition is mapped to "
      "Bachelor / Female+Calf / Mixed / Unspecified and drives the colour of "
      "the herd-composition map (elephant_sightings_events / "
      "buffalo_sightings_events); herd_size is binned (equal-interval, "
      "k = 5) and drives a bar chart (*_herd_size_bar_chart) plus a separate "
      "clustered 'herd size' bubble map (*_herd_types_map)."),
    p("Lion, Leopard, Cheetah (mid tier): a single point map coloured by "
      "pride (Lion) or individuals present (Leopard, Cheetah), plus a single "
      "aggregate summary table — no bar chart or bubble map."),
    p("Giraffe, Rhino, Hartebeest (simplest tier): a fixed-colour point map "
      "with no attribute breakdown; the summary table is a plain daily "
      "observation count."),
    sp(6),
    h2("8.5  Elephant/buffalo herd-size map and bar chart"),
    make_table(
        [
            ["Output", "Detail"],
            ["Herd-size bar chart",
             "herd_size binned (equal-interval, k = 5) → draw_bar_chart → "
             "persist HTML → html_to_png. Files: elephant_herd_size_bar_chart / "
             "buffalo_herd_size_bar_chart (.html/.png)."],
            ["Herd-size bubble map",
             "A clustered scatterplot layer sized by herd_size, combined "
             "with the 2-layer conservancy+parcels map style → draw_map → "
             "persist HTML → html_to_png. Files: elephant_herd_types_map / "
             "buffalo_herd_types_map (.html/.png)."],
            ["Herd-composition map",
             "A separate point map coloured by herd_composition. Files: "
             "elephant_sightings_events / buffalo_sightings_events (.html/.png)."],
        ],
        [3.5*cm, W - 3.5*cm],
    ),
    sp(6),
    h2("8.6  Wildlife incidents"),
    p("Filter: event_type in {snare_rep, fire_rep, wildlife_injury_rep, "
      "wildlife_treatment_rep, wildlife_carcass_rep}. Raw records are "
      "persisted, a categorical summary and a daily-count table are built, "
      "and a point map coloured by event type is drawn using the "
      "<b>ecoscope_workflows_ext_big_life</b> draw_map task — functionally "
      "equivalent to the custom draw_map task used by Livestock, but a "
      "different implementation module."),
    make_table(
        [
            ["Output file", "Description", "Widget"],
            ["wildlife_events_recorded.csv",
             "Raw normalised wildlife incident records.", "None (CSV only)"],
            ["wildlife_incidents_summary_table.csv",
             "Categorical incident summary by event type.", "None (CSV only)"],
            ["wildlife_incidents_recorded_by_date.csv",
             "Daily incident counts.", "None (CSV only)"],
            ["wildlife_incidents_map.html/.png",
             "Point map of incident locations, coloured by event type.",
             "'Wildlife Incident Map'"],
        ],
        [5*cm, 6.5*cm, W - 11.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. SECTION 5 — PATROL REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Section 5 — Patrol Report"),
    hr(),
    p("The patrol section derives trajectory data from <b>patrol_info</b> "
      "events in events_temporal, then fetches full patrol records and GPS "
      "observations from EarthRanger. It produces event counts, a patrol "
      "purpose summary, three mode-specific coverage maps, an overall "
      "coverage map, per-mode and per-ranger effort summaries, and a "
      "conservancy patrol occupancy table. Section 9.1 below also covers the "
      "cross-section 'Events Overview' outputs, which sit alongside the "
      "patrol-specific pipeline but are not themselves patrol data."),
    sp(6),
    h2("9.1  Event counts (Events Overview)"),
    p("Before the patrol-specific pipeline, a cross-section events overview "
      "is built from events_temporal with <b>distancecountwildlife_rep</b>, "
      "<b>distancecountpatrol_rep</b>, and <b>airstrip_operations</b> "
      "excluded (exclude_row_values):"),
    make_table(
        [
            ["CSV filename", "Group-by", "Description"],
            ["total_events_recorded_by_date.csv",
             "date", "Unique event count per date"],
            ["total_events_recorded_by_type.csv",
             "date + event_type", "Unique event count per date per event type"],
        ],
        [5.5*cm, 3*cm, W - 8.5*cm],
    ),
    p("A line chart of total events per day is also drawn and saved as "
      "<b>total_events_recorded.html/.png</b>. Widget: 'Total Events "
      "Recorded' (plot)."),
    sp(6),
    h2("9.2  Patrol purpose summary"),
    p("Filter: events_temporal for event_type == <b>patrol_info</b>. "
      "Records are processed/normalised and the raw filtered records are "
      "persisted as <b>patrol_events.csv</b> (no widget). The events are "
      "then summarised by <b>patrol_purpose</b>:"),
    make_table(
        [
            ["Output file", "Description", "Widget"],
            ["patrol_events.csv",
             "Raw normalised patrol_info event records.", "None (CSV only)"],
            ["patrol_purpose_summary.csv",
             "Patrol counts summarised by patrol_purpose.", "None (CSV only)"],
            ["patrol_purpose_summary_table.html",
             "Rendered HTML of the purpose summary.",
             "'Patrol Purpose Summary'"],
        ],
        [5.5*cm, 6.5*cm, W - 12*cm],
    ),
    sp(6),
    h2("9.3  Patrol observations and relocations"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "explode_multiple_columns",
             "Explode patrol_id (and participant) lists into rows."],
            ["2", "get_patrol_values",
             "Fetch full patrol records from EarthRanger by patrol_id."],
            ["3", "get patrol observations",
             "Fetch GPS observations for each patrol."],
            ["4", "merge / explode participants",
             "Merge observations with patrol info; explode participants."],
            ["5", "process_relocations",
             "Convert observations to relocations."],
            ["6", "persist_df",
             "Save the raw, pre-mode-split relocation points as "
             "<b>patrol_relocations.geoparquet</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("9.4  Trajectory building"),
    p("Relocations are split by <b>transport_type</b> into Foot, Vehicle, "
      "and Motorbike sub-groups, each independently converted to "
      "trajectories with mode-specific segment filters. Foot patrols use "
      "much tighter speed/time thresholds than vehicle or motorbike "
      "patrols, reflecting the different realistic travel speeds:"),
    make_table(
        [
            ["Sub-group", "transport_type filter", "Segment filter characteristics"],
            ["Foot patrols",     "Foot",      "Tight speed/time thresholds appropriate to walking pace"],
            ["Vehicle patrols",  "Vehicle",   "Wider speed/time thresholds appropriate to vehicle travel"],
            ["Motorbike patrols","Motorbike", "Wider speed/time thresholds appropriate to motorbike travel"],
        ],
        [3.5*cm, 4*cm, W - 7.5*cm],
    ),
    sp(6),
    h2("9.5  Patrol effort CSVs"),
    make_table(
        [
            ["CSV filename", "Group-by", "Columns"],
            ["foot_patrol_efforts.csv",      "patrol_type_value",
             "no_of_patrols, distance_km, duration_hrs, average_speed"],
            ["vehicle_patrol_efforts.csv",   "patrol_type_value",
             "no_of_patrols, distance_km, duration_hrs, average_speed"],
            ["motorbike_patrol_efforts.csv", "patrol_type_value",
             "no_of_patrols, distance_km, duration_hrs, average_speed"],
            ["overall_patrol_efforts.csv",   "participants (i.e. per-ranger)",
             "number_of_patrols, distance_km, duration_hours (no average_speed "
             "column — a different shape from the three per-mode tables above)"],
        ],
        [5*cm, 4*cm, W - 9*cm],
    ),
    note("overall_patrol_efforts.csv is <b>not</b> simply the three per-mode "
         "tables concatenated — it re-summarises the combined trajectories "
         "grouped by <b>participants</b> (ranger), producing a per-ranger "
         "effort breakdown rather than a per-patrol-type one."),
    sp(6),
    h2("9.6  Patrol trajectory maps"),
    p("Each mode produces its own coverage grid and map: build a 1 km grid "
      "over the conservancy boundary, classify unique patrol visits per cell "
      "(equal-interval, k = 5), colour with RdYlGn, and render via draw_map:"),
    make_table(
        [
            ["Mode", "Effort CSV", "Map filename", "Widget"],
            ["Foot",      "foot_patrol_efforts.csv",
             "foot_patrol_map.html/.png", "Foot Patrol Coverage Map"],
            ["Vehicle",   "vehicle_patrol_efforts.csv",
             "vehicle_patrol_map.html/.png", "Vehicle Patrol Coverage Map"],
            ["Motorbike", "motorbike_patrol_efforts.csv",
             "motor_patrol_map.html/.png", "Motorbike Patrol Coverage Map"],
        ],
        [2.5*cm, 4.5*cm, 4.5*cm, W - 11.5*cm],
    ),
    note("The motorbike map's <b>filename</b> uses the abbreviation 'motor' "
         "— <b>motor_patrol_map.html/.png</b> — while its <b>widget title</b> "
         "reads 'Motorbike Patrol Coverage Map' in full. This filename/title "
         "mismatch is exact-as-specified, not an error to fix in this guide."),
    sp(6),
    h2("9.7  Overall patrol coverage map and occupancy"),
    p("Foot, vehicle, and motorbike trajectories are concatenated and a "
      "combined coverage grid/map is built the same way as the per-mode "
      "maps. This section produces two <b>distinct</b> kinds of output — a "
      "visual coverage map and a numeric occupancy table — which should not "
      "be conflated:"),
    make_table(
        [
            ["Output file", "Nature", "Widget"],
            ["overall_patrol_map.html/.png",
             "The overall coverage MAP (visual) — combined foot+vehicle+motor "
             "coverage grid rendered spatially. This is the only 'overall "
             "coverage map' output in the workflow.",
             "'Overall Patrol Coverage Map'"],
            ["patrol_trajectories.geoparquet",
             "Despite the task name ('Persist combined trajectories data') "
             "and the filename, this file actually persists the "
             "<b>reprojected overall coverage grid</b> (density cells), "
             "not raw trajectory line geometries. Confirmed against the "
             "spec: it is written from the same reprojected grid DataFrame "
             "used to build overall_patrol_map.",
             "None (file only)"],
            ["overall_patrol_efforts.csv + overall_patrol_efforts_table.html",
             "Per-ranger effort summary (see Section 9.5).",
             "'Overall Patrol Efforts'"],
            ["patrol_coverage.csv + patrol_coverage_table.html",
             "Conservancy occupancy percentage from compute_patrol_occupancy "
             "— a plain numeric TABLE, not a map.",
             "'Conservancy Patrol Occupancy'"],
        ],
        [5*cm, 7*cm, W - 12*cm],
    ),
    note("There is no separate 'patrol coverage map' distinct from a "
         "'patrol coverage table' the way earlier documentation implied. "
         "The visual coverage-map role is filled entirely by "
         "<b>overall_patrol_map.html</b>; patrol_coverage_table.html is a "
         "plain occupancy-percentage table widget with no spatial rendering "
         "at all."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. REPORT GENERATION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Report Generation"),
    hr(),
    p("The workflow concludes with two final-assembly tasks: a Word report "
      "and a results dashboard."),
    sp(6),
    h2("10.1  Word report"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task id",        "generate_overall_report"],
            ["Task ref",       "generate_mnc_report"],
            ["template_path",  "mara_north_event_template.docx, fetched by "
                                "fetch_mnc_template (Dropbox)"],
            ["output_dir",     "ECOSCOPE_WORKFLOWS_RESULTS"],
            ["generated_by",   "Ecoscope"],
            ["validate_images","true"],
            ["time_period",    "from time_range"],
            ["filename",       "overall_report.docx"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("Unlike the dashboard's gather_dashboard task, generate_overall_report's "
         "partial does <b>not</b> enumerate any explicit list of images, tables, "
         "or sections in spec.yaml. The order and content of the assembled "
         "document is driven entirely by the structure of the Word template "
         "itself (mara_north_event_template.docx) and whatever "
         "generate_mnc_report's implementation scans from output_dir at run "
         "time — it is <b>not</b> something declared or orderable in "
         "spec.yaml. This guide does not assert a section order for the "
         "docx because none is specified."),
    sp(6),
    h2("10.2  Dashboard"),
    p("Task id <b>mnc_events_dashboard</b>, task ref <b>gather_dashboard</b>, "
      "built from workflow_details, time_range, and groupers plus an "
      "explicit ordered <b>widgets:</b> list of 44 widgets, grouped (by "
      "spec comments) in this exact order:"),
    make_table(
        [
            ["Group", "Count", "Widgets"],
            ["Weather", "7",
             "Precipitation, Temperature, Wind Speed, Wind Gusts, Soil "
             "Temperature, Relative Humidity, Atmospheric Pressure"],
            ["Logistics", "3",
             "Balloon Landing Summary, Airstrip Operations Summary, "
             "Airstrip Maintenance Summary"],
            ["Livestock", "5",
             "Mobile Boma Movement Map, Livestock Predation Events Map, "
             "Illegal Grazing Events Map, Total Cattle Count Summary, "
             "Livestock Predation Summary"],
            ["Wildlife", "21",
             "Wildlife Incident Map; Elephant Herd Size Map / Herd "
             "Composition Map / Herd Size Distribution / Herd Composition "
             "Summary; Buffalo (same 4); Lion Sightings Map / Summary; "
             "Leopard Sightings Map / Summary; Cheetah Sightings Map / "
             "Summary; Giraffe Sightings Map / Summary; Hartebeest "
             "Sightings Map / Summary; Rhino Sightings Map / Summary"],
            ["Patrol", "8",
             "Foot / Vehicle / Motorbike / Overall Patrol Coverage Map, "
             "Total Events Recorded, Patrol Purpose Summary, Overall "
             "Patrol Efforts, Conservancy Patrol Occupancy"],
        ],
        [3*cm, 1.5*cm, W - 4.5*cm],
    ),
    note("No dashboard widget exists for: weather_summary_table, "
         "wildlife_events_recorded.csv / wildlife_incidents_summary_table.csv / "
         "wildlife_incidents_recorded_by_date.csv, "
         "total_events_recorded_by_date.csv / total_events_recorded_by_type.csv, "
         "patrol_events.csv, patrol_relocations.geoparquet, and "
         "patrol_trajectories.geoparquet — these persist as downloadable "
         "files only and never surface on the dashboard."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Output Files"),
    hr(),
    p("All outputs are written to <b>ECOSCOPE_WORKFLOWS_RESULTS</b>."),
    h2("11.1  Weather"),
    make_table(
        [
            ["File", "Description"],
            ["weather_summary_table.csv",
             "Daily per-station summary: precipitation (sum), temperature "
             "(mean), wind speed (mean), wind gusts (max), soil temperature "
             "(mean), relative humidity (mean), atmospheric pressure (mean)"],
            ["precipitation_readings_over_time.html/.png",
             "Precipitation line chart per weather station"],
            ["temperature_readings_over_time.html/.png",
             "Temperature line chart per weather station"],
            ["wind_speed_readings_over_time.html/.png",
             "Wind speed line chart"],
            ["wind_gusts_readings_over_time.html/.png",
             "Wind gusts line chart"],
            ["soil_temperature_readings_over_time.html/.png",
             "Soil temperature line chart"],
            ["relative_humidity_readings_over_time.html/.png",
             "Relative humidity line chart"],
            ["atmospheric_pressure_readings_over_time.html/.png",
             "Atmospheric pressure line chart"],
        ],
        [6.5*cm, W - 6.5*cm],
    ),
    sp(6),
    h2("11.2  Logistics"),
    make_table(
        [
            ["File", "Description"],
            ["balloon_landing_summary_table.csv (+ HTML)",
             "Balloon company, lodging, and passenger records"],
            ["airstrip_operations_summary_table.csv (+ HTML)",
             "Client counts per camp/lodge, pivoted by arrival/departure"],
            ["airstrip_maintenance_summary_table.csv (+ HTML)",
             "Dated log of airstrip maintenance activity types"],
            ["— (none)",
             "Airline complaints are fetched and normalised but produce no "
             "output file or widget (see Section 6.4)"],
        ],
        [6.5*cm, W - 6.5*cm],
    ),
    sp(6),
    h2("11.3  Livestock"),
    make_table(
        [
            ["File", "Description"],
            ["mobile_boma_movement_summary_table.csv",
             "Daily unique boma event count"],
            ["boma_movement_map.html/.png",
             "Mobile boma locations, 3-layer map (parcels + grazing zones + conservancy)"],
            ["total_cattle_count_summary_table.csv (+ HTML)",
             "Cattle counts per zone (zone_1, zone_2_3, zone_4) plus a "
             "computed total column"],
            ["total_livestock_predation_summary_table.csv",
             "Daily unique predation event count"],
            ["livestock_predation_summary_table.html",
             "Rendered HTML of the daily predation count table (see 7.3)"],
            ["livestock_predation_summary_table.csv",
             "Separate detailed per-event predation table (species, "
             "predator, total affected) — same filename stem as the HTML "
             "above but a different dataset (see 7.3)"],
            ["livestock_predation_events.html/.png",
             "Predation incident locations, coloured by species (tab10)"],
            ["illegal_grazing_map.html/.png",
             "Illegal grazing incidents, 3-layer map (no summary CSV/table exists)"],
        ],
        [6.5*cm, W - 6.5*cm],
    ),
    sp(6),
    h2("11.4  Wildlife"),
    make_table(
        [
            ["File", "Description"],
            ["wildlife_events_recorded.csv",
             "Raw wildlife incident records (snares, fires, carcasses, "
             "injuries, veterinary treatments)"],
            ["wildlife_incidents_summary_table.csv",
             "Incident counts by event type"],
            ["wildlife_incidents_recorded_by_date.csv",
             "Incident counts by date"],
            ["wildlife_incidents_map.html/.png",
             "Wildlife incident locations map, coloured by event type"],
            ["elephant_sightings_events.html/.png",
             "Elephant herd-composition sightings map"],
            ["elephant_herd_types_map.html/.png",
             "Elephant herd-size bubble map"],
            ["elephant_herd_size_bar_chart.html/.png",
             "Elephant herd-size distribution bar chart (5 bins)"],
            ["overall_elephant_summary_table.csv (+ HTML)",
             "Elephant sightings summary by herd type"],
            ["buffalo_sightings_events.html/.png",
             "Buffalo herd-composition sightings map"],
            ["buffalo_herd_types_map.html/.png",
             "Buffalo herd-size bubble map"],
            ["buffalo_herd_size_bar_chart.html/.png",
             "Buffalo herd-size distribution bar chart (5 bins)"],
            ["overall_buffalo_summary_table.csv (+ HTML)",
             "Buffalo sightings summary by herd type"],
            ["lion_pride_sightings_map.html/.png",
             "Lion sightings map, coloured by pride"],
            ["overall_lion_summary_table.csv (+ HTML)",
             "Lion sightings summary by pride"],
            ["leopard_sightings_map.html/.png",
             "Leopard sightings map, coloured by individuals present"],
            ["overall_leopard_summary_table.csv (+ HTML)",
             "Leopard sightings summary"],
            ["cheetah_sightings_map.html/.png",
             "Cheetah sightings map, coloured by individuals present"],
            ["overall_cheetah_summary_table.csv (+ HTML)",
             "Cheetah sightings summary"],
            ["giraffe_sightings_map.html/.png",
             "Giraffe sightings map (fixed colour)"],
            ["overall_giraffe_summary_table.csv (+ HTML)",
             "Giraffe daily sightings summary"],
            ["rhino_sightings_map.html/.png",
             "Rhino sightings map (fixed colour)"],
            ["overall_rhino_summary_table.csv (+ HTML)",
             "Rhino daily sightings summary"],
            ["hartebeest_sightings_map.html/.png",
             "Hartebeest sightings map (fixed colour)"],
            ["overall_hart_summary_table.csv (+ HTML)",
             "Hartebeest daily sightings summary — NOTE filename uses "
             "abbreviation 'hart', not 'hartebeest'"],
        ],
        [6.5*cm, W - 6.5*cm],
    ),
    sp(6),
    h2("11.5  Patrol"),
    make_table(
        [
            ["File", "Description"],
            ["patrol_events.csv",
             "Raw normalised patrol_info event records"],
            ["patrol_purpose_summary.csv (+ HTML)",
             "Patrol count and distance by purpose"],
            ["patrol_relocations.geoparquet",
             "Raw, pre-mode-split GPS relocations for all patrol types"],
            ["foot_patrol_efforts.csv",
             "Foot patrol metrics (patrols, distance, duration, avg speed) by patrol_type_value"],
            ["foot_patrol_map.html/.png",
             "Foot patrol coverage grid map (1 km cells, RdYlGn)"],
            ["vehicle_patrol_efforts.csv",
             "Vehicle patrol metrics by patrol_type_value"],
            ["vehicle_patrol_map.html/.png",
             "Vehicle patrol coverage grid map"],
            ["motorbike_patrol_efforts.csv",
             "Motorbike patrol metrics by patrol_type_value"],
            ["motor_patrol_map.html/.png",
             "Motorbike patrol coverage grid map — NOTE filename uses "
             "'motor', widget title says 'Motorbike'"],
            ["overall_patrol_map.html/.png",
             "Combined (foot + vehicle + motorbike) patrol coverage grid map"],
            ["patrol_trajectories.geoparquet",
             "NOTE: despite the name, this is the reprojected overall "
             "coverage GRID (density cells), not raw trajectory line "
             "geometries — see Section 9.7"],
            ["overall_patrol_efforts.csv (+ HTML)",
             "Per-ranger (participants) summary of patrols, distance, and duration"],
            ["patrol_coverage.csv (+ HTML)",
             "Conservancy patrol occupancy percentage — a numeric table, not a map"],
        ],
        [6.5*cm, W - 6.5*cm],
    ),
    sp(6),
    h2("11.6  Report"),
    make_table(
        [
            ["File", "Description"],
            ["mara_north_event_template.docx",
             "Word template downloaded from Dropbox (input, not an output)"],
            ["overall_report.docx",
             "Populated Word report; section order is template-driven, not "
             "declared in spec.yaml (see Section 10.1)"],
        ],
        [6.5*cm, W - 6.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 12. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("12. Workflow Execution Logic"),
    hr(),
    h2("12.1  Per-task skip conditions"),
    p("This workflow declares a global <b>task-instance-defaults</b> block "
      "applying the same skipif conditions to every task:"),
    make_table(
        [
            ["Condition", "Behaviour"],
            ["any_is_empty_df",
             "Skip this task if any input DataFrame is empty"],
            ["any_dependency_skipped",
             "Skip this task if any upstream dependency was skipped"],
        ],
        [5*cm, W - 5*cm],
    ),
    p("Most individual tasks additionally redeclare this same skipif block "
      "explicitly. <b>Widget-creation tasks</b> (e.g. create_table_widget_single_view, "
      "the map/plot widget builders) override the default with "
      "<b>skipif.conditions: [never]</b>, so a placeholder widget always "
      "renders on the dashboard even if the upstream branch that would feed "
      "it was skipped for lack of data."),
    note("Because skips propagate per-task rather than being suppressed "
         "globally, each section's branches skip independently. For example, "
         "if no balloon_landing events are returned, only the balloon branch "
         "skips; all other Logistics/Livestock/Wildlife/Patrol branches "
         "continue normally, and the corresponding widgets still render "
         "(empty) due to the [never] override."),
    sp(6),
    h2("12.2  Two independent data sources"),
    make_table(
        [
            ["Entry point", "Task", "Feeds"],
            ["Weather observations",
             "get_subjectgroup_observations (ER2ER - From GMMF)",
             "Section 1 — Weather only"],
            ["All event records",
             "get_events (event_types: [], fetch all)",
             "Sections 2–5 — Logistics, Livestock, Wildlife, Events "
             "Overview, Patrol (each applies its own downstream filter)"],
        ],
        [3.5*cm, 6*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("12.3  No mapvalues or fan-out"),
    p("This workflow processes all records as a single batch. There is no "
      "<b>mapvalues</b>, <b>split_groups</b>, or <b>zip_groupbykey</b> "
      "directive, and groupers is []; every task runs exactly once per "
      "workflow execution."),
    sp(6),
    h2("12.4  GeoJSON trajectories and URL rewriting"),
    p("Patrol trajectory / coverage maps that render vector overlays use a "
      "geospatial layer referencing an on-disk file. Before HTML-to-PNG "
      "conversion, a URL-rewriting step replaces the file:// reference in "
      "the rendered HTML with a locally-served path so the headless browser "
      "used for screenshotting can load the geometry."),
    sp(6),
    h2("12.5  HTML-to-PNG conversion settings"),
    p("Every HTML chart/map output in the workflow is converted to PNG via "
      "html_to_png, with settings tuned per output type — fast, low-wait "
      "conversion for simple charts, longer wait times for map renders that "
      "need basemap tiles and vector layers to finish loading before the "
      "screenshot is taken."),
    sp(6),
    h2("12.6  Known quirks (summary)"),
    p("The following naming/behaviour discrepancies were identified while "
      "auditing this spec and are called out individually in their "
      "respective sections; they are collected here for quick reference:"),
    bullet("<b>Airline complaints dead-end</b> (6.4): fetched and normalised "
           "but no file or widget is ever produced."),
    bullet("<b>Livestock predation dual naming</b> (7.3): "
           "livestock_predation_summary_table.html backs the daily-count "
           "widget, while the identically-stemmed "
           "livestock_predation_summary_table.csv is a completely different, "
           "detailed per-event dataset."),
    bullet("<b>Hartebeest 'hart' abbreviation</b> (8.3): "
           "overall_hart_summary_table.csv/.html, inconsistent with the map "
           "filename and widget titles which say 'Hartebeest' in full."),
    bullet("<b>Motorbike filename vs. widget title</b> (9.6): "
           "motor_patrol_map.html/.png backs the 'Motorbike Patrol Coverage "
           "Map' widget."),
    bullet("<b>patrol_trajectories.geoparquet content mismatch</b> (9.7): "
           "named and task-labelled as combined trajectories, but actually "
           "persists the reprojected overall coverage grid (density cells)."),
    bullet("<b>Non-underscored / short event_type values</b> (8.2): "
           "leopardsightingrep (no underscores), giraffe_sighting and "
           "hartebeest_sighting (no '_rep' suffix), unlike every other "
           "sighting/incident event_type in the spec."),
    bullet("<b>Report assembly order is template-driven</b> (10.1): "
           "unlike the dashboard, spec.yaml declares no explicit section/"
           "image list for the Word report — order comes entirely from "
           "mara_north_event_template.docx."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 13. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("13. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned in spec.yaml"],
            ["ecoscope-platform",                ">=2.15.0, <2.16.0"],
            ["ecoscope-workflows-ext-custom",     "0.1.0rc14.*"],
            ["ecoscope-workflows-ext-ste",        "0.0.0rc1.*"],
            ["ecoscope-workflows-ext-wwf-virunga","0.0.0rc9.*"],
            ["ecoscope-workflows-ext-big-life",   "1.0.1.*"],
            ["ecoscope-workflows-ext-mnc",        "1.0.3.*"],
            ["pydeck",                            "0.9.2"],
            ["opentelemetry-sdk",                 ">=1.20.0,<2.0.0"],
        ],
        [8*cm, W - 8*cm],
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")
