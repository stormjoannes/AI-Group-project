from create_connnection import create_connection
import random

db = create_connection()
cur = db[0]
conn = db[1]

print("\n### RecommendedPerUser.py ###\n")

print("Setting up tables...")

# Maakt tabel met data van views per product uit tabel products.
def frame_base():
    cur.execute("DROP TABLE IF EXISTS valuesproducts")

    cur.execute("CREATE TABLE valuesproducts AS (select id, name, targetaudience, brand, category, subcategory, "
                "subsubcategory, categoryviews, subcategoryviews, subsubcategoryviews, productviews from products)")

    # Maakt tabel met data van favoriete categorys per profiel uit tabel profiles.

    cur.execute("DROP TABLE IF EXISTS popular_categorys_per_user")

    cur.execute("CREATE TABLE popular_categorys_per_user AS (select id, mostusedcat, mostusedsubcat, mostusedsubsubcat "
                "from profiles)")

    # Zet kolommen voor recommendations op basis van category in tabel popular_categorys_per_user.

    cur.execute("ALTER TABLE popular_categorys_per_user ADD catrecommend varchar")
    cur.execute("ALTER TABLE popular_categorys_per_user ADD subcatrecommend varchar")
    cur.execute("ALTER TABLE popular_categorys_per_user ADD subsubcatrecommend varchar")
    cur.execute("ALTER TABLE popular_categorys_per_user ADD subsubcatrecommend_2 varchar")
    conn.commit()
    favorite_most_seen()

def favorite_most_seen():
    print("Getting data...")
    # Haalt alle favoriete categorys op en zorgt ervoor dat er maar 1 van elk in de lijst staat.

    cur.execute("select mostusedcat from popular_categorys_per_user")

    categorys = list(set(cur.fetchall()))

    # Haalt meest bekeken product op aan de hand van meest bekeken category.

    cur.execute("select id from valuesproducts where categoryviews is not null and subcategoryviews is not null and"
                " subsubcategoryviews is not null and productviews is not null "
                "order by categoryviews desc,  subcategoryviews desc, subsubcategoryviews desc, productviews desc "
                "limit 1")

    defaultcatrec = cur.fetchall()

    # Haalt alle favoriete subcategorys op en zorgt ervoor dat er maar 1 van elk in de lijst staat.

    cur.execute("select mostusedsubcat from popular_categorys_per_user")

    subcategorys = list(set(cur.fetchall()))

    # Haalt 2 meest bekeken producten op aan de hand van meest bekeken subcategory.

    cur.execute("select id from valuesproducts where subcategoryviews is not null and"
                " subsubcategoryviews is not null and productviews is not null "
                "order by subcategoryviews desc, subsubcategoryviews desc, productviews desc "
                "limit 2")

    defaultsubcatrec = cur.fetchall()

    # Haalt alle favoriete subsubcategorys op en zorgt ervoor dat er maar 1 van elk in de lijst staat.

    cur.execute("select mostusedsubsubcat from popular_categorys_per_user")

    subsubcategorys = list(set(cur.fetchall()))

    # Haalt 3 meest bekeken producten op aan de hand van meest bekeken subsubcategory.

    cur.execute("select id from valuesproducts where subsubcategoryviews is not null and productviews is not null "
                "order by subsubcategoryviews desc, productviews desc "
                "limit 3")

    defaultsubsubcatrec = cur.fetchall()
    category_recommend(categorys, defaultcatrec)
    subcategory_recommend(subcategorys, defaultsubcatrec)
    subsubcategory_recommend(subsubcategorys, defaultsubsubcatrec)

