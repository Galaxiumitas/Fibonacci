import time
from concurrent.futures import ProcessPoolExecutor

def fibonacci(n):
    #fibonacci secuencial
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq

def fibonacciParalelo(n, depth=0, max_depth=2):
    # version paralela
    if n <= 1:
        return [0] if n == 1 else []

    if depth < max_depth:
        with ProcessPoolExecutor() as executor:
            # calculamos ramas en paralelo
            f1 = executor.submit(fibonacciParalelo, n - 1, depth + 1, max_depth)
            f2 = executor.submit(fibonacciParalelo, n - 2, depth + 1, max_depth)
            left = f1.result()
            right = f2.result()
    else:
        # es secuencial a partir de cierto nivel
        left = fibonacci(n - 1)
        right = fibonacci(n - 2)

    # La secuencia de F(n) es la de F(n-1) extendida con el último valor
    seq = left + [left[-1] + (right[-1] if right else 0)]
    return seq

if __name__ == "__main__":
    n = 30

    inicio = time.perf_counter_ns()
    seq_s = fibonacci(n)
    fin = time.perf_counter_ns()
    print(f"[Secuencial] Tiempo: {fin - inicio} ns")
    print(seq_s)

    inicio_par = time.perf_counter_ns()
    seq_p = fibonacciParalelo(n)
    fin_par = time.perf_counter_ns()
    print(f"[Paralelo] Tiempo: {fin_par - inicio_par} ns")
    print(seq_p)