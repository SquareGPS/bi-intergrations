# Behavior Impact Dashboard

- **File:** `13-behavior-impact-dashboard-schema.json`
- **UID:** `behavior-impact-dashboard`
- **Default period:** `now-7d → now`

## Goal of the Dashboard

Analyze driver behavior impact on fleet operations without fuel metrics. The dashboard quantifies idling, aggressive driving, high-speed trips, and high RPM events, then highlights week-over-week trends and compares drivers on shared routes.

It helps to:
- Track four key behavior types: idling (≥5 min), aggressive driving, high speed, high RPM (>5000)
- Identify units with the worst week-over-week behavior increase
- Compare drivers on the same routes to isolate behavior-related risk
- Prioritize coaching and corrective action

---

## Why This Dashboard is Important

### Fleet Efficiency
- Excessive idling wastes fuel and increases engine wear
- High RPM operation shortens component life

### Driver Safety
- Aggressive driving (harsh braking/acceleration) is a leading crash indicator
- Speeding above vehicle limits significantly increases accident severity

### Accountability
- Route-based comparison removes route difficulty as an excuse — same route, different behavior scores
- Week-over-week trends catch deteriorating habits early

### Cost Control
- Behavior events directly correlate with maintenance costs
- Identifying top offenders enables targeted intervention

---

## Target Audience

### Fleet Managers
- Weekly behavior review and trend monitoring

### Safety Officers
- Prioritize coaching based on behavior impact scores

### HR / Driver Managers
- Data-driven KPIs for performance reviews

### Operations Directors
- High-level fleet behavior health overview

---

## Dashboard Elements

### 1. KPI Summary

| Panel | Type | Description |
|-------|------|-------------|
| Idling Events (7d) | KPI | Events with `event_type = 'idle over 5 min'` from `driver_performance_events` |
| Aggressive Driving Events (7d) | KPI | All `driver_performance_events` excluding idle, rpm exceeded, and overspeeding |
| High Speed Trips (7d) | KPI | Trips where max speed exceeds vehicle limit (default 70 km/h) from `trips` |
| High RPM > 5000 Events (7d) | KPI | Events with `event_type = 'rpm exceeded'` from `driver_performance_events` |

---

### 2. Behavior Distribution

| Panel | Type | Description |
|-------|------|-------------|
| Top Behaviors Impacting Fleet (7d) | Pie (donut) | Proportional breakdown: Idling ≥5 min, Aggressive Driving, High Speed Trips |

---

### 3. Week-over-Week Comparisons

| Panel | Type | Description |
|-------|------|-------------|
| Top Units: Idling vs Previous Week | Bar chart | Top 15 vehicles by idling increase (current vs previous week) |
| Top Units: Aggressive Driving vs Previous Week | Bar chart | Top 15 vehicles by aggressive driving increase |
| Top Units: High Speed vs Previous Week | Bar chart | Top 15 vehicles by high-speed trips increase |
| Top Units: High RPM > 5000 vs Previous Week | Bar chart | Top 15 vehicles by RPM events increase |

---

### 4. Route-Based Driver Comparison

| Panel | Type | Description |
|-------|------|-------------|
| Route-Based Driver Impact (30d) | Table | Compares drivers on the same route: trips, distance, behavior points, points per 100 km, route rank (top 3 per route) |

---

## Logic Behind Calculations

### Единый источник поведенческих событий
Все метрики поведения (idling, aggressive, RPM) теперь берутся из одной таблицы `processed_common_data.driver_performance_events`, фильтруя по `event_type`. Прямые запросы к `raw_telematics_data.states`/`inputs` и `raw_business_data.sensor_description` больше не используются.

### Idling Events
Фильтр: `event_type = 'idle over 5 min'` из `processed_common_data.driver_performance_events`.

### Aggressive Driving
Все события из `driver_performance_events`, исключая `idle over 5 min`, `rpm exceeded` и `overspeeding`. Включает: braking, acceleration, turns, lane changes и другие.

### High Speed
Trips from `processed_common_data.trips` where `max_speed` exceeds the vehicle-specific limit from `raw_business_data.vehicles.max_speed` (default fallback: 70 km/h).

### High RPM
Фильтр: `event_type = 'rpm exceeded'` из `processed_common_data.driver_performance_events`.

### Week-over-Week
Current 7-day window vs previous 7-day window (total 14 days). Only units where current week count > previous week count are shown, sorted by the largest absolute increase. WoW-панели для idling, aggressive, RPM также работают через `driver_performance_events`.

### Route-Based Impact
Routes are identified by start/end zone pairs from `processed_common_data.trips`. Behavior points are weighted by `event_type`:
- `Driver performance acceleration/braking (and turn)` → **3.0** points
- `idle over 5 min`, `rpm exceeded` → **1.0** point
- All other event types → **2.0** points

Points per 100 km normalizes for distance. Minimum thresholds: ≥2 trips, ≥5 km total. Top 3 drivers per route shown.

---

## Слой данных

### Используемые таблицы

| Таблица | Назначение |
|---------|------------|
| `processed_common_data.driver_performance_events` | Все поведенческие события (idle, aggressive, RPM, overspeeding) |
| `processed_common_data.trips` | Поездки — для high speed и route-based impact |
| `raw_business_data.objects` | Справочник объектов (label, device_id) |
| `raw_business_data.vehicles` | Лимиты скорости (`max_speed`) |
| `raw_business_data.employees` | Привязка водителей к объектам |

### Рефакторинг клиентской БД

| Изменение | Суть |
|-----------|------|
| Схема обработки | **`processed_common_data`** вместо `business_data` |
| Поездки | Таблица **`trips`**, поля **`trip_*`** (`trip_start_time`, `trip_distance_meters`, …) |
| Справочники / сырые объекты | **`raw_business_data`**, телематика — **`raw_telematics_data`** |
| События | Для подписей к кодам: **`processed_common_data.event_description`** |
| Настройки устройств | **`processed_common_data.device_settings`** (ключ–значение при полной синхронизации) |
| Датчики по часам | **`processed_common_data.sensors_data_by_hours`**, колонка **`value_title`** — подпись значения с клиента |

Инфраструктура SQL: `19_trips.sql` / `20_generate_trips.sql` вместо `18_tracks.sql` / `20_generate_tracks.sql`; переименован `02_update_description_parameters.sql`.
