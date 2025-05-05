# Connecting Streamlit

In this article, we will walk through the process of building a dashboard using Streamlit. To make it more illustrative, we will create a dashboard that connects to the analytical database and monitors the real-time status of vehicles.

> This guide is part of the Private Telematics Lakehouse documentation suite and specifically covers connecting Power BI to your data warehouse. If you're still deciding which BI tool to use, refer to the [Selecting BI tools](https://squaregps.atlassian.net/wiki/spaces/DTP/pages/3247505491/Selecting+BI+tools) overview.

## Dashboard features

- Display total number of objects
- Visualize movement statuses (moving/stopped/parked)
- Visualize connection statuses (active/idle/offline)
- Detailed table with current status of all vehicles
- Filtering by vehicle type, group, movement status, and connection status
- Automatic data refresh every 5 minutes
- Toggle between light and dark themes

## Technical requirements

- Python 3.8+
- Internet access for database connection
- Minimum 2 GB RAM

## Installation and setup

### 1. Clone the repository

```bash
git clone https://github.com/SquareGPS/bi-intergrations.git
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

> Make sure you have Python 3.8 or higher installed. You can check the version with the command `python --version`.

### 3. Install dependencies

After activating the virtual environment, install all necessary libraries:

```bash
pip install -r requirements.txt
```

## Database connection

### 1. Create a configuration file

Create a `.env` file in the project's root directory:

```bash
DB_HOST=your_db_host
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_password
DB_PORT=5432
DB_SCHEMA=raw_business_data
```

#### Connection parameter reference

| Lakehouse Parameter | Streamlit Setting Location | Notes |
|---------------------|---------------------------|-------|
| Host | `DB_HOST` in `.env` file | The database server address provided in your welcome email |
| Port | `DB_PORT` in `.env` file | Default is 5432 for PostgreSQL |
| Database name | `DB_NAME` in `.env` file | Your assigned database name |
| Username | `DB_USER` in `.env` file | Your database username |
| Password | `DB_PASS` in `.env` file | Your secure database password |
| SSL mode | Connection string in Python code | Set to **require** in the connection string |
| Schema | `DB_SCHEMA` in `.env` file | Specify schema (**raw_business_data** or **raw_telematics_data**) |

### 2. Obtaining credentials

Request credentials for connecting to the demonstration database by contacting the administrator.

> The `.env` file should not be included in version control (GitHub) to ensure credentials security. The `.gitignore` file is already configured to exclude this file.

## Running the dashboard

After setting up the database connection, start the dashboard with the command:

```bash
streamlit run moving_status_dashboard.py
```

After launching, you'll see a message similar to:

```bash
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.5:8501
```

Open the specified URL in your browser. The dashboard will be available at [http://localhost:8501](http://localhost:8501) (or at the network URL if you want to open it from another device on the network).

## Project structure

```
├── moving_status_dashboard.py  # Main application file
├── style.css                  # Styles for improved appearance
├── requirements.txt           # Project dependencies
├── .env                       # Database connection settings (created by the user)
└── README.md                  # This guide
```

## Developing custom components

If you want to modify the dashboard or create new components:

### 1. Modifying the existing dashboard

Streamlit automatically reloads the application when you change the source code. Simply edit the `moving_status_dashboard.py` file and save your changes.

### 2. Adding new visualizations

To add new charts and diagrams, use libraries:

- Plotly: `import plotly.express as px` or `import plotly.graph_objects as go`
- Built-in Streamlit visualizations: `st.bar_chart()`, `st.line_chart()`, etc.

Example of adding a new chart:

```python
import plotly.express as px

# Get data from the database
df = ... # your database query

# Create chart
fig = px.pie(df, values='count', names='status', title='Vehicle Statuses')
st.plotly_chart(fig, use_container_width=True)
```

### 3. Debugging

For debugging, use

```python
# Output to Streamlit interface
st.write(f"Debug: {your_variable}")

# Output to console
print(f"Console debug: {your_variable}")

# Extended data output
st.json(data_dict)
st.dataframe(pandas_dataframe)
```

## Troubleshooting

### Database connection issues

- **Connection error:** Check the correctness of credentials in the `.env` file and database availability
- **SSL error:** Make sure your IP is on the allowlist for database access
- **Timeout errors:** Check your internet connection stability and firewall settings

### Dependency issues

**Error installing psycopg2-binary:**

- Windows: `pip install pipwin && pipwin install psycopg2-binary`
- Linux: `sudo apt install python3-dev libpq-dev`
- macOS: `brew install postgresql`

**Dependency conflicts:**

- Create a new virtual environment
- Install dependencies one by one, starting with streamlit

### Other issues

Here are some tricks that can help you fix common issues:

1. Update dependencies: `pip install -r requirements.txt --upgrade`
2. Check Python compatibility: `python --version` (should be 3.8+)
3. When changing code, include debug messages:
   ```python
   st.write(f"Debug: {your_variable}")
   ```
4. Streamlit cache errors: stop the application and run with the `--clear_cache` flag:
   ```bash
   streamlit run moving_status_dashboard.py --clear_cache
   ```

## Next steps

After successfully connecting Power BI to your Private Telematics Lakehouse instance, we recommend you to:

- Explore the available data schemas by reviewing the [Schema overview](https://squaregps.atlassian.net/wiki/spaces/DTP/pages/3208282180/Schema+overview) section to better understand the data structure and relationships.
- Start with simple queries focused on specific business entities before building complex dashboards - check our [Example queries](https://squaregps.atlassian.net/wiki/spaces/DTP/pages/3208282212/Example+queries) for reference.

### Support

For technical questions or requests for access to the demonstration database, please contact: [support@squaregps.com](mailto:support@squaregps.com)
