import mysql.connector as mysql

class dbservices:
    def __init__(self):
        self.connector = None
        self.dbcursor = None
        self.connect_database()
        self.create_table()
    
    def connect_database(self):
        self.connector = mysql.connect(host='127.0.0.1', user='root', password='vishal')

        self.dbcursor = self.connector.cursor()
        self.dbcursor.execute('USE Storekeeping')

    def create_table(self):

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Products` (
            `Id` INT NOT NULL AUTO_INCREMENT,
            `Name` VARCHAR(40) NOT NULL,
            `Category` VARCHAR(40) NOT NULL,
            `Price` FLOAT NOT NULL,
            `Stock` INT DEFAULT 0,
            `Desc` TEXT DEFAULT NULL,
            `Date` DATETIME NOT NULL,
            PRIMARY KEY(`Id`)
        ); ''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Sales`(
            `Bill_Id` INT NOT NULL AUTO_INCREMENT,
            `Sale_date` DATETIME NOT NULL,
            `Amount` FLOAT NOT NULL,
            PRIMARY KEY (`Bill_Id`)
        ); ''')

        self.dbcursor.execute('''ALTER TABLE Sales AUTO_INCREMENT=11001;''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Admin`(
            `Id` INT NOT NULL AUTO_INCREMENT,
            `Name` VARCHAR(40) NOT NULL,
            `Username` VARCHAR(25) NOT NULL UNIQUE,
            `Password` VARCHAR(15) NOT NULL,
            PRIMARY KEY (`Id`)
        ); ''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Sales_mapping`(
            `Sale_Id` INT NOT NULL,
            `Product_Id` INT NOT NULL,
            `Qty` FLOAT DEFAULT NULL,
            `Unit` INT DEFAULT NULL,
            `Amount` FLOAT NOT NULL,
            FOREIGN KEY (`Sale_Id`) REFERENCES Products(Id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (`Product_Id`) REFERENCES Sales(`Bill_Id`) ON UPDATE CASCADE ON DELETE CASCADE
        ); ''')

        self.connector.commit()

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
