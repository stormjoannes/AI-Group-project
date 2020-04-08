import psycopg2

# create connection function so I can use it everywhere


def create_connection():
    try:
        conn = psycopg2.connect("dbname=Onlinestore user=postgres password=0Ksndjskxw")
        cur = conn.cursor()
        # return two values so I can close them both at the end
        return cur, conn

    except(Exception, psycopg2.DatabaseError):
        print(psycopg2.DatabaseError)