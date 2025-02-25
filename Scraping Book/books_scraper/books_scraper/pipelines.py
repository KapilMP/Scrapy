import sqlite3

class BooksScraperPipeline:
    def __init__(self):
        #Connecto sqlite db
        self.conn = sqlite3.connect('BookScrapy.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS category(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE
            )
        """)
        
     
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price TEXT,
                category_id INTEGER,
                availability TEXT,
                FOREIGN KEY (category_id) REFERENCES category (id)
            )
        """)
        
    def process_item(self, item):
        #Extract category and book details
        category_name = item.get('category')
        title = item.get('title')
        price = item.get('price')
        availability = item.get('availability')

        #Check if category already exists in the category table
        self.cur.execute("SELECT id FROM category WHERE category_name = ?", (category_name,))
        category_id = self.cur.fetchone()

        if category_id:
            category_id = category_id[0]  #if category exists, get its ID
        else:
            #if category doesn't exist, insert it and fetch the ID
            self.cur.execute("INSERT INTO category (category_name) VALUES (?)", (category_name,))
            category_id = self.cur.lastrowid
        
        #insert the book into the books table
        self.cur.execute("""
            INSERT INTO books (title, price, category_id, availability) 
            VALUES (?, ?, ?, ?)
        """, (title, price, category_id, availability))
        
        #commit the changes to the database
        self.conn.commit()
        
        return item
    
    def close_spider(self):
        #close db connection when spider is done
        self.conn.close()
