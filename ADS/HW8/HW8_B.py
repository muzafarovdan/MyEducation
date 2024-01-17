def solve(n):
    seats = [4 * n - i for i in range(0, 2 * n, 2)]
    return seats

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        result = solve(n)
        print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()
