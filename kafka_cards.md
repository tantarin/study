# Карточки для изучения Apache Kafka

## Основные концепты

### Карточка 1: Что такое Apache Kafka?
**Вопрос**: Что представляет собой Apache Kafka?

**Технический ответ**: Apache Kafka - это распределенная платформа потоковой передачи данных, которая позволяет:
- Публиковать и подписываться на потоки записей
- Хранить потоки записей отказоустойчивым способом
- Обрабатывать потоки записей в режиме реального времени

**Простое объяснение**: 
Представьте себе Kafka как огромную систему очередей, похожую на YouTube для данных. Вот как это работает:

1. **Публикация и подписка** (как в YouTube):
   - Производители данных (как авторы на YouTube) публикуют информацию
   - Потребители (как зрители) подписываются на нужные им данные
   - Пример из жизни: интернет-магазин отправляет информацию о новых заказах, а складская система получает эти данные

2. **Хранение данных**:
   - Kafka хранит все сообщения надёжно и долго (как YouTube хранит видео)
   - Даже если потребитель временно отключился, он не потеряет данные
   - Пример: если складская система временно не работает, она всё равно получит все заказы после восстановления

3. **Обработка в реальном времени**:
   - Данные обрабатываются мгновенно, как только появляются
   - Можно создавать цепочки обработки данных
   - Пример: как только поступает заказ:
     * Система оплаты проверяет платёж
     * Складская система резервирует товар
     * Система доставки планирует маршрут
     * Клиент получает уведомление

**Практический пример**:
```java
// Производитель отправляет заказ
OrderProducer producer = new OrderProducer();
Order order = new Order("iPhone 13", 1, "123 Main St");
producer.send("orders", order);

// Потребители получают и обрабатывают заказ
@KafkaListener(topics = "orders")
public void processOrder(Order order) {
    // Складская система обрабатывает заказ
    warehouse.reserveItem(order.getProduct(), order.getQuantity());
    
    // Система доставки планирует доставку
    delivery.schedule(order.getAddress());
}
```

**Где используется**:
- Netflix использует Kafka для обработки просмотров в реальном времени
- Uber обрабатывает поездки и местоположение водителей
- LinkedIn (где создали Kafka) использует для активности пользователей
- Банки обрабатывают транзакции и выявляют мошенничество

### Карточка 2: Основные компоненты Kafka
**Вопрос**: Перечислите основные компоненты Apache Kafka.

**Технический ответ**: Основные компоненты:
1. Producer (Производитель) - публикует сообщения в топики
2. Consumer (Потребитель) - подписывается на топики и читает сообщения
3. Broker (Брокер) - сервер Kafka, хранящий сообщения
4. Topic (Топик) - категория или канал для сообщений
5. Partition (Раздел) - физическое разделение топика для масштабирования
6. ZooKeeper - координирует работу кластера (в новых версиях опционально)

**Простое объяснение**: 
Представьте Kafka как большой почтовый офис. Вот как работают его компоненты:

1. **Producer (Производитель)** - это как отправитель письма:
   - Создаёт сообщения и отправляет их в систему
   - Пример: кассовый аппарат в магазине, отправляющий информацию о продажах
   ```java
   // Пример Producer
   KafkaProducer<String, String> producer = new KafkaProducer<>(props);
   producer.send(new ProducerRecord<>("sales", "store123", "sale: 100$"));
   ```

2. **Consumer (Потребитель)** - как получатель письма:
   - Читает сообщения из системы
   - Может быть частью группы потребителей (как отдел обработки писем)
   - Пример: система аналитики, обрабатывающая данные о продажах
   ```java
   // Пример Consumer
   KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
   consumer.subscribe(Arrays.asList("sales"));
   ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
   ```

3. **Broker (Брокер)** - как почтовое отделение:
   - Хранит сообщения
   - Обеспечивает их доставку
   - Может быть частью кластера (сети почтовых отделений)
   ```properties
   # Пример конфигурации брокера
   broker.id=1
   listeners=PLAINTEXT://localhost:9092
   log.dirs=/var/lib/kafka/data
   ```

4. **Topic (Топик)** - как почтовый ящик для определённого типа писем:
   - Разделяет сообщения по категориям
   - Имеет настраиваемое время хранения
   - Пример: отдельные топики для заказов, платежей, доставки
   ```bash
   # Создание топика
   kafka-topics.sh --create --topic orders --partitions 3 --replication-factor 2
   ```

5. **Partition (Раздел)** - как сортировочные ячейки в почтовом отделении:
   - Позволяет параллельно обрабатывать сообщения
   - Обеспечивает масштабируемость
   - Пример: разделение заказов по регионам
   ```plaintext
   Топик "orders":
   Partition 0 -> Заказы из Москвы
   Partition 1 -> Заказы из Санкт-Петербурга
   Partition 2 -> Заказы из других городов
   ```

6. **ZooKeeper** - как главный диспетчер почтовой службы:
   - Следит за работой всех брокеров
   - Хранит конфигурацию
   - Обеспечивает координацию
   ```properties
   # Пример конфигурации ZooKeeper
   zookeeper.connect=localhost:2181
   zookeeper.connection.timeout.ms=18000
   ```

