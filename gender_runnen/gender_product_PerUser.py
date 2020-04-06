import random
from backend.create_connnection import create_connection

db = create_connection()
cur = db[0]
conn = db[1]

cur.execute("DROP TABLE IF EXISTS all_prof_rec;")  # Verwijderd de table die ik ga aanmaken als de table al bestaat, zo voorkom ik errors.

cur.execute("CREATE TABLE all_prof_rec (id serial PRIMARY KEY, "            # hier create ik mijn table.
            "id_ varchar, "
            "recommendation_1 varchar,"
            "recommendation_2 varchar, "
            "recommendation_3 varchar, "
            "recommendation_4 varchar);")

def base():
    all = all_inf()
    all_profid = all[0]
    all_prodid = all[1]
    for i in range(0, len(all_profid)):
        print("\rRendering profile recommendations: {} from 2081649....".format(i), end='')
        executer = """select deal, targetaudience from products where id = %s or id = %s or id = %s;"""
        cur.execute(executer, (all_prodid[i][0], all_prodid[i][1], all_prodid[i][2],))
        targ_prod_all = cur.fetchall()

        all_audience = []
        all_deal = []
        for index in targ_prod_all:
            all_audience.append(index[1])
            if index[0] != None:
                all_deal.append(index[0])
        targ_prod = most_common(all_audience)
        best_deal = most_common(all_deal)

        rand_choice = recommended(targ_prod, best_deal)
        random.shuffle(rand_choice)
        all_rand_choice = rand_choice[0:4]
        cur.execute("INSERT INTO all_prof_rec (id_, "
                    "recommendation_1, "
                    "recommendation_2, "
                    "recommendation_3, "
                    "recommendation_4) VALUES (%s, %s, %s, %s, %s)", (all_profid[i], all_rand_choice[0], all_rand_choice[1], all_rand_choice[2], all_rand_choice[3]))

def recommended(targ_prod, best_deal):
    if None == targ_prod or None == best_deal:
        if targ_prod == None and best_deal != None:
            exe = """select id from products where targetaudience IS NULL and deal LIKE %s LIMIT 10"""
            cur.execute(exe, (best_deal,))
        elif best_deal == None and targ_prod != None:
            exe = """select id from products where targetaudience LIKE %s and deal IS NULL LIMIT 10"""
            cur.execute(exe, (targ_prod,))
        else:
            cur.execute("select id from products where targetaudience IS NULL and deal IS NULL LIMIT 10")

    else:
        exe = """select id from products where targetaudience LIKE %s and deal like %s LIMIT 10"""
        cur.execute(exe, (targ_prod, best_deal,))

    all_rec = cur.fetchall()
    if len(all_rec) < 4:
        exe = """select id from products where targetaudience LIKE %s LIMIT 10"""
        cur.execute(exe, (targ_prod,))
        all_rec = cur.fetchall()
    return all_rec

def most_common(list):
    temp_count = []
    for tem in list:
        how_much = list.count(tem)
        temp_count.append(how_much)
    if len(temp_count) > 0:
        popular = max(temp_count)
        for index in range(0, len(temp_count)):
            if popular == temp_count[index]:
                if list[index] != None:
                    if list[index].count("'") > 1:
                        list[index] = list[index][1, len(list[index]) - 1]
                    if "'" in list[index]:
                        list[index] = list[index].split("'")
                        list[index] = str(list[index][0]) + '%'
                return list[index]

def all_inf():
    cur.execute("select id from profile_recommendations;")
    all_profid = cur.fetchall()
    cur.execute("select catrecommend, subcatrecommend, subsubcatrecommend from profile_recommendations;")
    all_prodid = cur.fetchall()
    return all_profid, all_prodid

base()
conn.commit()

# Hier sluit ik de communicatie met de database
cur.close()
conn.close()