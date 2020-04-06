from backend.create_connnection import create_connection

db = create_connection()
cur = db[0]
conn = db[1]

print("\n### RecommendedPerUser.py ###\n")

# Maakt tabel met data van views per product uit tabel products.


print("Creating table with recommendations per user...")

# Maakt tabel met recommendations per profiel uit tabel popular_categorys_per_user.

cur.execute("DROP TABLE IF EXISTS profile_recommendations")

cur.execute("CREATE TABLE profile_recommendations AS (select id, catrecommend, subcatrecommend, subsubcatrecommend ,subsubcatrecommend_2 from popular_categorys_per_user)")

print("Recommendations created for user!")

conn.commit()

cur.close()
conn.close()

# Start het eerstvolgende bestand.

exec(open('RecommendPerProduct.py').read())