**Практический пример взаимодействия компонентов**:
```java
// Настройка Producer
Properties producerProps = new Properties();
producerProps.put("bootstrap.servers", "localhost:9092");
producerProps.put("key.serializer", StringSerializer.class.getName());
producerProps.put("value.serializer", StringSerializer.class.getName());

// Создание Producer
KafkaProducer<String, String> producer = new KafkaProducer<>(producerProps);

// Отправка сообщения
producer.send(new ProducerRecord<>("orders", "order123", "iPhone:1:1000$"));

// Настройка Consumer
Properties consumerProps = new Properties();
consumerProps.put("bootstrap.servers", "localhost:9092");
consumerProps.put("group.id", "order-processing-group");
consumerProps.put("key.deserializer", StringDeserializer.class.getName());
consumerProps.put("value.deserializer", StringDeserializer.class.getName());

// Создание Consumer
KafkaConsumer<String, String> consumer = new KafkaConsumer<>(consumerProps);
consumer.subscribe(Arrays.asList("orders"));

// Чтение сообщений
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        System.out.printf("Получен заказ: key = %s, value = %s%n", 
                         record.key(), record.value());
    }
}
```

**Реальные примеры использования**:
1. **E-commerce**:
   - Producer: система оформления заказов
   - Topic: "orders"
   - Consumer: складская система, система доставки

2. **Банковская система**:
   - Producer: банкоматы, онлайн-банкинг
   - Topic: "transactions"
   - Consumer: система обработки транзакций, антифрод-система

3. **IoT (Интернет вещей)**:
   - Producer: датчики температуры
   - Topic: "sensor-data"
   - Consumer: система мониторинга, система оповещений

**Важно помнить**:
- Один Producer может писать в несколько топиков
- Один Consumer может читать из нескольких топиков
- Топик может иметь множество партиций для параллельной обработки
- Брокеры работают в кластере для отказоустойчивости
- ZooKeeper (или новая система KRaft) обеспечивает координацию всех компонентов

### Карточка 3: Что такое топик?
**Вопрос**: Объясните концепцию топика в Kafka.

**Ответ**: Топик - это:
- Именованный поток сообщений определенного типа
- Логическая группировка сообщений
- Может быть разделен на партиции для параллельной обработки
- Имеет настраиваемое время хранения сообщений
- Поддерживает репликацию для отказоустойчивости

### Карточка 4: Партиции в Kafka
**Вопрос**: Как работают партиции в Kafka?

**Ответ**: Партиции - это:
- Физическое разделение топика на части
- Каждая партиция хранится на отдельном брокере
- Обеспечивают параллельную обработку данных
- Имеют строгий порядок сообщений внутри себя
- Могут быть реплицированы для надежности

### Карточка 5: Producer API
**Вопрос**: Какие основные возможности предоставляет Producer API?

**Ответ**: Producer API позволяет:
- Отправлять сообщения в топики
- Выбирать партицию для сообщения
- Настраивать подтверждения записи (acks)
- Использовать сжатие данных
- Управлять батчингом сообщений

## Архитектура и масштабирование

### Карточка 6: Репликация в Kafka
**Вопрос**: Как работает репликация в Kafka?

**Ответ**: Репликация обеспечивает:
- Копирование данных между брокерами
- Отказоустойчивость при сбоях
- Leader-Follower модель для каждой партиции
- Автоматическое восстановление при сбоях
- Настраиваемый фактор репликации

### Карточка 7: Consumer Groups
**Вопрос**: Что такое Consumer Groups и как они работают?

**Ответ**: Consumer Groups это:
- Группы потребителей, работающих как единое целое
- Автоматическое распределение партиций между потребителями
- Автоматическое перебалансирование при изменении состава группы
- Гарантия, что сообщение будет обработано только один раз в группе
- Возможность горизонтального масштабирования обработки

### Карточка 8: Гарантии доставки
**Вопрос**: Какие гарантии доставки предоставляет Kafka?

**Ответ**: Kafka обеспечивает:
- At-least-once доставку по умолчанию
- Exactly-once семантику при необходимости
- Сохранение порядка сообщений в пределах партиции
- Настраиваемые подтверждения записи (acks)
- Возможность повторной обработки данных

## Конфигурация и мониторинг

### Карточка 9: Важные настройки Producer
**Вопрос**: Какие основные настройки Producer следует знать?

**Ответ**: Ключевые настройки:
- acks (0, 1, all) - уровень подтверждений
- batch.size - размер батча сообщений
- linger.ms - время ожидания формирования батча
- compression.type - тип сжатия
- retries - количество повторных попыток

### Карточка 10: Мониторинг Kafka
**Вопрос**: Какие метрики важно отслеживать в Kafka?

**Ответ**: Основные метрики:
- Under-replicated партиции
- Задержка репликации (replica.lag)
- Количество сообщений в секунду
- Латентность операций
- Использование дискового пространства

## Примеры кода на Java

### Карточка 11: Создание Producer
**Вопрос**: Как создать и настроить Producer в Java?

**Ответ**: Пример базовой настройки и создания Producer:
```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("acks", "all");

Producer<String, String> producer = new KafkaProducer<>(props);

// Отправка сообщения
ProducerRecord<String, String> record = 
    new ProducerRecord<>("my-topic", "key", "value");

producer.send(record, (metadata, exception) -> {
    if (exception == null) {
        System.out.println("Message sent to partition " + metadata.partition());
    } else {
        exception.printStackTrace();
    }
});

producer.close();
```

### Карточка 12: Создание Consumer
**Вопрос**: Как создать и настроить Consumer в Java?

