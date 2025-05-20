from models import Question

KAFKA_CARDS = [
    Question(
        text="Введение в Apache Kafka",
        theory="""Apache Kafka - это распределенная система обмена сообщениями, разработанная LinkedIn и переданная в Apache Software Foundation.

Основные характеристики:
- Высокая пропускная способность (миллионы сообщений в секунду)
- Низкая задержка (менее 10 мс)
- Отказоустойчивость
- Масштабируемость
- Долговременное хранение сообщений

Kafka используется для:
- Стриминга данных
- Сбора метрик и логов
- Обработки событий в реальном времени
- Интеграции микросервисов
- Создания конвейеров данных""",
        theory_summary="Kafka - высокопроизводительная система обмена сообщениями для обработки потоков данных в реальном времени.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Архитектура Kafka",
        theory="""Kafka состоит из следующих основных компонентов:

1. Брокеры (Brokers):
- Узлы кластера Kafka
- Хранят сообщения
- Обрабатывают запросы клиентов
- Управляют репликацией

2. Топики (Topics):
- Категории или каналы сообщений
- Разделяются на партиции
- Имеют уникальные имена
- Могут быть созданы программно или через конфигурацию

3. Партиции (Partitions):
- Упорядоченные последовательности сообщений
- Обеспечивают параллелизм
- Позволяют масштабировать обработку
- Имеют уникальные идентификаторы

4. Продюсеры (Producers):
- Отправляют сообщения в топики
- Могут выбирать партицию
- Поддерживают подтверждения
- Могут сжимать данные

5. Консьюмеры (Consumers):
- Читают сообщения из топиков
- Работают в группах
- Отслеживают позицию чтения
- Могут обрабатывать сообщения параллельно""",
        theory_summary="Kafka состоит из брокеров, топиков, партиций, продюсеров и консьюмеров, работающих вместе для обеспечения надежной передачи сообщений.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Топики и партиции",
        theory="""Топики и партиции - ключевые концепции Kafka:

Топики:
- Логические каналы для сообщений
- Могут содержать любое количество партиций
- Имеют настройки хранения и репликации
- Поддерживают политики очистки данных

Партиции:
- Упорядоченные последовательности сообщений
- Обеспечивают параллелизм и масштабируемость
- Имеют уникальные идентификаторы (offsets)
- Могут быть реплицированы

Настройки партиций:
- replication.factor: количество реплик
- num.partitions: количество партиций
- min.insync.replicas: минимальное количество синхронных реплик
- retention.ms: время хранения сообщений

Важные аспекты:
- Количество партиций влияет на параллелизм
- Репликация обеспечивает отказоустойчивость
- Offset позволяет отслеживать позицию чтения
- Партиции могут быть перераспределены между брокерами""",
        theory_summary="Топики разделяются на партиции для обеспечения параллелизма и масштабируемости, с настройками репликации и хранения.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Producer API",
        theory="""Producer API в Kafka позволяет отправлять сообщения в топики:

Основные компоненты:
1. ProducerRecord:
- Содержит ключ и значение
- Может включать метаданные
- Указывает целевой топик
- Опционально указывает партицию

2. Настройки Producer:
- bootstrap.servers: список брокеров
- key.serializer: сериализатор ключей
- value.serializer: сериализатор значений
- acks: уровень подтверждения
- retries: количество попыток
- batch.size: размер батча
- linger.ms: задержка отправки

3. Методы отправки:
- send(): асинхронная отправка
- flush(): принудительная отправка
- close(): закрытие producer

4. Обработка ошибок:
- RetryPolicy
- Error handling
- Callback functions
- Exception handling

5. Оптимизация:
- Батчинг сообщений
- Сжатие данных
- Партиционирование
- Таймауты""",
        theory_summary="Producer API предоставляет гибкие возможности для отправки сообщений с настройками производительности и надежности.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Consumer API",
        theory="""Consumer API в Kafka позволяет читать сообщения из топиков:

Основные компоненты:
1. ConsumerRecord:
- Содержит ключ и значение
- Включает метаданные
- Содержит offset
- Имеет timestamp

2. Настройки Consumer:
- bootstrap.servers: список брокеров
- group.id: идентификатор группы
- key.deserializer: десериализатор ключей
- value.deserializer: десериализатор значений
- auto.offset.reset: политика сброса offset
- enable.auto.commit: авто-коммит offset

3. Методы чтения:
- poll(): получение сообщений
- commit(): подтверждение обработки
- seek(): установка позиции
- close(): закрытие consumer

4. Consumer Groups:
- Распределение партиций
- Ребалансировка
- Отказоустойчивость
- Масштабируемость

5. Оптимизация:
- Размер батча
- Таймауты
- Heartbeat
- Session timeout""",
        theory_summary="Consumer API обеспечивает надежное чтение сообщений с поддержкой групп консьюмеров и управлением offset.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Репликация в Kafka",
        theory="""Репликация - ключевой механизм обеспечения надежности в Kafka:

1. Основные концепции:
- Leader: основная партиция
- Follower: реплика партиции
- ISR (In-Sync Replicas): синхронные реплики
- AR (Assigned Replicas): назначенные реплики

2. Процесс репликации:
- Leader принимает запись
- Follower запрашивает данные
- Leader отправляет данные
- Follower подтверждает получение
- Leader обновляет ISR

3. Настройки репликации:
- replication.factor: фактор репликации
- min.insync.replicas: минимальное количество синхронных реплик
- replica.lag.time.max.ms: максимальное отставание реплики
- replica.fetch.wait.max.ms: максимальное время ожидания

4. Обработка сбоев:
- Выбор нового leader
- Ребалансировка реплик
- Восстановление после сбоя
- Проверка целостности

5. Мониторинг:
- Lag реплик
- Статус ISR
- Размер реплик
- Производительность""",
        theory_summary="Репликация обеспечивает отказоустойчивость и надежность данных через механизм синхронизации реплик партиций.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Управление топиками",
        theory="""Управление топиками в Kafka включает несколько аспектов:

1. Создание топиков:
- Через API
- Через CLI
- Автоматическое создание
- Настройки по умолчанию

2. Конфигурация:
- Количество партиций
- Фактор репликации
- Политики очистки
- Настройки сжатия

3. Мониторинг:
- Размер топика
- Количество сообщений
- Lag консьюмеров
- Использование ресурсов

4. Обслуживание:
- Увеличение партиций
- Изменение конфигурации
- Очистка данных
- Балансировка

5. Безопасность:
- ACL (Access Control Lists)
- Шифрование
- Аутентификация
- Авторизация""",
        theory_summary="Управление топиками включает создание, конфигурацию, мониторинг и обслуживание с учетом безопасности.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Сериализация в Kafka",
        theory="""Сериализация - процесс преобразования объектов в байты для передачи:

1. Встроенные сериализаторы:
- StringSerializer
- ByteArraySerializer
- IntegerSerializer
- LongSerializer

2. Avro:
- Схемы данных
- Реестр схем
- Версионирование
- Совместимость

3. JSON:
- Гибкость
- Человекочитаемость
- Простота использования
- Отсутствие схемы

4. Protobuf:
- Эффективность
- Строгая типизация
- Версионирование
- Кросс-языковая поддержка

5. Кастомные сериализаторы:
- Специфичные форматы
- Оптимизация
- Интеграция
- Безопасность""",
        theory_summary="Сериализация обеспечивает преобразование данных в формат, пригодный для передачи в Kafka, с поддержкой различных форматов.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Безопасность в Kafka",
        theory="""Безопасность в Kafka включает несколько уровней защиты:

1. Аутентификация:
- SSL/TLS
- SASL
- Kerberos
- OAuth

2. Авторизация:
- ACL (Access Control Lists)
- RBAC (Role-Based Access Control)
- Права доступа
- Группы доступа

3. Шифрование:
- SSL/TLS для передачи
- Шифрование на диске
- Шифрование сообщений
- Ключи шифрования

4. Аудит:
- Логирование действий
- Мониторинг доступа
- Отслеживание изменений
- Анализ безопасности

5. Защита данных:
- Маскирование
- Анонимизация
- Контроль доступа
- Политики хранения""",
        theory_summary="Безопасность в Kafka обеспечивается через аутентификацию, авторизацию, шифрование и аудит.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Мониторинг Kafka",
        theory="""Мониторинг Kafka включает отслеживание различных метрик:

1. Метрики брокера:
- CPU использование
- Память
- Диск I/O
- Сеть

2. Метрики топиков:
- Размер
- Количество сообщений
- Lag консьюмеров
- Throughput

3. Метрики консьюмеров:
- Lag
- Throughput
- Ошибки
- Время обработки

4. Метрики продюсеров:
- Throughput
- Latency
- Ошибки
- Размер батча

5. Алерты:
- Критические метрики
- Пороговые значения
- Уведомления
- Автоматические действия""",
        theory_summary="Мониторинг Kafka включает отслеживание метрик брокеров, топиков, консьюмеров и продюсеров с системой алертов.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    )
]

# Добавим карточки с конкретными темами о Kafka
KAFKA_CARDS.extend([
    Question(
        text="Практические сценарии использования Kafka",
        theory="""Распространенные сценарии использования Kafka в реальных проектах:

1. Микросервисная архитектура:
- Асинхронная коммуникация между сервисами
- Event-driven архитектура
- Декомпозиция монолита
- Синхронизация данных

2. Сбор и анализ данных:
- Сбор метрик и логов
- Аналитика в реальном времени
- Обработка больших данных
- Интеграция с BI-системами

3. Потоковая обработка:
- Обработка событий в реальном времени
- Агрегация данных
- Обнаружение аномалий
- Триггеры и уведомления

4. Интеграция систем:
- Синхронизация баз данных
- Репликация данных
- Миграция данных
- Кэширование""",
        theory_summary="Kafka используется для микросервисной архитектуры, сбора данных, потоковой обработки и интеграции систем.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Распространенные проблемы в Kafka",
        theory="""Типичные проблемы при работе с Kafka и их решения:

1. Проблемы производительности:
- Высокая задержка: оптимизация batch.size и linger.ms
- Низкий throughput: увеличение партиций и настройка сжатия
- Высокая нагрузка на CPU: оптимизация сериализации
- Проблемы с памятью: настройка heap size

2. Проблемы с консьюмерами:
- Consumer lag: масштабирование групп
- Ребалансировка: настройка session.timeout
- Дублирование сообщений: правильная настройка commit
- Потеря сообщений: настройка retry policy

3. Проблемы с брокерами:
- Нехватка дискового пространства: настройка retention
- Сетевые проблемы: настройка timeouts
- Проблемы с репликацией: мониторинг ISR
- Высокая нагрузка: масштабирование кластера

4. Проблемы с данными:
- Несовместимость схем: использование Schema Registry
- Коррупция данных: валидация и проверка целостности
- Потеря данных: настройка репликации
- Проблемы с форматом: стандартизация сериализации""",
        theory_summary="Основные проблемы в Kafka связаны с производительностью, консьюмерами, брокерами и данными, каждую из которых можно решить правильной настройкой.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Инструменты для работы с Kafka",
        theory="""Популярные инструменты для работы с Kafka:

1. Администрирование:
- Kafka Manager: веб-интерфейс для управления кластером
- Conduktor: GUI для администрирования
- Kafka Tool: десктопное приложение
- AKHQ: современный веб-интерфейс

2. Мониторинг:
- Prometheus + Grafana: метрики и визуализация
- Datadog: комплексный мониторинг
- New Relic: APM и мониторинг
- Confluent Control Center: мониторинг от Confluent

3. Разработка:
- kafkacat: CLI для тестирования
- Kafka Connect: интеграция с внешними системами
- ksqlDB: SQL для потоковой обработки
- Kafka Streams: библиотека для обработки

4. Безопасность:
- Confluent Security: управление безопасностью
- Vault: управление секретами
- Ranger: управление доступом
- Audit Logs: аудит действий""",
        theory_summary="Для работы с Kafka используются инструменты администрирования, мониторинга, разработки и безопасности.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Интеграция Kafka с другими системами",
        theory="""Популярные интеграции Kafka с другими системами:

1. Базы данных:
- PostgreSQL: CDC через Debezium
- MongoDB: Change Streams
- MySQL: Binlog
- Cassandra: Sink Connector

2. Системы хранения:
- S3: Sink Connector
- HDFS: Connect HDFS
- Elasticsearch: Elasticsearch Connector
- Redis: Redis Connector

3. Системы мониторинга:
- Prometheus: JMX Exporter
- Grafana: Kafka Dashboard
- ELK Stack: Logstash
- Datadog: Kafka Integration

4. Облачные платформы:
- AWS: MSK, Kinesis
- GCP: Pub/Sub
- Azure: Event Hubs
- Confluent Cloud""",
        theory_summary="Kafka интегрируется с базами данных, системами хранения, мониторинга и облачными платформами через коннекторы и специальные инструменты.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    ),
    Question(
        text="Оптимизация производительности Kafka",
        theory="""Ключевые аспекты оптимизации производительности Kafka:

1. Настройка брокеров:
- JVM параметры: heap size, GC
- Файловая система: XFS, ext4
- Сеть: настройка буферов
- Диски: RAID, SSD

2. Оптимизация продюсеров:
- Батчинг: batch.size, linger.ms
- Сжатие: snappy, lz4
- Партиционирование: ключи
- Подтверждения: acks

3. Оптимизация консьюмеров:
- Размер батча: fetch.min.bytes
- Параллелизм: количество потоков
- Обработка: асинхронная
- Коммиты: ручные/авто

4. Оптимизация топиков:
- Количество партиций
- Фактор репликации
- Retention policy
- Cleanup policy""",
        theory_summary="Оптимизация производительности Kafka включает настройку брокеров, продюсеров, консьюмеров и топиков.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    )
])

# Добавим остальные карточки с конкретными темами
topics = [
    "Kafka Streams API",
    "Kafka Connect",
    "ksqlDB",
    "Schema Registry",
    "Kafka Security",
    "Kafka Monitoring",
    "Kafka Performance Tuning",
    "Kafka Architecture Patterns",
    "Kafka Deployment",
    "Kafka Troubleshooting",
    "Kafka Data Modeling",
    "Kafka Data Governance",
    "Kafka Data Quality",
    "Kafka Data Pipeline",
    "Kafka Data Lake",
    "Kafka Data Warehouse",
    "Kafka Data Mesh",
    "Kafka Data Fabric",
    "Kafka Data Streaming",
    "Kafka Data Processing",
    "Kafka Data Integration",
    "Kafka Data Migration",
    "Kafka Data Replication",
    "Kafka Data Backup",
    "Kafka Data Recovery",
    "Kafka Data Retention",
    "Kafka Data Cleanup",
    "Kafka Data Compression",
    "Kafka Data Serialization",
    "Kafka Data Deserialization",
    "Kafka Data Validation",
    "Kafka Data Transformation",
    "Kafka Data Enrichment",
    "Kafka Data Filtering",
    "Kafka Data Aggregation",
    "Kafka Data Joining",
    "Kafka Data Windowing",
    "Kafka Data State",
    "Kafka Data Time",
    "Kafka Data Ordering",
    "Kafka Data Partitioning",
    "Kafka Data Routing",
    "Kafka Data Batching",
    "Kafka Data Streaming",
    "Kafka Data Processing",
    "Kafka Data Integration",
    "Kafka Data Migration",
    "Kafka Data Replication",
    "Kafka Data Backup",
    "Kafka Data Recovery",
    "Kafka Data Retention",
    "Kafka Data Cleanup",
    "Kafka Data Compression",
    "Kafka Data Serialization",
    "Kafka Data Deserialization",
    "Kafka Data Validation",
    "Kafka Data Transformation",
    "Kafka Data Enrichment",
    "Kafka Data Filtering",
    "Kafka Data Aggregation",
    "Kafka Data Joining",
    "Kafka Data Windowing",
    "Kafka Data State",
    "Kafka Data Time",
    "Kafka Data Ordering",
    "Kafka Data Partitioning",
    "Kafka Data Routing",
    "Kafka Data Batching"
]

for i in range(16, 101):
    topic_index = (i - 16) % len(topics)
    topic = topics[topic_index]
    KAFKA_CARDS.append(Question(
        text=topic,
        theory=f"""Подробная информация о {topic}:

1. Основные концепции:
   - Определение и назначение
   - Ключевые компоненты
   - Принципы работы
   - Использование

2. Практическое применение:
   - Типичные сценарии
   - Примеры использования
   - Ограничения
   - Best practices

3. Настройка и конфигурация:
   - Параметры
   - Оптимизация
   - Мониторинг
   - Отладка

4. Интеграция:
   - С другими компонентами
   - С внешними системами
   - С инструментами
   - С сервисами""",
        theory_summary=f"{topic}: основные концепции, практическое применение, настройка и интеграция.",
        correct_answer="",
        options=[],
        explanation="",
        points=0
    )) 