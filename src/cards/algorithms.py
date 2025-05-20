from src.models.algorithm import Algorithm, AlgorithmExample

# Примеры для бинарного поиска
BINARY_SEARCH_EXAMPLES = [
    AlgorithmExample(
        input_data="arr = [1, 2, 3, 4, 5, 6, 7, 8, 9], target = 5",
        output_data="4 (индекс элемента 5)",
        explanation="Массив отсортирован, ищем элемент 5. Находим его на позиции 4."
    ),
    AlgorithmExample(
        input_data="arr = [1, 3, 5, 7, 9], target = 4",
        output_data="-1",
        explanation="Элемент 4 отсутствует в массиве."
    )
]

# Коллекция алгоритмов
ALGORITHMS = [
    Algorithm(
        title="Бинарный поиск",
        description="Эффективный алгоритм поиска элемента в отсортированном массиве",
        complexity="Временная сложность: O(log n), Пространственная сложность: O(1)",
        theory="""Бинарный поиск - это эффективный алгоритм поиска элемента в отсортированном массиве.
Алгоритм работает путем многократного деления области поиска пополам.
На каждом шаге:
1. Проверяем средний элемент
2. Если он равен искомому - поиск завершен
3. Если искомый элемент меньше - ищем в левой половине
4. Если больше - ищем в правой половине""",
        visualization_url="https://visualgo.net/en/binarysearch",
        java_code='''public class BinarySearch {
    public static int binarySearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid;
            }
            
            if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1;
    }
}''',
        python_code='''def binary_search(arr: list, target: int) -> int:
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1''',
        leetcode_problems=[
            "704. Binary Search - https://leetcode.com/problems/binary-search/",
            "35. Search Insert Position - https://leetcode.com/problems/search-insert-position/",
            "74. Search a 2D Matrix - https://leetcode.com/problems/search-a-2d-matrix/"
        ],
        examples=BINARY_SEARCH_EXAMPLES,
        category="поиск",
        difficulty="easy"
    ),
    
    Algorithm(
        title="Быстрая сортировка (QuickSort)",
        description="Эффективный алгоритм сортировки массива методом разделяй и властвуй",
        complexity="Среднее время: O(n log n), Худшее время: O(n²), Память: O(log n)",
        theory="""QuickSort - это эффективный алгоритм сортировки, использующий подход "разделяй и властвуй".
Основные шаги:
1. Выбор опорного элемента (pivot)
2. Разделение массива на элементы меньше и больше опорного
3. Рекурсивная сортировка подмассивов
4. Объединение результатов""",
        visualization_url="https://visualgo.net/en/sorting",
        java_code='''public class QuickSort {
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }
    
    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = (low - 1);
        
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;
        
        return i + 1;
    }
}''',
        leetcode_problems=[
            "912. Sort an Array - https://leetcode.com/problems/sort-an-array/",
            "215. Kth Largest Element in an Array - https://leetcode.com/problems/kth-largest-element-in-an-array/"
        ],
        examples=[
            AlgorithmExample(
                input_data="[64, 34, 25, 12, 22, 11, 90]",
                output_data="[11, 12, 22, 25, 34, 64, 90]",
                explanation="Сортировка массива по возрастанию"
            )
        ],
        category="сортировка",
        difficulty="medium"
    )
]

