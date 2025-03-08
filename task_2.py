import timeit
import functools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class SplayTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left else root
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)
            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, root):
        new_root = root.right
        root.right = new_root.left
        new_root.left = root
        return new_root

    def _rotate_right(self, root):
        new_root = root.left
        root.left = new_root.right
        new_root.right = root
        return new_root

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayTreeNode(key, value)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return
        new_node = SplayTreeNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def search(self, key):
        self.root = self._splay(self.root, key)
        return self.root.value if self.root and self.root.key == key else None


# Fibonacci with LRU Cache
@functools.lru_cache(None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


# Fibonacci with Splay Tree
def fibonacci_splay(n, tree):
    if n <= 1:
        return n
    cached_value = tree.search(n)
    if cached_value is not None:
        return cached_value
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


# Define test values
n_values = np.arange(0, 1000, 50)

# Measure execution time
lru_times = []
splay_times = []

for n in n_values:
    tree = SplayTree()

    # Time LRU Cache Fibonacci
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10) / 10
    lru_times.append(lru_time)

    # Time Splay Tree Fibonacci
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=10) / 10
    splay_times.append(splay_time)

# Create DataFrame
df = pd.DataFrame({"n": n_values, "LRU Cache Time (s)": lru_times, "Splay Tree Time (s)": splay_times})

# Display table
print(df.to_string(index=False))

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, marker="o", linestyle="-", label="LRU Cache")
plt.plot(n_values, splay_times, marker="x", linestyle="-", label="Splay Tree")
plt.xlabel("Число Фібоначчі (n)")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
plt.legend()
plt.grid(True)
plt.show()