**Ответ**: Пример создания и использования Consumer:
```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("auto.offset.reset", "earliest");

Consumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Arrays.asList("my-topic"));

try {
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            System.out.printf("offset = %d, key = %s, value = %s%n", 
                record.offset(), record.key(), record.value());
        }
    }
} finally {
    consumer.close();
}
```

### Карточка 13: Транзакционный Producer
**Вопрос**: Как использовать транзакции в Kafka Producer?

**Ответ**: Пример использования транзакционного Producer:
```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("transactional.id", "my-transactional-id");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

Producer<String, String> producer = new KafkaProducer<>(props);
producer.initTransactions();

try {
    producer.beginTransaction();
    
    // Отправка нескольких сообщений в транзакции
    producer.send(new ProducerRecord<>("topic1", "key1", "value1"));
    producer.send(new ProducerRecord<>("topic2", "key2", "value2"));
    
    producer.commitTransaction();
} catch (Exception e) {
    producer.abortTransaction();
    throw e;
} finally {
    producer.close();
}
```

### Карточка 14: Kafka Streams
**Вопрос**: Как создать простой Kafka Streams приложение?

**Ответ**: Пример простого приложения на Kafka Streams:
```java
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-app");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

StreamsBuilder builder = new StreamsBuilder();

// Чтение из входного топика
KStream<String, String> source = builder.stream("input-topic");

// Преобразование данных
KStream<String, String> transformed = source
    .mapValues(value -> value.toUpperCase());

// Запись в выходной топик
transformed.to("output-topic");

KafkaStreams streams = new KafkaStreams(builder.build(), props);
streams.start();
```

### Карточка 15: Пользовательский Serializer
**Вопрос**: Как создать пользовательский сериализатор для объектов?

**Ответ**: Пример создания пользовательского сериализатора:
```java
public class User {
    private String name;
    private int age;
    // геттеры, сеттеры, конструкторы
}

public class UserSerializer implements Serializer<User> {
    private final ObjectMapper mapper = new ObjectMapper();

    @Override
    public byte[] serialize(String topic, User user) {
        try {
            return mapper.writeValueAsBytes(user);
        } catch (Exception e) {
            throw new SerializationException("Error serializing User", e);
        }
    }
}

// Использование:
Properties props = new Properties();
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "com.example.UserSerializer");

Producer<String, User> producer = new KafkaProducer<>(props);
producer.send(new ProducerRecord<>("users", "user1", new User("John", 30)));
```

### Карточка 16: Обработка ошибок
**Вопрос**: Как правильно обрабатывать ошибки в Kafka Producer и Consumer?

**Ответ**: Пример обработки ошибок:
```java
// Producer с обработкой ошибок
Properties producerProps = new Properties();
// ... настройка properties ...

Producer<String, String> producer = new KafkaProducer<>(producerProps);
ProducerRecord<String, String> record = 
    new ProducerRecord<>("topic", "key", "value");

try {
    producer.send(record, (metadata, exception) -> {
        if (exception != null) {
            // Обработка ошибки отправки
            log.error("Failed to send message", exception);
            // Возможно, сохранение в dead letter queue
        }
    }).get(); // .get() делает отправку синхронной
} catch (InterruptedException | ExecutionException e) {
    // Обработка ошибок
    log.error("Error sending message", e);
} finally {
    producer.close();
}

// Consumer с обработкой ошибок
Properties consumerProps = new Properties();
// ... настройка properties ...

Consumer<String, String> consumer = new KafkaConsumer<>(consumerProps);
consumer.subscribe(Arrays.asList("topic"));

try {
    while (true) {
        try {
            ConsumerRecords<String, String> records = 
                consumer.poll(Duration.ofMillis(100));
            
            for (ConsumerRecord<String, String> record : records) {
                try {
                    // Обработка сообщения
                    processRecord(record);
                    // Ручной коммит после обработки
                    consumer.commitSync(
                        Collections.singletonMap(
                            new TopicPartition(record.topic(), record.partition()),
                            new OffsetAndMetadata(record.offset() + 1)
                        )
                    );
                } catch (Exception e) {
                    // Обработка ошибки конкретного сообщения
                    log.error("Error processing record", e);
                    // Возможно, отправка в dead letter queue
                }
            }
        } catch (Exception e) {
            // Обработка ошибок poll()
            log.error("Error polling messages", e);
        }
    }
} finally {
    consumer.close();
}
```

## Безопасность и аутентификация

### Карточка 17: SSL/TLS в Kafka
**Вопрос**: Как настроить SSL/TLS в Kafka?

**Ответ**: Основные шаги настройки SSL:
1. Создание сертификатов и ключей
2. Настройка брокера:
```properties
listeners=SSL://localhost:9093
security.inter.broker.protocol=SSL
ssl.keystore.location=/path/to/kafka.server.keystore.jks
ssl.keystore.password=keystore-password
ssl.key.password=key-password
ssl.truststore.location=/path/to/kafka.server.truststore.jks
ssl.truststore.password=truststore-password
ssl.client.auth=required
```
3. Настройка клиента:
```properties
security.protocol=SSL
ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=truststore-password
ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=keystore-password
ssl.key.password=key-password
```

### Карточка 18: SASL Аутентификация
**Вопрос**: Как настроить SASL аутентификацию?

