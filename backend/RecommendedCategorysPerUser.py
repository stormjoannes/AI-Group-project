from create_connnection import create_connection

db = create_connection()
cur = db[0]
conn = db[1]


def get_all_inf():
    print("\n### RecommendedCategorysPerUser.py ###\n")

    invoer = 'CategorysPerUser'
    inv = open(invoer, 'r')

    print("Getting CategorysPerUser...")

    read = inv.readlines()

    # Haalt data van alle categorys per profiel uit het .txt bestand.

    data = []
    for i in range(len(read)):
        current_data = eval(read[i])
        data.append(current_data)

    inv.close()
    most_seen_per_user(data)


def most_seen_per_user(data):
    print("Calculating most used categorys per user...")
    # Berekend per profiel wat de meest bekeken category, subcategory en subsubcategory is.
    favsperuser = []
    for i in range(len(data)):
        categorycount = []
        categorys = list(set(data[i][1][1]))
        for j in range(len(categorys)):
            if categorys[j] is not None:
                currentcount = [(data[i][1][1].count(categorys[j])), categorys[j]]
                categorycount.append(currentcount)
        categorycount.sort(reverse=True)
        if len(categorycount) < 1:
            categorycount = [[0, None]]

        subcategorycount = []
        subcategorys = list(set(data[i][2][1]))
        for j in range(len(subcategorys)):
            if subcategorys[j] is not None:
                currentcount = [(data[i][2][1].count(subcategorys[j])), subcategorys[j]]
                subcategorycount.append(currentcount)
        subcategorycount.sort(reverse=True)
        if len(subcategorycount) < 1:
            subcategorycount = [[0, None]]

        subsubcategorycount = []
        subsubcategorys = list(set(data[i][3][1]))
        for j in range(len(subsubcategorys)):
            if subsubcategorys[j] is not None:
                currentcount = [(data[i][3][1].count(subsubcategorys[j])), subsubcategorys[j]]
                subsubcategorycount.append(currentcount)
        subsubcategorycount.sort(reverse=True)
        if len(subsubcategorycount) < 1:
            subsubcategorycount = [[0, None]]

        currentfavs = [data[i][0], [categorycount[0][1], subcategorycount[0][1], subsubcategorycount[0][1]]]
        favsperuser.append(currentfavs)

    print("Putting calculated data in table...")
    fix_table()
    cat_favo(favsperuser)


def fix_table():
    # Voegt kolommen toe aan tabel profiles om data van favoriete categorien per user in te stoppen.

    cur.execute("ALTER TABLE profiles DROP COLUMN IF EXISTS mostusedcat")
    cur.execute("ALTER TABLE profiles DROP COLUMN IF EXISTS mostusedsubcat")
    cur.execute("ALTER TABLE profiles DROP COLUMN IF EXISTS mostusedsubsubcat")

    cur.execute("ALTER TABLE profiles ADD mostusedcat varchar")
    cur.execute("ALTER TABLE profiles ADD mostusedsubcat varchar")
    cur.execute("ALTER TABLE profiles ADD mostusedsubsubcat varchar")

    conn.commit()


def cat_favo(favsperuser):
    # Voegt data van favoriete category, subcategory en subsubcategory bij bijbehorende profiel.
    print('Adding favorite category...')
    for i in range(len(favsperuser)):
        print("\r{} of {} in table...".format(i + 1, len(favsperuser)), end="")
        catname = favsperuser[i][1][0]
        if catname is not None:
            if "'" in catname:
                catname = catname.split("'")
                catname = catname[0] + "''" + catname[1]
            cur.execute("UPDATE profiles SET mostusedcat='{}' WHERE id='{}'".format(catname, favsperuser[i][0]))
        else:
            cur.execute("UPDATE profiles SET mostusedcat='{}' WHERE id='{}'".format(catname, favsperuser[i][0]))
    subcat_favo(favsperuser, i)


def subcat_favo(favsperuser, i):
    print('Adding favorite subcategory...')
    subcatname = favsperuser[i][1][1]
    if subcatname is not None:
        if "'" in subcatname:
            subcatname = subcatname.split("'")
            subcatname = subcatname[0] + "''" + subcatname[1]
        cur.execute("UPDATE profiles SET mostusedsubcat='{}' WHERE id='{}'".format(subcatname, favsperuser[i][0]))
    else:
        cur.execute("UPDATE profiles SET mostusedsubcat='{}' WHERE id='{}'".format(subcatname, favsperuser[i][0]))
    subsubcat_favo(favsperuser, i)

def subsubcat_favo(favsperuser, i):
    print('Adding favorite subsubcategory...')
    subsubcatname = favsperuser[i][1][2]
    if subsubcatname is not None:
        if "'" in subsubcatname:
            subsubcatname = subsubcatname.split("'")
            subsubcatname = subsubcatname[0] + "''" + subsubcatname[1]
        cur.execute(
            "UPDATE profiles SET mostusedsubsubcat='{}' WHERE id='{}'".format(subsubcatname, favsperuser[i][0]))
    else:
        cur.execute("UPDATE profiles SET mostusedsubsubcat='{}' WHERE id='{}'".format(subsubcatname, favsperuser[i][0]))
    conn.commit()


get_all_inf()


cur.close()
conn.close()

# Start het eerstvolgende bestand.

exec(open('RecommendedPerUser.py').read())
