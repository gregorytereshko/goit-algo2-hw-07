import random
import time
from functools import lru_cache

# Функції без кешу
def range_sum_no_cache(array, L, R):
    """Обчислює суму елементів масиву на відрізку [L, R] без кешу."""
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    """Оновлює значення елемента масиву за індексом без кешу."""
    array[index] = value

# Функції з кешем
@lru_cache(maxsize=1000)
def range_sum_with_cache(tuple_array, L, R):
    """Обчислює суму елементів масиву на відрізку [L, R] з використанням вбудованого LRU-кешу."""
    return sum(tuple_array[L:R+1])

def update_with_cache(array, index, value):
    """Оновлює значення елемента масиву та очищує кеш, оскільки дані стали неактуальними."""
    array[index] = value
    range_sum_with_cache.cache_clear()

# Генерація випадкового масиву та запитів
N = 100_000
Q = 50_000
array = [random.randint(1, 1000) for _ in range(N)]
tuple_array = tuple(array)  # Використовуємо tuple, оскільки lru_cache працює лише з незмінними об'єктами

queries = []
for _ in range(Q):
    if random.random() < 0.5:
        L, R = sorted(random.sample(range(N), 2))
        queries.append(('Range', L, R))
    else:
        index = random.randint(0, N-1)
        value = random.randint(1, 1000)
        queries.append(('Update', index, value))

# Вимірювання часу виконання запитів
start_no_cache = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_no_cache(array, query[1], query[2])
    else:
        update_no_cache(array, query[1], query[2])
end_no_cache = time.time()

start_with_cache = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_with_cache(tuple_array, query[1], query[2])
    else:
        update_with_cache(array, query[1], query[2])
end_with_cache = time.time()

# Вивід результатів
print("Час виконання запитів:")
print(f"Без кешу: {end_no_cache - start_no_cache:.6f} секунд")
print(f"З кешем: {end_with_cache - start_with_cache:.6f} секунд")