**Ответ**: Настройка SASL PLAIN:
1. Настройка брокера:
```properties
listeners=SASL_PLAINTEXT://localhost:9092
security.inter.broker.protocol=SASL_PLAINTEXT
sasl.mechanism.inter.broker.protocol=PLAIN
sasl.enabled.mechanisms=PLAIN
```
2. Создание файла JAAS:
```
KafkaServer {
    org.apache.kafka.common.security.plain.PlainLoginModule required
    username="admin"
    password="admin-secret"
    user_admin="admin-secret"
    user_alice="alice-secret";
};
```
3. Настройка клиента:
```properties
security.protocol=SASL_PLAINTEXT
sasl.mechanism=PLAIN
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="alice" password="alice-secret";
```

### Карточка 19: ACL в Kafka
**Вопрос**: Как работают ACL в Kafka?

**Ответ**: Access Control Lists позволяют:
- Контролировать доступ к топикам
- Управлять правами на чтение/запись
- Настраивать права для групп потребителей

Пример команд:
```bash
# Добавление ACL
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 \
    --add --allow-principal User:Alice \
    --operation Read --topic test-topic

# Просмотр ACL
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 \
    --list --topic test-topic
```

## Интеграция и расширения

### Карточка 20: Spring Kafka
**Вопрос**: Как использовать Kafka в Spring Boot приложении?

**Ответ**: Пример интеграции:
```java
@Configuration
public class KafkaConfig {
    @Bean
    public ProducerFactory<String, String> producerFactory() {
        Map<String, Object> config = new HashMap<>();
        config.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        config.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        config.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        return new DefaultKafkaProducerFactory<>(config);
    }

    @Bean
    public KafkaTemplate<String, String> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
}

@Service
public class KafkaProducer {
    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    public void sendMessage(String topic, String message) {
        kafkaTemplate.send(topic, message);
    }
}

@Service
public class KafkaConsumer {
    @KafkaListener(topics = "topic-name", groupId = "group-id")
    public void listen(String message) {
        System.out.println("Received message: " + message);
    }
}
```

### Карточка 21: Schema Registry
**Вопрос**: Что такое Schema Registry и как его использовать?

**Ответ**: Schema Registry - это сервис для управления схемами Avro/Protobuf/JSON.

Пример использования с Avro:
```java
// Настройка Producer
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", StringSerializer.class);
props.put("value.serializer", KafkaAvroSerializer.class);
props.put("schema.registry.url", "http://localhost:8081");

// Определение схемы
String userSchema = "{\"type\":\"record\"," +
                   "\"name\":\"User\"," +
                   "\"fields\":[" +
                   "{\"name\":\"name\",\"type\":\"string\"}," +
                   "{\"name\":\"age\",\"type\":\"int\"}]}";

// Создание объекта
Schema.Parser parser = new Schema.Parser();
Schema schema = parser.parse(userSchema);
GenericRecord user = new GenericData.Record(schema);
user.put("name", "John");
user.put("age", 25);

// Отправка
ProducerRecord<String, GenericRecord> record = 
    new ProducerRecord<>("users", user);
producer.send(record);
```

### Карточка 22: Kafka Connect
**Вопрос**: Как использовать Kafka Connect?

**Ответ**: Kafka Connect - это фреймворк для интеграции с внешними системами.

Пример конфигурации Source Connector (JDBC):
```json
{
    "name": "jdbc-source",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
        "connection.url": "jdbc:mysql://localhost:3306/test",
        "connection.user": "user",
        "connection.password": "password",
        "topic.prefix": "mysql-",
        "mode": "incrementing",
        "incrementing.column.name": "id",
        "table.whitelist": "users"
    }
}
```

Пример REST API для управления:
```bash
# Создание коннектора
curl -X POST -H "Content-Type: application/json" \
    --data @connector-config.json \
    http://localhost:8083/connectors

# Просмотр статуса
curl http://localhost:8083/connectors/jdbc-source/status
```

### Карточка 23: KSQL
**Вопрос**: Что такое KSQL и как его использовать?

**Ответ**: KSQL - это SQL движок для обработки потоков данных.

Примеры запросов:
```sql
-- Создание потока
CREATE STREAM users (
    id BIGINT,
    name VARCHAR,
    email VARCHAR
) WITH (
    kafka_topic='users',
    value_format='JSON',
    partitions=1
);

-- Создание материализованного представления
CREATE TABLE user_counts AS
    SELECT name, COUNT(*) AS count
    FROM users
    WINDOW TUMBLING (SIZE 1 MINUTE)
    GROUP BY name;

-- Фильтрация данных
CREATE STREAM important_users AS
    SELECT *
    FROM users
    WHERE id > 1000;
```

### Карточка 24: Мониторинг JMX
**Вопрос**: Как настроить мониторинг Kafka через JMX?

**Ответ**: 
1. Включение JMX:
```bash
export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9999
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false"
```

2. Основные метрики:
```
# Брокер
kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec

# Producer
kafka.producer:type=producer-metrics,client-id=*

# Consumer
kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*
```

3. Интеграция с Prometheus:
```yaml
jmx_exporter_config.yaml:
rules:
  - pattern: "kafka.server<type=BrokerTopicMetrics, name=(.+)><>Count"
    name: kafka_server_brokertopicmetrics_$1_count
  - pattern: "kafka.server<type=BrokerTopicMetrics, name=(.+)><>FifteenMinuteRate"
    name: kafka_server_brokertopicmetrics_$1_fifteen_minute_rate
```

### Карточка 25: Kafka Streams Processors
**Вопрос**: Как создавать пользовательские процессоры в Kafka Streams?

