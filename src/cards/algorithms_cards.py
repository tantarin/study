from src.models import Question

ALGORITHMS_CARDS = [
    Question(
        text="Сложность алгоритмов",
        theory="""Сложность алгоритмов - это оценка эффективности алгоритма:

1. Временная сложность:
- O(1) - константное время
- O(log n) - логарифмическое время
- O(n) - линейное время
- O(n log n) - линейно-логарифмическое время
- O(n²) - квадратичное время
- O(2ⁿ) - экспоненциальное время

2. Пространственная сложность:
- Дополнительная память
- Входные данные
- Выходные данные

3. Анализ алгоритмов:
- Худший случай
- Лучший случай
- Средний случай""",
        theory_summary="Сложность алгоритмов определяет эффективность использования времени и памяти.",
        correct_answer="""Сложность алгоритмов - это оценка эффективности алгоритма, которая показывает, как быстро растет время выполнения или объем используемой памяти при увеличении размера входных данных.

Основные типы временной сложности:
1. O(1) - константное время (доступ к элементу массива)
2. O(log n) - логарифмическое время (бинарный поиск)
3. O(n) - линейное время (линейный поиск)
4. O(n log n) - линейно-логарифмическое время (сортировка слиянием)
5. O(n²) - квадратичное время (пузырьковая сортировка)
6. O(2ⁿ) - экспоненциальное время (рекурсивный Фибоначчи)

Пространственная сложность показывает, сколько дополнительной памяти требуется алгоритму для работы.""",
        options=[],
        explanation="""Примеры сложности алгоритмов:

1. O(1) - константное время:
```java
int getFirstElement(int[] array) {
    return array[0];  // Всегда одно действие
}
```

2. O(log n) - бинарный поиск:
```java
int binarySearch(int[] array, int target) {
    int left = 0;
    int right = array.length - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (array[mid] == target) return mid;
        if (array[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

3. O(n) - линейный поиск:
```java
int linearSearch(int[] array, int target) {
    for (int i = 0; i < array.length; i++) {
        if (array[i] == target) return i;
    }
    return -1;
}
```

4. O(n log n) - сортировка слиянием:
```java
void mergeSort(int[] array, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(array, left, mid);
        mergeSort(array, mid + 1, right);
        merge(array, left, mid, right);
    }
}
```

5. O(n²) - пузырьковая сортировка:
```java
void bubbleSort(int[] array) {
    for (int i = 0; i < array.length - 1; i++) {
        for (int j = 0; j < array.length - i - 1; j++) {
            if (array[j] > array[j + 1]) {
                int temp = array[j];
                array[j] = array[j + 1];
                array[j + 1] = temp;
            }
        }
    }
}
```""",
        points=0
    ),
    Question(
        text="Структуры данных",
        theory="""Структуры данных - это способы организации и хранения данных:

1. Линейные структуры:
- Массивы
- Связные списки
- Стеки
- Очереди

2. Древовидные структуры:
- Бинарные деревья
- Деревья поиска
- Красно-черные деревья
- B-деревья

3. Хеш-таблицы:
- Хеширование
- Разрешение коллизий
- Динамическое расширение

4. Графы:
- Списки смежности
- Матрицы смежности
- Алгоритмы обхода""",
        theory_summary="Структуры данных определяют эффективность операций с данными.",
        correct_answer="""Структуры данных - это способы организации и хранения данных в памяти компьютера. Выбор правильной структуры данных критически важен для эффективности алгоритмов.

Основные категории структур данных:

1. Линейные структуры:
- Массивы: фиксированный размер, быстрый доступ по индексу
- Связные списки: динамический размер, быстрая вставка/удаление
- Стеки: LIFO (Last In, First Out)
- Очереди: FIFO (First In, First Out)

2. Древовидные структуры:
- Бинарные деревья: каждый узел имеет не более двух потомков
- Деревья поиска: упорядоченное хранение данных
- Красно-черные деревья: самобалансирующиеся деревья
- B-деревья: оптимизированы для работы с диском

3. Хеш-таблицы:
- Быстрый поиск по ключу
- Разрешение коллизий (цепочки, открытая адресация)
- Динамическое расширение при необходимости

4. Графы:
- Представление связей между объектами
- Списки смежности: эффективны для разреженных графов
- Матрицы смежности: эффективны для плотных графов""",
        options=[],
        explanation="""Примеры реализации структур данных:

1. Связный список:
```java
class Node {
    int data;
    Node next;
    
    Node(int data) {
        this.data = data;
        this.next = null;
    }
}

class LinkedList {
    Node head;
    
    void add(int data) {
        Node newNode = new Node(data);
        if (head == null) {
            head = newNode;
            return;
        }
        Node current = head;
        while (current.next != null) {
            current = current.next;
        }
        current.next = newNode;
    }
}
```

2. Бинарное дерево поиска:
```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    
    TreeNode(int val) {
        this.val = val;
    }
}

class BinarySearchTree {
    TreeNode root;
    
    TreeNode insert(TreeNode root, int val) {
        if (root == null) {
            return new TreeNode(val);
        }
        if (val < root.val) {
            root.left = insert(root.left, val);
        } else if (val > root.val) {
            root.right = insert(root.right, val);
        }
        return root;
    }
}
```

3. Хеш-таблица:
```java
class HashMap<K, V> {
    private static final int CAPACITY = 16;
    private Node<K, V>[] buckets;
    
    static class Node<K, V> {
        K key;
        V value;
        Node<K, V> next;
        
        Node(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }
    
    public void put(K key, V value) {
        int index = getIndex(key);
        Node<K, V> node = new Node<>(key, value);
        if (buckets[index] == null) {
            buckets[index] = node;
        } else {
            Node<K, V> current = buckets[index];
            while (current.next != null) {
                if (current.key.equals(key)) {
                    current.value = value;
                    return;
                }
                current = current.next;
            }
            current.next = node;
        }
    }
}
```

4. Граф (список смежности):
```java
class Graph {
    private int V;
    private List<List<Integer>> adj;
    
    Graph(int V) {
        this.V = V;
        adj = new ArrayList<>(V);
        for (int i = 0; i < V; i++) {
            adj.add(new ArrayList<>());
        }
    }
    
    void addEdge(int v, int w) {
        adj.get(v).add(w);
        adj.get(w).add(v);  // для неориентированного графа
    }
    
    void BFS(int s) {
        boolean[] visited = new boolean[V];
        Queue<Integer> queue = new LinkedList<>();
        visited[s] = true;
        queue.add(s);
        
        while (!queue.isEmpty()) {
            s = queue.poll();
            System.out.print(s + " ");
            
            for (int n : adj.get(s)) {
                if (!visited[n]) {
                    visited[n] = true;
                    queue.add(n);
                }
            }
        }
    }
}
```""",
        points=0
    )
] 