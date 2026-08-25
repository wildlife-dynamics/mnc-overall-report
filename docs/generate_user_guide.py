"""
Generate the MNC Overall Report User Guide as a PDF using ReportLab.
Run with: python3 generate_user_guide.py
Output: assets/MNC_Overall_Report_User_Guide.pdf
"""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, ListFlowable, ListItem,
)
from datetime import date

OUTPUT_FILE = Path(__file__).parent / "assets" / "MNC_Overall_Report_User_Guide.pdf"

# ── Colour palette (matches docs/index.html and the Technical Guide) ───────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ───────────────────────────────────────────────────────────────────
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
STEP     = _style("StepItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, leftIndent=14, firstLineIndent=-14, bulletIndent=0)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
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
def code_block(text):    return Paragraph(text, CODE)

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

def numbered_steps(items):
    return ListFlowable(
        [ListItem(Paragraph(text, STEP), leftIndent=14) for text in items],
        bulletType="1", start=1, leftIndent=14, bulletFontSize=9,
        bulletColor=GREEN_MID,
    )


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"MNC Overall Report — User Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    str(OUTPUT_FILE),
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
    p("User Guide", SUBTITLE),
    sp(4),
    p("Configuring and running the workflow that consolidates weather, logistics, "
      "livestock, wildlife, and patrol data from EarthRanger into a single monthly "
      "report and dashboard for Mara North Conservancy", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>mara_north_event_report</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Overview"),
    p("This guide walks you through configuring and running the MNC Overall Report "
      "workflow, which consolidates weather observations, logistics events, wildlife "
      "sightings, livestock events, and patrol data from EarthRanger into a single "
      "comprehensive monthly report and dashboard for Mara North Conservancy."),
    sp(4),
    p("The workflow delivers, for each run:"),
    bullet("<b>7 weather charts</b> (HTML + PNG) — daily precipitation, temperature, wind speed, wind gusts, soil temperature, relative humidity, and atmospheric pressure per station"),
    bullet("<b>Logistics tables</b> — balloon landing summary, airstrip operations (pivoted by arrival/departure), and airstrip maintenance log"),
    bullet("<b>Livestock reports</b> — mobile boma movement map and summary, cattle count table, livestock predation map and summary, illegal grazing map"),
    bullet("<b>Wildlife reports</b> — a wildlife incident map, and for all 8 species (elephant, buffalo, rhino, lion, leopard, cheetah, giraffe, hartebeest): a sightings map and summary table, with elephant and buffalo additionally getting a herd-composition map, herd-size bubble map, and herd-size bar chart"),
    bullet("<b>Events overview</b> — total events recorded by date and by type, with a line chart"),
    bullet("<b>Patrol reports</b> — foot, vehicle, motorbike, and overall patrol coverage maps, per-mode effort summaries, overall per-ranger effort, and conservancy patrol occupancy"),
    bullet("<b>Results dashboard</b> — all 44 map, chart, and table widgets assembled into a single dashboard view"),
    bullet("<b>1 Word report</b> (overall_report.docx) — generated from a Dropbox-hosted report template"),
    sp(8),
    hr(),
]

# ══════════════════════════════════════════════════════════════════════════════
# PREREQUISITES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Prerequisites"),
    p("Before running the workflow, ensure you have access to an <b>EarthRanger</b> "
      "instance with the following recorded for the analysis period:"),
    bullet("Weather station observations under the <font face='Courier'>ER2ER - From GMMF</font> subject group"),
    bullet("Logistics events: <font face='Courier'>balloon_landing</font>, <font face='Courier'>airstrip_operations</font>, <font face='Courier'>airstrip_maintenance</font>"),
    bullet("Livestock events: <font face='Courier'>mobile_boma_rep</font>, <font face='Courier'>cattle_count</font>, <font face='Courier'>livestock_predation_rep</font>, <font face='Courier'>illegal_grazing_rep</font>"),
    bullet("Wildlife incident events: <font face='Courier'>snare_rep</font>, <font face='Courier'>fire_rep</font>, <font face='Courier'>wildlife_injury_rep</font>, <font face='Courier'>wildlife_treatment_rep</font>, <font face='Courier'>wildlife_carcass_rep</font>"),
    bullet("Wildlife sighting events: <font face='Courier'>elephant_sighting_rep</font>, <font face='Courier'>buffalo_sighting_rep</font>, <font face='Courier'>rhino_sighting_rep</font>, <font face='Courier'>lion_sighting_rep</font>, <font face='Courier'>leopardsightingrep</font>, <font face='Courier'>cheetah_sighting_rep</font>, <font face='Courier'>giraffe_sighting</font>, <font face='Courier'>hartebeest_sighting</font>"),
    bullet("<font face='Courier'>patrol_info</font> events and associated patrol observations"),
    sp(4),
    p("You will also need network access to <b>Dropbox</b>, so the workflow can "
      "download the MNC conservancy boundary, parcels, and Word report template "
      "files at runtime."),
    sp(8),
    hr(),
]

