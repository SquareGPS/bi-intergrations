# Driving Score Dashboard

- **File:** `12-driver-performance-dashboard-schema.json`
- **UID:** `driving-score-dashboard`
- **Default period:** `now-1d → now`

Шаблон из `Driver performance Dashboard-schema.json` (в Grafana title — **Driving Score Dashboard**): оценка стиля вождения по телематике и связям с объектами/ТС в **`raw_business_data`**.

При доработке панелей события можно обогащать через **`processed_common_data.event_description`**, контекст устройства — через **`processed_common_data.device_settings`**.

---

## Слой данных (после рефакторинга клиентской БД)

| Изменение | Суть |
|-----------|------|
| Схема обработки | **`processed_common_data`** вместо `business_data` |
| Поездки | Таблица **`trips`**, поля **`trip_*`** |
| Справочники / сырые объекты | **`raw_business_data`**, телематика — **`raw_telematics_data`** |
| События | **`processed_common_data.event_description`** |
| Настройки устройств | **`processed_common_data.device_settings`** |
| Датчики по часам | **`processed_common_data.sensors_data_by_hours`**, колонка **`value_title`** |

Инфраструктура SQL: `19_trips.sql` / `20_generate_trips.sql` вместо `18_tracks.sql` / `20_generate_tracks.sql`; переименован `02_update_description_parameters.sql`.
