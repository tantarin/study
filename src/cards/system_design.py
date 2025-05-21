from src.models import Question

SYSTEM_DESIGN_CARDS = [
    Question(
        text="Основы проектирования распределенных систем",
        theory="""# Проектирование распределенных систем

## Ключевые аспекты:

1. **Масштабируемость**
   - Горизонтальная (добавление новых машин)
   - Вертикальная (увеличение мощности существующих машин)
   - Автоматическое масштабирование (Auto-scaling)

2. **Надежность и отказоустойчивость**
   - Репликация данных
   - Резервное копирование
   - Обработка отказов
   - Graceful degradation

3. **Производительность**
   - Латентность (задержка)
   - Пропускная способность
   - Оптимизация запросов
   - Кэширование

4. **Согласованность данных**
   - Eventual Consistency
   - Strong Consistency
   - CAP теорема
   - ACID vs BASE

## Основные компоненты:

1. **Load Balancers**
   - Round Robin
   - Least Connections
   - IP Hash
   - Layer 4 vs Layer 7

2. **Кэширование**
   - CDN
   - Redis/Memcached
   - Application Cache
   - Database Cache

3. **Базы данных**
   - Реляционные vs NoSQL
   - Шардирование
   - Репликация
   - Master-Slave архитектура

4. **Очереди сообщений**
   - Kafka
   - RabbitMQ
   - Асинхронная обработка
   - Event-driven архитектура""",
        theory_summary="Основные принципы и компоненты проектирования распределенных систем",
        correct_answer="",
        options=[],
        explanation="""## Практические примеры

### 1. Проектирование системы с высокой доступностью

```plaintext
                    [DNS + CDN]
                         ↓
                [Load Balancer]
                    ↙     ↘
            [Server1]   [Server2]
                ↘         ↙
            [Database Cluster]
                ↙     ↘
        [Master DB] [Slave DB]
```

Компоненты:
- DNS для геораспределения
- CDN для статического контента
- Load Balancer для распределения нагрузки
- Несколько серверов приложений
- Кластер баз данных с репликацией

### 2. Пример расчета нагрузки

Дано:
- 1 миллион активных пользователей в день
- Каждый пользователь делает 10 запросов в день
- Средний размер запроса: 1KB
- Средний размер ответа: 10KB

Расчет:
```
Запросов в день = 1M * 10 = 10M запросов
Запросов в секунду = 10M / (24 * 3600) ≈ 116 RPS
Входящий трафик = 116 * 1KB ≈ 116KB/s
Исходящий трафик = 116 * 10KB ≈ 1.16MB/s
```

### 3. Обеспечение отказоустойчивости

```java
// Пример реализации Circuit Breaker
public class CircuitBreaker {
    private int failureThreshold;
    private int resetTimeout;
    private int failureCount;
    private long lastFailureTime;
    private State state;
    
    public enum State {
        CLOSED, OPEN, HALF_OPEN
    }
    
    public CircuitBreaker(int failureThreshold, int resetTimeout) {
        this.failureThreshold = failureThreshold;
        this.resetTimeout = resetTimeout;
        this.state = State.CLOSED;
        this.failureCount = 0;
    }
    
    public boolean allowRequest() {
        if (state == State.CLOSED) {
            return true;
        }
        
        if (state == State.OPEN) {
            long currentTime = System.currentTimeMillis();
            if (currentTime - lastFailureTime >= resetTimeout) {
                state = State.HALF_OPEN;
                return true;
            }
            return false;
        }
        
        return true; // HALF_OPEN
    }
    
    public void recordSuccess() {
        failureCount = 0;
        state = State.CLOSED;
    }
    
    public void recordFailure() {
        failureCount++;
        if (failureCount >= failureThreshold) {
            state = State.OPEN;
            lastFailureTime = System.currentTimeMillis();
        }
    }
}
```

### 4. Шардирование данных

```sql
-- Пример шардирования по user_id
CREATE TABLE users_shard_1 (
    user_id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100)
) PARTITION BY RANGE (user_id);

-- Создание шардов
CREATE TABLE users_0000_0999 PARTITION OF users_shard_1
    FOR VALUES FROM (0) TO (1000);
CREATE TABLE users_1000_1999 PARTITION OF users_shard_1
    FOR VALUES FROM (1000) TO (2000);

-- Функция выбора шарда
CREATE OR REPLACE FUNCTION get_shard_id(user_id INT) 
RETURNS INT AS $$
BEGIN
    RETURN user_id / 1000;
END;
$$ LANGUAGE plpgsql;
```

### 5. Балансировка нагрузки

```python
class LoadBalancer:
    def __init__(self):
        self.servers = []
        self.current_index = 0
    
    def add_server(self, server):
        self.servers.append({
            'address': server,
            'health': True,
            'connections': 0
        })
    
    def get_next_server(self):
        # Round Robin с учетом здоровья сервера
        attempts = 0
        while attempts < len(self.servers):
            self.current_index = (self.current_index + 1) % len(self.servers)
            server = self.servers[self.current_index]
            if server['health']:
                server['connections'] += 1
                return server['address']
            attempts += 1
        raise Exception("No healthy servers available")
    
    def mark_server_down(self, server_address):
        for server in self.servers:
            if server['address'] == server_address:
                server['health'] = False
                break
```

### 6. Кэширование

```java
public class CacheManager<K, V> {
    private final Map<K, CacheEntry<V>> cache;
    private final int maxSize;
    private final long ttlMillis;
    
    public CacheManager(int maxSize, long ttlMillis) {
        this.cache = new ConcurrentHashMap<>();
        this.maxSize = maxSize;
        this.ttlMillis = ttlMillis;
    }
    
    public V get(K key) {
        CacheEntry<V> entry = cache.get(key);
        if (entry == null) {
            return null;
        }
        
        if (isExpired(entry)) {
            cache.remove(key);
            return null;
        }
        
        return entry.value;
    }
    
    public void put(K key, V value) {
        if (cache.size() >= maxSize) {
            evictOldest();
        }
        
        cache.put(key, new CacheEntry<>(value));
    }
    
    private boolean isExpired(CacheEntry<V> entry) {
        return System.currentTimeMillis() - entry.timestamp > ttlMillis;
    }
    
    private void evictOldest() {
        K oldestKey = null;
        long oldestTimestamp = Long.MAX_VALUE;
        
        for (Map.Entry<K, CacheEntry<V>> entry : cache.entrySet()) {
            if (entry.getValue().timestamp < oldestTimestamp) {
                oldestTimestamp = entry.getValue().timestamp;
                oldestKey = entry.getKey();
            }
        }
        
        if (oldestKey != null) {
            cache.remove(oldestKey);
        }
    }
    
    private static class CacheEntry<V> {
        final V value;
        final long timestamp;
        
        CacheEntry(V value) {
            this.value = value;
            this.timestamp = System.currentTimeMillis();
        }
    }
}
```

### Рекомендации по проектированию:

1. **Анализ требований**
   - Определите функциональные и нефункциональные требования
   - Оцените ожидаемую нагрузку
   - Определите SLA (доступность, латентность)

2. **Выбор архитектуры**
   - Монолит vs Микросервисы
   - Синхронная vs Асинхронная коммуникация
   - Выбор технологического стека

3. **Проектирование данных**
   - Выбор типа БД (SQL/NoSQL)
   - Схема шардирования
   - Стратегия репликации
   - Политика кэширования

4. **Масштабирование**
   - Определите точки масштабирования
   - Выберите стратегию масштабирования
   - Настройте мониторинг
   - Планируйте capacity

5. **Безопасность**
   - Аутентификация и авторизация
   - Шифрование данных
   - Защита от DDoS
   - Аудит и логирование"""
    ),
    
    Question(
        text="Оценка производительности и ресурсов системы",
        theory="""# Оценка производительности системы

## Ключевые метрики:

1. **Латентность (Latency)**
   - Время отклика (Response Time)
   - Время обработки (Processing Time)
   - Задержка сети (Network Latency)
   - p95, p99 перцентили

2. **Пропускная способность (Throughput)**
   - Запросы в секунду (RPS)
   - Транзакции в секунду (TPS)
   - Байты в секунду (BPS)

3. **Утилизация ресурсов**
   - CPU Usage
   - Memory Usage
   - Disk I/O
   - Network I/O

4. **Масштабируемость**
   - Линейная
   - Суб-линейная
   - Супер-линейная

## Методы оценки:

1. **Нагрузочное тестирование**
   - Stress Testing
   - Load Testing
   - Spike Testing
   - Soak Testing

2. **Профилирование**
   - CPU Profiling
   - Memory Profiling
   - I/O Profiling
   - Network Profiling

3. **Мониторинг**
   - Real-time мониторинг
   - Алертинг
   - Логирование
   - Трейсинг""",
        theory_summary="Методы и метрики оценки производительности распределенных систем",
        correct_answer="",
        options=[],
        explanation="""## Практические примеры

### 1. Расчет ресурсов для веб-приложения

```plaintext
Исходные данные:
- 1M DAU (Daily Active Users)
- 10 действий на пользователя в день
- Средний размер запроса: 1KB
- Средний размер ответа: 10KB
- Хранение данных за 1 год
- Соотношение чтение:запись = 10:1

Расчеты:

1. Запросы:
   RPS = (1M * 10) / (24 * 3600) ≈ 116 RPS

2. Пропускная способность:
   Входящий трафик = 116 * 1KB = 116KB/s
   Исходящий трафик = 116 * 10KB = 1.16MB/s

3. Хранилище:
   Данные в день = 1M * 10 * (1KB + 10KB) = 110GB
   Данные за год = 110GB * 365 = 40.15TB

4. Память:
   Cache hit ratio = 80%
   Активные данные = 20% от общего объема
   RAM = 40.15TB * 0.2 * 0.2 = 1.6TB
```

### 2. Мониторинг производительности

```java
public class PerformanceMonitor {
    private Map<String, Metric> metrics = new ConcurrentHashMap<>();
    
    public void recordLatency(String operation, long startTime) {
        long latency = System.currentTimeMillis() - startTime;
        Metric metric = metrics.computeIfAbsent(operation, 
            k -> new Metric());
        metric.addLatency(latency);
    }
    
    public void recordThroughput(String operation) {
        Metric metric = metrics.computeIfAbsent(operation, 
            k -> new Metric());
        metric.incrementRequests();
    }
    
    private static class Metric {
        private final Queue<Long> latencies = new ConcurrentLinkedQueue<>();
        private final AtomicLong requestCount = new AtomicLong();
        private final AtomicLong totalLatency = new AtomicLong();
        
        public void addLatency(long latency) {
            latencies.offer(latency);
            totalLatency.addAndGet(latency);
            while (latencies.size() > 1000) {
                Long old = latencies.poll();
                if (old != null) {
                    totalLatency.addAndGet(-old);
                }
            }
        }
        
        public void incrementRequests() {
            requestCount.incrementAndGet();
        }
        
        public double getAverageLatency() {
            long count = latencies.size();
            return count > 0 ? totalLatency.get() / (double) count : 0;
        }
        
        public long getRequestCount() {
            return requestCount.get();
        }
    }
}
```

### 3. Нагрузочное тестирование

```java
public class LoadTester {
    private final int numThreads;
    private final int requestsPerThread;
    private final String endpoint;
    
    public LoadTester(int numThreads, int requestsPerThread, 
                     String endpoint) {
        this.numThreads = numThreads;
        this.requestsPerThread = requestsPerThread;
        this.endpoint = endpoint;
    }
    
    public TestResults runTest() throws InterruptedException {
        ExecutorService executor = 
            Executors.newFixedThreadPool(numThreads);
        CountDownLatch latch = new CountDownLatch(numThreads);
        List<Future<ThreadStats>> futures = new ArrayList<>();
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < numThreads; i++) {
            futures.add(executor.submit(() -> {
                ThreadStats stats = new ThreadStats();
                try {
                    for (int j = 0; j < requestsPerThread; j++) {
                        long reqStartTime = System.nanoTime();
                        makeRequest();
                        long latency = System.nanoTime() - reqStartTime;
                        stats.addLatency(latency);
                    }
                } finally {
                    latch.countDown();
                }
                return stats;
            }));
        }
        
        latch.await();
        long totalTime = System.currentTimeMillis() - startTime;
        
        TestResults results = new TestResults();
        for (Future<ThreadStats> future : futures) {
            ThreadStats stats = future.get();
            results.merge(stats);
        }
        
        results.setTotalTime(totalTime);
        return results;
    }
    
    private void makeRequest() {
        // Реализация HTTP запроса
    }
}
```

### 4. Профилирование памяти

```java
public class MemoryProfiler {
    private static final Runtime runtime = Runtime.getRuntime();
    
    public static MemoryStats getMemoryStats() {
        long total = runtime.totalMemory();
        long free = runtime.freeMemory();
        long used = total - free;
        long max = runtime.maxMemory();
        
        return new MemoryStats(total, free, used, max);
    }
    
    public static void logMemoryUsage(String operation) {
        MemoryStats stats = getMemoryStats();
        logger.info("{}: Used={}MB, Free={}MB, Total={}MB, Max={}MB",
            operation,
            stats.getUsed() / 1024 / 1024,
            stats.getFree() / 1024 / 1024,
            stats.getTotal() / 1024 / 1024,
            stats.getMax() / 1024 / 1024);
    }
}
```

### Рекомендации по оценке производительности:

1. **Определение метрик**
   - Выберите ключевые метрики (KPI)
   - Установите целевые значения
   - Определите методы измерения

2. **Нагрузочное тестирование**
   - Создайте реалистичные сценарии
   - Используйте репрезентативные данные
   - Тестируйте граничные случаи

3. **Анализ результатов**
   - Определите узкие места
   - Анализируйте тренды
   - Составьте план оптимизации

4. **Мониторинг**
   - Настройте системы мониторинга
   - Установите алерты
   - Ведите историю изменений"""
    )
] 