# HW Status Dashboard

- **File:** `11-hw-status-dashboard-schema.json`
- **UID:** `hw-status-dashboard`
- **Default period:** `now-72h → now`

Состояние «железа» и датчиков: использует **`processed_common_data.latest_calibrated_sensors`**, **`raw_business_data.sensor_description`**, объекты и телематику. Для булевых датчиков с `calc_method = bit_index` подписи состояний могут браться из JSON-параметров датчика (`value_titles`).

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
