#!/usr/bin/env python2

import psycopg2

question_1 = 'The most popular three articles:-'
invest_1 = """
select title, count(*) as views from articles inner join
log on concat('/article/', articles.slug) = log.path
where log.status like '%200%'
group by log.path, articles.title order by views desc limit 3;
"""

question_2 = 'The most popular article authors:-'
invest_2 = """
select authors.name, count(*) as views from articles inner join
authors on articles.author = authors.id inner join
log on concat('/article/', articles.slug) = log.path where
log.status like '%200%' group by authors.name order by views desc
"""

question_3 = 'Days with more than 1% errors:-'
invest_3 = """
select * from (
    select a.day,
    round(cast((100*b.hits) as numeric) / cast(a.hits as numeric), 2)
    as errp from
        (select date(time) as day, count(*) as hits from log group by day) as a
        inner join
        (select date(time) as day, count(*) as hits from log where status
        like '%404%' group by day) as b
    on a.day = b.day)
as t where errp > 1.0;
"""


class investigation:
    def __init__(self):
        try:
            self.db = psycopg2.connect('dbname=news')
            self.cursor = self.db.cursor()
        except Exception as o:
            print (o)

    def execute_invest(self, invest):
        self.cursor.execute(invest)
        return self.cursor.fetchall()

    def solve(self, question, invest, suffix='views'):
        invest = invest.replace('\n', ' ')
        result = self.execute_invest(invest)
        print question
        for v in range(len(result)):
            print '\t', v + 1, '.', result[v][0], '--', result[v][1], suffix
        # blank line
        print ''

    def exit(self):
        self.db.close()


if __name__ == '__main__':
    investigation = investigation()
    investigation.solve(question_1, invest_1)
    investigation.solve(question_2,invest_2)
    investigation.solve(question_3, invest_3, '% error')
investigation.exit()
