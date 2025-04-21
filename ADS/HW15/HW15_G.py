def sieve_of_eratosthenes(upper_limit):
    is_prime = [True] * (upper_limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(upper_limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, upper_limit + 1, i):
                is_prime[j] = False

    return is_prime

def print_primes_in_range(lower, upper):
    is_prime = sieve_of_eratosthenes(upper)

    for i in range(max(2, lower), upper + 1):
        if is_prime[i]:
            print(i, end=" ")

    print()

if __name__ == "__main__":
    lower_limit, upper_limit = map(int, input().split())

    print_primes_in_range(lower_limit, upper_limit)
