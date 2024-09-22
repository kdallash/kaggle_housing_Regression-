"""def quicksort(a, lo, hi):
    if lo >= hi or lo < 0:
        return 
    if lo < hi:
        p = partition(a, lo, hi)
        quicksort(a, lo, p - 1)
        quicksort(a, p + 1, hi)
def partition(a, lo, hi):
    pivite = a[hi]
    i = lo
    for j in range(lo, hi ):
        if a[j]  <+ pivite:
            a[i],a[j] = a[j],a[i]
            i += 1
    a[i],a[hi] = a[hi],a[i]
    return i
if __name__ == '__main__':
    tests = [
        [11,9,29,7,2,15,28],
        [3, 7, 9, 11],
        [25, 22, 21, 10],
        [29, 15, 28],
        [],
        [6]
    ]
    # elements = ["mona", "dhaval", "aamir", "tina", "chang"]

    for elements in tests:
        quicksort(elements, 0, len(elements)-1)
        print(f'sorted array: {elements}')"""
for i in range(9):
    for f in range(3):
        print(i)
        break