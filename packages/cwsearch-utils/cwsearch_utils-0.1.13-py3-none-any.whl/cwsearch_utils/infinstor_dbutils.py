import sqlite3

def create_table(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE links(tag, name, timestamp, link, msg)")
    cur.execute("CREATE INDEX idx_links ON links(tag)")
    con.commit()    
