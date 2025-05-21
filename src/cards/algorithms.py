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
    ),

    Algorithm(
        title="Line Reflection",
        description="Проверка возможности отражения точек относительно вертикальной линии",
        complexity="Временная сложность: O(n), Пространственная сложность: O(n)",
        theory="""Задача: Проверить, можно ли отразить точки на плоскости относительно вертикальной линии так, чтобы получился симметричный набор.

Подход к решению:
1. Найти минимальную и максимальную x-координаты для определения центральной линии
2. Для каждой точки проверить наличие её отражения относительно центральной линии
3. Использовать HashSet для эффективной проверки наличия отраженных точек""",
        visualization_url="https://leetcode.com/problems/line-reflection/",
        java_code='''public class Solution {
    public boolean isReflected(int[][] points) {
        if (points == null || points.length == 0) return true;
        
        int min = Integer.MAX_VALUE;
        int max = Integer.MIN_VALUE;
        Set<String> set = new HashSet<>();
        
        for (int[] p : points) {
            min = Math.min(min, p[0]);
            max = Math.max(max, p[0]);
            set.add(p[0] + "," + p[1]);
        }
        
        int sum = min + max;
        for (int[] p : points) {
            String reflection = (sum - p[0]) + "," + p[1];
            if (!set.contains(reflection)) {
                return false;
            }
        }
        
        return true;
    }
}''',
        python_code='''def is_reflected(points: List[List[int]]) -> bool:
    if not points:
        return True
        
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    point_set = {f"{p[0]},{p[1]}" for p in points}
    
    sum_x = min_x + max_x
    for p in points:
        reflection = f"{sum_x - p[0]},{p[1]}"
        if reflection not in point_set:
            return False
            
    return True''',
        leetcode_problems=[
            "356. Line Reflection - https://leetcode.com/problems/line-reflection/"
        ],
        examples=[
            AlgorithmExample(
                input_data="points = [[1,1],[-1,1]]",
                output_data="true",
                explanation="Точки можно отразить относительно линии x = 0"
            )
        ],
        category="геометрия",
        difficulty="medium"
    ),

    Algorithm(
        title="Longest Subarray of 1's After Deleting One Element",
        description="Поиск максимальной длины подмассива из единиц после удаления одного элемента",
        complexity="Временная сложность: O(n), Пространственная сложность: O(1)",
        theory="""Задача: Найти максимальную длину подмассива из единиц после удаления одного элемента.

Подход к решению:
1. Использовать метод скользящего окна
2. Поддерживать счетчик нулей в текущем окне
3. Если количество нулей превышает 1, сдвигать левую границу окна
4. Обновлять максимальную длину при каждом валидном окне""",
        visualization_url="https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/",
        java_code='''public class Solution {
    public int longestSubarray(int[] nums) {
        int left = 0;
        int zeros = 0;
        int maxLen = 0;
        
        for (int right = 0; right < nums.length; right++) {
            if (nums[right] == 0) {
                zeros++;
            }
            
            while (zeros > 1) {
                if (nums[left] == 0) {
                    zeros--;
                }
                left++;
            }
            
            maxLen = Math.max(maxLen, right - left);
        }
        
        return maxLen;
    }
}''',
        python_code='''def longest_subarray(nums: List[int]) -> int:
    left = zeros = max_len = 0
    
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1
            
        while zeros > 1:
            if nums[left] == 0:
                zeros -= 1
            left += 1
            
        max_len = max(max_len, right - left)
        
    return max_len''',
        leetcode_problems=[
            "1493. Longest Subarray of 1's After Deleting One Element - https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/"
        ],
        examples=[
            AlgorithmExample(
                input_data="nums = [1,1,0,1]",
                output_data="3",
                explanation="После удаления нуля получаем подмассив [1,1,1] длиной 3"
            )
        ],
        category="массивы",
        difficulty="medium"
    ),

    Algorithm(
        title="String Compression",
        description="Сжатие строки с заменой повторяющихся символов на их количество",
        complexity="Временная сложность: O(n), Пространственная сложность: O(1)",
        theory="""Задача: Сжать строку, заменяя повторяющиеся символы на их количество.

Подход к решению:
1. Использовать два указателя: один для чтения, другой для записи
2. Подсчитывать количество повторений текущего символа
3. Записывать символ и его количество (если больше 1)
4. Возвращать новую длину строки""",
        visualization_url="https://leetcode.com/problems/string-compression/",
        java_code='''public class Solution {
    public int compress(char[] chars) {
        int write = 0;
        int read = 0;
        
        while (read < chars.length) {
            char current = chars[read];
            int count = 0;
            
            while (read < chars.length && chars[read] == current) {
                read++;
                count++;
            }
            
            chars[write++] = current;
            
            if (count > 1) {
                for (char c : String.valueOf(count).toCharArray()) {
                    chars[write++] = c;
                }
            }
        }
        
        return write;
    }
}''',
        python_code='''def compress(chars: List[str]) -> int:
    write = read = 0
    
    while read < len(chars):
        current = chars[read]
        count = 0
        
        while read < len(chars) and chars[read] == current:
            read += 1
            count += 1
            
        chars[write] = current
        write += 1
        
        if count > 1:
            for c in str(count):
                chars[write] = c
                write += 1
                
    return write''',
        leetcode_problems=[
            "443. String Compression - https://leetcode.com/problems/string-compression/"
        ],
        examples=[
            AlgorithmExample(
                input_data='chars = ["a","a","b","b","c","c","c"]',
                output_data='6, chars = ["a","2","b","2","c","3"]',
                explanation="Строка сжата до 'a2b2c3'"
            )
        ],
        category="строки",
        difficulty="medium"
    ),

    Algorithm(
        title="Valid Palindrome",
        description="Проверка строки на палиндром с игнорированием не-алфавитных символов",
        complexity="Временная сложность: O(n), Пространственная сложность: O(1)",
        theory="""Задача: Проверить, является ли строка палиндромом, игнорируя не-алфавитные символы.

Подход к решению:
1. Использовать два указателя: с начала и конца строки
2. Пропускать не-алфавитные символы
3. Сравнивать символы в нижнем регистре
4. Продолжать до встречи указателей""",
        visualization_url="https://leetcode.com/problems/valid-palindrome/",
        java_code='''public class Solution {
    public boolean isPalindrome(String s) {
        int left = 0;
        int right = s.length() - 1;
        
        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
                left++;
            }
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) {
                right--;
            }
            
            if (Character.toLowerCase(s.charAt(left)) != 
                Character.toLowerCase(s.charAt(right))) {
                return false;
            }
            
            left++;
            right--;
        }
        
        return true;
    }
}''',
        python_code='''def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
            
        if s[left].lower() != s[right].lower():
            return False
            
        left += 1
        right -= 1
        
    return True''',
        leetcode_problems=[
            "125. Valid Palindrome - https://leetcode.com/problems/valid-palindrome/"
        ],
        examples=[
            AlgorithmExample(
                input_data='s = "A man, a plan, a canal: Panama"',
                output_data="true",
                explanation="Строка является палиндромом после удаления не-алфавитных символов"
            )
        ],
        category="строки",
        difficulty="easy"
    ),

    Algorithm(
        title="Subarray Sum Equals K",
        description="Поиск количества подмассивов с суммой равной K",
        complexity="Временная сложность: O(n), Пространственная сложность: O(n)",
        theory="""Задача: Найти количество подмассивов с суммой равной K.

Подход к решению:
1. Использовать префиксные суммы и HashMap
2. Для каждой позиции проверять, есть ли префиксная сумма (текущая сумма - K)
3. Поддерживать счетчик префиксных сумм
4. Обновлять результат при нахождении подходящего префикса""",
        visualization_url="https://leetcode.com/problems/subarray-sum-equals-k/",
        java_code='''public class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        map.put(0, 1);
        
        int sum = 0;
        int count = 0;
        
        for (int num : nums) {
            sum += num;
            if (map.containsKey(sum - k)) {
                count += map.get(sum - k);
            }
            map.put(sum, map.getOrDefault(sum, 0) + 1);
        }
        
        return count;
    }
}''',
        python_code='''def subarray_sum(nums: List[int], k: int) -> int:
    prefix_sum = {0: 1}
    current_sum = count = 0
    
    for num in nums:
        current_sum += num
        if current_sum - k in prefix_sum:
            count += prefix_sum[current_sum - k]
        prefix_sum[current_sum] = prefix_sum.get(current_sum, 0) + 1
        
    return count''',
        leetcode_problems=[
            "560. Subarray Sum Equals K - https://leetcode.com/problems/subarray-sum-equals-k/"
        ],
        examples=[
            AlgorithmExample(
                input_data="nums = [1,1,1], k = 2",
                output_data="2",
                explanation="Есть два подмассива с суммой 2: [1,1] и [1,1]"
            )
        ],
        category="массивы",
        difficulty="medium"
    ),

    Algorithm(
        title="Merge k Sorted Lists",
        description="Объединение k отсортированных связных списков в один",
        complexity="Временная сложность: O(n log k), Пространственная сложность: O(k)",
        theory="""Задача: Объединить k отсортированных связных списков в один.

Подход к решению:
1. Использовать минимальную кучу (PriorityQueue)
2. Добавить головы всех списков в кучу
3. Извлекать минимальный элемент и добавлять следующий из того же списка
4. Продолжать пока куча не пуста""",
        visualization_url="https://leetcode.com/problems/merge-k-sorted-lists/",
        java_code='''public class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;
        
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> a.val - b.val);
        
        for (ListNode node : lists) {
            if (node != null) {
                pq.offer(node);
            }
        }
        
        ListNode dummy = new ListNode(0);
        ListNode current = dummy;
        
        while (!pq.isEmpty()) {
            ListNode node = pq.poll();
            current.next = node;
            current = current.next;
            
            if (node.next != null) {
                pq.offer(node.next);
            }
        }
        
        return dummy.next;
    }
}''',
        python_code='''def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    if not lists:
        return None
        
    pq = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(pq, (node.val, i, node))
            
    dummy = ListNode(0)
    current = dummy
    
    while pq:
        val, i, node = heapq.heappop(pq)
        current.next = node
        current = current.next
        
        if node.next:
            heapq.heappush(pq, (node.next.val, i, node.next))
            
    return dummy.next''',
        leetcode_problems=[
            "23. Merge k Sorted Lists - https://leetcode.com/problems/merge-k-sorted-lists/"
        ],
        examples=[
            AlgorithmExample(
                input_data="lists = [[1,4,5],[1,3,4],[2,6]]",
                output_data="[1,1,2,3,4,4,5,6]",
                explanation="Объединенный отсортированный список"
            )
        ],
        category="связные списки",
        difficulty="hard"
    ),

    Algorithm(
        title="Trapping Rain Water",
        description="Вычисление количества воды, которое может быть задержано между столбиками",
        complexity="Временная сложность: O(n), Пространственная сложность: O(1)",
        theory="""Задача: Вычислить, сколько воды может быть задержано между столбиками гистограммы.

Подход к решению:
1. Использовать два указателя: с начала и конца массива
2. Поддерживать максимальные высоты слева и справа
3. Для каждой позиции вычислять количество воды как min(leftMax, rightMax) - height[i]
4. Обновлять максимумы при движении указателей""",
        visualization_url="https://leetcode.com/problems/trapping-rain-water/",
        java_code='''public class Solution {
    public int trap(int[] height) {
        int left = 0;
        int right = height.length - 1;
        int leftMax = 0;
        int rightMax = 0;
        int water = 0;
        
        while (left < right) {
            if (height[left] < height[right]) {
                leftMax = Math.max(leftMax, height[left]);
                water += leftMax - height[left];
                left++;
            } else {
                rightMax = Math.max(rightMax, height[right]);
                water += rightMax - height[right];
                right--;
            }
        }
        
        return water;
    }
}''',
        python_code='''def trap(height: List[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
            
    return water''',
        leetcode_problems=[
            "42. Trapping Rain Water - https://leetcode.com/problems/trapping-rain-water/"
        ],
        examples=[
            AlgorithmExample(
                input_data="height = [0,1,0,2,1,0,1,3,2,1,2,1]",
                output_data="6",
                explanation="Можно задержать 6 единиц воды"
            )
        ],
        category="массивы",
        difficulty="hard"
    ),

    Algorithm(
        title="Two Sum",
        description="Поиск двух чисел в массиве, сумма которых равна заданному значению",
        complexity="Временная сложность: O(n), Пространственная сложность: O(n)",
        theory="""Задача: Найти два числа в массиве, сумма которых равна заданному значению.

Подход к решению:
1. Использовать HashMap для хранения чисел и их индексов
2. Для каждого числа проверять, есть ли в HashMap число (target - текущее число)
3. Если есть - возвращать индексы обоих чисел
4. Если нет - добавлять текущее число в HashMap""",
        visualization_url="https://leetcode.com/problems/two-sum/",
        java_code='''public class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[] { map.get(complement), i };
            }
            map.put(nums[i], i);
        }
        
        return new int[] {};
    }
}''',
        python_code='''def two_sum(nums: List[int], target: int) -> List[int]:
    num_map = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
        
    return []''',
        leetcode_problems=[
            "1. Two Sum - https://leetcode.com/problems/two-sum/"
        ],
        examples=[
            AlgorithmExample(
                input_data="nums = [2,7,11,15], target = 9",
                output_data="[0,1]",
                explanation="nums[0] + nums[1] = 2 + 7 = 9"
            )
        ],
        category="массивы",
        difficulty="easy"
    ),

    Algorithm(
        title="Number of Islands",
        description="Подсчет количества островов в матрице",
        complexity="Временная сложность: O(m*n), Пространственная сложность: O(m*n)",
        theory="""Задача: Посчитать количество островов в матрице, где '1' — это земля, а '0' — вода.

Подход к решению:
1. Использовать поиск в глубину (DFS) или ширину (BFS)
2. Помечать посещенные клетки
3. Для каждой непосещенной клетки с '1':
   - Увеличивать счетчик островов
   - Помечать все связанные клетки как посещенные
4. Возвращать количество островов""",
        visualization_url="https://leetcode.com/problems/number-of-islands/",
        java_code='''public class Solution {
    public int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;
        
        int count = 0;
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[0].length; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    dfs(grid, i, j);
                }
            }
        }
        return count;
    }
    
    private void dfs(char[][] grid, int i, int j) {
        if (i < 0 || i >= grid.length || j < 0 || j >= grid[0].length || grid[i][j] == '0') {
            return;
        }
        
        grid[i][j] = '0';
        dfs(grid, i + 1, j);
        dfs(grid, i - 1, j);
        dfs(grid, i, j + 1);
        dfs(grid, i, j - 1);
    }
}''',
        python_code='''def num_islands(grid: List[List[str]]) -> int:
    if not grid:
        return 0
        
    def dfs(i: int, j: int):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == '0':
            return
            
        grid[i][j] = '0'
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)
        
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)
                
    return count''',
        leetcode_problems=[
            "200. Number of Islands - https://leetcode.com/problems/number-of-islands/"
        ],
        examples=[
            AlgorithmExample(
                input_data='''grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]''',
                output_data="3",
                explanation="В матрице есть 3 острова"
            )
        ],
        category="графы",
        difficulty="medium"
    ),

    Algorithm(
        title="Longest Palindromic Substring",
        description="Поиск самой длинной подстроки-палиндрома",
        complexity="Временная сложность: O(n²), Пространственная сложность: O(1)",
        theory="""Задача: Найти самую длинную подстроку-палиндром в строке.

Подход к решению:
1. Использовать метод расширения от центра
2. Для каждого символа и пары символов:
   - Расширять влево и вправо, пока символы совпадают
   - Обновлять максимальную длину и начальную позицию
3. Возвращать подстроку с максимальной длиной""",
        visualization_url="https://leetcode.com/problems/longest-palindromic-substring/",
        java_code='''public class Solution {
    public String longestPalindrome(String s) {
        if (s == null || s.length() < 1) return "";
        
        int start = 0;
        int maxLength = 0;
        
        for (int i = 0; i < s.length(); i++) {
            int len1 = expandAroundCenter(s, i, i);
            int len2 = expandAroundCenter(s, i, i + 1);
            int len = Math.max(len1, len2);
            
            if (len > maxLength) {
                start = i - (len - 1) / 2;
                maxLength = len;
            }
        }
        
        return s.substring(start, start + maxLength);
    }
    
    private int expandAroundCenter(String s, int left, int right) {
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
            left--;
            right++;
        }
        return right - left - 1;
    }
}''',
        python_code='''def longest_palindrome(s: str) -> str:
    if not s:
        return ""
        
    def expand_around_center(left: int, right: int) -> int:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
        
    start = max_length = 0
    
    for i in range(len(s)):
        len1 = expand_around_center(i, i)
        len2 = expand_around_center(i, i + 1)
        length = max(len1, len2)
        
        if length > max_length:
            start = i - (length - 1) // 2
            max_length = length
            
    return s[start:start + max_length]''',
        leetcode_problems=[
            "5. Longest Palindromic Substring - https://leetcode.com/problems/longest-palindromic-substring/"
        ],
        examples=[
            AlgorithmExample(
                input_data='s = "babad"',
                output_data='"bab" или "aba"',
                explanation="Обе подстроки являются палиндромами максимальной длины"
            )
        ],
        category="строки",
        difficulty="medium"
    )
]) 