# Connecting Apache Superset

In this article, we will walk through the process of connecting Apache Superset to the analytical database. To make it more illustrative, we will also build a dashboard that connects to the analytical database and monitors the real-time status of vehicles, all using Apache Superset.

> **Note**: This guide is part of the Private Telematics Lakehouse documentation suite and covers connecting Apache Superset to your data warehouse. If you're still deciding which BI tool to use, refer to the [Selecting BI tools](https://docs.navixy.com/user-guide/connecting-apache-superset) overview.

## Dashboard features

- Display total number of objects
- Visualize vehicle movement statuses (moving/stopped/parked)
- Visualize connection statuses (active/idle/offline)
- Detailed table with current status of all vehicles
- Filtering by vehicle type, group, movement status, and connection status
- Data and report export capabilities
- Customizable notifications and alerts

## Technical requirements

- Docker and Docker Compose
- Minimum 4 GB RAM (8 GB recommended)
- 20 GB of free disk space
- Linux/Windows with WSL2/macOS
- Python 3.8+
- Internet access for database connection

## Installation and setup

### 1. Installation with Docker (recommended method)

1. Install Docker and Docker Compose by following the official documentation:
   - [Docker Installation](https://docs.docker.com/engine/install/)
   - [Docker Compose Installation](https://docs.docker.com/compose/install/)

2. Download the official docker-compose file:
```bash
curl -fL https://raw.githubusercontent.com/apache/superset/master/docker-compose-non-dev.yml -o docker-compose.yml
```

3. Start Superset:
```bash
docker-compose up -d
```

4. Create an administrator:
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
```

6. Load examples and initialize roles:
```bash
docker-compose exec superset superset init
```

### 2. Installation with pip (for development)

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # for Linux/macOS
# or
.\venv\Scripts\activate  # for Windows
```

2. Install Superset:
```bash
pip install apache-superset
```

3. Initialize the database:
```bash
superset db upgrade
```

4. Create an administrator:
```bash
export FLASK_APP=superset
superset fab create-admin
```

5. Load examples and initialize roles:
```bash
superset init
```

6. Start Superset:
```bash
superset run -p 8088 --with-threads --reload --debugger
```

## Database connection

1. Log in to Superset (default: http://localhost:8088)
2. Navigate to Data → Databases
3. Click "+" to add a new database
4. Fill in the connection parameters:
   - Database: PostgreSQL
   - SQLAlchemy URI: `postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}`
   - Display Name: Analytics Database
   - Extra: `{"engine_params": {"connect_args": {"sslmode": "require"}}}`
5. Click **Test Connection** to verify the connection
6. Save the settings

### Connection parameter reference

| Lakehouse Parameter | Apache Superset Setting Location | Notes |
|-------------------|--------------------------------|------------|
| Host | `DB_HOST` in SQLAlchemy URI | The database server address provided in your welcome email |
| Port | `DB_PORT` in SQLAlchemy URI | Default is 5432 for PostgreSQL |
| Database name | `DB_NAME` in SQLAlchemy URI | Your assigned database name |
| Username | `DB_USER` in SQLAlchemy URI | Your database username |
| Password | `DB_PASS` in SQLAlchemy URI | Your secure database password |
| SSL mode | `connect_args` in Extra parameters | Set to **require** in the Extra JSON configuration |
| Schema | Dataset configuration | Specify schema (`raw_business_data` or `raw_telematics_data`) in each dataset |

## Dashboard and chart import

1. Download the files from the repository:
```bash
git clone https://github.com/yourusername/superset-dashboard.git
```

2. In Superset, go to **Settings → Import/Export**
3. Import the files in the following order:
   - `datasets.json` - datasets
   - `charts.json` - charts
   - `dashboards.json` - dashboards
4. After importing, update the database connections in each dataset

## Project structure

```
├── datasets/                    # Folder with datasets
│   ├── vehicles.json           # Vehicle data dataset
│   └── tracking.json           # Tracking data dataset
├── charts/                      # Folder with charts
│   ├── status_charts.json      # Status charts
│   └── movement_charts.json    # Movement charts
├── dashboards/                  # Folder with dashboards
│   └── main_dashboard.json     # Main dashboard
├── documentation/               # Documentation
│   ├── data_model.md           # Data model description
│   └── setup_guide.md          # Setup guide
└── README.md                    # This guide
```

## Troubleshooting

### Database connection issues

- **Connection error:** Check the correctness of credentials and connection parameters
- **Firewall error:** Ensure your IP address is added to the allowlist
- **SSL issues:** Check SSL settings in connection parameters

### Performance issues

- **Slow visualization loading:**
  - Optimize SQL queries
  - Reduce the number of simultaneously displayed elements
  - Use result caching
- **High memory usage:**
  - Increase Docker container resources
  - Optimize database queries

### Other issues

Here are some tricks that can help you fix common issues:

1. Check Superset logs:
```bash
docker-compose logs superset
```

2. Restart containers:
```bash
docker-compose restart
```

3. Clear browser cache
4. Check Superset version and update if necessary

## Next steps

After successfully connecting Power BI to your Private Telematics Lakehouse instance, we recommend you to:

- Explore the available data schemas by reviewing the [Schema overview](https://squaregps.atlassian.net/wiki/spaces/DTP/pages/3208282180/Schema+overview) section to better understand the data structure and relationships.
- Start with simple queries focused on specific business entities before building complex dashboards - check our [Example queries](https://squaregps.atlassian.net/wiki/spaces/DTP/pages/3208282212/Example+queries) for reference.

### Support

For technical questions or requests for access to the demonstration database, please contact: support@squaregps.com