#!/usr/bin/env python

# postgress liabrary files are imported
import psycopg2

# date module from datetime are imported
from datetime import date


def output(quest):
    try:
        db = psycopg2.connect("dbname = news")
        curs = db.cursor()
        curs.execute(quest)
        resu = curs.fetchall()
        db.close()
        return resu
    except BaseException as errors:
        print(errors)

articles1 = ("SELECT title, COUnt(*) as views FROM articles "
             "JOIN log"
             "    ON articles.slug = SUBSTRING(log.path, 10)"
             "    GROUP BY title ORDER bY views DESC LIMIT 3;")
authors2 = """select authors.name,
           count(*) as views FROM articles
           JOIN authors on articles.author = authors.id JOIN log
           ON articles.slug = SUBSTRING(log.path, 10)
           WHERE log.status LIKE '200 OK'
           GROUP by authors.NAME ORDER BY views DESC;"""
errors3 = """SELECT * from (SELECT date(time),
            ROUND(100.0*sum(case log.status
            WHEN '200 OK'
                then 0 else 1 end)/
                COUNT(log.status),3)
                as error FROM log GROUP
                by DATE(time) ORDER by error DESC) as
                SUBQ WHERE error > 1;"""


def fam_articles():
    famo = output(articles1)
    print('The most famous 3 articles of all time:')
    for sk in famo:
        print('"' + sk[0] + '" -- ' + str(sk[1]) + " views")
    print('')


def fam_authors():
    famos = output(authors2)
    print('The most famous 3 authors of all time:')
    for t in famos:
        print('"' + t[0] + '" -- ' + str(t[1]) + ' views')
    print('')


def error_day():
    print('Error days with more than 1% errors:')
    res = output("""
    SELECT * from (select DATE(time),
    round(100.0*sum(case log.status
    WHEN '200 OK'  then 0 else 1 end) /
    COUNT(log.status),3)
    as error FROM log GROUP
    by DATE(time) ORDER by error desc) as subq where error > 1;
                   """)
    # To print the output
    for result in res:
                print (" %s: %s views" % (result[0], result[1]))
if __name__ == '__main__':
    print("RESULTS:")

    fam_articles()
    fam_authors()
    error_day()

