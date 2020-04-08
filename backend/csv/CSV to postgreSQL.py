from backend.create_connnection import create_connection

print("\n### CSV to postgreSQL.py ###\n")

db = create_connection()
c = db[1]
cur = db[0]

filenames = ['products', 'profiles', 'profiles_previously_viewed', 'sessions']

for filename in filenames:
    with open(filename+'.csv') as csvfile:
        print("Copying {}...".format(filename))
        cur.copy_expert("COPY "+filename+" FROM STDIN DELIMITER ',' CSV HEADER", csvfile)
        c.commit()

c.commit()
cur.close()
c.close()