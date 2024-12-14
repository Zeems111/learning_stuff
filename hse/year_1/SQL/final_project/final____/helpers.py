import psycopg2


def function_with_sql():
    # Create a connection
    con = psycopg2.connect(
        database="cars", user="postgres", password="sql", host="localhost"
    )
    # create a client-side cursor
    cur = con.cursor()
    # write a query and execute it
    cur.execute("select count(*) as all_count from res")
    # loop through the results
    for record in cur:
        # handle the result
        print(record[0])  # print the first column of the record
    con.close()
