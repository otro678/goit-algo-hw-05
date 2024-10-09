import timeit

with open('article1.txt', 'r', encoding='utf-8') as file:
    article1 = file.read()

with open('article2.txt', 'r', encoding='utf-8') as file:
    article2 = file.read()


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1



def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    base = 256 
    modulus = 101  
    
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

# 1 підрядок з першого файлу, другий з другого, відповідно при пошуку в кожному файлі один підрядок є, одного нема
patterns = [
    "Для початку необхідно три монети по 25 копійок (4 монети дають більшу суму, ніж потрібно).",
    "експериментів працює за наступним принципом: Крок 1."
]

texts = [article1, article2]

def measure_time(algorithm, pattern, text):
    return timeit.timeit(lambda: algorithm(text, pattern), number=1)

results = {}

for i, pattern in enumerate(patterns):
    for j, text in enumerate(texts):
        text_name = f"article{j + 1}"
        pattern_type = f"pattern_{i + 1}"
        
        kmp_time = measure_time(kmp_search, pattern, text)
        rabin_karp_time = measure_time(rabin_karp_search, pattern, text)
        boyer_moore_time = measure_time(boyer_moore_search, pattern, text)

        results[f"{text_name}_{pattern_type}"] = {
            'KMP': kmp_time,
            'Rabin-Karp': rabin_karp_time,
            'Boyer-Moore': boyer_moore_time
        }

for test, times in results.items():
    print(f"Results for {test}:")
    for algorithm, time_taken in times.items():
        print(f"{algorithm}: {time_taken:.6f} seconds")
    print()