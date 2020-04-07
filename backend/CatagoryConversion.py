print("\n### CatagoryConversion.py ###\n")

invoer = 'DataProductsPerUser'
uitvoer = 'CategorysPerUser'
alluitvoer = 'AllUsedCategorys'

print("Getting DataProductsPerUser...")
inv = open(invoer, 'r')
uit = open(uitvoer, 'w')
alluit = open(alluitvoer, 'w')


def get_data():
    # Haalt de data van elk bekeken product per profiel uit het .txt bestand.

    read = inv.readlines()
    data = []
    for i in range(len(read)):
        current_data = eval(read[i])
        data.append(current_data)

    return data


print("Converting data...")


def split_per_profile():
    # Splitst per profiel alle categorys, subcategorys, subsubcategorys en namen, en zet deze in aparte lijsten per profiel.
    # Zet daarnaast al de gespliteste code van alle profielen ook in een lijst, waaruit later de views per category worden berekend.

    data = get_data()
    profcats = []
    allcats = []
    allsubcats = []
    allsubsubcats = []
    allnames = []

    for i in range(len(data)):
        category = []
        subcategory = []
        subsubcategory = []
        for j in range(len(data[i][1])):
            category.append(data[i][1][j][0])
            allcats.append(data[i][1][j][0])
            subcategory.append(data[i][1][j][1])
            allsubcats.append(data[i][1][j][1])
            subsubcategory.append(data[i][1][j][2])
            allsubsubcats.append(data[i][1][j][2])
            allnames.append(data[i][1][j][3])

        profcats.append(
            [data[i][0], ['categorys', category], ['subcategorys', subcategory], ['subsubcategorys', subsubcategory]])

    totallcats = [['categorys', allcats], ['subcategorys', allsubcats], ['subsubcategorys', allsubsubcats],
                    ['names', allnames]]

    return profcats, totallcats


print("Exporting data into CategorysPerUser and AllUsedCategorys...")


def write_to_files():
    # De data van categorys per profiel worden uit een list in een .txt bestand gezet.
    data = split_per_profile()
    profcats = data[0]
    totallcats = data[1]

    for i in range(len(profcats)):
        print("\r{} of {} in file...".format(i + 1, len(profcats)), end="")
        uit.write('{}\n'.format(profcats[i]))

    # De data van categorys van alle profielen wordt uit een list in een .txt bestand gezet.

    for i in range(len(totallcats)):
        alluit.write('{}\n'.format(totallcats[i]))

    print("\nPrinted {} items!".format(len(profcats)))


write_to_files()

uit.close()
alluit.close()
inv.close()
# Start het eerstvolgende bestand.

exec(open('ProductviewsToDatabase.py').read())
