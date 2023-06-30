# Project Documentation
This is the documentation for the project that utilizes the Dash framework to create a web application for data visualization and analysis. The project is built using Python and incorporates various libraries such as Dash, Plotly, and pandas.

# Table of Contents
Introduction
Installation
Usage
Features
Data Source
Dependencies
Introduction
The project aims to provide a user-friendly interface for visualizing and analyzing data using interactive charts and graphs. The web application allows users to explore different aspects of the data and gain insights from it. The project utilizes the Dash framework, which is a powerful tool for creating web applications with Python.

# Installation
To run the project locally, follow these steps:

Clone the repository:

bash
Copy code
git clone <repository-url>
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
python app.py
Open a web browser and navigate to http://localhost:8050 to access the web application.

# Usage
Once the application is running, you can use it to visualize and analyze the provided data. The application provides various charts and graphs to explore different aspects of the data. The user interface allows you to select specific parameters, such as stabilimento (facility), fascia_oraria (time slot), and anno (year), to filter and customize the displayed data.

# Features
The project includes the following features:

Number Cards Dataset: Displays the total energy consumption (consumi_kw_h) for each stabilimento (facility) and fascia_oraria (time slot).

Linebar Chart Dataset: Shows a bar chart that visualizes the energy consumption (consumi_kw_h) over time (date) for specific stabilimenti (facilities) and fascia_oraria (time slot).

Radar Weekdays Chart Dataset: Presents a line chart that represents the energy consumption (consumi_kw_h) for different stabilimenti (facilities) across different weekdays (giorno_sett) and hour groups (hour_group).

Radar Months Chart Dataset: Displays a line chart that shows the energy consumption (consumi_kw_h) for different stabilimenti (facilities) across different months (mese) and hour groups (hour_group).

Linebar Monthly Dataset: Provides a bar chart that visualizes the energy consumption (consumi_kw_h) for specific stabilimenti (facilities) over different months (mese) and fascia_oraria (time slot).

# Data Source
The data used in this project is fetched from a CSV file hosted on GitHub. The data contains hourly energy consumption records for different facilities and time slots. The CSV file is read into a pandas DataFrame for further processing and analysis.