**Ответ**: Пример создания процессора:
```java
public class CustomProcessor implements Processor<String, String> {
    private ProcessorContext context;
    private KeyValueStore<String, Long> kvStore;

    @Override
    public void init(ProcessorContext context) {
        this.context = context;
        this.kvStore = (KeyValueStore<String, Long>) context
            .getStateStore("Counts");
    }

    @Override
    public void process(String key, String value) {
        Long count = kvStore.get(key);
        if (count == null) {
            count = 0L;
        }
        kvStore.put(key, count + 1);
        
        // Пересылка обработанного сообщения
        context.forward(key, "Processed: " + value);
    }

    @Override
    public void close() {
        // Очистка ресурсов
    }
}

// Использование:
Topology topology = new Topology();
topology.addSource("Source", "input-topic")
        .addProcessor("Process", CustomProcessor::new, "Source")
        .addStateStore(
            Stores.keyValueStoreBuilder(
                Stores.persistentKeyValueStore("Counts"),
                Serdes.String(),
                Serdes.Long()
            ),
            "Process"
        )
        .addSink("Sink", "output-topic", "Process");
```

### Карточка 26: Партиционирование
**Вопрос**: Как работает пользовательское партиционирование?

**Ответ**: Пример реализации партиционера:
```java
public class CustomPartitioner implements Partitioner {
    @Override
    public int partition(
        String topic, Object key, byte[] keyBytes,
        Object value, byte[] valueBytes, Cluster cluster
    ) {
        List<PartitionInfo> partitions = cluster.partitionsForTopic(topic);
        int numPartitions = partitions.size();
        
        if (keyBytes == null) {
            return Utils.toPositive(Utils.murmur2(valueBytes)) % numPartitions;
        }
        
        // Пользовательская логика партиционирования
        if (key.toString().startsWith("A")) {
            return 0;
        } else if (key.toString().startsWith("B")) {
            return 1;
        }
        
        return Utils.toPositive(Utils.murmur2(keyBytes)) % numPartitions;
    }

    @Override
    public void close() {}

    @Override
    public void configure(Map<String, ?> configs) {}
}

// Использование:
Properties props = new Properties();
props.put("partitioner.class", CustomPartitioner.class.getName());
```

## Производительность и оптимизация

### Карточка 27: Оптимизация Producer
**Вопрос**: Какие основные параметры влияют на производительность Producer?

**Ответ**: Ключевые параметры:
1. `batch.size`: Размер батча (по умолчанию 16KB)
```properties
batch.size=32768 # Увеличение для лучшей пропускной способности
```

2. `linger.ms`: Время ожидания заполнения батча
```properties
linger.ms=100 # Увеличение для лучшей компрессии
```

3. `compression.type`: Тип сжатия
```properties
compression.type=snappy # Варианты: none, gzip, snappy, lz4, zstd
```

4. `buffer.memory`: Размер буфера Producer
```properties
buffer.memory=67108864 # 64MB по умолчанию
```

### Карточка 28: Оптимизация Consumer
**Вопрос**: Как оптимизировать производительность Consumer?

**Ответ**: Основные настройки:
1. `fetch.min.bytes` и `fetch.max.bytes`:
```properties
fetch.min.bytes=1048576 # 1MB
fetch.max.bytes=52428800 # 50MB
```

2. `max.poll.records`:
```properties
max.poll.records=500 # Количество записей за один poll()
```

3. `enable.auto.commit` и `auto.commit.interval.ms`:
```properties
enable.auto.commit=false # Ручное управление коммитами
auto.commit.interval.ms=5000 # Интервал автокоммита
```

### Карточка 29: Оптимизация брокера
**Вопрос**: Какие параметры брокера важны для производительности?

**Ответ**: Ключевые настройки брокера:
```properties
# Диск и I/O
num.io.threads=8
num.network.threads=3
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400

# Размер сегмента
log.segment.bytes=1073741824

# Очистка
log.retention.hours=168
log.retention.bytes=1073741824

# Репликация
num.replica.fetchers=4
replica.fetch.max.bytes=1048576
```

### Карточка 30: Мониторинг производительности
**Вопрос**: Какие метрики важны для мониторинга производительности?

**Ответ**: Основные метрики:
1. Producer метрики:
```
record-error-rate
record-retry-rate
request-latency-avg
batch-size-avg
```

2. Consumer метрики:
```
records-lag-max
fetch-rate
bytes-consumed-rate
records-per-request-avg
```

3. Брокер метрики:
```
UnderReplicatedPartitions
RequestHandlerAvgIdlePercent
LogFlushRateAndTimeMs
```

### Карточка 31: Паттерны обработки сообщений
**Вопрос**: Какие существуют паттерны обработки сообщений в Kafka?

**Ответ**: Основные паттерны:
1. Fan-out (один-ко-многим):
```java
// Producer отправляет в один топик
producer.send(new ProducerRecord<>("input-topic", message));

// Множество Consumer Groups читают
@KafkaListener(topics = "input-topic", groupId = "group1")
public void consume1(String message) { ... }

@KafkaListener(topics = "input-topic", groupId = "group2")
public void consume2(String message) { ... }
```

2. Fan-in (многие-к-одному):
```java
// Разные Producer пишут в один топик
producer1.send(new ProducerRecord<>("output-topic", "source1-" + message));
producer2.send(new ProducerRecord<>("output-topic", "source2-" + message));

// Один Consumer читает все
@KafkaListener(topics = "output-topic", groupId = "aggregator")
public void aggregateMessages(String message) { ... }
```

