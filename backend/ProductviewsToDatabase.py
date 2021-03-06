from create_connnection import create_connection

db = create_connection()
cur = db[0]
conn = db[1]

print("\n### ProductviewsToDatabase.py ###\n")
invoer = 'AllUsedCategorys'
inv = open(invoer, 'r')

read = inv.readlines()


def count_objects_frame():
    # Haalt data van alle categorys van alle profielen uit het .txt bestand.

    data = []
    for i in range(len(read)):
        current_data = eval(read[i])
        data.append(current_data)

    inv.close()

    print("Counting categorys...")

    # Telt hoe vaak een category is bekeken.

    categorycount = []
    categorys = list(set(data[0][1]))
    for i in range(len(categorys)):
        print("\rCounted {} of {} categorys".format(i + 1, len(categorys)), end="")
        currentcount = [(data[0][1].count(categorys[i])), categorys[i]]
        categorycount.append(currentcount)

    categorycount.sort(reverse=True)

    print("\nCounting subcategorys...")

    # Telt hoe vaak een subcategory is bekeken.

    subcategorycount = []
    subcategorys = list(set(data[1][1]))
    for i in range(len(subcategorys)):
        print("\rCounted {} of {} subcategorys".format(i + 1, len(subcategorys)), end="")
        currentcount = [(data[1][1].count(subcategorys[i])), subcategorys[i]]
        subcategorycount.append(currentcount)

    subcategorycount.sort(reverse=True)

    print("\nCounting subsubcategorys...")

    # Telt hoe vaak een subsubcategory is bekeken.

    subsubcategorycount = []
    subsubcategorys = list(set(data[2][1]))
    for i in range(len(subsubcategorys)):
        print("\rCounted {} of {} subsubcatagorys".format(i + 1, len(subsubcategorys)), end="")
        currentcount = [(data[2][1].count(subsubcategorys[i])), subsubcategorys[i]]
        subsubcategorycount.append(currentcount)

    subsubcategorycount.sort(reverse=True)

    print("\nCounting names...")

    # Telt hoe vaak elk product is bekeken.

    namescount = []
    names = list(set(data[3][1]))
    for i in range(len(names)):
        print("\rCounted {} of {} names".format(i + 1, len(names)), end="")
        currentcount = [(data[3][1].count(names[i])), names[i]]
        namescount.append(currentcount)

    namescount.sort(reverse=True)

    # vanaf hier ga je de andere tables runnen en de informatie uit deze functie halen
    fix_table()
    category(categorycount)
    subcategory(subcategorycount)
    subsubcategory(subsubcategorycount)
    names_exp(namescount)


def fix_table():
    print("\nAltering Tables...")

    # Voegt kolommen toe aan products waar de data van het tellen in kan worden gezet.

    cur.execute("ALTER TABLE products DROP COLUMN IF EXISTS categoryviews")
    cur.execute("ALTER TABLE products DROP COLUMN IF EXISTS subcategoryviews")
    cur.execute("ALTER TABLE products DROP COLUMN IF EXISTS subsubcategoryviews")
    cur.execute("ALTER TABLE products DROP COLUMN IF EXISTS productviews")

    cur.execute("ALTER TABLE products ADD categoryviews integer")
    cur.execute("ALTER TABLE products ADD subcategoryviews integer")
    cur.execute("ALTER TABLE products ADD subsubcategoryviews integer")
    cur.execute("ALTER TABLE products ADD productviews integer")

    conn.commit()


def category(categorycount):
    print("Exporting data from category...")

    # Zet de teldata van alle categorys in de kolom bij producten met dezelfde category.

    for i in range(len(categorycount)):
        name = categorycount[i][1]
        if name is not None:
            if "'" in name:
                name = name.split("'")
                name = name[0] + "''" + name[1]
            cur.execute("UPDATE products SET categoryviews={} WHERE category='{}'".format(categorycount[i][0], name))
        else:
            cur.execute("UPDATE products SET categoryviews={} WHERE category='{}'".format(categorycount[i][0], name))

    # Zet de teldata van alle subcategorys in de kolom bij producten met dezelfde subcategory.


def subcategory(subcategorycount):
    print("Exporting data from subcategory...")
    for i in range(len(subcategorycount)):
        name = subcategorycount[i][1]
        if name is not None:
            if "'" in name:
                name = name.split("'")
                name = name[0] + "''" + name[1]
            cur.execute(
                "UPDATE products SET subcategoryviews={} WHERE subcategory='{}'".format(subcategorycount[i][0], name))
        else:
            cur.execute(
                "UPDATE products SET subcategoryviews={} WHERE subcategory='{}'".format(subcategorycount[i][0], name))

    # Zet de teldata van alle subsubcategorys in de kolom bij producten met dezelfde subsubcategory.


def subsubcategory(subsubcategorycount):
    print("Exporting data from subsubcategory...")
    for i in range(len(subsubcategorycount)):
        name = subsubcategorycount[i][1]
        if name is not None:
            if "'" in name:
                name = name.split("'")
                name = name[0] + "''" + name[1]
            cur.execute(
                "UPDATE products SET subsubcategoryviews={} WHERE subsubcategory='{}'".format(subsubcategorycount[i][0],
                                                                                              name))
        else:
            cur.execute(
                "UPDATE products SET subsubcategoryviews={} WHERE subsubcategory='{}'".format(subsubcategorycount[i][0],
                                                                                              name))


def names_exp(namescount):
    print("Exporting data from names...")
    # Zet de teldata van alle producten in de kolom bij producten met dezelfde naam.

    for i in range(len(namescount)):
        name = namescount[i][1]
        if name is not None:
            if "'" in name:
                name = name.split("'")
                name = name[0] + "''" + name[1]
            cur.execute("UPDATE products SET productviews={} WHERE name='{}'".format(namescount[i][0], name))
        else:
            cur.execute("UPDATE products SET productviews={} WHERE name='{}'".format(namescount[i][0], name))


count_objects_frame()

print("Data exported!")

conn.commit()

cur.close()
conn.close()

# Start het eerstvolgende bestand.

exec(open('RecommendedCategorysPerUser.py').read())
