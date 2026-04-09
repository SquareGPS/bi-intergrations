# BI Integrations Project

<<<<<<< HEAD
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
=======
Проект содержит примеры интеграции различных BI-инструментов с аналитической базой данных для мониторинга статусов транспортных средств в реальном времени.

## Структура проекта

Проект состоит из трех основных компонентов:

- **Streamlit** - веб-дашборд на Python
- **Apache Superset** - BI-платформа с дашбордами
- **Power BI** - дашборд для Microsoft Power BI Desktop

## Быстрый старт

### 🚀 Streamlit (Самый простой способ)

**Требования:**
- Python 3.8+
- Интернет-доступ для подключения к БД

**Шаги:**

1. Перейдите в папку streamlit:
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd
```bash
cd streamlit
```

<<<<<<< HEAD
2. Create a virtual environment:
=======
2. Создайте виртуальное окружение:
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

<<<<<<< HEAD
3. Install dependencies:
=======
3. Установите зависимости:
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd
```bash
pip install -r requirements.txt
```

<<<<<<< HEAD
4. Create a `.env` file with database connection parameters:
=======
4. Создайте файл `.env` с параметрами подключения к БД:
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd
```env
DB_HOST=your_db_host
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_password
DB_PORT=5432
DB_SCHEMA=raw_business_data
```

<<<<<<< HEAD
5. Run the dashboard:
=======
5. Запустите дашборд:
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd
```bash
streamlit run moving_status_dashboard.py
```

<<<<<<< HEAD
The dashboard will be available at: http://localhost:8501

📖 **Detailed instructions:** [streamlit/readme.md](streamlit/readme.md)
=======
Дашборд будет доступен по адресу: http://localhost:8501

📖 **Подробная инструкция:** [streamlit/readme.md](streamlit/readme.md)
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd

---

### 📊 Apache Superset

<<<<<<< HEAD
**Requirements:**
- Docker and Docker Compose
- At least 4 GB RAM (8 GB recommended)
- 20 GB free disk space
- Linux / Windows with WSL2 / macOS

**Steps:**

1. Install Docker and Docker Compose (if not already installed)

2. Download the docker-compose file:
=======
**Требования:**
- Docker и Docker Compose
- Минимум 4 GB RAM (рекомендуется 8 GB)
- 20 GB свободного места на диске
- Linux/Windows с WSL2/macOS

**Шаги:**

1. Установите Docker и Docker Compose (если еще не установлены)

2. Скачайте docker-compose файл:
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd
```bash
curl -fL https://raw.githubusercontent.com/apache/superset/master/docker-compose-non-dev.yml -o docker-compose.yml
```

<<<<<<< HEAD
3. Start Superset:
=======
3. Запустите Superset:
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd
```bash
docker-compose up -d
```

<<<<<<< HEAD
4. Create an admin user:
=======
4. Создайте администратора:
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd
```bash
docker-compose exec superset superset fab create-admin \
  --username admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@superset.com \
  --password admin
```

<<<<<<< HEAD
5. Initialize the database:
=======
5. Инициализируйте базу данных:
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd
```bash
docker-compose exec superset superset db upgrade
docker-compose exec superset superset init
```

<<<<<<< HEAD
6. Open Superset in your browser: http://localhost:8088

📖 **Detailed instructions:** [SuperSet/readme.md](SuperSet/readme.md)
=======
6. Откройте Superset в браузере: http://localhost:8088

📖 **Подробная инструкция:** [SuperSet/readme.md](SuperSet/readme.md)
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd

---

### 💼 Power BI

<<<<<<< HEAD
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
=======
**Требования:**
- Windows 10/11 или Windows Server 2016+
- Microsoft Power BI Desktop
- Минимум 4 GB RAM (рекомендуется 8 GB)

**Шаги:**

1. Установите Power BI Desktop с официального сайта Microsoft

2. Откройте файл `power_bi/moving_status_dashboard.pbix`

3. Обновите параметры подключения к БД в меню **Transform data → Edit parameters**

4. Нажмите **Refresh** для обновления данных

📖 **Подробная инструкция:** [power_bi/readme.md](power_bi/readme.md)

---

## Получение учетных данных для БД

Для подключения к демонстрационной базе данных обратитесь к администратору:
- Email: support@squaregps.com

## Дополнительные ресурсы

- [Schema overview](https://squaregps.atlassian.net/wiki/spaces/DTP/pages/3208282180/Schema+overview) - обзор структуры данных
- [Example queries](https://squaregps.atlassian.net/wiki/spaces/DTP/pages/3208282212/Example+queries) - примеры запросов

## Поддержка

По техническим вопросам обращайтесь: support@squaregps.com
>>>>>>> 2899c648644db4a2daa143896efb9b345234eccd

