from pprint import pprint
import numpy as np


# Lab1
def create_matrix_the_text(text_in, row_length, matr=None):
    matr = [] if not matr else matr

    row = []
    text_iterator = iter(text_in)
    while True:
        try:
            row.append(next(text_iterator))
            if len(row) == row_length:
                matr.append(row)
                row = []

        except StopIteration:
            while len(row) < row_length:
                row.append(" ")
            if row:
                matr.append(row)
            break

    return matr


def matr_cypher_encode(text_in: str, row_key: str, col_key: str) -> str:
    text_in = text_in.replace(" ", "")

    init_matr = [
        list(row_key)
    ]
    init_matr = create_matrix_the_text(text_in, len(row_key), matr=init_matr)

    matr = np.asarray(init_matr)

    inds = np.argsort(matr[0])
    matr = matr[:, inds]

    matr = np.delete(matr, 0, 0)

    columns = np.asarray(list(col_key))
    matr = np.insert(matr, 0, columns, axis=1)

    matr = matr[matr[:, 0].argsort()]
    matr = np.delete(matr, 0, 1)

    return ' '.join(''.join(row) for row in matr.T)


def _decode(matr, key):
    matr = np.asarray(matr)
    inds = [sorted(key).index(ch) for ch in key]
    rows = np.asarray(list(sorted(key)))

    matr = np.insert(matr, 0, rows, axis=0)
    matr = matr[:, inds]

    return matr


def matr_cypher_decode(text_in: str, row_key: str, col_key: str) -> str:
    matr = []
    i = 0
    offset = len(col_key)
    while i < len(text_in):
        matr.append(list(text_in[i:i + offset]))
        i += (offset + 1)

    matr = _decode(matr, col_key)
    matr = np.delete(matr, 0, 0).T

    matr = _decode(matr, row_key)
    matr = np.delete(matr, 0, 0)
    return ''.join(''.join(row) for row in matr).strip()


if __name__ == '__main__':
    pprint("Матричний шифр")
    text_in = "якість та безпека"

    pprint(f"Текст, що кодується: {text_in}")

    keyword_one = "шифро"
    keyword_two = "ключ"

    encod_text = matr_cypher_encode(text_in, keyword_one, keyword_two)
    pprint(f"кодування: {encod_text}")
    pprint(f"розкодування: {matr_cypher_decode(encod_text, keyword_one, keyword_two)}")