### Карточка 32: Обработка ошибок
**Вопрос**: Какие паттерны обработки ошибок существуют в Kafka?

**Ответ**: Основные паттерны:
1. Dead Letter Queue:
```java
@KafkaListener(topics = "main-topic")
public void processMessage(String message) {
    try {
        // Обработка сообщения
        processData(message);
    } catch (Exception e) {
        // Отправка в DLQ
        kafkaTemplate.send("dead-letter-topic", message);
        // Сохранение информации об ошибке
        saveError(message, e);
    }
}
```

2. Retry Topic:
```java
@Configuration
public class RetryConfig {
    @Bean
    public RetryTopicConfiguration retryTopicConfiguration(
            KafkaTemplate<String, String> template) {
        return RetryTopicConfigurationBuilder
            .newInstance()
            .fixedBackOff(3000) // 3 секунды между попытками
            .maxAttempts(3)
            .includeTopics("main-topic")
            .build();
    }
}
```

### Карточка 33: Тестирование Kafka приложений
**Вопрос**: Как тестировать приложения с Kafka?

**Ответ**: Примеры тестов:
1. Модульное тестирование с EmbeddedKafka:
```java
@SpringBootTest
@EmbeddedKafka(partitions = 1, topics = {"test-topic"})
class KafkaTest {
    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;
    
    @Autowired
    private Consumer consumer;
    
    @Test
    void testKafkaFlow() {
        // Отправка сообщения
        kafkaTemplate.send("test-topic", "test-message");
        
        // Проверка получения
        ConsumerRecord<String, String> record = KafkaTestUtils
            .getSingleRecord(consumer, "test-topic");
        assertEquals("test-message", record.value());
    }
}
```

2. Интеграционное тестирование:
```java
@TestConfiguration
public class KafkaTestConfig {
    @Bean
    public ConsumerFactory<String, String> consumerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, 
                 kafka.getBootstrapServers());
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        return new DefaultKafkaConsumerFactory<>(props);
    }
}

@Test
void testEndToEnd() {
    // Отправка сообщения
    producer.sendMessage("test-data");
    
    // Ожидание обработки
    await()
        .atMost(5, TimeUnit.SECONDS)
        .until(() -> messageProcessor.getProcessedCount() > 0);
    
    // Проверка результата
    verify(messageHandler).handleMessage(any());
}
```

### Карточка 34: Масштабирование Kafka
**Вопрос**: Какие существуют стратегии масштабирования Kafka?

**Ответ**: Основные стратегии:
1. Горизонтальное масштабирование брокеров:
```bash
# Добавление нового брокера
broker.id=3
listeners=PLAINTEXT://new-broker:9092
log.dirs=/kafka/kafka-logs-3
```

2. Репартиционирование:
```json
{
    "version": 1,
    "partitions": [
        {"topic": "my-topic", "partition": 0, "replicas": [1,2,3]},
        {"topic": "my-topic", "partition": 1, "replicas": [2,3,1]},
        {"topic": "my-topic", "partition": 2, "replicas": [3,1,2]}
    ]
}
```

3. Масштабирование Consumer Group:
```java
@KafkaListener(
    topics = "high-volume-topic",
    concurrency = "3" // Параллельная обработка
)
public void processMessages(String message) {
    // Обработка сообщения
}
```

### Карточка 35: Kafka Streams DSL
**Вопрос**: Какие основные операции доступны в Kafka Streams DSL?

**Ответ**: Примеры операций:
```java
StreamsBuilder builder = new StreamsBuilder();

// Фильтрация
KStream<String, String> filtered = builder
    .stream("input-topic")
    .filter((key, value) -> value.contains("important"));

// Маппинг
KStream<String, Integer> mapped = builder
    .stream("input-topic")
    .mapValues(value -> value.length());

// Агрегация
KTable<String, Long> counted = builder
    .stream("input-topic")
    .groupByKey()
    .count();

// Объединение потоков
KStream<String, String> joined = stream1
    .join(
        stream2,
        (value1, value2) -> value1 + value2,
        JoinWindows.of(Duration.ofMinutes(5))
    );

// Windowing
TimeWindowedKStream<String, String> windowed = stream
    .groupByKey()
    .windowedBy(TimeWindows.of(Duration.ofMinutes(5)));
```

### Карточка 36: Интеграция с внешними системами
**Вопрос**: Как интегрировать Kafka с различными внешними системами?

**Ответ**: Примеры интеграций:
1. Elasticsearch:
```json
{
    "name": "elastic-sink",
    "config": {
        "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
        "topics": "my-topic",
        "connection.url": "http://elasticsearch:9200",
        "type.name": "kafka-connect",
        "key.ignore": "true",
        "schema.ignore": "true"
    }
}
```

2. MongoDB:
```json
{
    "name": "mongo-sink",
    "config": {
        "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
        "topics": "my-topic",
        "connection.uri": "mongodb://localhost:27017",
        "database": "mydb",
        "collection": "mycollection"
    }
}
```

3. JDBC (MySQL):
```json
{
    "name": "jdbc-source",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
        "connection.url": "jdbc:mysql://localhost:3306/test",
        "mode": "timestamp",
        "timestamp.column.name": "modified_date",
        "topic.prefix": "mysql-"
    }
}
```

