import sqlite3

con = sqlite3.connect('data.db')
cur = con.cursor()

cur.execute('''CREATE TABLE "article" (
	"board"	TEXT,
	"articleID"	TEXT,
	"articleTitle"	TEXT,
	"articleContent"	TEXT,
	"articleTime"	TEXT,
	"articleUser"	TEXT,
	"articleView"	TEXT,
	"articlegood"	TEXT,
	"articlebad"	TEXT
)''')

cur.execute('''CREATE TABLE "board" (
    "name"	TEXT, 
    "board"	TEXT)''')

cur.execute('''INSERT into board(name, board) VALUES('main', '메인')''')
cur.execute('''INSERT into board(name, board) VALUES('wiki', '위키게시판')''')
cur.execute('''INSERT into board(name, board) VALUES('creative', '창작게시판')''')
cur.execute('''INSERT into board(name, board) VALUES('talk', '자유게시판')''')
cur.execute('''INSERT into board(name, board) VALUES('sonawiki', '소나위키 게시판')''')

con.commit()
con.close()