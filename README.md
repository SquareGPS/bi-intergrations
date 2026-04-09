# BI Integrations Project

This project contains examples of integrating various BI tools with an analytical database for real-time vehicle status monitoring.

## Project Structure

The project consists of three main components:

- **Streamlit** - Python-based web dashboard
- **Apache Superset** - BI platform with dashboards
- **Power BI** - dashboard for Microsoft Power BI Desktop

## Quick Start

### 🚀 Streamlit (Easiest Option)

**Requirements:**
- Python 3.8+
- Internet access to connect to the database

**Steps:**

1. Navigate to the streamlit folder:
```bash
cd streamlit
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with database connection parameters:
```env
DB_HOST=your_db_host
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_password
DB_PORT=5432
DB_SCHEMA=raw_business_data
```

5. Run the dashboard:
```bash
streamlit run moving_status_dashboard.py
```

The dashboard will be available at: http://localhost:8501

📖 **Detailed instructions:** [streamlit/readme.md](streamlit/readme.md)

---

### 📊 Apache Superset

**Requirements:**
- Docker and Docker Compose
- At least 4 GB RAM (8 GB recommended)
- 20 GB free disk space
- Linux / Windows with WSL2 / macOS

**Steps:**

1. Install Docker and Docker Compose (if not already installed)

2. Download the docker-compose file:
```bash
curl -fL https://raw.githubusercontent.com/apache/superset/master/docker-compose-non-dev.yml -o docker-compose.yml
```

3. Start Superset:
```bash
docker-compose up -d
```

4. Create an admin user:
```bash
docker-compose exec superset superset fab create-admin \
  --username admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@superset.com \
  --password admin
```

5. Initialize the database:
```bash
docker-compose exec superset superset db upgrade
docker-compose exec superset superset init
```

6. Open Superset in your browser: http://localhost:8088

📖 **Detailed instructions:** [SuperSet/readme.md](SuperSet/readme.md)

---

### 💼 Power BI

**Requirements:**
- Windows 10/11 or Windows Server 2016+
- Microsoft Power BI Desktop
- At least 4 GB RAM (8 GB recommended)

**Steps:**

1. Install Power BI Desktop from the official Microsoft website

2. Open the file `power_bi/moving_status_dashboard.pbix`

3. Update the database connection parameters via **Transform data → Edit parameters**

4. Click **Refresh** to reload the data

📖 **Detailed instructions:** [power_bi/readme.md](power_bi/readme.md)

---

## Obtaining Database Credentials

To connect to the demo database, contact the administrator:
- Email: support@squaregps.com

## Additional Resources

- [Schema overview](https://squaregps.atlassian.net/wiki/spaces/DTP/pages/3208282180/Schema+overview) - data schema overview
- [Example queries](https://squaregps.atlassian.net/wiki/spaces/DTP/pages/3208282212/Example+queries) - example SQL queries

## Support

For technical questions, contact: support@squaregps.com