def category_recommend(categorys, defaultcatrec):
    print("Calculating category recommendations...")
    # Haalt recommendations per favoriete category op aan de hand van categoryviews,
    # en zet deze in popular_categorys_per_user bij de juiste categorys.
    # Daarnaast zet hij in de lege velden het meest overal bekeken product op basis van meest bekeken category.
    catrecs = []
    for i in range(len(categorys)):
        if categorys[i][0]:
            cur.execute("select id from valuesproducts where categoryviews is not null and "
                        "productviews is not null and category = '{}'"
                        "order by categoryviews desc, subcategoryviews desc, subsubcategoryviews desc, productviews desc "
                        "limit 1".format(categorys[i][0]))
            fetch = cur.fetchall()
            catrecs.append([categorys[i][0], fetch])

    for i in range(len(catrecs)):
        if catrecs[i][1]:
            if catrecs[i][0] != 'None':
                name = catrecs[i][0]
                if "'" in name:
                    name = name.split("'")
                    name = name[0] + "''" + name[1]
                    cur.execute("UPDATE popular_categorys_per_user SET catrecommend = '{}' "
                                "WHERE mostusedcat = '{}'".format(catrecs[i][1][0][0], name))
                else:
                    cur.execute("UPDATE popular_categorys_per_user SET catrecommend = '{}' "
                                "WHERE mostusedcat = '{}'".format(catrecs[i][1][0][0], name))


    cur.execute("UPDATE popular_categorys_per_user SET catrecommend = '{}' "
                "WHERE catrecommend is null".format(defaultcatrec[0][0]))

    conn.commit()

def subcategory_recommend(subcategorys, defaultsubcatrec):
    print("Calculating subcategory recommendations...")

    # Haalt recommendations per favoriete subcategory op aan de hand van subcategoryviews,
    # en zet deze in popular_categorys_per_user bij de juiste subcategorys.
    # Daarnaast zet hij in de lege velden het meest overal bekeken product op basis van meest bekeken subcategory.

    subcatrecs = []

    for i in range(len(subcategorys)):
        if subcategorys[i][0]:
            name = subcategorys[i][0]
            if "'" in name:
                name = name.split("'")
                name = name[0] + "''" + name[1]
                cur.execute("select id from valuesproducts where subcategoryviews is not null and productviews is not null "
                            "and subcategory = '{}'"
                            "order by categoryviews desc, subcategoryviews desc, subsubcategoryviews desc, "
                            "productviews desc "
                            "limit 2".format(name))
                fetch = cur.fetchall()
                if len(fetch) == 1:
                    subcatrecs.append([name, [fetch[0], fetch[0]]])
                else:
                    subcatrecs.append([name, fetch])
            else:
                cur.execute("select id from valuesproducts where subcategoryviews is not null and productviews is not null "
                            "and subcategory = '{}'"
                            "order by categoryviews desc, subcategoryviews desc, subsubcategoryviews desc, "
                            "productviews desc "
                            "limit 2".format(name))
                fetch = cur.fetchall()
                if len(fetch) == 1:
                    subcatrecs.append([name, [fetch[0], fetch[0]]])
                else:
                    subcatrecs.append([name, fetch])

    for i in range(len(subcatrecs)):
        if subcatrecs[i][1]:
            if subcatrecs[i][0] != 'None':
                for j in range(2):
                    cur.execute("UPDATE popular_categorys_per_user SET subcatrecommend = '{}' "
                                "WHERE mostusedsubcat = '{}' "
                                "and catrecommend != '{}' "
                                "and subcatrecommend is null".format(subcatrecs[i][1][j][0], subcatrecs[i][0],
                                                                     subcatrecs[i][1][j][0]))

    for i in range(2):
        cur.execute("UPDATE popular_categorys_per_user SET subcatrecommend = '{}' "
                    "WHERE subcatrecommend is null and catrecommend != '{}'".format(defaultsubcatrec[i][0],
                                                                                    defaultsubcatrec[i][0]))

    conn.commit()

