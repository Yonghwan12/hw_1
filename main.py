import random, time, sys

# ---------- 퀵 정렬 (랜덤 피벗, 3-way 분할, 작은 쪽 재귀) ----------
def quick_sort(a):
    def sort(lo, hi):
        while lo < hi:
            p = a[random.randint(lo, hi)]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if a[i] < p:
                    a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
                elif a[i] > p:
                    a[i], a[gt] = a[gt], a[i]; gt -= 1
                else:
                    i += 1
            # 작은 구간만 재귀 -> 재귀 깊이 O(log n) 보장
            if lt - lo < hi - gt:
                sort(lo, lt - 1); lo = gt + 1
            else:
                sort(gt + 1, hi); hi = lt - 1
    sort(0, len(a) - 1)

# ---------- 병합 정렬 (보조 배열 1개 재사용) ----------
def merge_sort(a):
    tmp = a[:]
    def sort(lo, hi):
        if hi - lo < 1: return
        mid = (lo + hi) // 2
        sort(lo, mid); sort(mid + 1, hi)
        i, j, k = lo, mid + 1, lo
        while i <= mid and j <= hi:
            if a[i] <= a[j]: tmp[k] = a[i]; i += 1   # <= 로 안정성 유지
            else:            tmp[k] = a[j]; j += 1
            k += 1
        while i <= mid: tmp[k] = a[i]; i += 1; k += 1
        while j <= hi:  tmp[k] = a[j]; j += 1; k += 1
        a[lo:hi + 1] = tmp[lo:hi + 1]
    sort(0, len(a) - 1)

# ---------- 힙 정렬 (배우지 않은 정렬) ----------
def heap_sort(a):
    n = len(a)
    def sift_down(i, size):
        while True:
            l, r, m = 2 * i + 1, 2 * i + 2, i
            if l < size and a[l] > a[m]: m = l
            if r < size and a[r] > a[m]: m = r
            if m == i: return
            a[i], a[m] = a[m], a[i]; i = m
    for i in range(n // 2 - 1, -1, -1):      # 최대 힙 구성 O(n)
        sift_down(i, n)
    for end in range(n - 1, 0, -1):          # 최댓값을 뒤로 보내며 정렬
        a[0], a[end] = a[end], a[0]
        sift_down(0, end)

# ---------- 벤치마크 ----------
def make(kind, n):
    if kind == "random":     return [random.randint(0, n) for _ in range(n)]
    if kind == "sorted":     return list(range(n))
    if kind == "reversed":   return list(range(n, 0, -1))
    if kind == "duplicates": return [random.randint(0, 10) for _ in range(n)]

def bench(fn, data, repeat=3):
    best = float("inf")
    for _ in range(repeat):
        a = data[:]
        t = time.perf_counter(); fn(a); best = min(best, time.perf_counter() - t)
        assert a == sorted(data), f"{fn.__name__} 정렬 오류"
    return best

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    algos = [quick_sort, merge_sort, heap_sort]
    print(f"{'case':<11}{'n':>7}" + "".join(f"{f.__name__:>13}" for f in algos))
    for kind in ["random", "sorted", "reversed", "duplicates"]:
        for n in [1000, 5000, 10000, 50000]:
            data = make(kind, n)
            print(f"{kind:<11}{n:>7}" + "".join(f"{bench(f, data):>13.5f}" for f in algos))
