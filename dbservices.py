
import mysql.connector as mysql
from datetime import datetime
from datetime import datetime,date
from datetime import timedelta

class dbservices:
    def __init__(self):
        self.connector = None
        self.dbcursor = None
        self.connect_database()
        self.create_table()
    
    def connect_database(self):
        self.connector = mysql.connect(host='127.0.0.1', user='root', password='mysql27')

        self.dbcursor = self.connector.cursor()
        self.dbcursor.execute('USE Storekeeping')

    def create_table(self):

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Admin`(
            `Id` INT NOT NULL AUTO_INCREMENT,
            `Name` VARCHAR(40) NOT NULL,
            `Username` VARCHAR(25) NOT NULL UNIQUE,
            `Password` VARCHAR(15) NOT NULL,
            PRIMARY KEY (`Id`)
        ); ''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Category`(
            `Id` INT NOT NULL AUTO_INCREMENT,
            `Name` VARCHAR(30) NOT NULL UNIQUE,
            PRIMARY KEY(`Id`)
        );''')

        try:
            self.dbcursor.execute('''INSERT INTO Category (Name) 
            VALUES ('Beverages');''')

            self.dbcursor.execute('''INSERT INTO Category (Name) 
            VALUES ('Cleaning and household');''')

            self.dbcursor.execute('''INSERT INTO Category (Name) 
            VALUES ('Grocery');''')

            self.dbcursor.execute('''INSERT INTO Category (Name) 
            VALUES ('Packaged foods');''')

            self.dbcursor.execute('''INSERT INTO Category (Name) 
            VALUES ('Personal care');''')

        except Exception as e:
            pass

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Products` (
            `Id` INT NOT NULL AUTO_INCREMENT,
            `PName` VARCHAR(40) NOT NULL,
            `Category_Id` INT NOT NULL,
            `Price` FLOAT NOT NULL,
            `Stock` INT DEFAULT 0,
            `Description` TEXT DEFAULT NULL,
            `Date` DATETIME NOT NULL,
            PRIMARY KEY(`Id`),
            FOREIGN KEY (`Category_Id`) REFERENCES Category(`Id`) ON UPDATE CASCADE ON DELETE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Sales`(
            `Bill_Id` INT NOT NULL AUTO_INCREMENT,
            `Sale_date` DATETIME NOT NULL,
            `Amount` FLOAT NOT NULL,
            PRIMARY KEY (`Bill_Id`)
        ); ''')

        self.dbcursor.execute('''ALTER TABLE Sales AUTO_INCREMENT=11001;''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Sales_mapping`(
            `Sale_Id` INT NOT NULL,
            `Product_Id` INT NOT NULL,
            `Cat_Id` INT NOT NULL,
            `Qty` FLOAT DEFAULT NULL,
            `Amount` FLOAT NOT NULL,
            FOREIGN KEY (`Sale_Id`) REFERENCES Sales(`Bill_Id`) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (`Product_Id`) REFERENCES Products(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (`Cat_Id`) REFERENCES Category(`Id`) ON UPDATE CASCADE ON DELETE CASCADE
        ); ''')

        self.connector.commit()


    
    def sales_bill_id(self, table_name1, table_name2, val):
        
        try:
            select_query1 = (f"UPDATE Products SET Stock=Stock-{ val[1] } WHERE Id='{ val[0] }'")
            self.dbcursor.execute(select_query1)
            
            select_query2 = (f"SELECT Price,Category_Id FROM Products WHERE Id='{ val[0] }'")
            self.dbcursor.execute(select_query2)
            price = self.dbcursor.fetchall()
            p = price[0][0]
            p = p*val[1]
            val.append(p)
            catid = price[0][1]
            
            select_query3 = (f'SELECT Bill_id FROM {table_name1}')
            self.dbcursor.execute(select_query3)
            billid = self.dbcursor.fetchall()

            curr_bill_id = billid[-1][0]
            
            select_query4 = (f"INSERT INTO {table_name2} VALUES('{curr_bill_id}', '{val[0]}','{catid}', '{val[1]}', '{val[2]}') ")
            self.dbcursor.execute(select_query4)
            
            select_query5 = (f"SELECT SUM(Amount) FROM {table_name2} WHERE Sale_Id='{curr_bill_id}'")
            self.dbcursor.execute(select_query5)
            total_amount = self.dbcursor.fetchone()
            tm = total_amount[0]
            
            select_query6 = (f"UPDATE {table_name1} SET Amount={tm} WHERE Bill_Id='{curr_bill_id}'")
            self.dbcursor.execute(select_query6)

            select_query7 = (f"SELECT Sale_Id,PName,Qty,Amount FROM Products,{table_name2} WHERE Sale_Id='{curr_bill_id}' AND Product_Id=Id;")
            self.dbcursor.execute(select_query7)
            records = self.dbcursor.fetchall()
            self.connector.commit()
            
            return records
        except Exception as e:
            print(e)

    def sales_entering(self, table_name):
        
        try:
            sales_date = datetime.now()
            select_query = (f"INSERT INTO {table_name}( Sale_date, Amount) VALUES('{sales_date}','0')")
            self.dbcursor.execute(select_query)
            self.connector.commit()
        except Exception as e:
            print(e)
            

    def sales_delete(self, table_name):
        
        try:
            select_query = (f"DELETE FROM {table_name} WHERE Amount='0'")
            self.dbcursor.execute(select_query)
            self.connector.commit()
        except Exception as e:
            print(e)


    def bill_details(self, table_name):
        try:
            select_query3 = (f'SELECT Bill_id FROM {table_name}')
            self.dbcursor.execute(select_query3)
            billid = self.dbcursor.fetchall()

            curr_bill_id = billid[-1][0]
            
            select_query = (f"SELECT COUNT(Bill_Id) FROM {table_name} ")
            self.dbcursor.execute(select_query)
            billno = self.dbcursor.fetchall()
            billno1 = billno[0][0]
            
            select_query = (f"SELECT Amount,Sale_date FROM {table_name} WHERE Bill_Id='{curr_bill_id}'")
            self.dbcursor.execute(select_query)
            final_amount = self.dbcursor.fetchall()
            final_amount1 = final_amount[0][0]
            date = str(final_amount[0][1])
            # date = date.split(' ')
            # date = date[0]
            lst =[date,final_amount1, billno1]
            
            return lst
        except Exception as e:
            print(e)
        
    def fetch_item_records(self, table_name, category):

        try:
            select_query = (f"SELECT Id, PName, Price, Stock, Description, Date FROM {table_name} WHERE Category_Id = '{category}'")
            self.dbcursor.execute(select_query)
            records = self.dbcursor.fetchall()
        
            return records
        except Exception as e:
            print(e)


    def add_record(self, table_name, input_data):
        keys = list(input_data.keys())
        
        #Preparing Query
        table_data, table_values = '(', ' VALUES ('
        for i, x in enumerate(keys):
            if i != len(keys)-1:
                table_values += f'%({x})s, '
                table_data += f'{x}, '
            else:
                table_values += f'%({x})s)'
                table_data += f'{x})'

        add_query = (f'INSERT INTO {table_name} ' + table_data + table_values)
        print(add_query)

        #Execute Query
        try:
            self.dbcursor.execute(add_query, input_data)
            self.connector.commit()
        except Exception as e:
            print(e)

    def delete_record(self, table_name, id):
        delete_query = (f"DELETE FROM {table_name} WHERE Id = %(id)s")
        print(delete_query)
        try:
            self.dbcursor.execute(delete_query, {'id': id})
            self.connector.commit()
        except Exception as e:
            print(e)

    def fetch_records(self, table_name):
        select_query = (f'SELECT * FROM {table_name}')

        self.dbcursor.execute(select_query)
        records = self.dbcursor.fetchall()
        return records

    def update_record(self, table_name, Id, updated_data):
        set_values = ''

        for i, columns in enumerate(updated_data.keys()):
            if i != len(updated_data.keys())-1:
                set_values += f'{columns} = %({columns})s,'
            else:
                set_values += f'{columns} = %({columns})s WHERE Id = %(Id)s'
        
        updated_data['Id'] = Id
        update_query = (f'UPDATE {table_name} SET '+ set_values)
        print(update_query)
        try:
            self.dbcursor.execute(update_query, updated_data)
            self.connector.commit()
        except Exception as e:
            print(' *** Updation Failed *** \n', e)

    def fetch_column_data(self, table_name, columns, condition_name=None, condition_value=None):
        fetch_query = 'SELECT '

        for i,column in enumerate(columns):
            if i < len(columns)-1:
                fetch_query += f'{column}, '
            else:
                fetch_query += f'{column} FROM {table_name}'
        
        if condition_name != None and condition_value != None:
            fetch_query += f' WHERE {condition_name} = %(condition_value)s'
            print(fetch_query)
            self.dbcursor.execute(fetch_query, {'condition_value': condition_value})
        else:
            self.dbcursor.execute(fetch_query)
        columns_data = self.dbcursor.fetchall()

        return columns_data

    def signin_admin(self, table_name, input_data):
        pwd = (f"SELECT Username FROM {table_name} WHERE Password = %(paswd)s")
        paswd = input_data["Password"]
        try:
            self.dbcursor.execute(pwd,{'paswd':paswd})
            records = self.dbcursor.fetchone()
            if records == None:
                return 0
            else:
                return 1
        except Exception as e:
            print(e)
        return 0

    def fetch_sales_data(self):
        fetch_query = (f'''SELECT DISTINCT (product_id), Pname, Cat_id, Sum(Qty), SUM(amount) 
        FROM sales_mapping AS sm, products AS pr, category AS cat WHERE sm.Product_Id = pr.Id AND sm.Cat_Id = cat.Id GROUP
        BY product_id ORDER BY product_id;''')
        try:
            self.dbcursor.execute(fetch_query)
            sales_data = self.dbcursor.fetchall()
            return sales_data
        except Exception as e:
            print(e)
