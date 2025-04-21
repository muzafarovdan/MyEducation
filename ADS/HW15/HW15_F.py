def is_prime(number): #Works well with big numbers that are not prime
    state = 'YES'
    if number <= 0:
        state = 'NO'
        return state
    else:          
        for i in range(2,number):
            if number % i == 0:
                state = 'NO'
                break
        return state

tests = int(input())
for test in range(tests):
    number = int(input())
    print(is_prime(number))