## Администрирование и управление

### Карточка 37: Управление топиками
**Вопрос**: Какие основные операции доступны для управления топиками?

**Ответ**: Основные команды:
```bash
# Создание топика
kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --topic my-topic \
    --partitions 3 \
    --replication-factor 2 \
    --config retention.ms=604800000

# Изменение конфигурации
kafka-configs.sh --bootstrap-server localhost:9092 \
    --entity-type topics \
    --entity-name my-topic \
    --alter \
    --add-config max.message.bytes=1048576

# Добавление партиций
kafka-topics.sh --bootstrap-server localhost:9092 \
    --topic my-topic \
    --alter \
    --partitions 6

# Просмотр деталей
kafka-topics.sh --bootstrap-server localhost:9092 \
    --topic my-topic \
    --describe
```

### Карточка 38: Управление Consumer Groups
**Вопрос**: Как управлять Consumer Groups?

**Ответ**: Основные операции:
```bash
# Просмотр групп
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
    --list

# Описание группы
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
    --describe \
    --group my-group

# Сброс офсетов
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
    --group my-group \
    --topic my-topic \
    --reset-offsets \
    --to-earliest \
    --execute

# Удаление группы
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
    --delete \
    --group my-group
```

### Карточка 39: Мониторинг и алертинг
**Вопрос**: Как организовать мониторинг и алертинг в Kafka?

**Ответ**: Пример конфигурации:
1. Prometheus конфигурация:
```yaml
scrape_configs:
  - job_name: 'kafka'
    static_configs:
      - targets: ['kafka:7071']
    metrics_path: '/metrics'

rules:
  - alert: KafkaHighLag
    expr: kafka_consumer_group_lag > 10000
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High consumer lag"
      description: "Consumer group {{ $labels.group }} lag is high"
```

2. Grafana дашборд:
```json
{
  "panels": [
    {
      "title": "Consumer Lag",
      "targets": [
        {
          "expr": "kafka_consumer_group_lag",
          "legendFormat": "{{group}}"
        }
      ]
    },
    {
      "title": "Producer Rate",
      "targets": [
        {
          "expr": "rate(kafka_producer_record_send_total[5m])",
          "legendFormat": "{{topic}}"
        }
      ]
    }
  ]
}
```

### Карточка 40: Резервное копирование и восстановление
**Вопрос**: Как организовать бэкап и восстановление данных в Kafka?

**Ответ**: Основные подходы:
1. Копирование логов:
```bash
# Остановка записи в партицию
kafka-topics.sh --bootstrap-server localhost:9092 \
    --topic my-topic \
    --alter \
    --config segment.bytes=1

# Копирование файлов
tar -czf backup.tar.gz /kafka/kafka-logs/my-topic-*

# Восстановление
tar -xzf backup.tar.gz -C /kafka/kafka-logs/
```

2. Mirror Maker 2:
```properties
# connect-mirror-maker.properties
clusters=source, destination
source.bootstrap.servers=source-kafka:9092
destination.bootstrap.servers=destination-kafka:9092
source->destination.enabled=true
topics=.*
groups=.*

# Запуск
connect-mirror-maker.sh connect-mirror-maker.properties
```

### Карточка 41: Безопасность и аудит
**Вопрос**: Как настроить аудит и безопасность в Kafka?

**Ответ**: Основные настройки:
1. Аудит через Interceptor:
```java
public class AuditInterceptor implements ProducerInterceptor<String, String> {
    @Override
    public ProducerRecord<String, String> onSend(
            ProducerRecord<String, String> record) {
        logAudit("SEND", record.topic(), record.key(), 
                 record.value(), record.partition());
        return record;
    }

    private void logAudit(String operation, String topic, 
                         String key, String value, Integer partition) {
        String auditMessage = String.format(
            "Operation: %s, Topic: %s, Key: %s, Partition: %d",
            operation, topic, key, partition
        );
        // Запись в лог аудита
        auditLogger.info(auditMessage);
    }
}

// Использование:
properties.put(ProducerConfig.INTERCEPTOR_CLASSES_CONFIG,
              AuditInterceptor.class.getName());
```

2. Шифрование данных:
```java
public class EncryptionSerializer implements Serializer<String> {
    private final Cipher cipher;
    private final SecretKey secretKey;

    @Override
    public byte[] serialize(String topic, String data) {
        try {
            cipher.init(Cipher.ENCRYPT_MODE, secretKey);
            return cipher.doFinal(data.getBytes());
        } catch (Exception e) {
            throw new SerializationException("Error encrypting data", e);
        }
    }
}
```

### Карточка 42: Микросервисная архитектура
**Вопрос**: Как использовать Kafka в микросервисной архитектуре?

**Ответ**: Примеры паттернов:
1. Saga Pattern:
```java
@Service
public class OrderSaga {
    @KafkaListener(topics = "order-created")
    public void handleOrderCreated(OrderCreatedEvent event) {
        try {
            // Резервирование товара
            inventoryService.reserve(event.getOrderId());
            kafkaTemplate.send("inventory-reserved", 
                new InventoryReservedEvent(event.getOrderId()));
        } catch (Exception e) {
            // Компенсирующая транзакция
            kafkaTemplate.send("order-cancelled", 
                new OrderCancelledEvent(event.getOrderId()));
        }
    }

    @KafkaListener(topics = "payment-processed")
    public void handlePaymentProcessed(PaymentProcessedEvent event) {
        // Завершение заказа
        orderService.complete(event.getOrderId());
    }
}
```

