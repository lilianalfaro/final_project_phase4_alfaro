# Safety Observations Management System

This application helps manage safety observations, actions, and reports for Fouts Bros Inc. It allows users to record safety observations, filter and update them, generate PDF reports, and view a dashboard of key metrics.

## Novel Features
- **Dynamic Dropdowns**: The operations and subcategories dropdowns update based on user selections.
- **PDF Reports**: Generate PDF reports with company branding.
- **Dashboard**: View aggregated metrics and charts on the Dashboard page.

I am developed this web application during my internship that is specifically designed for managing safety observations. This application features an electronic safety observation form that replaces traditional paper-based reporting, ensuring standardized data collection and streamlined workflows. By storing all submissions in a centralized database, the system facilitates easy retrieval of records, enabling detailed trend analysis and data-driven decision-making. Beyond basic form submission and storage, the application includes dynamic filters, real-time dashboards, and PDF report generation with company branding. Users can sort and filter observations by commodity type, category, and severity, while operations and subcategories automatically adapt based on user selections, providing a tailored experience. These enhancements improve efficiency, support proactive safety measures, ensure compliance, and foster a safer work environment.


**Usage Instructions**  
Walk through basic operations: how to add a safety observation, how to generate a report, etc.
```markdown
Usage

- **Add a Safety Observation**: On the Safety Observations page, click "Add New Observation", fill in the details, and submit.
- **Filter Observations**: Use the dropdowns to filter by commodity, category, etc. The operations and subcategories dropdowns will update dynamically.
- **Add/Update Actions**: On the Actions page, you can add a new action or click "Edit" to open a modal and update an existing action.
- **Generate Report**: Go to the Reports page, apply any filters, and click "Generate Report" to view or download the PDF. The PDF will include logos at the top and a footer at the bottom.
- **Dashboard**: Check the Dashboard page to view charts and metrics summarizing your data.


Credits
- Developed by Lilian Alfaro.
- Uses Flask, Bootstrap, pdfkit, and MySQL.
