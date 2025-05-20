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
4. Абстракция помогает создавать четкие контракты между компонентами системы""",
        points=0
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

3. Решение проблемы гонки:
```java
public class BankAccount {
    private final ReentrantLock lock = new ReentrantLock();
    private double balance;
    
    public void transfer(BankAccount to, double amount) {
        lock.lock();
        try {
            this.balance -= amount;
            to.balance += amount;
        } finally {
            lock.unlock();
        }
    }
}
```

4. Использование ConcurrentHashMap:
```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("key1", 1);
map.putIfAbsent("key2", 2);
map.computeIfPresent("key1", (k, v) -> v + 1);
```

5. Ожидание завершения потоков:
```java
CountDownLatch latch = new CountDownLatch(3);

for (int i = 0; i < 3; i++) {
    executor.submit(() -> {
        try {
            // Выполнение задачи
        } finally {
            latch.countDown();
        }
    });
}

latch.await(); // Ожидание завершения всех задач
```

Практические советы:
1. Используйте ExecutorService вместо прямого создания потоков
2. Применяйте атомарные операции вместо synchronized где возможно
3. Используйте потокобезопасные коллекции
4. Избегайте блокировок и предпочитайте неблокирующие алгоритмы
5. Всегда освобождайте ресурсы в блоке finally""",
        points=0
    )
] 