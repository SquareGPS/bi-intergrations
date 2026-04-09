# BI Integrations Project

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
```bash
cd streamlit
```

2. Создайте виртуальное окружение:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` с параметрами подключения к БД:
```env
DB_HOST=your_db_host
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_password
DB_PORT=5432
DB_SCHEMA=raw_business_data
```

5. Запустите дашборд:
```bash
streamlit run moving_status_dashboard.py
```

Дашборд будет доступен по адресу: http://localhost:8501

📖 **Подробная инструкция:** [streamlit/readme.md](streamlit/readme.md)

---

### 📊 Apache Superset

**Требования:**
- Docker и Docker Compose
- Минимум 4 GB RAM (рекомендуется 8 GB)
- 20 GB свободного места на диске
- Linux/Windows с WSL2/macOS

**Шаги:**

1. Установите Docker и Docker Compose (если еще не установлены)

2. Скачайте docker-compose файл:
```bash
curl -fL https://raw.githubusercontent.com/apache/superset/master/docker-compose-non-dev.yml -o docker-compose.yml
```

3. Запустите Superset:
```bash
docker-compose up -d
```

4. Создайте администратора:
```bash
docker-compose exec superset superset fab create-admin \
  --username admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@superset.com \
  --password admin
```

5. Инициализируйте базу данных:
```bash
docker-compose exec superset superset db upgrade
docker-compose exec superset superset init
```

6. Откройте Superset в браузере: http://localhost:8088

📖 **Подробная инструкция:** [SuperSet/readme.md](SuperSet/readme.md)

---

### 💼 Power BI

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

