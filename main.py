import psycopg2


def main():
    conn = psycopg2.connect('postgres://avnadmin:AVNS_CJcdqhQzLk-s7LDYHpx@pg-28888-oasis-619815.d.aivencloud.com:20392/defaultdb?sslmode=require')

    query_sql = 'SELECT VERSION()'

    cur = conn.cursor()
    cur.execute(query_sql)

    version = cur.fetchone()[0]
    print(version)


if __name__ == "__main__":
    main()