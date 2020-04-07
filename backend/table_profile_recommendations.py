from create_connnection import create_connection
import random

db = create_connection()
cur = db[0]
conn = db[1]

print("\n### table_profile_recommendations.py ###\n")

# Maakt tabel met data van views per product uit tabel products.


print("Creating table with recommendations per user...")

# Maakt tabel met recommendations per profiel uit tabel popular_categorys_per_user.
def make_tabel():
    cur.execute("DROP TABLE IF EXISTS profile_recommendations")

    cur.execute("CREATE TABLE profile_recommendations AS (select id, catrecommend, subcatrecommend, subsubcatrecommend ,subsubcatrecommend_2 from popular_categorys_per_user)")
    get_rid_null()

def get_rid_null():
    cur.execute("select id from products;")
    all_prods = cur.fetchall()

    cur.execute("select catrecommend from profile_recommendations where subsubcatrecommend IS NULL")
    all_cat_rec_1 = cur.fetchall()
    all_cat_rec_1 = set(all_cat_rec_1)
    all_cat_rec_1 = list(all_cat_rec_1)

    cur.execute("select catrecommend from profile_recommendations where subsubcatrecommend_2 IS NULL")
    all_cat_rec_2 = cur.fetchall()
    all_cat_rec_2 = set(all_cat_rec_2)
    all_cat_rec_2 = list(all_cat_rec_2)

    for t in range(0, len(all_cat_rec_1)):
        print("\rRendering profile recommendations: {} from 7....".format(t), end='')
        ex = """UPDATE profile_recommendations SET subsubcatrecommend = %s where catrecommend like %s and subsubcatrecommend IS NULL"""
        cur.execute(ex, (random.choice(all_prods), all_cat_rec_1[t], ))
        conn.commit()
    print('Removed null from subsubcatrecommend')

    for ind in range(0, len(all_cat_rec_2)):
        print("\rRendering profile recommendations: {} from 8....".format(ind), end='')
        ex = """UPDATE profile_recommendations SET subsubcatrecommend_2 = %s where catrecommend like %s and subsubcatrecommend_2 IS NULL;"""
        cur.execute(ex, (random.choice(all_prods), all_cat_rec_2[ind], ))
    print('Removed null from subsubcatrecommend_2')

    print("Recommendations created for user!")

make_tabel()

conn.commit()

cur.close()
conn.close()

# Start het eerstvolgende bestand.

exec(open('RecommendPerProduct_names.py').read())