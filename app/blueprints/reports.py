from flask import Blueprint, render_template, request, make_response
import pdfkit  # For generating PDF reports
from app.db_connect import get_db

reports = Blueprint('reports', __name__)


@reports.route('/reports', methods=['GET', 'POST'])
def generate_report():
    db = get_db()
    cursor = db.cursor()

    # Fetch the data for the report
    cursor.execute('SELECT * FROM safety_observations')
    observations = cursor.fetchall()

    if request.method == 'POST':
        # Render the HTML template with the data
        rendered_html = render_template('report_template.html', observations=observations)

        # Path to wkhtmltopdf executable
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

        # Generate PDF
        pdf = pdfkit.from_string(rendered_html, False, configuration=config)

        # Prepare the response
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=report.pdf'
        return response

    return render_template('report.html', observations=observations)
