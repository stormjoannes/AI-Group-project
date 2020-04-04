from backend.create_connnection import create_connection

db = create_connection()
cur = db[0]
conn = db[1]

print("\n### RecommendedPerUser.py ###\n")

print("Setting up tables...")

cur.execute("DROP TABLE IF EXISTS all_prof_rec")

cur.execute("CREATE TABLE all_prof_rec (id varchar PRIMARY KEY, "                
            "catrecommend varchar, "
            "subcatrecommend varchar, "
            "subsubcatrecommend varchar, "
            "genderrecommend varchar);")

print("Getting all id's...")
cur.execute("select id from profile_recommendations;")
all_id = cur.fetchall()

print('Getting all category recommended...')
cur.execute("select catrecommend from profile_recommendations;")
all_catrecommend = cur.fetchall()

print('Getting all subcategory recommended...')
cur.execute("select subcatrecommend from profile_recommendations;")
all_subcatrecommend = cur.fetchall()

print('Getting all subsubcategory recommended...')
cur.execute("select subsubcatrecommend from profile_recommendations;")
all_subsubcatrecommend = cur.fetchall()

print('Getting all targetaudience + deal recommended...')
cur.execute("select recommendation from profid_targetaudience;")
all_genderrecommend = cur.fetchall()

for tel in range(0, len(all_id)):
    print("\rcalculating recommendations {}....".format(tel), end='')
    cur.execute("INSERT INTO all_prof_rec (id, catrecommend, subcatrecommend, subsubcatrecommend, genderrecommend) VALUES (%s, %s, %s, %s, %s)", (all_id[tel], all_catrecommend[tel], all_subcatrecommend[tel], all_subsubcatrecommend[tel], all_genderrecommend[tel]))

print("Recommendations created for user!")

conn.commit()

cur.close()
conn.close()

# Start het eerstvolgende bestand.
