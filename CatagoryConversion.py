print("\n### CatagoryConversion.py ###\n")

invoer = 'DataProductsPerUser'
uitvoer = 'CategorysPerUser'
alluitvoer = 'AllUsedCategorys'

inv = open(invoer, 'r')
uit = open(uitvoer, 'w')
alluit = open(alluitvoer, 'w')

print("Getting DataProductsPerUser...")

# Haalt de data van elk bekeken product per profiel uit het .txt bestand.

read = inv.readlines()
data = []
for i in range(len(read)):
    current_data = eval(read[i])
    data.append(current_data)

print("Converting data...")

# Splitst per profiel alle categorys, subcategorys, subsubcategorys en namen, en zet deze in aparte lijsten per profiel.
# Zet daarnaast al de gespliteste code van alle profielen ook in een lijst, waaruit later de views per category worden berekend.

inv.close()
allcats = []
allsubcats = []
allsubsubcats = []
allnames = []
profcats = []
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

print("Exporting data into CategorysPerUser and AllUsedCategorys...")

# De data van categorys per profiel worden uit een list in een .txt bestand gezet.

for i in range(len(profcats)):
    print("\r{} of {} in file...".format(i + 1, len(profcats)), end="")
    uit.write('{}\n'.format(profcats[i]))

# De data van categorys van alle profielen wordt uit een list in een .txt bestand gezet.

for i in range(len(totallcats)):
    alluit.write('{}\n'.format(totallcats[i]))

uit.close()
alluit.close()
print("\nPrinted {} items!".format(len(profcats)))

# Start het eerstvolgende bestand.

exec(open('ProductviewsToDatabase.py').read())
