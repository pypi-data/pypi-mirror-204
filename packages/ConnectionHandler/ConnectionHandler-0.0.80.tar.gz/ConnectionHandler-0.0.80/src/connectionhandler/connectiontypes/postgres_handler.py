from psycopg2 import sql
import psycopg2
import json
import traceback

class Postgres_Handler:
    #Key for table_name string
    table_name_key = 'table_name'
    
    #Initializer that takes the values for connection
    def __init__(self, user_name, password, host, database, port):
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port
        self.database = database
   
    # Used internally create to run query
    def __run_query(self, query, values):
        #Sets the message to 'No records found' and status -1
        status = 0
        results = 'No records found'
        
        #Creates cursor to iterate through rows
        with psycopg2.connect(user=self.user_name, password=self.password, host=self.host, dbname=self.database) as conn:
            with conn.cursor() as cursor:
        
                try:
                    print(query)
                    cursor.execute(query, values)
                    results = cursor.fetchall()

                    status = 1
                    conn.commit()
                    
                    if results.count == 0:
                        results = 'No records found'
                except psycopg2.ProgrammingError as ex:
                    #if ex == "no results to fetch":
                    status = 2
                    results = f"{ex}"
                except Exception as ex:
                    status = -1
                    results = f"{ex}"
            
        return (status, results)
    
    #Method to close the connection    
    def Close(self):
            try:
                self.conn.close() 
            except Exception as ex:
                return f'Error: {ex}'
        
    #Select all rows 
    def search_for_records(self, columns, keywords):
        payload = {}
    
        query_value_list = self.__build_search_query(keywords)       

        #Runs the query and returns the results
        results = self.__run_query(query_value_list[0], query_value_list[1])
        payload = self.__format_search_results(results, columns)
    
        return payload

    def __build_search_query(self, keywords):
        where_string = ''
        values_dict = {}
        table_name_key = 'table_name'
        
        #Start of query string
        query = f'SELECT * FROM "{keywords[table_name_key]}"'
        
        if table_name_key not in keywords:
            assert("Error: table_name required as argument")
        values_dict[table_name_key] = keywords[table_name_key]
        
        #Keys for the StartDate and EndDate
        start_date_key = "SearchStartDate"
        end_date_key = "SearchEndDate"

        if len(keywords) != 0:
            #Iterates through the keywords to build search string
            for key, item in keywords.items():
                if key == table_name_key: continue
                
                if where_string != '':
                    where_string += ' AND '
                
                if key == start_date_key:
                    where_string += f'"DocumentDate" >= %({key})s'
                    values_dict[key] = item
                elif key == end_date_key:
                    where_string += f'"DocumentDate" <= %({key})s'
                    values_dict[key] = item
                else:
                    where_string += f'"{key}" ILIKE %({key})s'
                    values_dict[key] = f'{item}'
                    
            if where_string != '':
                query = f"{query} WHERE {where_string}"
                
        return [query, values_dict]
        
    
    def __format_search_results(self, results, columns):
        formatted_rows = []
        records = ''
        error = ''
        
        status_code = 200
        internal_status = results[0]
        data = results[1]  
        
        if internal_status != -1:
            row_count = len(data)
            
            if row_count > 0:
                for row in data:
                    formatted_row = {}
                    
                    for index, item in enumerate(row):
                        formatted_row[columns[f"{index}"]] = f'{item}'
                    
                    formatted_rows.append(formatted_row)

            records = {
                'count': row_count,
                'records': formatted_rows
            }
        elif internal_status == 2:
            records = "No results found"
        else:
            error = data
            
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': "application/json",
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            },
            "body": json.dumps({
                'results': records,
                'error' : f'{error}'
            })
        } 
        
        
    #This needs to be looked at, likely there are only certain fields that will be passed and the rest will be created either in lambda or S3/postgresql
    def insert_row(self, **kwargs):
        #checks for the table name in args
        if self.table_name_key not in kwargs:
            return "Error: table_name required as argument"
       
        query_dict = {key: val for key,val in kwargs.items() if key != self.table_name_key}

        #Begining of the SQL query
        query = sql.SQL('INSERT INTO {table_name} ({columns}) VALUES({values})').format(
                columns = sql.SQL(', ').join(
                    map(sql.Identifier, query_dict.keys())
                ),
                values = sql.SQL(', ').join(
                    map(sql.Placeholder, query_dict.keys())
                ),
                table_name = sql.Identifier(kwargs[self.table_name_key])
        )
        
        results = self.__run_query(query, query_dict)
        return self.__format_results(results)
        
    def __format_results(self, results):
        internal_status = results[0]
        if internal_status == -1:
            print(results[1])
            error = results[1]
            message = ''
            status_code = 400
        else:
            error = ''
            message = results[1]
            status_code = 200
                
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': "application/json",
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            },
            "body": json.dumps({
                'results': f'{message}',
                'error' : f'{error}'
            })
        } 
        
    #Method to update a SQL row
    def update_record(self, **kwargs):
        try:
            values_dict = {}
            id_key = 'ID'
            clause_section = ''
            
                #checks for the table name in args
            if self.table_name_key not in kwargs:
                print("Error: table_name required as argument")
                assert("Error: table_name required as argument")
            
            #Begining of the SQL query
            query_string= "UPDATE {table_name} SET"
            
            for key, value in kwargs.items():
                if key.lower() == id_key.lower() or key.lower() == self.table_name_key: continue
                
                clause_section += f' "{key}"=%({key})s,'
                values_dict[key] = value
            
            query_string += clause_section[:-1]

            if id_key not in kwargs: assert("Error: ID of record required for an update!")
            
            query_string += f' WHERE "ID"=%(ID)s'
            values_dict[id_key] = kwargs[id_key]
            
            sql_string = sql.SQL(query_string).format(table_name = sql.Identifier(kwargs[self.table_name_key]))
            
            results = self.__run_query(sql_string, values_dict)
            
            return self.__format_results(results)
        except Exception as ex:
            print(ex)
            print(traceback.format_exc(ex))
    
    #Delete command, will use policy or agent number to delete
    #todo - This may requrie removing items from S3 not sure yet how that will work
    def delete_record(self, keywords):
        #key for table and id 
        table_name_key = "table_name"
        id_key = "ID"
        
        value_dict = {key: value for key, value in keywords.items() if key.lower() == id_key.lower()}
        
        #Builds query to run 
        query_string = 'DELETE FROM {table_name} WHERE {column_name} = {Id}'
        sql_query = sql.SQL(query_string).format(
            table_name = sql.Identifier(keywords[table_name_key]),
            column_name = sql.Identifier(id_key),
            Id= sql.Placeholder(id_key)
        )
        
        #Runs the query and handles the success or error.
        results = self.__run_query(sql_query, value_dict)
        
        return self.__format_results(results)

    def search_for_columns_from_id(self, table_name, return_columns, id):
        id_key = "ID"
        values_dict = {id_key: id}
        column_identifier = sql.SQL(',').join(return_columns)
        table_Identifier = sql.Identifier(table_name)
        
        query = sql.SQL('SELECT {columns} from {table} WHERE "ID"={Id}').format(
            columns = column_identifier,
            table = table_Identifier,
            Id = sql.Placeholder(id_key)
        )
        
        return self.__run_query(query, values_dict)
                
                