# ══════════════════════════════════════════════════════════════════════════════
# STEP-BY-STEP CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Step-by-Step Configuration"),

    h2("Step 1 — Add the Workflow Template"),
    p("In the workflow runner, go to <b>Workflow Templates</b> and click "
      "<b>Add Workflow Template</b>. Paste the GitHub repository URL into the "
      "<b>Github Link</b> field, then click <b>Add Template</b>."),
    code_block("https://github.com/wildlife-dynamics/mnc-overall-report.git"),
    sp(6),

    h2("Step 2 — Configure the EarthRanger Connection"),
    p("Navigate to <b>Data Sources</b> and click <b>Connect</b>, then select "
      "<b>EarthRanger</b>. Fill in the connection form:"),
    make_table(
        [["Field", "Description"],
         ["Data Source Name", "A label to identify this connection (e.g. Mara North Conservancy)"],
         ["EarthRanger URL", "Your instance URL (e.g. your-site.pamdas.org)"],
         ["EarthRanger Username", "Your EarthRanger username"],
         ["EarthRanger Password", "Your EarthRanger password"]],
        col_widths=[4.5*cm, W-4.5*cm],
    ),
    sp(4),
    note("Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs."),
    p("Click <b>Connect</b> to save."),
    sp(6),

    h2("Step 3 — Select the Workflow"),
    p("After the template is added, it appears in the <b>Workflow Templates</b> "
      "list as <b>mnc-overall-report</b>. Click the card to open the workflow "
      "configuration form."),
    sp(6),

    h2("Step 4 — Configure Workflow Details, Time Range, and EarthRanger Connection"),
    p("The configuration form has three sections on a single page."),
    h3("Set workflow details"),
    make_table(
        [["Field", "Description"],
         ["Workflow Name", "A short name to identify this run"],
         ["Workflow Description", "Optional notes (e.g. reporting month or site)"]],
        col_widths=[4.5*cm, W-4.5*cm],
    ),
    sp(4),
    h3("Time range"),
    make_table(
        [["Field", "Description"],
         ["Timezone", "Select the local timezone (e.g. Africa/Nairobi UTC+03:00)"],
         ["Since", "Start date and time — all data from this point is fetched"],
         ["Until", "End date and time of the analysis window"]],
        col_widths=[4.5*cm, W-4.5*cm],
    ),
    sp(4),
    h3("Connect to ER"),
    p("Select the EarthRanger data source configured in Step 2 from the "
      "<b>Data Source</b> dropdown (e.g. Mara North Conservancy)."),
    p("Once all three sections are filled, click <b>Submit</b>."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# RUNNING THE WORKFLOW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Running the Workflow"),
    p("Once submitted, the runner will:"),
    numbered_steps([
        "Download the MNC community conservancy boundary and parcels files from Dropbox; repair "
        "invalid geometries; derive the conservancy AOI (grazing_zone == Conservancy), the "
        "non-conservancy grazing zones (coloured individually), and the Mara North Conservancy "
        "extent (used to compute the shared map zoom/centre); build reusable conservancy, "
        "grazing-zone, and parcels map layers.",

        "Fetch weather station observations from the <font face='Courier'>ER2ER - From GMMF</font> "
        "subject group; extract seven meteorological variables from each observation; compute daily "
        "per-station aggregates; draw one line chart per variable.",

        "Fetch all events once; split off balloon landing, airstrip operations, and airstrip "
        "maintenance events; clean and summarise each into a table.",

        "Split off mobile boma, cattle count, livestock predation, and illegal grazing events; "
        "generate maps and summary tables — livestock maps are the only ones that additionally show "
        "the grazing-zone layer.",

        "Split off wildlife incident events (snares, fires, carcasses, injuries, veterinary "
        "treatments); generate an incident map and summary tables.",

        "Split off each of the 8 wildlife species' sighting events; generate a sightings map and "
        "summary table for each; elephant and buffalo additionally get herd-composition "
        "classification, a herd-size bar chart, and a herd-size bubble map.",

        "Summarise all events by date and by type (excluding distance-count and "
        "airstrip-operations event types); draw a total-events line chart.",

        "Fetch patrol_info events and associated patrol observations; convert to relocations; "
        "split into Foot, Vehicle, and Motorbike branches and convert each to trajectories using "
        "mode-appropriate segment filters; build a coverage grid and map for each mode and for the "
        "combined (overall) dataset; compute per-mode and per-ranger effort summaries and "
        "conservancy patrol occupancy.",

        "Download the Word report template from Dropbox and assemble "
        "<font face='Courier'>overall_report.docx</font> from the outputs above.",

        "Assemble all 44 widgets into the <b>MNC Overall Report dashboard</b>.",

        "Save all outputs to the directory specified by "
        "<font face='Courier'>ECOSCOPE_WORKFLOWS_RESULTS</font>.",
    ]),
    sp(4),
    note("Every task is automatically skipped if its input data is empty or an upstream step was skipped, so a run with no events of a given type simply omits that branch's outputs rather than failing. Widget-creation steps are the exception — they always run so that a placeholder widget still appears on the dashboard even if the branch behind it was skipped."),
    sp(4),
    hr(),
]

