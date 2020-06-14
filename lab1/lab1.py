import re
import numpy as np
from scipy.stats import chisquare
import matplotlib.pyplot as plt

abc = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
letter_freq = {'а': 0.074, 'б': 0.018, 'в': 0.054, 'г': 0.016, 'ґ': 0.001, 'д': 0.036, 'е': 0.017,
               'є': 0.008, 'ж': 0.009, 'з': 0.024, 'и': 0.063, 'і': 0.059, 'ї': 0.006, 'й': 0.009,
               'к': 0.036, 'л': 0.037, 'м': 0.032, 'н': 0.067, 'о': 0.097, 'п': 0.023, 'р': 0.049,
               'с': 0.042, 'т': 0.057, 'у': 0.041, 'ф': 0.001, 'х': 0.012, 'ц': 0.006, 'ч': 0.019,
               'ш': 0.012, 'щ': 0.001, 'ю': 0.004, 'я': 0.03, 'ь': 0.03}


def get_sequency(ct, key_len):
    dt = {i: [] for i in range(key_len)}
    for i, lt in enumerate(ct):
        dt[i % key_len] += lt
    return np.array(list(dt.values()))


def get_data(ct):
    if len(ct) < 2:
        return 0
    n = len(ct)
    res = 0
    for letter in abc:
        count = ct.count(letter)
        res += count * (count - 1)
    return res / (n * (n - 1))


def get_hist(ct):
    hist = [0] * len(abc)
    for index, letter in enumerate(abc):
        hist[index] = ct.count(letter)
    return hist


def read_file(path):
    with open(path, 'r') as f:
        return re.sub(f"[^{abc}]", "", f.read().lower())


def encrypt(key, pt):
    ct = ''
    for t, k in zip(pt, key * (1 + len(pt) // len(key))):
        ct += abc[(abc.find(t) + abc.find(k)) % len(abc)]
    return ct


def decrypt(key, ct):
    pt = ''
    for t, k in zip(ct, key * (1 + len(ct) // len(key))):
        pt += abc[(abc.find(t) - abc.find(k)) % len(abc)]
    return pt


def key_len_recognition(ct, max_len=33):
    res = []
    v_data = np.vectorize(get_data)
    for i in range(2, max_len + 1):
        seq = get_sequency(ct, i)
        ioc = v_data(seq)
        res.append(ioc.mean())
    return np.argmin(np.abs(np.array(res) - get_data(read_file('text.txt')))) + 2


def key_recognition(ct, key_len):
    key = ['_'] * key_len
    split_text = get_sequency(ct, key_len)
    for i, seq in enumerate(split_text):
        st = float('inf')
        for letter in abc:
            ch2 = chisquare(get_hist(decrypt(letter, seq)), list(letter_freq.values()))[0]
            if ch2 < st:
                st = ch2
                key[i] = letter

    return ''.join(key)


def analyze(ct):
    key_len = key_len_recognition(ct)
    key = key_recognition(ct, key_len)
    print("Key: {}\nLen: {}".format(key, key_len))
    proposed = decrypt(key, ct)
    return proposed


if __name__ == '__main__':
    pt = read_file('text.txt')
    hist = get_hist(pt)
    plt.bar(list(abc), hist)
    plt.show()
    key = 'ключ'
    ct = encrypt(key, pt)

    pt_1 = analyze(ct)
    hist = get_hist(ct)
    plt.bar(list(abc), hist)
    plt.show()
    print('Is equal', pt == pt_1)
