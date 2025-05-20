from src.models import Question

DATABASE_CARDS = [
    Question(
        text="Основы PostgreSQL",
        theory="""PostgreSQL - это мощная объектно-реляционная СУБД:

1. Основные концепции:
- Таблицы и схемы
- Индексы и их типы
- Транзакции и ACID
- Ограничения (constraints)

2. Типы данных:
- Числовые (INTEGER, NUMERIC, DECIMAL)
- Строковые (VARCHAR, TEXT)
- Дата и время (TIMESTAMP, DATE)
- Массивы и JSON
- Пользовательские типы

3. Оптимизация:
- Индексы (B-tree, Hash, GiST)
- Партиционирование
- Материализованные представления
- EXPLAIN и анализ запросов

4. Безопасность:
- Роли и привилегии
- Шифрование
- Аудит
- Резервное копирование""",
        theory_summary="PostgreSQL - это продвинутая СУБД с поддержкой сложных типов данных и оптимизацией производительности.",
        correct_answer="",
        options=[],
        explanation="""Давайте разберем основные концепции PostgreSQL на примерах:

1. Создание таблиц и индексов:
```sql
-- Создание таблицы
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    profile_data JSONB
);

-- Создание индекса
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- Создание составного индекса
CREATE INDEX idx_users_created_at_username 
ON users(created_at, username);
```

2. Работа с транзакциями:
```sql
BEGIN;
    -- Начало транзакции
    INSERT INTO users (username, email) 
    VALUES ('john_doe', 'john@example.com');
    
    INSERT INTO user_profiles (user_id, bio) 
    VALUES (LASTVAL(), 'Software Developer');
    
    -- Если все успешно
    COMMIT;
    -- Если произошла ошибка
    -- ROLLBACK;
```

3. Оптимизация запросов:
```sql
-- Анализ запроса
EXPLAIN ANALYZE
SELECT u.username, p.bio
FROM users u
JOIN user_profiles p ON u.id = p.user_id
WHERE u.created_at > '2024-01-01'
ORDER BY u.username;

-- Создание материализованного представления
CREATE MATERIALIZED VIEW active_users AS
SELECT u.*, p.bio
FROM users u
JOIN user_profiles p ON u.id = p.user_id
WHERE u.last_login > CURRENT_DATE - INTERVAL '30 days'
WITH DATA;

-- Обновление материализованного представления
REFRESH MATERIALIZED VIEW active_users;
```

4. Партиционирование:
```sql
-- Создание партиционированной таблицы
CREATE TABLE orders (
    id SERIAL,
    order_date DATE NOT NULL,
    customer_id INTEGER,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- Создание партиций
CREATE TABLE orders_2024_01 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE orders_2024_02 PARTITION OF orders
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

5. Безопасность:
```sql
-- Создание роли
CREATE ROLE app_user WITH LOGIN PASSWORD 'secret';

-- Предоставление прав
GRANT SELECT, INSERT, UPDATE ON users TO app_user;
GRANT USAGE ON SEQUENCE users_id_seq TO app_user;

-- Создание политики безопасности
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY users_policy ON users
    FOR ALL
    TO app_user
    USING (created_by = current_user);
```

Практические советы:
1. Всегда используйте индексы для часто запрашиваемых полей
2. Применяйте транзакции для обеспечения целостности данных
3. Регулярно анализируйте и оптимизируйте запросы
4. Используйте партиционирование для больших таблиц
5. Следуйте принципу наименьших привилегий при настройке прав""",
        points=0
    ),
    Question(
        text="Оптимизация производительности PostgreSQL",
        theory="""Оптимизация производительности PostgreSQL включает несколько аспектов:

1. Настройка сервера:
- shared_buffers
- work_mem
- maintenance_work_mem
- effective_cache_size
- max_connections

2. Оптимизация запросов:
- EXPLAIN и EXPLAIN ANALYZE
- Индексы и их типы
- Статистика таблиц
- VACUUM и ANALYZE

3. Мониторинг:
- pg_stat_activity
- pg_stat_statements
- pg_stat_user_tables
- pg_stat_user_indexes

4. Масштабирование:
- Репликация
- Шардирование
- Connection pooling
- Кэширование""",
        theory_summary="Оптимизация PostgreSQL требует комплексного подхода к настройке сервера, запросов и мониторингу.",
        correct_answer="",
        options=[],
        explanation="""Давайте разберем оптимизацию PostgreSQL на примерах:

1. Настройка параметров сервера:
```sql
-- postgresql.conf
shared_buffers = 4GB  # 25% от RAM
work_mem = 64MB      # Для операций сортировки
maintenance_work_mem = 1GB  # Для обслуживания
effective_cache_size = 12GB  # 75% от RAM
max_connections = 100  # Зависит от нагрузки
```

2. Анализ и оптимизация запросов:
```sql
-- Анализ запроса
EXPLAIN ANALYZE
SELECT u.username, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.username
HAVING COUNT(o.id) > 5;

-- Создание индекса для оптимизации
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Обновление статистики
ANALYZE users;
ANALYZE orders;
```

3. Мониторинг производительности:
```sql
-- Активные запросы
SELECT pid, query, state, wait_event
FROM pg_stat_activity
WHERE state != 'idle';

-- Статистика таблиц
SELECT schemaname, relname, 
       seq_scan, idx_scan,
       n_live_tup, n_dead_tup
FROM pg_stat_user_tables
ORDER BY seq_scan DESC;

-- Статистика индексов
SELECT schemaname, relname, indexrelname,
       idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

4. Настройка репликации:
```sql
-- Настройка основной БД
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10

-- Настройка реплики
hot_standby = on
```

5. Оптимизация больших таблиц:
```sql
-- Партиционирование по дате
CREATE TABLE orders (
    id SERIAL,
    order_date DATE NOT NULL,
    customer_id INTEGER,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- Создание партиций
CREATE TABLE orders_2024_01 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Создание индекса на партиционированной таблице
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

Практические советы:
1. Регулярно обновляйте статистику таблиц
2. Используйте EXPLAIN для анализа запросов
3. Настраивайте параметры сервера под вашу нагрузку
4. Применяйте партиционирование для больших таблиц
5. Мониторьте производительность системы""",
        points=0
    )
] 