import random
from create_connnection import create_connection

db = create_connection()
cur = db[0]
conn = db[1]

print("\n### tester.py ###\n")

def get_inf():
    cur.execute("select * from profile_recommendations;")
    all = cur.fetchall()
    rand_choice = []
    while len(rand_choice) < 20000:
        rand = random.choice(all)
        if rand not in rand_choice:
            rand_choice.append(rand)
    check_all(rand_choice)


def check_all(rand_choice):
    true = 0
    false = 0
    for i in range(0, len(rand_choice)):
        id = "'" + rand_choice[i][0] + "'"
        cur.execute(f"""SELECT mostusedcat, mostusedsubcat, mostusedsubsubcat from profiles where id like {id};""")
        uitk = cur.fetchall()
        uitk = uitk[0]
        if None not in uitk and 'None' not in uitk:
            ca = "'" + rand_choice[i][1] + "'"
            subca = "'" + rand_choice[i][2] + "'"
            subsubca = "'" + rand_choice[i][2] + "'"
            cur.execute(f"SELECT category from products where id like {ca};")
            cat = cur.fetchall()
            cur.execute(f"""SELECT subcategory from products where id like {subca}""")
            subcat = cur.fetchall()
            cur.execute(f"""SELECT subsubcategory from products where id like {subsubca}""")
            subsubcat = cur.fetchall()
            rec_cats = (cat[0][0], subcat[0][0])
            if None not in rec_cats and 'None' not in uitk:
                if rec_cats[0] == uitk[0] and rec_cats[1] == uitk[1]:
                    true += 1
                else:
                    print('\n')
                    print(uitk)
                    print(rec_cats)
                    false += 1
            else:
                continue
        else:
            continue

    print(true, ' are true')
    print(false, ' are false')


get_inf()

# Hier sluit ik de communicatie met de database
cur.close()
conn.close()