# Problem E. Patchwork Staccato II
import sys
import bisect
def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    q = int(data[idx]); idx += 1
    a = data[idx:idx+n]
    a = list(map(int, a))
    idx += n
    a.sort()
    out = []
    for _ in range(q):
        l1 = int(data[idx]); r1 = int(data[idx+1])
        l2 = int(data[idx+2]); r2 = int(data[idx+3])
        idx += 4
        def count_range(l, r):
            if l > r:
                return 0
            left = bisect.bisect_left(a, l)
            right = bisect.bisect_right(a, r)
            return right - left
        cnt1 = count_range(l1, r1)
        cnt2 = count_range(l2, r2)
        lo = max(l1, l2)
        hi = min(r1, r2)
        inter = count_range(lo, hi)
        ans = cnt1 + cnt2 - inter
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")
main()