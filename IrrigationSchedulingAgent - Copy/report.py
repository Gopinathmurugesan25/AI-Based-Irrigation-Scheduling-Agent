import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# Define report folder path
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def fetch_report_data(farmer_id=None, report_type="Weekly"):
    """
    Fetches irrigation history data from database filtered by report type.
    report_type can be 'Daily', 'Weekly', or 'Monthly'.
    """
    from database import get_db_connection
    conn = get_db_connection()
    
    # Calculate starting date based on report_type
    today = datetime.now()
    if report_type == "Daily":
        start_date = today - timedelta(days=1)
    elif report_type == "Weekly":
        start_date = today - timedelta(days=7)
    elif report_type == "Monthly":
        start_date = today - timedelta(days=30)
    else:
        start_date = today - timedelta(days=7)
        
    start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
    
    if farmer_id:
        query = """
            SELECT h.date_time, f.name as farmer_name, f.crop_type, f.farm_size, f.farm_unit,
                   h.soil_moisture, h.temperature, h.rain_prob, h.status, h.water_liters, h.duration_minutes, h.reason
            FROM IrrigationHistory h
            JOIN Farmers f ON h.farmer_id = f.id
            WHERE h.farmer_id = ? AND h.date_time >= ?
            ORDER BY h.date_time DESC
        """
        df = pd.read_sql_query(query, conn, params=(farmer_id, start_date_str))
    else:
        query = """
            SELECT h.date_time, f.name as farmer_name, f.crop_type, f.farm_size, f.farm_unit,
                   h.soil_moisture, h.temperature, h.rain_prob, h.status, h.water_liters, h.duration_minutes, h.reason
            FROM IrrigationHistory h
            JOIN Farmers f ON h.farmer_id = f.id
            WHERE h.date_time >= ?
            ORDER BY h.date_time DESC
        """
        df = pd.read_sql_query(query, conn, params=(start_date_str,))
        
    conn.close()
    return df

def generate_pdf_report(farmer_id=None, farmer_name="All Farmers", report_type="Weekly"):
    """
    Generates a beautifully styled agricultural PDF report and saves it to disk.
    Returns the absolute file path of the generated PDF.
    """
    df = fetch_report_data(farmer_id, report_type)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    f_name_clean = farmer_name.replace(" ", "_").lower()
    filename = f"{report_type.lower()}_report_{f_name_clean}_{timestamp}.pdf"
    file_path = os.path.join(REPORTS_DIR, filename)
    
    # Establish document layout
    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Define custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor('#1B5E20'), # Deep Green
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor('#5D4037'), # Soil Brown
        spaceAfter=10
    )
    
    header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.white
    )
    
    body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#212121')
    )
    
    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#2E7D32'),
        spaceBefore=15,
        spaceAfter=8
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Irrigation Scheduling Agent", title_style))
    story.append(Paragraph(f"{report_type} Irrigation & Water Usage Report", subtitle_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Target: {farmer_name}", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Summary Cards Table
    total_water = df['water_liters'].sum() if not df.empty else 0
    total_irrigations = df[df['status'] == 'YES'].shape[0] if not df.empty else 0
    total_events = df.shape[0] if not df.empty else 0
    
    summary_data = [
        [
            Paragraph("<b>Total Log Entries</b>", styles['Normal']),
            Paragraph("<b>Irrigation Triggers (YES)</b>", styles['Normal']),
            Paragraph("<b>Total Water Used (Liters)</b>", styles['Normal'])
        ],
        [
            Paragraph(f"{total_events}", styles['Normal']),
            Paragraph(f"{total_irrigations}", styles['Normal']),
            Paragraph(f"{total_water:,.0f} L", styles['Normal'])
        ]
    ]
    
    summary_table = Table(summary_data, colWidths=[2.3*inch, 2.3*inch, 2.3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8F5E9')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#C8E6C9')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#C8E6C9')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(Paragraph("Key Highlights", section_title))
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # Data Table
    story.append(Paragraph("Detailed Log History", section_title))
    
    if df.empty:
        story.append(Paragraph("No records found for the selected period.", styles['Italic']))
    else:
        # Construct Table
        table_content = [[
            Paragraph("Date/Time", header_style),
            Paragraph("Farmer Profile", header_style),
            Paragraph("Crop", header_style),
            Paragraph("Moisture", header_style),
            Paragraph("Rain Prob", header_style),
            Paragraph("Water (L)", header_style),
            Paragraph("Duration", header_style),
        ]]
        
        for idx, row in df.iterrows():
            date_formatted = datetime.strptime(row['date_time'], "%Y-%m-%d %H:%M:%S").strftime("%m/%d %H:%M")
            unit_str = row.get('farm_unit', 'Acres')
            table_content.append([
                Paragraph(date_formatted, body_style),
                Paragraph(f"<b>{row['farmer_name']}</b><br/><font size='7' color='#616161'>{row['farm_size']} {unit_str}</font>", body_style),
                Paragraph(row['crop_type'], body_style),
                Paragraph(f"{row['soil_moisture']}%", body_style),
                Paragraph(f"{row['rain_prob']}%", body_style),
                Paragraph(f"{row['water_liters']:.0f}", body_style),
                Paragraph(f"{row['duration_minutes']}m" if row['status']=='YES' else "0m", body_style),
            ])
            
        history_table = Table(table_content, colWidths=[1.1*inch, 1.2*inch, 1.0*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch])
        history_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(history_table)
        
    doc.build(story)
    
    # Save the report details in the Reports database table
    try:
        from database import log_report
        title = f"{report_type} Report - {farmer_name}"
        desc = f"Generated report for {farmer_name} showing summary of {total_events} events and {total_water} Liters."
        log_report(title, desc, report_type, file_path)
    except Exception as e:
        print("Could not log PDF generation to database table:", str(e))
        
    return file_path

if __name__ == "__main__":
    # Test generation
    path = generate_pdf_report(farmer_id=None, farmer_name="All Farmers", report_type="Weekly")
    print("Test PDF generated at:", path)
