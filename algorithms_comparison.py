# порівняння алгоритмів пошуку підрядка з автоматичним завантаженням текстів з google drive

import timeit
import urllib.request

# завантаження вмісту файлу з google drive за file id
def load_gdrive_text(file_id):
    # формуємо посилання на пряме завантаження
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    # намагаємось декодувати як utf-8, інакше ігноруємо помилки
    text = data.decode("utf-8", errors="ignore")
    return text

# алгоритм боєра мура
def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0
    last = {}
    for i, c in enumerate(pattern):
        last[c] = i
    i = m - 1
    k = m - 1
    while i < n:
        if text[i] == pattern[k]:
            if k == 0:
                return i
            i -= 1
            k -= 1
        else:
            j = last.get(text[i], -1)
            i = i + m - min(k, j + 1)
            k = m - 1
    return -1

# алгоритм кнута морріса пратта
def kmp_search(text, pattern):
    if not pattern:
        return 0

    def build_lps(p):
        lps = [0] * len(p)
        j = 0
        for i in range(1, len(p)):
            while j > 0 and p[i] != p[j]:
                j = lps[j - 1]
            if p[i] == p[j]:
                j += 1
                lps[i] = j
        return lps

    lps = build_lps(pattern)
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# алгоритм рабіна карпа
def rabin_karp(text, pattern, d=256, q=101):
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0
    if n < m:
        return -1
    h = pow(d, m - 1, q)
    p = 0
    t = 0
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for s in range(n - m + 1):
        if p == t:
            if text[s:s + m] == pattern:
                return s
        if s < n - m:
            t = (t - ord(text[s]) * h) * d + ord(text[s + m])
            t %= q
    return -1

# вимірювання часу виконання однієї операції пошуку
def measure_once(func, text, pattern, runs=10):
    return timeit.timeit(lambda: func(text, pattern), number=runs) / runs

def pick_real_pattern(txt, start=100, length=20):
    # вибір шматка тексту як існуючого підрядка з грубою нормалізацією прогалин
    s = max(0, min(start, max(0, len(txt) - length)))
    p = txt[s:s + length]
    # прибираємо перевод рядків для чистоти
    return p.replace("\n", " ").strip() or txt[:min(10, len(txt))]

def main():
    # id з твого завдання
    file1_id = "1EdQUqE_qLDCL_54v8aQ5zlcMf2L9dF_B"
    file2_id = "1o5uZ8NBMtZmThGIeilCRWgspIOfOnbzQ"

    print("завантаження текстів з google drive")
    text1 = load_gdrive_text(file1_id)
    text2 = load_gdrive_text(file2_id)

    # формуємо підрядки
    real1 = pick_real_pattern(text1, start=100, length=24)
    real2 = pick_real_pattern(text2, start=200, length=24)
    fake1 = "вигаданий_рядок_для_перевірки"
    fake2 = "fictional_pattern_for_test"

    algorithms = {
        "boyer moore": boyer_moore,
        "kmp": kmp_search,
        "rabin karp": rabin_karp,
    }

    tests = [
        ("текст 1", text1, real1, fake1),
        ("текст 2", text2, real2, fake2),
    ]

    for title, txt, real_p, fake_p in tests:
        print(f"\n{title}")
        print(f"довжина тексту {len(txt)} символів")
        print(f"існуючий підрядок `{real_p}`")
        print("пошук існуючого підрядка")
        for name, fn in algorithms.items():
            t = measure_once(fn, txt, real_p)
            print(f"{name:12s} {t:.6f} c")
        print("пошук вигаданого підрядка")
        fake = fake_p
        for name, fn in algorithms.items():
            t = measure_once(fn, txt, fake)
            print(f"{name:12s} {t:.6f} c")

    print("\nготово")

if __name__ == "__main__":
    main()