# ══════════════════════════════════════════════════════════════════════════════
# OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Output Files"),
    p("All outputs are written to <font face='Courier'>$ECOSCOPE_WORKFLOWS_RESULTS/</font>."),

    h2("Weather"),
    make_table(
        [["File", "Description"],
         ["weather_summary_table.csv", "Daily per-station summary of all 7 weather variables"],
         ["precipitation_readings_over_time.html / .png", "Daily total precipitation"],
         ["temperature_readings_over_time.html / .png", "Daily mean surface air temperature"],
         ["wind_speed_readings_over_time.html / .png", "Daily mean wind speed"],
         ["wind_gusts_readings_over_time.html / .png", "Daily maximum wind gusts"],
         ["soil_temperature_readings_over_time.html / .png", "Daily mean soil temperature"],
         ["relative_humidity_readings_over_time.html / .png", "Daily mean relative humidity"],
         ["atmospheric_pressure_readings_over_time.html / .png", "Daily mean atmospheric pressure"]],
        col_widths=[7.5*cm, W-7.5*cm],
    ),
    sp(4),

    h2("Logistics"),
    make_table(
        [["File", "Description"],
         ["balloon_landing_summary_table.csv (+ HTML)", "Passenger records by balloon company and lodge"],
         ["airstrip_operations_summary_table.csv (+ HTML)", "Client counts pivoted by camp/lodge and arrival/departure"],
         ["airstrip_maintenance_summary_table.csv (+ HTML)", "Dated log of airstrip maintenance activities"]],
        col_widths=[7.5*cm, W-7.5*cm],
    ),
    sp(4),

    h2("Livestock"),
    make_table(
        [["File", "Description"],
         ["mobile_boma_movement_summary_table.csv", "Daily count of boma movement events"],
         ["boma_movement_map.html / .png", "Boma movement locations map"],
         ["total_cattle_count_summary_table.csv (+ HTML)", "Cattle counts by zone, with total"],
         ["total_livestock_predation_summary_table.csv", "Daily count of livestock predation events"],
         ["livestock_predation_summary_table.html", "Rendered HTML of the daily predation count table (dashboard widget)"],
         ["livestock_predation_summary_table.csv", "Detailed per-event predation table (species, predator, total affected)"],
         ["livestock_predation_events.html / .png", "Predation events map, coloured by species"],
         ["illegal_grazing_map.html / .png", "Illegal grazing locations map"]],
        col_widths=[7.5*cm, W-7.5*cm],
    ),
    sp(4),

    h2("Wildlife Incidents"),
    make_table(
        [["File", "Description"],
         ["wildlife_events_recorded.csv", "Raw wildlife incident records (snares, fires, carcasses, injuries, veterinary treatments)"],
         ["wildlife_incidents_summary_table.csv", "Pivot table of incidents by type"],
         ["wildlife_incidents_recorded_by_date.csv", "Daily count of unique incidents"],
         ["wildlife_incidents_map.html / .png", "Incident locations map, coloured by incident type"]],
        col_widths=[7.5*cm, W-7.5*cm],
    ),
    sp(4),

    h2("Wildlife Sightings"),
    make_table(
        [["File", "Description"],
         ["elephant_sightings_events.html / .png", "Elephant herd-composition sightings map"],
         ["elephant_herd_types_map.html / .png", "Elephant herd-size bubble map"],
         ["elephant_herd_size_bar_chart.html / .png", "Elephant herd-size distribution (5 bins)"],
         ["overall_elephant_summary_table.csv (+ HTML)", "Elephant sightings summary by herd type"],
         ["buffalo_sightings_events.html / .png", "Buffalo herd-composition sightings map"],
         ["buffalo_herd_types_map.html / .png", "Buffalo herd-size bubble map"],
         ["buffalo_herd_size_bar_chart.html / .png", "Buffalo herd-size distribution (5 bins)"],
         ["overall_buffalo_summary_table.csv (+ HTML)", "Buffalo sightings summary by herd type"],
         ["lion_pride_sightings_map.html / .png", "Lion sightings map, coloured by pride"],
         ["overall_lion_summary_table.csv (+ HTML)", "Lion sightings summary by pride"],
         ["leopard_sightings_map.html / .png", "Leopard sightings map, coloured by individuals present"],
         ["overall_leopard_summary_table.csv (+ HTML)", "Leopard sightings summary"],
         ["cheetah_sightings_map.html / .png", "Cheetah sightings map, coloured by individuals present"],
         ["overall_cheetah_summary_table.csv (+ HTML)", "Cheetah sightings summary"],
         ["giraffe_sightings_map.html / .png", "Giraffe sightings map"],
         ["overall_giraffe_summary_table.csv (+ HTML)", "Giraffe daily sightings summary"],
         ["rhino_sightings_map.html / .png", "Rhino sightings map"],
         ["overall_rhino_summary_table.csv (+ HTML)", "Rhino daily sightings summary"],
         ["hartebeest_sightings_map.html / .png", "Hartebeest sightings map"],
         ["overall_hart_summary_table.csv (+ HTML)", "Hartebeest daily sightings summary"]],
        col_widths=[7.5*cm, W-7.5*cm],
    ),
    sp(4),

    h2("Events Overview"),
    make_table(
        [["File", "Description"],
         ["total_events_recorded_by_date.csv", "All events recorded by date"],
         ["total_events_recorded_by_type.csv", "All events recorded by type"],
         ["total_events_recorded.html / .png", "All-events line chart"]],
        col_widths=[7.5*cm, W-7.5*cm],
    ),
    sp(4),

    h2("Patrols"),
    make_table(
        [["File", "Description"],
         ["patrol_events.csv", "Flattened patrol_info event details"],
         ["patrol_purpose_summary.csv (+ HTML)", "Patrol count by patrol purpose"],
         ["patrol_relocations.geoparquet", "Combined patrol observation dataset with patrol metadata"],
         ["foot_patrol_efforts.csv", "Foot patrol effort summary (count, distance, duration, speed)"],
         ["foot_patrol_map.html / .png", "Foot patrol coverage grid map"],
         ["vehicle_patrol_efforts.csv", "Vehicle patrol effort summary"],
         ["vehicle_patrol_map.html / .png", "Vehicle patrol coverage grid map"],
         ["motorbike_patrol_efforts.csv", "Motorbike patrol effort summary"],
         ["motor_patrol_map.html / .png", "Motorbike patrol coverage grid map"],
         ["overall_patrol_map.html / .png", "Combined (foot + vehicle + motorbike) patrol coverage grid map"],
         ["patrol_trajectories.geoparquet", "Reprojected overall patrol coverage grid"],
         ["overall_patrol_efforts.csv (+ HTML)", "Per-ranger summary of patrols, distance, and duration"],
         ["patrol_coverage.csv (+ HTML)", "Conservancy patrol occupancy percentage"]],
        col_widths=[7.5*cm, W-7.5*cm],
    ),
    sp(4),

    h2("Report"),
    make_table(
        [["File", "Description"],
         ["overall_report.docx", "Final Word report, assembled from the Dropbox-hosted template and all outputs above"]],
        col_widths=[7.5*cm, W-7.5*cm],
    ),
    sp(8),
    hr(),
]

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Dashboard"),
    p("The workflow run also produces the <b>MNC Overall Report dashboard</b>, "
      "viewable in the workflow runner, with 44 widgets:"),
    make_table(
        [["Group", "Widgets"],
         ["Weather (7)", "Precipitation, Temperature, Wind Speed, Wind Gusts, Soil Temperature, Relative Humidity, Atmospheric Pressure"],
         ["Logistics (3)", "Balloon Landing Summary, Airstrip Operations Summary, Airstrip Maintenance Summary"],
         ["Livestock (5)", "Mobile Boma Movement Map, Livestock Predation Events Map, Illegal Grazing Events Map, Total Cattle Count Summary, Livestock Predation Summary"],
         ["Wildlife (21)", "Wildlife Incident Map, Elephant Herd Size Map, Elephant Herd Composition Map, Elephant Herd Size Distribution, Elephant Herd Composition Summary, Buffalo Herd Size Map, Buffalo Herd Composition Map, Buffalo Herd Size Distribution, Buffalo Herd Composition Summary, Lion Sightings Map, Lion Sightings Summary, Leopard Sightings Map, Leopard Sightings Summary, Cheetah Sightings Map, Cheetah Sightings Summary, Giraffe Sightings Map, Giraffe Sightings Summary, Hartebeest Sightings Map, Hartebeest Sightings Summary, Rhino Sightings Map, Rhino Sightings Summary"],
         ["Patrol (8)", "Foot Patrol Coverage Map, Vehicle Patrol Coverage Map, Motorbike Patrol Coverage Map, Overall Patrol Coverage Map, Total Events Recorded, Patrol Purpose Summary, Overall Patrol Efforts, Conservancy Patrol Occupancy"]],
        col_widths=[3*cm, W-3*cm],
    ),
    sp(4),
    note("Each table widget is sortable and filterable in place; downloading directly from the widget is disabled — use the corresponding CSV output file for that."),
]

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Wrote {OUTPUT_FILE}")
