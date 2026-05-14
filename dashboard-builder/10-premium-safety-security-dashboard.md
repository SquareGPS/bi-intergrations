# Safety & Security (Premium)

- **File:** `10-premium-safety-security-dashboard-schema.json`
- **UID:** `premium-safety-security-dashboard`
- **Default period:** `now-24h → now`

Шаблон из инфраструктуры клиентской БД: зоны риска, визиты в геозоны, телематика и датчики за последние 24 часа. SQL опирается на **`processed_common_data`** (в т.ч. `zone_visits`, `trips` при наличии панелей), справочники зон и тегов — **`raw_business_data`**.

Для расшифровки кодов событий трекера в кастомных панелях можно подключать **`processed_common_data.event_description`**; пользовательские подписи значений датчиков — через **`value_title`** в почасовых агрегатах и связанные справочники.

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
