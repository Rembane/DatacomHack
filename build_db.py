#!/usr/bin/env python2

import sqlite3, sys

def init_db():
    conn = sqlite3.connect('exams.db')
    c = conn.cursor()
    c.execute(u"""CREATE TABLE IF NOT EXISTS post (id INTEGER PRIMARY KEY, body TEXT, exam_id INTEGER)""")
    c.execute(u"""CREATE TABLE IF NOT EXISTS tag (id INTEGER PRIMARY KEY, name TEXT)""")
    c.execute(u"""CREATE TABLE IF NOT EXISTS post_tag (id INTEGER PRIMARY KEY, post_id INTEGER, tag_id INTEGER)""")
    c.execute(u"""CREATE TABLE IF NOT EXISTS exam (id INTEGER PRIMARY KEY, name TEXT)""")

    return (conn, c)


def generate_db(fn, cursor):
    utags = {}
    tags  = []
    exams = {}
    cex   = u''
    txt   = u''
    lts   = []

    with open(fn) as fh:
        for row in fh: 
            row = unicode(row, 'utf-8')
            # New post!
            if row.startswith(u'='):
                exid = exams.get(cex, False)
                if not exid:
                    cursor.execute(u"""INSERT INTO exam(name) VALUES(?)""", (cex,))
                    exams[cex] = exid = int(cursor.lastrowid)

                cursor.execute(u"""INSERT INTO post(body, exam_id) VALUES(?,?)""", (txt, exid,))
                tags.append((cursor.lastrowid, lts))
                for t in lts:
                    utags[t.lower()] = t

                txt = u''
                cex = u''
                lts = []

            # New exam!
            elif row.startswith(u'>'):
                cex = row.strip(u'> \n')

            elif row.startswith(u':'):
                lts = [t.lstrip(':') for t in row.strip().split()]

            else:
                txt += row
                
    for (pid,ts) in tags:
        for t in ts:
            cursor.execute(u"""INSERT INTO tag(name) VALUES(?)""", (utags[t.lower()],))
            cursor.execute(u"""INSERT INTO post_tag(post_id, tag_id) VALUES(?,?)""", (pid, cursor.lastrowid))

if __name__ == '__main__':
    conn, cursor = init_db()
    generate_db(sys.argv[1], cursor)
    conn.commit()
    conn.close()
