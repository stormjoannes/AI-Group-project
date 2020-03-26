import psycopg2

print("\n### FetchCode.py ###\n")

uitvoer = 'DataProductsPerUser'

uit = open(uitvoer, 'w')

conn = psycopg2.connect("dbname=Onlinestore user=postgres password=0Ksndjskxw")
cur = conn.cursor()
print("Getting code...")

# Haalt de sessiedata op per profiel met daarbij de producten die zijn bekeken.

cur.execute("select profiles.id, sessions.endtime, sessions.duration, sessions.sale, "
            "profiles_previously_viewed.prodid, products.category, products.subcategory, products.subsubcategory, "
            "products.name, products.targetaudience, products.sellingprice, products.deal from profiles "
            "left JOIN sessions ON profiles.id=sessions.profid "
            "left JOIN profiles_previously_viewed ON profiles.id=profiles_previously_viewed.profid "
            "inner JOIN products ON products.id=profiles_previously_viewed.prodid "
            "ORDER BY profiles.id, sessions.endtime, sessions.sale")

code = cur.fetchall()
profids = []
ids = []
count = 0
print("Formatting...")

# Zet het profiel samen met de categorien en namen van alle producten die zijn bekeken door dat profiel in een list.
# Daarnaast zit er code in die maar max 1 profiel per keer converteerd, om zo het programma een beetje snel te houden.

for j in range(len(code)):
    print("\rFormatting {} of {}...".format(j+1, len(code)), end="")
    if len(profids) > 1:
        uit.write('{}\n'.format(profids[0]))
        profids = [profids[1]]
        ids = [ids[1]]
        count += 1

        current = []
        if code[j][0] not in ids:
            ids.append(code[j][0])
            current.append(code[j][0])
            current.append([[code[j][5], code[j][6], code[j][7], code[j][8]]])
            profids.append(current)
        else:
            for k in range(len(profids)):
                if profids[k][0] == code[j][0]:
                    profids[k][1].append([code[j][5], code[j][6], code[j][7], code[j][8]])
                    break
    else:
        current = []
        if code[j][0] not in ids:
            ids.append(code[j][0])
            current.append(code[j][0])
            current.append([[code[j][5], code[j][6], code[j][7], code[j][8]]])
            profids.append(current)
        else:
            for k in range(len(profids)):
                if profids[k][0] == code[j][0]:
                    profids[k][1].append([code[j][5], code[j][6], code[j][7], code[j][8]])
                    break

uit.write('{}\n'.format(profids[0]))

print("Exporting data to DataProductsPerUser...")

# De data die is gelinkt wordt uit de list in een .txt bestand gezet.

uit.close()
print("\nPrinted {} items!".format(count))
cur.close()
conn.close()

# Start het eerstvolgende bestand.

exec(open("CatagoryConversion.py").read())
