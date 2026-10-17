from django.db import connection

def call_procedure(name, params=(), out_count=0, fetch=True):
    """
    Универсальный вызов хранимой процедуры.

    :param name: имя процедуры
    :param params: список IN-параметров
    :param out_count: сколько OUT-параметров добавить
    :param fetch: возвращать ли строки результата
    :return: (rows, out_values)
    """
    args = list(params) + [0] * out_count
    placeholders = ','.join(['%s'] * len(args))
    sql = f"CALL {name}({placeholders})"

    with connection.cursor() as cur:
        cur.execute(sql, args)
        rows = cur.fetchall() if fetch else None
        out_values = args[-out_count:] if out_count else []
    return rows, out_values


def call_function(name, params=()):
    """Вызов хранимой функции, возвращающей скаляр."""
    placeholders = ','.join(['%s'] * len(params))
    sql = f"SELECT {name}({placeholders})"
    with connection.cursor() as cur:
        cur.execute(sql, list(params))
        return cur.fetchone()[0]
