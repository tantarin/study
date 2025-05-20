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