2. Event Sourcing:
```java
@Service
public class OrderEventSourcing {
    @KafkaListener(topics = "order-events")
    public void handleOrderEvent(OrderEvent event) {
        switch (event.getType()) {
            case CREATED:
                orderRepository.save(new Order(event.getOrderId()));
                break;
            case ITEM_ADDED:
                Order order = orderRepository.findById(event.getOrderId());
                order.addItem(event.getItem());
                orderRepository.save(order);
                break;
            case STATUS_CHANGED:
                order = orderRepository.findById(event.getOrderId());
                order.setStatus(event.getStatus());
                orderRepository.save(order);
                break;
        }
    }
}
```

### Карточка 43: Обработка больших данных
**Вопрос**: Как использовать Kafka для обработки больших данных?

**Ответ**: Примеры интеграций:
1. Spark Streaming:
```scala
val spark = SparkSession.builder()
    .appName("KafkaSparkStreaming")
    .getOrCreate()

val kafkaStream = spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "input-topic")
    .load()

val query = kafkaStream
    .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    .writeStream
    .outputMode("append")
    .format("console")
    .start()
```

2. Flink:
```java
StreamExecutionEnvironment env = 
    StreamExecutionEnvironment.getExecutionEnvironment();

FlinkKafkaConsumer<String> consumer = 
    new FlinkKafkaConsumer<>("input-topic", 
                            new SimpleStringSchema(), 
                            properties);

DataStream<String> stream = env.addSource(consumer);

stream.map(new MapFunction<String, String>() {
    @Override
    public String map(String value) {
        return value.toUpperCase();
    }
}).addSink(new FlinkKafkaProducer<>("output-topic",
                                   new SimpleStringSchema(),
                                   properties));
```

### Карточка 44: Форматы данных
**Вопрос**: Какие форматы данных можно использовать в Kafka?

**Ответ**: Примеры работы с разными форматами:
1. Avro:
```java
// Схема Avro
String schema = "{\"type\":\"record\"," +
                "\"name\":\"Customer\"," +
                "\"fields\":[" +
                  "{\"name\":\"id\",\"type\":\"int\"}," +
                  "{\"name\":\"name\",\"type\":\"string\"}," +
                  "{\"name\":\"email\",\"type\":\"string\"}" +
                "]}";

// Сериализация
props.put("key.serializer", 
         "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("value.serializer", 
         "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("schema.registry.url", "http://localhost:8081");
```

2. Protobuf:
```protobuf
message Customer {
    int32 id = 1;
    string name = 2;
    string email = 3;
}

// Использование
props.put("key.serializer", 
         "io.confluent.kafka.serializers.protobuf.KafkaProtobufSerializer");
props.put("value.serializer", 
         "io.confluent.kafka.serializers.protobuf.KafkaProtobufSerializer");
```

3. JSON Schema:
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["id", "name", "email"]
}
```

### Карточка 45: Kafka Streams Продвинутые темы
**Вопрос**: Какие продвинутые возможности есть в Kafka Streams?

**Ответ**: Примеры:
1. Интерактивные запросы:
```java
@RestController
public class StreamsController {
    private final KafkaStreams streams;
    
    @GetMapping("/count/{word}")
    public Long getWordCount(@PathVariable String word) {
        ReadOnlyKeyValueStore<String, Long> store =
            streams.store(
                StoreQueryParameters.fromNameAndType(
                    "counts",
                    QueryableStoreTypes.keyValueStore()
                )
            );
        return store.get(word);
    }
}
```

2. Пользовательские окна:
```java
public class CustomWindows 
    extends Windows<TimeWindow> {
    
    @Override
    public Map<Long, TimeWindow> windowsFor(long timestamp) {
        // Пользовательская логика создания окон
        long windowStart = timestamp - size;
        return Collections.singletonMap(
            windowStart,
            new TimeWindow(windowStart, timestamp)
        );
    }
}
```

### Карточка 46: Отказоустойчивость
**Вопрос**: Как обеспечить отказоустойчивость в Kafka?

**Ответ**: Основные механизмы:
1. Репликация и ISR:
```properties
# Настройки брокера
min.insync.replicas=2
unclean.leader.election.enable=false

# Настройки Producer
acks=all
retries=3
retry.backoff.ms=100
```

2. Обработка сбоев:
```java
@KafkaListener(topics = "important-topic")
public void processMessage(
        ConsumerRecord<String, String> record,
        Acknowledgment ack) {
    try {
        // Обработка сообщения
        processData(record.value());
        
        // Подтверждение обработки
        ack.acknowledge();
    } catch (RetryableException e) {
        // Повторная попытка
        throw new RetryTopicException();
    } catch (Exception e) {
        // Отправка в DLQ
        kafkaTemplate.send("dead-letter-queue", record.value());
        ack.acknowledge();
    }
}
```

3. Мониторинг здоровья:
```java
@Component
public class KafkaHealthIndicator 
    extends AbstractHealthIndicator {
    
    @Override
    protected void doHealthCheck(Builder builder) {
        try {
            AdminClient admin = AdminClient.create(props);
            admin.describeCluster()
                .nodes()
                .get(5, TimeUnit.SECONDS);
            
            builder.up()
                   .withDetail("cluster", "OK");
        } catch (Exception e) {
            builder.down()
                   .withException(e);
        }
    }
} 