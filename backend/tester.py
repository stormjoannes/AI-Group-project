from create_connnection import create_connection
import psycopg2

db = create_connection()
cur = db[0]
conn = db[1]

# def homepage_algoritme_test(profileid):
#     hompage_test1 = """SELECT catrecommend FROM profile_recommendations WHERE id = %s"""
#     cur.execute(hompage_test1)
#     ((test1,),) = cur.fetchall()
#     hompage_test1 = """SELECT category FROM products WHERE id = %s"""
#     cur.execute(hompage_test1(test1))
#     test1 = cur.fetchall()
#     hompage_catrecommend = """SELECT category FROM products WHERE id = %s"""
#     cur.execute(hompage_catrecommend)
#     hompage_catrecommend = cur.fetchall()
#
#
#     hompage_test2 = """SELECT subcatrecommend FROM profile_recommendations WHERE id = %s"""
#     cur.execute(hompage_test2)
#     ((test2,),) = cur.fetchall()
#     hompage_sub = """SELECT subcategory FROM products WHERE id = %s"""
#     cur.execute(hompage_test1)
#     hompage_subcatrecommend = """SELECT subcategory FROM products WHERE id = %s"""
#     cur.execute(hompage_subcatrecommend)
#
#
#     hompage_test3 = """SELECT subsubcatrecommend FROM profile_recommendations WHERE id = %s"""
#     cur.execute(hompage_test3)
#     ((test3,),) = cur.fetchall()
#     hompage_subcatrecommend = """SELECT subsubcategory FROM products WHERE id = %s"""
#     cur.execute(hompage_subcatrecommend)
#
#
#     hompage_test4 = """SELECT subsubcatrecommend_2 FROM profile_recommendations WHERE id = %s"""
#     cur.execute(hompage_test4)
#     ((test4,),) = cur.fetchall()
#     hompage_subcatrecommend_2 = """SELECT subsubcategory FROM products WHERE id = %s"""
#     cur.execute(hompage_subcatrecommend_2)
#
#
#     return
#
#
# homepage_algoritme_test(profileid)


# def target_audience_deal_algoritme_test():
#     #Verglijkt deal en targetaudience van
#     target_test1 = """SELECT recommendation_1 FROM all_prof_rec WHERE id_ = '5a70719a06d25200017b8437'"""
#     cur.execute(target_test1)
#     ((test1,),) = cur.fetchall()
#     print(type)
#     target_deal1 = """SELECT targetaudience,targdeal FROM products WHERE id = %s"""%(test1)
#     cur.execute(target_deal1)
#
#
#     # Verglijkt deal en targetaudience van
#     target_test2 = """SELECT recommendation_2 FROM all_prof_rec WHERE id_ = '5a70719a06d25200017b8437'"""
#     cur.execute(target_test2)
#     ((test2,),) = cur.fetchall()
#     target_deal2 = """SELECT targetaudience,deal FROM products WHERE id = %s"""%(test2)
#     cur.execute(target_deal2)
#
#
#     # Verglijkt deal en targetaudience van
#     target_test3 = """SELECT recommendation_3 FROM all_prof_rec WHERE id_ = '5a70719a06d25200017b8437'"""
#     cur.execute(target_test3)
#     ((test3,),) = cur.fetchall()
#     target_deal3 = """SELECT targetaudience,deal FROM products WHERE id = %s"""%(test3)
#     cur.execute(target_deal3)
#
#
#     # Verglijkt deal en targetaudience van
#     target_test4 = """SELECT recommendation_4 FROM all_prof_rec WHERE id_ = '5a70719a06d25200017b8437'"""
#     cur.execute(target_test4)
#     ((test,),) = cur.fetchall()
#     target_deal4 = """SELECT targetaudience,deal FROM products WHERE id = %s"""%(test4)
#     cur.execute(target_deal4)
#
#     return
#
#
# target_audience_deal_algoritme_test()


def product_specifieke_algoritme_test(self, prodid):
    # verglijkt de category van het product op de pagina en het product van de recommendation.
    product_test1 = """SELECT catrecommend FROM products WHERE id = %S""" % (prodid)
    cur.execute(product_test1)
    ((test1,),) = cur.fetchall()
    cat = """SELECT category FROM products WHERE id = %s""" % (test1)
    cur.execute(cat)
    verglijk1 = """SELECT category FROM products WHERE id = '28846'""" % (prodid)
    cat == verglijk1

    # verglijkt de subategory van het product op de pagina en het product van de recommendation.
    product_test2 = """SELECT subcatrecommend FROM products WHERE id = %s""" % (prodid)
    cur.execute(product_test2)
    ((test2,),) = cur.fetchall()
    subcat = """SELECT subcategory FROM products WHERE id = %s""" % (test2)
    cur.execute(subcat)
    verglijk2 = """SELECT category FROM products WHERE id = %S""" % (prodid)
    print(subcat == verglijk2)

    # verglijkt de subsubcategory van het product op de pagina en het product van de recommendation.
    product_test3 = """SELECT subsubcatrecommend FROM products WHERE id = %S""" % (prodid)
    cur.execute(product_test3)
    ((test3,),) = cur.fetchall()
    subsubcat = """SELECT subsubcategory FROM products WHERE id = %s""" % (test3)
    cur.execute(subsubcat)
    verglijk3 = """SELECT category FROM products WHERE id = %s""" % (prodid)
    print(subsubcat == verglijk3)

    # verglijkt de subsubcategory van het product op de pagina en het product van de tweede recommendation.
    product_test4 = """SELECT namerecommend FROM products WHERE id = %S""" % (prodid)
    cur.execute(product_test4)
    ((test4,),) = cur.fetchall()
    subsubcat2 = """SELECT namerecommend FROM products WHERE id = %s""" % (test4)
    cur.execute(subsubcat2)
    verglijk4 = """SELECT category FROM products WHERE id = %s""" % (prodid)
    print(subsubcat2 == verglijk4)
    return


product_specifieke_algoritme_test(prodid)

product_specifieke_algoritme_test()