def subsubcategory_recommend(subsubcategorys, defaultsubsubcatrec):
    print("Calculating subsubcategory recommendations...")
    # Haalt recommendations per favoriete subsubcategory op aan de hand van subsubcategoryviews,
    # en zet deze in popular_categorys_per_user bij de juiste subsubcategorys.
    # Daarnaast zet hij in de lege velden het meest overal bekeken product op basis van meest bekeken subsubcategory.

    subsubcatrecs = []

    for i in range(len(subsubcategorys)):
        if subsubcategorys[i][0]:
            name = subsubcategorys[i][0]
            if "'" in name:
                name = name.split("'")
                name = name[0] + "''" + name[1]
            cur.execute("select id from valuesproducts where subsubcategoryviews is not null "
                        "and productviews is not null "
                        "and subsubcategory = '{}'"
                        "order by categoryviews desc, subcategoryviews desc, subsubcategoryviews desc, "
                        "productviews desc "
                        "limit 6".format(name))
            fetch = cur.fetchall()
            random.shuffle(fetch)
            if len(fetch) == 1:
                subsubcatrecs.append([name, [fetch[0], fetch[0], fetch[0], fetch[0], fetch[0], fetch[0]]])
            elif len(fetch) == 2:
                subsubcatrecs.append([name, [fetch[0], fetch[0], fetch[0], fetch[1], fetch[1], fetch[1]]])
            elif len(fetch) == 3:
                subsubcatrecs.append([name, [fetch[0], fetch[0], fetch[1], fetch[1], fetch[2], fetch[2]]])
            elif len(fetch) == 4:
                subsubcatrecs.append([name, [fetch[0], fetch[1], fetch[1], fetch[2], fetch[3], fetch[3]]])
            elif len(fetch) == 5:
                subsubcatrecs.append([name, [fetch[0], fetch[1], fetch[1], fetch[2], fetch[3], fetch[4]]])
            else:
                subsubcatrecs.append([name, fetch])

    for i in range(len(subsubcatrecs)):
        print("\rRendering profile subsub- en subsub_2recommendations: {} from 216....".format(i), end='')
        if subsubcatrecs[i][1]:
            if subsubcatrecs[i][0] != 'None':
                for j in range(0, 6):
                    cur.execute("UPDATE popular_categorys_per_user SET subsubcatrecommend = '{}' "
                                "WHERE mostusedsubsubcat = '{}' "
                                "and subcatrecommend != '{}' "
                                "and catrecommend != '{}' "
                                "and subsubcatrecommend is null".format(subsubcatrecs[i][1][j][0], subsubcatrecs[i][0],
                                                                        subsubcatrecs[i][1][j][0],
                                                                        subsubcatrecs[i][1][j][0]))
                conn.commit()
                for h in range(0, 6):
                    cur.execute("UPDATE popular_categorys_per_user SET subsubcatrecommend_2 = '{}' "
                                "WHERE mostusedsubsubcat = '{}' "
                                "and subcatrecommend != '{}' "
                                "and catrecommend != '{}' "
                                "and subsubcatrecommend != '{}' "
                                "and subsubcatrecommend_2 is null".format(subsubcatrecs[i][1][h][0], subsubcatrecs[i][0],
                                                                          subsubcatrecs[i][1][h][0],
                                                                          subsubcatrecs[i][1][h][0],
                                                                          subsubcatrecs[i][1][h][0]))
                conn.commit()

    for i in range(2):
        cur.execute("UPDATE popular_categorys_per_user SET subsubcatrecommend = '{}' "
                    "WHERE subsubcatrecommend is null "
                    "and catrecommend != '{}' "
                    "and subcatrecommend != '{}'".format(defaultsubsubcatrec[0][0], defaultsubsubcatrec[0][0],
                                                         defaultsubsubcatrec[0][0]))

        cur.execute("UPDATE popular_categorys_per_user SET subsubcatrecommend_2 = '{}' "
                    "WHERE subsubcatrecommend is null "
                    "and catrecommend != '{}' "
                    "and subcatrecommend != '{}'".format(defaultsubsubcatrec[1][0], defaultsubsubcatrec[1][0],
                                                         defaultsubsubcatrec[1][0]))
    conn.commit()
frame_base()

cur.close()
conn.close()

# Start het eerstvolgende bestand.

exec(open('table_profile_recommendations.py').read())