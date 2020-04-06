import time
from backend.create_connnection import create_connection
db = create_connection()
cur = db[0]
conn = db[1]
tijd = time.time()
print("\n### RecommendPerProduct_names.py ###\n")
def vergelijking(naam):
    naam = naam[0]
    if naam:
        if "'" in naam:
            current = naam.split("'")
            naam = "''".join(map(str, current))
        vergelijknaam = naam
        loophouder = 0
        runcounter = 0
        run = 0
        while loophouder == 0:
            if "'" in vergelijknaam:
                current = vergelijknaam.split("'")
                vergelijknaam = "''".join(map(str, current))
            cur.execute("""select id FROM products WHERE name like '{}' AND name != '{}' LIMIT 5""".format(('%' + vergelijknaam + '%'), naam))
            record = cur.fetchall()
            if len(record) < 5:
                if ' ' in naam and runcounter < 2:
                    vergelijknaam = naam.split(' ')[runcounter]
                    if runcounter == 0:
                        vergelijknaam = vergelijknaam + ' '
                    if runcounter == 1:
                        vergelijknaam = ' ' + vergelijknaam
                else:
                    if run == 0:
                        vergelijknaam = naam.split(' ')[0]
                        run = 1
                    vergelijknaam = vergelijknaam[:len(vergelijknaam)//2]
                runcounter += 1
            else:
                loophouder = 1
        cur.execute(
            "SELECT catrecommend, subcatrecommend, subsubcatrecommend, id FROM products WHERE name = '{}'".format(naam))
        recs_raw = cur.fetchall()
        recs = [recs_raw[0][0], recs_raw[0][1], recs_raw[0][2], None, recs_raw[0][3]]
        for i in range(len(record)):
            if not recs[3]:
                if recs[0] is None and record[i][0] not in recs:
                    if "'" in record[i][0]:
                        current = record[i][0].split("'")
                        recordid = "''".join(map(str, current))
                    else:
                        recordid = record[i][0]
                    recs[0] = recordid
                elif recs[1] is None and record[i][0] not in recs:
                    if "'" in record[i][0]:
                        current = record[i][0].split("'")
                        recordid = "''".join(map(str, current))
                    else:
                        recordid = record[i][0]
                    recs[1] = recordid
                elif recs[2] is None and record[i][0] not in recs:
                    if "'" in record[i][0]:
                        current = record[i][0].split("'")
                        recordid = "''".join(map(str, current))
                    else:
                        recordid = record[i][0]
                    recs[2] = recordid
                elif recs[3] is None and record[i][0] not in recs:
                    if "'" in record[i][0]:
                        current = record[i][0].split("'")
                        recordid = "''".join(map(str, current))
                    else:
                        recordid = record[i][0]
                    recs[3] = recordid
            else:
                break
        execute = "UPDATE products SET catrecommend = %s, subcatrecommend = %s, subsubcatrecommend = %s, namerecommend = %s WHERE name = %s"
        cur.execute(execute, (recs[0], recs[1], recs[2], recs[3], naam))
        # cur.execute("UPDATE products SET catrecommend = '{}', subcatrecommend = '{}', "
        #             "subsubcatrecommend = '{}', namerecommend = '{}' "
        #             "WHERE name = '{}'".format(recs[0], recs[1], recs[2], recs[3], naam))

print("Setting up tables...")
# Maakt tabel met data van views per product uit tabel products.
cur.execute("DROP TABLE IF EXISTS valuesproducts")
cur.execute("CREATE TABLE valuesproducts AS (select id, name, targetaudience, brand, category, subcategory, "
            "subsubcategory, categoryviews, subcategoryviews, subsubcategoryviews, productviews from products)")
# Zet kolommen voor recommendations op basis van category in tabel products.
cur.execute("ALTER TABLE products DROP COLUMN IF EXISTS catrecommend")
cur.execute("ALTER TABLE products DROP COLUMN IF EXISTS subcatrecommend")
cur.execute("ALTER TABLE products DROP COLUMN IF EXISTS subsubcatrecommend")
cur.execute("ALTER TABLE products DROP COLUMN IF EXISTS namerecommend")
cur.execute("ALTER TABLE products ADD catrecommend varchar")
cur.execute("ALTER TABLE products ADD subcatrecommend varchar")
cur.execute("ALTER TABLE products ADD subsubcatrecommend varchar")
cur.execute("ALTER TABLE products ADD namerecommend varchar")
conn.commit()
print("Getting data...")
# Haalt alle categorys op en zorgt ervoor dat er maar 1 van elk in de lijst staat.
cur.execute("select category from products")
categorys = list(set(cur.fetchall()))
# Haalt alle subcategorys op en zorgt ervoor dat er maar 1 van elk in de lijst staat.
cur.execute("select subcategory from products")
subcategorys = list(set(cur.fetchall()))
# Haalt alle subsubcategorys op en zorgt ervoor dat er maar 1 van elk in de lijst staat.
cur.execute("select subsubcategory from products")
subsubcategorys = list(set(cur.fetchall()))
print("Calculating category recommendations...")
# Haalt recommendations per category op aan de hand van categoryviews,
# en zet deze in products bij de juiste categorys.
# Daarnaast zet hij in de lege velden het meest overal bekeken product op basis van meest bekeken category.
conn.commit()
catrecs = []
for i in range(len(categorys)):
    if categorys[i][0]:
        if '[' not in categorys[i][0]:
            name = categorys[i][0]
            if "'" in name:
                currentcat = name.split("'")
                name = "''".join(map(str, currentcat))
            cur.execute("select id from valuesproducts where categoryviews is not null and "
                        "productviews is not null and category = '{}'"
                        "order by categoryviews desc, subcategoryviews desc, "
                        "subsubcategoryviews desc, productviews desc "
                        "limit 2".format(name))
            fetch = cur.fetchall()
            if len(fetch) == 1:
                catrecs.append([name, [fetch[0], fetch[0]]])
            else:
                catrecs.append([name, fetch])
for i in range(len(catrecs)):
    if catrecs[i][1]:
        if catrecs[i][0] != 'None':
            for j in range(len(catrecs[i][1])):
                cur.execute("UPDATE products SET catrecommend = '{}' "
                            "WHERE category = '{}' "
                            "and catrecommend is null "
                            "and id != '{}'".format(catrecs[i][1][j][0], catrecs[i][0], catrecs[i][1][j][0]))
print("Calculating subcategory recommendations...")
# Haalt recommendations per subcategory op aan de hand van subcategoryviews,
# en zet deze in products bij de juiste subcategorys.
# Daarnaast zet hij in de lege velden het meest overal bekeken product op basis van meest bekeken subcategory.
subcatrecs = []
for i in range(len(subcategorys)):
    name = subcategorys[i][0]
    if subcategorys[i][0]:
        if "'" in name:
            currentsubcat = name.split("'")
            name = "''".join(map(str, currentsubcat))
        cur.execute("select id from valuesproducts where subsubcategoryviews is not null and "
                    "productviews is not null and subsubcategory = '{}'"
                    "order by categoryviews desc, subcategoryviews desc, "
                    "subsubcategoryviews desc, productviews desc "
                    "limit 3".format(name))
        fetch = cur.fetchall()
        if len(fetch) == 1:
            subcatrecs.append([name, [fetch[0], fetch[0], fetch[0]]])
        elif len(fetch) == 2:
            subcatrecs.append([name, [fetch[0], fetch[1], fetch[1]]])
        else:
            subcatrecs.append([name, fetch])
for i in range(len(subcatrecs)):
    if subcatrecs[i][1]:
        if subcatrecs[i][0] != 'None':
            for j in range(len(subcatrecs[i][1])):
                cur.execute("UPDATE products SET subcatrecommend = '{}' "
                            "WHERE subcategory = '{}' "
                            "and catrecommend != '{}' "
                            "and subcatrecommend is null "
                            "and id != '{}'".format(subcatrecs[i][1][j][0], subcatrecs[i][0],
                                                    subcatrecs[i][1][j][0], subcatrecs[i][1][j][0]))
conn.commit()
print("Calculating subsubcategory recommendations...")
# Haalt recommendations per subsubcategory op aan de hand van subsubcategoryviews,
# en zet deze in products bij de juiste subsubcategorys.
# Daarnaast zet hij in de lege velden het meest overal bekeken product op basis van meest bekeken subsubcategory.
subsubcatrecs = []
for i in range(len(subsubcategorys)):
    if subsubcategorys[i][0]:
        name = subsubcategorys[i][0]
        if "'" in name:
            currentsubsubcat = name.split("'")
            name = "''".join(map(str, currentsubsubcat))
        cur.execute("select id from valuesproducts where subsubcategoryviews is not null and "
                    "productviews is not null and subsubcategory = '{}'"
                    "order by categoryviews desc, subcategoryviews desc, "
                    "subsubcategoryviews desc, productviews desc "
                    "limit 4".format(name))
        fetch = cur.fetchall()
        if len(fetch) == 1:
            subsubcatrecs.append([name, [fetch[0], fetch[0], fetch[0], fetch[0]]])
        elif len(fetch) == 2:
            subsubcatrecs.append([name, [fetch[0], fetch[1], fetch[1], fetch[1]]])
        elif len(fetch) == 2:
            subsubcatrecs.append([name, [fetch[0], fetch[1], fetch[2], fetch[2]]])
        else:
            subsubcatrecs.append([name, fetch])
for i in range(len(subsubcatrecs)):
    if subsubcatrecs[i][1]:
        if subsubcatrecs[i][0] != 'None':
            for j in range(len(subsubcatrecs[i][1])):
                cur.execute("UPDATE products SET subsubcatrecommend = '{}' "
                            "WHERE subsubcategory = '{}' "
                            "and subcatrecommend != '{}' "
                            "and catrecommend != '{}' "
                            "and subsubcatrecommend is null "
                            "and id != '{}'".format(subsubcatrecs[i][1][j][0], subsubcatrecs[i][0],
                                                    subsubcatrecs[i][1][j][0], subsubcatrecs[i][1][j][0],
                                                    subsubcatrecs[i][1][j][0]))
print("Calculating name recommendations...")
cur.execute("select name FROM products")
namen = cur.fetchall()
count = 0
conn.commit()
for naam in namen:
    count += 1
    print('\r{} of {}'.format(count, len(namen)), end='')
    vergelijking(naam)
    conn.commit()
print("\nCreating table with recommendations per product...")
# Maakt tabel met recommendations per product uit tabel products.
cur.execute("DROP TABLE IF EXISTS product_recommendations")
cur.execute("CREATE TABLE product_recommendations AS (select id, catrecommend, subcatrecommend, subsubcatrecommend, "
            "namerecommend from products)")
print("Recommendations created for products!")
conn.commit()
cur.close()
conn.close()
eind = time.time()
print('tijd:')
print(eind-tijd)

exec(open('gender-discount_per_user.py').read())