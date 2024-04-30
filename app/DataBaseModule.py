import app.ConfigModule as Config
import psycopg2
import psycopg2.extras
from psycopg2 import Error


class DataBase:

    def __init__(self):
        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(**Config.load_config('database.ini','postgresql')) as conn:
                print('Connected to the PostgreSQL server.')
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
    

    def Execute(self, query):
        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(**Config.load_config('database.ini','postgresql')) as conn:
                print('Connected to the PostgreSQL server.')
                # usando cursor para executar o query
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute(query)
                return True,'ok'
        except(psycopg2.Error) as e :

            if e.pgcode == '23505':  # Código de erro para UniqueViolation
                print("Erro de violação de chave única: Já existe um registro com os mesmos valores.")
                return False, "UniqueViolation"
            else:
                print(f"Erro inesperado: {e}")

        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
            return False, None


    def Select(self, query, cursor_func = psycopg2.extras.DictCursor):
        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(**Config.load_config('database.ini','postgresql')) as conn:
                print('Connected to the PostgreSQL server.')
                # usando cursor para executar o query
                with conn.cursor(cursor_factory=cursor_func) as cur:
                    cur.execute(query)
                    rows = cur.fetchall()
                    result = []
                    for row in rows:
                        result.append(dict(row))


                return result
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
            return []

