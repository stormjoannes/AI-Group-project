from create_connnection import create_connection

print("\n### FetchCode.py ###\n")

uitvoer = 'DataProductsPerUser'

uit = open(uitvoer, 'w')

db = create_connection()
cur = db[0]
conn = db[1]
print("Getting code...")


def sessionsdata():
    # Haalt de sessiedata op per profiel met daarbij de producten die zijn bekeken.
    query = """SELECT profiles.id, sessions.endtime, sessions.duration, sessions.sale,
                profiles_previously_viewed.prodid, products.category, products.subcategory, products.subsubcategory,
                products.name, products.targetaudience, products.sellingprice, products.deal FROM profiles
                LEFT JOIN sessions ON profiles.id=sessions.profid
                LEFT JOIN profiles_previously_viewed ON profiles.id=profiles_previously_viewed.profid
                INNER JOIN products ON products.id=profiles_previously_viewed.prodid
                ORDER BY profiles.id, sessions.endtime, sessions.sale"""
    cur.execute(query)

    code = cur.fetchall()
    return code


def write_data(data):
    profids = []
    ids = []
    count = 0
    print("Formatting")

    # Zet het profiel samen met de categorien en namen van alle producten die zijn bekeken door dat profiel in een list.
    # Daarnaast zit er code in die maar max 1 profiel per keer converteerd, om zo het programma een beetje snel te houden.

    for j in range(len(data)):
        if j == 10000:
            break
        print("\rFormatting {} of {}...".format(j+1, len(data)), end="")
        if len(profids) > 1:
            uit.write('{}\n'.format(profids[0]))
            profids = [profids[1]]
            ids = [ids[1]]
            count += 1

            current = []
            if data[j][0] not in ids:
                ids.append(data[j][0])
                current.append(data[j][0])
                current.append([[data[j][5], data[j][6], data[j][7], data[j][8]]])
                profids.append(current)
            else:
                for k in range(len(profids)):
                    if profids[k][0] == data[j][0]:
                        profids[k][1].append([data[j][5], data[j][6], data[j][7], data[j][8]])
                        break
        else:
            current = []
            if data[j][0] not in ids:
                ids.append(data[j][0])
                current.append(data[j][0])
                current.append([[data[j][5], data[j][6], data[j][7], data[j][8]]])
                profids.append(current)
            else:
                for k in range(len(profids)):
                    if profids[k][0] == data[j][0]:
                        profids[k][1].append([data[j][5], data[j][6], data[j][7], data[j][8]])
                        break

    uit.write('{}\n'.format(profids[0]))

    print("Exporting data to DataProductsPerUser...")

    # De data die is gelinkt wordt uit de list in een .txt bestand gezet.

    uit.close()
    print("\nPrinted {} items!".format(count))


data = sessionsdata()
write_data(data)

cur.close()
conn.close()

# Start het eerstvolgende bestand.

exec(open("CatagoryConversion.py").read())
