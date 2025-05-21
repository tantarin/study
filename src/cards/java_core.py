from src.models import Question

JAVA_CORE_CARDS = [
    Question(
        text="Основные принципы ООП в Java",
        theory="""Объектно-ориентированное программирование в Java основано на четырех основных принципах:

1. Инкапсуляция:
- Скрытие внутренней реализации
- Доступ к данным через методы
- Модификаторы доступа (private, protected, public)
- Геттеры и сеттеры

2. Наследование:
- Переиспользование кода
- Иерархия классов
- Ключевое слово extends
- Переопределение методов

3. Полиморфизм:
- Разные формы одного интерфейса
- Переопределение методов
- Абстрактные классы
- Интерфейсы

4. Абстракция:
- Выделение важных характеристик
- Скрытие деталей реализации
- Абстрактные классы
- Интерфейсы""",
        theory_summary="ООП в Java основано на четырех принципах: инкапсуляция, наследование, полиморфизм и абстракция.",
        correct_answer="",
        options=[],
        explanation="""Давайте разберем каждый принцип на примере:

1. Инкапсуляция:
```java
public class BankAccount {
    private double balance;  // приватное поле
    
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }
    
    public double getBalance() {
        return balance;
    }
}
```

2. Наследование:
```java
public class Animal {
    protected String name;
    
    public void makeSound() {
        System.out.println("Some sound");
    }
}

public class Dog extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Woof!");
    }
}
```

3. Полиморфизм:
```java
public interface Shape {
    double getArea();
}

public class Circle implements Shape {
    private double radius;
    
    @Override
    public double getArea() {
        return Math.PI * radius * radius;
    }
}

public class Rectangle implements Shape {
    private double width;
    private double height;
    
    @Override
    public double getArea() {
        return width * height;
    }
}
```

4. Абстракция:
```java
public abstract class Vehicle {
    protected String brand;
    
    public abstract void start();
    public abstract void stop();
}

public class Car extends Vehicle {
    @Override
    public void start() {
        System.out.println("Car starting...");
    }
    
    @Override
    public void stop() {
        System.out.println("Car stopping...");
    }
}
```

Практическое применение:
1. Инкапсуляция помогает защитить данные от неправильного использования
2. Наследование позволяет переиспользовать код и создавать иерархии классов
3. Полиморфизм делает код более гибким и расширяемым
4. Абстракция помогает создавать четкие контракты между компонентами системы"""
    ),
    
    Question(
        text="Многопоточность в Java",
        theory="""Многопоточность в Java позволяет выполнять несколько задач одновременно:

1. Основные концепции:
- Thread: поток выполнения
- Runnable: интерфейс для создания потоков
- ExecutorService: управление пулом потоков
- Future: результат асинхронной операции

2. Синхронизация:
- synchronized: блокировка
- volatile: видимость изменений
- Atomic классы: атомарные операции
- Lock: интерфейс блокировок

3. Проблемы многопоточности:
- Race condition: состояние гонки
- Deadlock: взаимная блокировка
- Starvation: голодание
- Livelock: активное ожидание

4. Решения:
- Thread-safe коллекции
- ConcurrentHashMap
- BlockingQueue
- CountDownLatch
- CyclicBarrier""",
        theory_summary="Многопоточность в Java обеспечивает параллельное выполнение задач с механизмами синхронизации.",
        correct_answer="",
        options=[],
        explanation="""Давайте разберем многопоточность на практических примерах:

1. Создание и запуск потоков:
```java
// Через Runnable
Runnable task = () -> {
    System.out.println("Выполняется в потоке: " + Thread.currentThread().getName());
};

Thread thread = new Thread(task);
thread.start();

// Через ExecutorService
ExecutorService executor = Executors.newFixedThreadPool(3);
executor.submit(task);
executor.shutdown();
```

2. Синхронизация:
```java
public class Counter {
    private int count = 0;
    private final Object lock = new Object();
    
    public void increment() {
        synchronized(lock) {
            count++;
        }
    }
    
    // Или с использованием AtomicInteger
    private AtomicInteger atomicCount = new AtomicInteger(0);
    
    public void incrementAtomic() {
        atomicCount.incrementAndGet();
    }
}
```

3. Предотвращение deadlock:
```java
public class DeadlockExample {
    private final Lock lock1 = new ReentrantLock();
    private final Lock lock2 = new ReentrantLock();
    
    public void method1() {
        try {
            if (lock1.tryLock(1, TimeUnit.SECONDS)) {
                try {
                    if (lock2.tryLock(1, TimeUnit.SECONDS)) {
                        try {
                            // Критическая секция
                        } finally {
                            lock2.unlock();
                        }
                    }
                } finally {
                    lock1.unlock();
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

4. Использование BlockingQueue:
```java
public class ProducerConsumer {
    private final BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);
    
    public void produce(String item) throws InterruptedException {
        queue.put(item);
    }
    
    public String consume() throws InterruptedException {
        return queue.take();
    }
}
```"""
    ),
    
    Question(
        text="Коллекции в Java",
        theory="""Java Collections Framework предоставляет набор интерфейсов и классов для работы с наборами объектов:

1. List интерфейс:
- ArrayList: динамический массив
- LinkedList: двусвязный список
- Vector: потокобезопасный динамический массив

2. Set интерфейс:
- HashSet: неупорядоченное множество
- TreeSet: отсортированное множество
- LinkedHashSet: упорядоченное по добавлению

3. Map интерфейс:
- HashMap: хеш-таблица
- TreeMap: отсортированная карта
- LinkedHashMap: упорядоченная по добавлению
- ConcurrentHashMap: потокобезопасная

4. Queue и Deque:
- PriorityQueue: очередь с приоритетами
- ArrayDeque: двусторонняя очередь
- LinkedList: реализует оба интерфейса

5. Особенности:
- Generics типизация
- Fail-fast итераторы
- Модификаторы unmodifiable
- Утилитные методы Collections""",
        theory_summary="Java Collections Framework предоставляет различные реализации коллекций для разных задач.",
        correct_answer="",
        options=[],
        explanation="""Рассмотрим примеры использования различных коллекций:

1. ArrayList vs LinkedList:
```java
// ArrayList: быстрый доступ по индексу
List<String> arrayList = new ArrayList<>();
arrayList.add("One");
arrayList.add("Two");
String second = arrayList.get(1); // O(1)

// LinkedList: быстрая вставка/удаление
List<String> linkedList = new LinkedList<>();
linkedList.add("One");
linkedList.addFirst("Zero"); // O(1)
```

2. HashSet vs TreeSet:
```java
// HashSet: быстрый поиск
Set<Integer> hashSet = new HashSet<>();
hashSet.add(3);
hashSet.add(1);
hashSet.add(2);
System.out.println(hashSet); // Порядок не гарантирован

// TreeSet: отсортированное множество
Set<Integer> treeSet = new TreeSet<>();
treeSet.add(3);
treeSet.add(1);
treeSet.add(2);
System.out.println(treeSet); // [1, 2, 3]
```

3. HashMap и его особенности:
```java
Map<String, User> userMap = new HashMap<>();

// Добавление с проверкой
userMap.putIfAbsent("john", new User("John Doe"));

// Получение с дефолтным значением
User user = userMap.getOrDefault("jane", new User("Unknown"));

// Обработка значения
userMap.computeIfPresent("john", (key, oldValue) -> {
    oldValue.incrementLoginCount();
    return oldValue;
});
```

4. PriorityQueue:
```java
// Очередь с приоритетами
PriorityQueue<Task> taskQueue = new PriorityQueue<>((t1, t2) -> 
    Integer.compare(t1.getPriority(), t2.getPriority()));

taskQueue.offer(new Task("Low", 3));
taskQueue.offer(new Task("High", 1));
taskQueue.offer(new Task("Medium", 2));

// Задачи будут извлекаться в порядке приоритета
while (!taskQueue.isEmpty()) {
    Task task = taskQueue.poll();
    System.out.println(task.getName());
}
```

5. Потокобезопасные коллекции:
```java
// ConcurrentHashMap для многопоточной работы
Map<String, Integer> concurrentMap = new ConcurrentHashMap<>();
concurrentMap.put("counter", 0);

// Атомарное обновление
concurrentMap.compute("counter", (key, value) -> value + 1);

// CopyOnWriteArrayList для потокобезопасного списка
List<String> threadSafeList = new CopyOnWriteArrayList<>();
threadSafeList.add("Safe");
```"""
    ),
    
    Question(
        text="Обработка исключений в Java",
        theory="""Механизм обработки исключений в Java:

1. Иерархия исключений:
- Throwable
  - Error: критические ошибки
  - Exception
    - RuntimeException: непроверяемые
    - Checked Exception: проверяемые

2. Ключевые слова:
- try: блок потенциальных исключений
- catch: обработка исключений
- finally: выполняется всегда
- throw: выбрасывание исключения
- throws: объявление исключений

3. Try-with-resources:
- AutoCloseable интерфейс
- Автоматическое закрытие ресурсов
- Множественные ресурсы
- Подавленные исключения

4. Лучшие практики:
- Специфичные исключения
- Правильная иерархия
- Информативные сообщения
- Логирование исключений""",
        theory_summary="Java предоставляет мощный механизм обработки исключительных ситуаций.",
        correct_answer="",
        options=[],
        explanation="""Рассмотрим практические примеры обработки исключений:

1. Базовая обработка исключений:
```java
public class ExceptionExample {
    public void readFile(String path) {
        try {
            BufferedReader reader = new BufferedReader(new FileReader(path));
            String line = reader.readLine();
            System.out.println(line);
        } catch (FileNotFoundException e) {
            System.err.println("Файл не найден: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Ошибка чтения: " + e.getMessage());
        } finally {
            // Всегда выполняется
            System.out.println("Завершение операции");
        }
    }
}
```

2. Try-with-resources:
```java
public class ResourceExample {
    public void copyFile(String src, String dest) {
        try (BufferedReader reader = new BufferedReader(new FileReader(src));
             BufferedWriter writer = new BufferedWriter(new FileWriter(dest))) {
            
            String line;
            while ((line = reader.readLine()) != null) {
                writer.write(line);
                writer.newLine();
            }
        } catch (IOException e) {
            System.err.println("Ошибка копирования: " + e.getMessage());
        }
    }
}
```

3. Создание собственных исключений:
```java
public class BusinessException extends Exception {
    private final ErrorCode code;
    
    public BusinessException(String message, ErrorCode code) {
        super(message);
        this.code = code;
    }
    
    public ErrorCode getCode() {
        return code;
    }
}

public class BusinessService {
    public void processOrder(Order order) throws BusinessException {
        if (order.getAmount() <= 0) {
            throw new BusinessException(
                "Сумма заказа должна быть положительной",
                ErrorCode.INVALID_AMOUNT
            );
        }
    }
}
```

4. Обработка множественных исключений:
```java
public class MultipleExceptionHandler {
    public void process() {
        try {
            // Потенциально опасный код
            riskyOperation();
        } catch (SQLException | IOException e) {
            // Обработка нескольких типов исключений
            logger.error("Ошибка обработки: " + e.getMessage(), e);
            throw new RuntimeException("Ошибка обработки данных", e);
        } catch (Exception e) {
            // Общий обработчик
            logger.error("Неизвестная ошибка: " + e.getMessage(), e);
            throw new RuntimeException("Системная ошибка", e);
        }
    }
}
```

5. Подавление исключений:
```java
public class SuppressedExceptionExample implements AutoCloseable {
    private final String name;
    
    public SuppressedExceptionExample(String name) {
        this.name = name;
    }
    
    @Override
    public void close() throws Exception {
        throw new Exception("Ошибка закрытия: " + name);
    }
    
    public static void main(String[] args) {
        try (SuppressedExceptionExample first = new SuppressedExceptionExample("first");
             SuppressedExceptionExample second = new SuppressedExceptionExample("second")) {
            
            throw new Exception("Основное исключение");
            
        } catch (Exception e) {
            System.err.println("Основное: " + e.getMessage());
            
            // Вывод подавленных исключений
            for (Throwable suppressed : e.getSuppressed()) {
                System.err.println("Подавленное: " + suppressed.getMessage());
            }
        }
    }
}
```"""
    ),
    
    Question(
        text="Stream API в Java",
        theory="""Stream API - мощный инструмент для работы с коллекциями данных:

1. Основные концепции:
- Stream: поток данных
- Pipeline: конвейер операций
- Lazy evaluation: ленивые вычисления
- Terminal operations: терминальные операции

2. Промежуточные операции:
- filter: фильтрация элементов
- map: преобразование элементов
- flatMap: преобразование в поток
- sorted: сортировка
- distinct: уникальные элементы

3. Терминальные операции:
- collect: сбор результатов
- forEach: обход элементов
- reduce: свертка
- count: подсчет элементов
- anyMatch/allMatch/noneMatch

4. Параллельные потоки:
- parallel: параллельная обработка
- sequential: последовательная обработка
- Spliterator: разделение данных""",
        theory_summary="Stream API предоставляет функциональный подход к обработке коллекций.",
        correct_answer="",
        options=[],
        explanation="""Рассмотрим практические примеры использования Stream API:

1. Базовые операции:
```java
List<String> names = Arrays.asList("John", "Jane", "Bob", "Alice");

// Фильтрация и преобразование
List<String> filteredNames = names.stream()
    .filter(name -> name.startsWith("J"))
    .map(String::toUpperCase)
    .collect(Collectors.toList());

// Статистика
IntSummaryStatistics stats = names.stream()
    .mapToInt(String::length)
    .summaryStatistics();
```

2. Сложные преобразования:
```java
class Order {
    private List<OrderItem> items;
    // getters, setters
}

class OrderItem {
    private String name;
    private BigDecimal price;
    // getters, setters
}

// Получение всех товаров из всех заказов
List<String> allItems = orders.stream()
    .flatMap(order -> order.getItems().stream())
    .map(OrderItem::getName)
    .distinct()
    .sorted()
    .collect(Collectors.toList());

// Группировка и подсчет
Map<String, Long> itemCounts = orders.stream()
    .flatMap(order -> order.getItems().stream())
    .collect(Collectors.groupingBy(
        OrderItem::getName,
        Collectors.counting()
    ));
```

3. Reduce операции:
```java
// Сумма чисел
int sum = numbers.stream()
    .reduce(0, Integer::sum);

// Конкатенация строк
String combined = strings.stream()
    .reduce("", (a, b) -> a + "," + b);

// Поиск максимального элемента
Optional<Integer> max = numbers.stream()
    .reduce(Integer::max);
```

4. Параллельная обработка:
```java
// Параллельная обработка большого набора данных
long count = bigList.parallelStream()
    .filter(item -> item.getSize() > 100)
    .map(Item::process)
    .count();

// Кастомный Spliterator
public class CustomSpliterator implements Spliterator<Data> {
    private final List<Data> data;
    private int current = 0;
    
    @Override
    public boolean tryAdvance(Consumer<? super Data> action) {
        if (current < data.size()) {
            action.accept(data.get(current++));
            return true;
        }
        return false;
    }
    
    @Override
    public Spliterator<Data> trySplit() {
        int currentSize = data.size() - current;
        if (currentSize < 10) {
            return null;
        }
        
        int splitPos = current + currentSize / 2;
        Spliterator<Data> spliterator = 
            new CustomSpliterator(data.subList(current, splitPos));
        current = splitPos;
        return spliterator;
    }
}
```"""
    ),
    
    Question(
        text="Garbage Collection в Java",
        theory="""Сборка мусора в Java - автоматическое управление памятью:

1. Основные концепции:
- Heap: куча для объектов
- Young Generation: молодое поколение
- Old Generation: старое поколение
- Метапространство (до Java 8 - PermGen)

2. Алгоритмы GC:
- Serial GC: однопоточный
- Parallel GC: многопоточный
- CMS: параллельная пометка
- G1: сборщик с разбиением на регионы
- ZGC: масштабируемый с малыми паузами

3. Этапы сборки:
- Mark: пометка живых объектов
- Sweep: удаление мертвых объектов
- Compact: уплотнение памяти
- Copy: копирование объектов

4. Настройка:
- Размер поколений
- Пороги сборки
- Выбор сборщика
- Параметры тюнинга""",
        theory_summary="Garbage Collection автоматически управляет памятью в Java, освобождая неиспользуемые объекты.",
        correct_answer="",
        options=[],
        explanation="""Рассмотрим практические аспекты работы с GC:

1. Мониторинг GC:
```java
public class GCMonitoring {
    public static void main(String[] args) {
        // Включение подробного логирования GC
        System.setProperty("java.util.logging.config.file", "logging.properties");
        
        // Добавление обработчика для событий GC
        sun.management.ManagementFactory.getGarbageCollectorMXBeans().forEach(gc ->
            System.out.println(gc.getName() + " collections: " + gc.getCollectionCount())
        );
    }
}
```

2. Правильное освобождение ресурсов:
```java
public class ResourceManager implements AutoCloseable {
    private final List<Resource> resources = new ArrayList<>();
    
    public void addResource(Resource resource) {
        resources.add(resource);
    }
    
    @Override
    public void close() {
        resources.forEach(Resource::close);
        resources.clear();
    }
    
    // Защита от finalize
    @Override
    protected void finalize() {
        try {
            close();
        } finally {
            super.finalize();
        }
    }
}
```

3. Weak References:
```java
public class CacheManager<K, V> {
    private final Map<K, WeakReference<V>> cache = new WeakHashMap<>();
    
    public void put(K key, V value) {
        cache.put(key, new WeakReference<>(value));
    }
    
    public V get(K key) {
        WeakReference<V> ref = cache.get(key);
        if (ref != null) {
            V value = ref.get();
            if (value == null) {
                cache.remove(key);
            }
            return value;
        }
        return null;
    }
}
```

4. Настройка JVM параметров:
```bash
# Пример настройки G1 GC
java -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=200 \
     -XX:ParallelGCThreads=4 \
     -XX:ConcGCThreads=2 \
     -XX:InitiatingHeapOccupancyPercent=45 \
     -Xmx4g \
     -Xms4g \
     -jar application.jar

# Включение GC логирования
java -Xlog:gc*=debug:file=gc.log \
     -XX:+HeapDumpOnOutOfMemoryError \
     -XX:HeapDumpPath=/path/to/dumps \
     -jar application.jar
```

5. Мониторинг утечек памяти:
```java
public class MemoryLeakDetector {
    private static final Runtime runtime = Runtime.getRuntime();
    
    public static void logMemoryStats() {
        long total = runtime.totalMemory();
        long free = runtime.freeMemory();
        long used = total - free;
        
        System.out.printf(
            "Memory - Total: %d MB, Used: %d MB, Free: %d MB%n",
            total / 1024 / 1024,
            used / 1024 / 1024,
            free / 1024 / 1024
        );
    }
    
    public static void forceGC() {
        System.gc();
        Runtime.getRuntime().runFinalization();
        System.gc();
    }
}
```"""
    ),
    
    Question(
        text="Рефлексия в Java",
        theory="""Рефлексия позволяет исследовать и модифицировать программу во время выполнения:

1. Основные возможности:
- Получение информации о классах
- Создание объектов
- Вызов методов
- Доступ к полям
- Работа с аннотациями

2. Классы рефлексии:
- Class: метаданные класса
- Method: информация о методах
- Field: информация о полях
- Constructor: конструкторы
- Annotation: аннотации

3. Применение:
- Фреймворки
- Dependency Injection
- Сериализация
- Тестирование
- Плагины

4. Особенности:
- Производительность
- Безопасность
- Доступ к private членам
- Dynamic Proxy""",
        theory_summary="Рефлексия позволяет динамически исследовать и модифицировать структуру и поведение программы.",
        correct_answer="",
        options=[],
        explanation="""Рассмотрим практические примеры использования рефлексии:

1. Базовая работа с классами:
```java
public class ReflectionExample {
    public static void inspectClass(String className) throws Exception {
        Class<?> clazz = Class.forName(className);
        
        // Получение методов
        Method[] methods = clazz.getDeclaredMethods();
        for (Method method : methods) {
            System.out.println("Method: " + method.getName());
            System.out.println("Return type: " + method.getReturnType());
            System.out.println("Parameters: " + Arrays.toString(method.getParameterTypes()));
        }
        
        // Получение полей
        Field[] fields = clazz.getDeclaredFields();
        for (Field field : fields) {
            System.out.println("Field: " + field.getName());
            System.out.println("Type: " + field.getType());
        }
    }
}
```

2. Создание объектов и вызов методов:
```java
public class DynamicInvoker {
    public static Object createAndInvoke(String className, String methodName, Object... args) 
            throws Exception {
        // Загрузка класса
        Class<?> clazz = Class.forName(className);
        
        // Создание объекта
        Constructor<?> constructor = clazz.getDeclaredConstructor();
        Object instance = constructor.newInstance();
        
        // Поиск метода
        Method method = clazz.getDeclaredMethod(methodName, 
            Arrays.stream(args)
                .map(Object::getClass)
                .toArray(Class[]::new));
        
        // Разрешение доступа к private методам
        method.setAccessible(true);
        
        // Вызов метода
        return method.invoke(instance, args);
    }
}
```

3. Работа с аннотациями:
```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Secured {
    String role() default "USER";
}

public class SecurityAspect {
    public static void checkSecurity(Method method) {
        if (method.isAnnotationPresent(Secured.class)) {
            Secured secured = method.getAnnotation(Secured.class);
            String role = secured.role();
            
            // Проверка прав доступа
            if (!hasRole(role)) {
                throw new SecurityException("Access denied");
            }
        }
    }
}
```

4. Dynamic Proxy:
```java
public interface UserService {
    void createUser(String username);
    User findUser(String username);
}

public class LoggingProxy implements InvocationHandler {
    private final Object target;
    
    public LoggingProxy(Object target) {
        this.target = target;
    }
    
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        System.out.println("Before method: " + method.getName());
        try {
            Object result = method.invoke(target, args);
            System.out.println("After method: " + method.getName());
            return result;
        } catch (Exception e) {
            System.out.println("Exception in method: " + method.getName());
            throw e;
        }
    }
    
    public static UserService createProxy(UserService target) {
        return (UserService) Proxy.newProxyInstance(
            target.getClass().getClassLoader(),
            new Class<?>[] { UserService.class },
            new LoggingProxy(target)
        );
    }
}
```

5. Сканирование пакетов:
```java
public class PackageScanner {
    public static Set<Class<?>> findAnnotatedClasses(String packageName, 
            Class<? extends Annotation> annotation) {
        Set<Class<?>> classes = new HashSet<>();
        String path = packageName.replace('.', '/');
        
        try {
            ClassLoader classLoader = Thread.currentThread().getContextClassLoader();
            Enumeration<URL> resources = classLoader.getResources(path);
            
            while (resources.hasMoreElements()) {
                URL resource = resources.nextElement();
                File directory = new File(resource.getFile());
                
                if (directory.exists()) {
                    String[] files = directory.list();
                    for (String file : files) {
                        if (file.endsWith(".class")) {
                            String className = packageName + '.' + 
                                file.substring(0, file.length() - 6);
                            Class<?> clazz = Class.forName(className);
                            
                            if (clazz.isAnnotationPresent(annotation)) {
                                classes.add(clazz);
                            }
                        }
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        return classes;
    }
}
```"""
    )
] 