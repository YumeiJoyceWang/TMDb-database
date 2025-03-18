import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
# SHOW = True
SHOW = False
############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

   
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = "CREATE TABLE movies(id integer, title text, score real);"
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = "CREATE TABLE movie_cast(movie_id integer, cast_id integer, cast_name text, birthday text, popularity real);"
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open (path, 'r') as file:
            contents = csv.reader(file, delimiter=',')
            data = next(contents)
            query = "INSERT INTO movies VALUES(?, ?, ?)"
            cursor = connection.cursor()
            cursor.execute(query, data)
            for data in contents:
                cursor.execute(query, data)
            connection.commit()

       #####################################################################

        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open (path, 'r') as file:
            contents = csv.reader(file, delimiter=',')
            data = next(contents)
            query = "INSERT INTO movie_cast VALUES(?, ?, ?, ?, ?)"
            cursor = connection.cursor()
            cursor.execute(query, data)
            for data in contents:
                cursor.execute(query, data)
            connection.commit()

        ######################################################################

        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = "CREATE TABLE cast_bio(cast_id integer, cast_name text, birthday text, popularity real, FOREIGN KEY (cast_id) REFERENCES movie_cast(id));"
        
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = "INSERT INTO cast_bio (cast_id, cast_name, birthday, popularity) SELECT DISTINCT mc.cast_id, mc.cast_name, mc.birthday, mc.popularity FROM movie_cast AS mc;"
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = "CREATE UNIQUE INDEX movie_index ON movies (id);"
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = "CREATE INDEX cast_index ON movie_cast (cast_id);"
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = "CREATE UNIQUE INDEX cast_bio_index ON cast_bio (cast_id);"
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = "WITH warMovie (movie_num) AS (SELECT printf('%.2f', COUNT(id)) FROM movies WHERE score > 50 and lower(title) LIKE '%war%') SELECT printf('%.2f', 100 * movie_num / (SELECT printf('%.2f', count(*)) FROM movies)) AS proportion FROM warMovie;"
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = "SELECT cast_name, COUNT(movie_id) AS appearance_count FROM movie_cast WHERE popularity > 10 GROUP BY cast_id ORDER BY appearance_count DESC, cast_name ASC LIMIT 5;"
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = "SELECT title AS movie_title, printf('%.2f', score) AS movie_score, count(cast_id) AS cast_count FROM movies INNER JOIN movie_cast as mc ON mc.movie_id = movies.id GROUP BY movie_id ORDER BY score DESC, cast_count ASC, movie_title ASC LIMIT 5;"
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = "SELECT cast_id, cast_name, printf('%.2f', AVG(score)) AS average_score FROM movie_cast mc INNER JOIN movies ON mc.movie_id = movies.id WHERE score >= 25 GROUP BY cast_id HAVING COUNT(DISTINCT movie_id) > 2 ORDER BY average_score DESC, cast_name ASC LIMIT 10;"
        # part_f_sql = "WITH castScore (cast_id, cast_name, avg_score) AS (SELECT cast_id, cast_name, AVG(score) FROM movie_cast mc INNER JOIN movies ON mc.movie_id = movies.id WHERE score >= 25 GROUP BY cast_id HAVING COUNT(movie_id) > 3) SELECT cast_id, cast_name, printf('%.2f', AVG(score)) AS average_score FROM castScore ORDER BY average_score DESC, cast_name ASC LIMIT 10;"
        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = "CREATE VIEW good_collaboration AS WITH castCollaboration AS (SELECT mc1.movie_id AS movie_id, mc1.cast_id AS cast_member_id1, mc2.cast_id AS cast_member_id2 FROM movie_cast mc1 INNER JOIN movie_cast mc2 ON mc1.cast_id < mc2.cast_id AND mc1.movie_id = mc2.movie_id) SELECT movie_id, cast_member_id1, cast_member_id2, COUNT(movie_id) AS movie_count, AVG(score) AS average_movie_score FROM castCollaboration cc INNER JOIN movies ON cc.movie_id = movies.id GROUP BY cast_member_id1, cast_member_id2 HAVING movie_count > 2 and average_movie_score >= 40;"
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        # part_g_i_sql = "SELECT * FROM good_collaboration LIMIT 10"
        part_g_i_sql = "WITH castScore (cast_id, average_movie_score) AS (SELECT cast_member_id1 as cast_id, average_movie_score FROM good_collaboration gc1 UNION SELECT gc2.cast_member_id2 as cast_id, average_movie_score FROM good_collaboration gc2) SELECT cs.cast_id, cast_name, printf('%.2f', AVG(average_movie_score)) AS collaboration_score FROM castScore cs INNER JOIN movie_cast mc ON cs.cast_id = mc.cast_id GROUP BY cs.cast_id ORDER BY collaboration_score DESC, cast_name ASC LIMIT 5;"
        # part_g_i_sql = "WITH castScore (cast_id, average_movie_score) AS (SELECT cast_member_id1 as cast_id, average_movie_score FROM good_collaboration gc1 UNION SELECT gc2.cast_member_id2 as cast_id, average_movie_score FROM good_collaboration gc2) SELECT cs.cast_id, cast_name, printf('%.2f', AVG(average_movie_score)) AS collaboration_score FROM castScore AS cs INNER JOIN movie_cast AS mc ON cs.cast_id = mc.cast_id GROUP BY cast_id ORDER BY collaboration_score DESC, cast_name ASC LIMIT 5;"
        # part_g_i_sql = "SELECT gc.cast_id, cast_name, printf('%.2f', AVG(average_movie_score)) AS collaboration_score FROM good_collaboration gc INNER JOIN movie_cast AS mc ON cast_id = mc.cast_id GROUP BY cast_id ORDER BY collaboration_score DESC, cast_name ASC LIMIT 5;"
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = "CREATE VIRTUAL TABLE movie_overview USING fts3(id integer, overview text);"
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        with open (path, 'r') as file:
            contents = csv.reader(file, delimiter=',')
            data = next(contents)
            query = "INSERT INTO movie_overview VALUES(?, ?)"
            cursor = connection.cursor()
            cursor.execute(query, data)
            for data in contents:
                cursor.execute(query, data)
            connection.commit()
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = "SELECT COUNT(id) FROM movie_overview WHERE overview MATCH 'fight';"
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = "SELECT COUNT(id) FROM movie_overview WHERE overview MATCH 'space NEAR/5 program';"
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":

    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except:
         print("Error in Part a.i")

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except:
        print("Error in part a.ii")

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except:
        print("Error in part a.iii")

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except:
        print("Error in part b")

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except:
        print("Error in part c")

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except:
        print("Error in part d")

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part e")

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part f")
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part g")

    try:   
        print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    except:
        print("Error in part h")

    conn.close()

    #################################################################################
  