# Добавляем новые алгоритмы в коллекцию
ALGORITHMS.extend([
    Algorithm(
        title="Обход дерева в глубину (DFS)",
        description="Алгоритм обхода или поиска древовидной или графовой структуры данных",
        complexity="Временная сложность: O(V + E), где V - количество вершин, E - количество рёбер",
        theory="""Поиск в глубину (DFS) - это алгоритм для обхода дерева или графа. Алгоритм начинает обход с корневого узла и идет вглубь насколько это возможно по каждой ветви.

Основные шаги:
1. Начать с корневого узла (или любой вершины для графа)
2. Пометить текущий узел как посещенный
3. Рекурсивно обойти все смежные непосещенные узлы
4. Вернуться и продолжить обход необработанных узлов""",
        visualization_url="https://visualgo.net/en/dfsbfs",
        java_code='''public class DFS {
    private List<List<Integer>> adj;
    private boolean[] visited;
    
    public void dfs(int v) {
        visited[v] = true;
        System.out.print(v + " ");
        
        for (int u : adj.get(v)) {
            if (!visited[u]) {
                dfs(u);
            }
        }
    }
}''',
        python_code='''def dfs(graph: Dict[int, List[int]], start: int, visited: Set[int] = None) -> None:
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start, end=' ')
    
    for next_vertex in graph[start]:
        if next_vertex not in visited:
            dfs(graph, next_vertex, visited)''',
        leetcode_problems=[
            "200. Number of Islands - https://leetcode.com/problems/number-of-islands/",
            "94. Binary Tree Inorder Traversal - https://leetcode.com/problems/binary-tree-inorder-traversal/",
            "733. Flood Fill - https://leetcode.com/problems/flood-fill/"
        ],
        examples=[
            AlgorithmExample(
                input_data="graph = {1: [2, 3], 2: [4], 3: [4], 4: []}",
                output_data="1 2 4 3",
                explanation="Обход графа в глубину, начиная с вершины 1"
            )
        ],
        category="графы",
        difficulty="medium"
    ),

    Algorithm(
        title="Динамическое программирование: Числа Фибоначчи",
        description="Классическая задача на динамическое программирование",
        complexity="Временная сложность: O(n), Пространственная сложность: O(1)",
        theory="""Числа Фибоначчи - это последовательность чисел, где каждое следующее число является суммой двух предыдущих.
Задача часто используется для демонстрации концепций динамического программирования.

Подходы к решению:
1. Рекурсивный (неэффективный): O(2^n)
2. Динамическое программирование с массивом: O(n) память
3. Оптимизированный подход с двумя переменными: O(1) память""",
        visualization_url="https://visualgo.net/en/recursion",
        java_code='''public class Fibonacci {
    // Оптимизированное решение
    public static long fib(int n) {
        if (n <= 1) return n;
        
        long prev = 0;
        long current = 1;
        
        for (int i = 2; i <= n; i++) {
            long next = prev + current;
            prev = current;
            current = next;
        }
        
        return current;
    }
}''',
        python_code='''def fibonacci(n: int) -> int:
    if n <= 1:
        return n
        
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr''',
        leetcode_problems=[
            "509. Fibonacci Number - https://leetcode.com/problems/fibonacci-number/",
            "70. Climbing Stairs - https://leetcode.com/problems/climbing-stairs/",
            "1137. N-th Tribonacci Number - https://leetcode.com/problems/n-th-tribonacci-number/"
        ],
        examples=[
            AlgorithmExample(
                input_data="n = 5",
                output_data="5",
                explanation="F(5) = F(4) + F(3) = 3 + 2 = 5"
            )
        ],
        category="динамическое программирование",
        difficulty="easy"
    ),

    Algorithm(
        title="Связный список: Обнаружение цикла",
        description="Алгоритм поиска цикла в связном списке (Алгоритм Флойда)",
        complexity="Временная сложность: O(n), Пространственная сложность: O(1)",
        theory="""Алгоритм Флойда (также известный как алгоритм "черепахи и зайца") используется для определения наличия цикла в связном списке.

Основная идея:
1. Используем два указателя: медленный (движется на 1 шаг) и быстрый (движется на 2 шага)
2. Если есть цикл, указатели встретятся
3. Если цикла нет, быстрый указатель достигнет конца списка""",
        visualization_url="https://visualgo.net/en/list",
        java_code='''public class LinkedListCycle {
    class ListNode {
        int val;
        ListNode next;
    }
    
    public boolean hasCycle(ListNode head) {
        if (head == null || head.next == null) {
            return false;
        }
        
        ListNode slow = head;
        ListNode fast = head;
        
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            
            if (slow == fast) {
                return true;
            }
        }
        
        return false;
    }
}''',
        leetcode_problems=[
            "141. Linked List Cycle - https://leetcode.com/problems/linked-list-cycle/",
            "142. Linked List Cycle II - https://leetcode.com/problems/linked-list-cycle-ii/",
            "202. Happy Number - https://leetcode.com/problems/happy-number/"
        ],
        examples=[
            AlgorithmExample(
                input_data="1 -> 2 -> 3 -> 4 -> 2 (цикл к узлу 2)",
                output_data="true",
                explanation="В списке есть цикл, так как узел 4 указывает на узел 2"
            )
        ],
        category="структуры данных",
        difficulty="medium"
    ),

    Algorithm(
        title="Система непересекающихся множеств (Union-Find)",
        description="Структура данных для эффективного объединения множеств и проверки принадлежности элементов к одному множеству",
        complexity="Почти константное время операций (с использованием оптимизаций)",
        theory="""Union-Find (Система непересекающихся множеств) - это структура данных, которая поддерживает два основных операции:
1. Union(A, B) - объединение двух множеств
2. Find(A) - определение к какому множеству принадлежит элемент

Оптимизации:
- Сжатие путей (path compression)
- Объединение по рангу (union by rank)""",
        visualization_url="https://visualgo.net/en/ufds",
        java_code='''public class UnionFind {
    private int[] parent;
    private int[] rank;
    
    public UnionFind(int size) {
        parent = new int[size];
        rank = new int[size];
        
        for (int i = 0; i < size; i++) {
            parent[i] = i;
        }
    }
    
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // Path compression
        }
        return parent[x];
    }
    
    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX != rootY) {
            if (rank[rootX] < rank[rootY]) {
                parent[rootX] = rootY;
            } else if (rank[rootX] > rank[rootY]) {
                parent[rootY] = rootX;
            } else {
                parent[rootY] = rootX;
                rank[rootX]++;
            }
        }
    }
}''',
        leetcode_problems=[
            "547. Number of Provinces - https://leetcode.com/problems/number-of-provinces/",
            "684. Redundant Connection - https://leetcode.com/problems/redundant-connection/",
            "1319. Number of Operations to Make Network Connected - https://leetcode.com/problems/number-of-operations-to-make-network-connected/"
        ],
        examples=[
            AlgorithmExample(
                input_data="Union(1,2), Union(2,3), Find(1), Find(3)",
                output_data="1, 1",
                explanation="После объединения элементов 1,2 и 2,3 они находятся в одном множестве"
            )
        ],
        category="структуры данных",
        difficulty="medium"
    ),

    Algorithm(
        title="Алгоритм Дейкстры",
        description="Алгоритм поиска кратчайшего пути во взвешенном графе",
        complexity="O((V + E) * log V) с бинарной кучей, где V - количество вершин, E - количество рёбер",
        theory="""Алгоритм Дейкстры находит кратчайшие пути от одной вершины до всех остальных в графе с неотрицательными весами рёбер.

Основные шаги:
1. Инициализация расстояний (0 для начальной вершины, бесконечность для остальных)
2. Выбор непосещенной вершины с минимальным расстоянием
3. Обновление расстояний до соседних вершин
4. Повторение шагов 2-3 пока есть непосещенные вершины""",
        visualization_url="https://visualgo.net/en/sssp",
        java_code='''public class Dijkstra {
    public int[] shortestPath(int[][] graph, int start) {
        int n = graph.length;
        int[] dist = new int[n];
        boolean[] visited = new boolean[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;
        
        PriorityQueue<int[]> pq = new PriorityQueue<>((a,b) -> a[1] - b[1]);
        pq.offer(new int[]{start, 0});
        
        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int u = curr[0];
            
            if (visited[u]) continue;
            visited[u] = true;
            
            for (int v = 0; v < n; v++) {
                if (graph[u][v] > 0 && !visited[v]) {
                    int newDist = dist[u] + graph[u][v];
                    if (newDist < dist[v]) {
                        dist[v] = newDist;
                        pq.offer(new int[]{v, newDist});
                    }
                }
            }
        }
        
        return dist;
    }
}''',
        leetcode_problems=[
            "743. Network Delay Time - https://leetcode.com/problems/network-delay-time/",
            "1631. Path With Minimum Effort - https://leetcode.com/problems/path-with-minimum-effort/",
            "787. Cheapest Flights Within K Stops - https://leetcode.com/problems/cheapest-flights-within-k-stops/"
        ],
        examples=[
            AlgorithmExample(
                input_data="""graph = [
    [0, 4, 0, 0, 0, 0, 0, 8, 0],
    [4, 0, 8, 0, 0, 0, 0, 11, 0],
    [0, 8, 0, 7, 0, 4, 0, 0, 2],
    ...
], start = 0""",
                output_data="[0, 4, 12, 19, 21, 11, 9, 8, 14]",
                explanation="Кратчайшие расстояния от вершины 0 до всех остальных вершин"
            )
        ],
        category="графы",
        difficulty="hard"
    )
]) 