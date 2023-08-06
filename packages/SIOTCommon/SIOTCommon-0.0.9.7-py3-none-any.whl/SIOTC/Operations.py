from SIOTC import DatabaseLayer
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
dl = DatabaseLayer

def executeQuery(query_func, *args, **kwargs):
    # Get a database session and the SQLAlchemy Base object
    session, base = dl.GetSession()
    try:
        # Execute the query function with the session and additional arguments as arguments
        result = query_func(session, base, *args, **kwargs)
        if result is None:
            print('Error: Could not proccess query')
            return None, 404
        # Print a success message to indicate that the query was successful
        print('Success')
        # Return the result
        return result
    except (SQLAlchemyError, IntegrityError, ValueError, AssertionError, TypeError, AttributeError) as e:
        # If an error occurs, rollback the session and return the error
        session.rollback()
        print(str(e))
        return 'Failure' 
    finally:
        # Close the session
        session.close()

def GetSpecificFromColumnInTable(value, column, table):
    def queryFunc(session, base, value, column, table):
        # Check if value is provided
        assert value is not None, "Error: No value provided"
        # Get all rows from the specified table and column
        theTable = GetAllOfColumnFromTable(table, column)
        # Check if an error occurred during retrieval
        if(theTable == False):
            print('Error: No table exist with provided values')
            return None, 'Error: No table exist with provided values'
        # If no error, query the row that matches the provided value
        else:
            return theTable.query.filter_by(value).first()
    return executeQuery(queryFunc, value, column, table)

# Add to any table to the database. Currently checks if missing columns and database constraints
def InsertToTable(table, values):
    def queryFunc(session, base, values):
        # Get table model and columns
        name = "public." + table
        tableModel = base.metadata.tables.get(name)
        # Check if table exists
        if tableModel is None:
            return False, 'Error: Table not found'
        columnsModel = tableModel.columns.keys()
        newValues = {}
        # Ensure that values are provided
        assert values is not None, "Error: No values provided"
        # Loop through the columns in the table and create a dictionary
        # with column names and values to insert
        for column in columnsModel:
            if column in values:
                newValues[column] = values[column]
            elif column == 'id':
                # Generate a new id value using the default sequence
                query = f"SELECT nextval('{table}_id_seq')"
                result = session.execute(query)
                newValues[column] = result.scalar()
            else:
                newValues[column] = None  # Use default value for missing columns
        # Insert the new object into the table
        newObject = tableModel.insert().values(**newValues)
        session.execute(newObject)
        session.commit()
        # Return success
        return True
    return executeQuery(queryFunc, values)

def GetFromTable(table, id):
    def queryFunc(session, base, table, id):
        # Get the table model from the metadata based on the provided table name
        name = "public." + table
        tableModel = base.metadata.tables.get(name)
        # Check if the table exists in the metadata
        if tableModel is None:
            return False, 'Error: Table not found'
        # Ensure that an ID is provided
        assert id is not None, "Error: No ID provided"
        # Create a query to get a row with the given ID from the table
        query = tableModel.select().where(tableModel.c.id == id)
        # Execute the query and return the result
        result = session.execute(query)
        return result.first()
    return executeQuery(queryFunc, table, id)

def RemoveFromTable(table, id):
    def queryFunc(session, base, table, id):
        # Get the table model from the metadata based on the provided table name
        name = "public." + table
        tableModel = base.metadata.tables.get(name)
        # Check if the table exists in the metadata
        if tableModel is None:
            return False, 'Error: Table not found'
        # Ensure that an ID is provided
        assert id is not None, "Error: No ID provided"
        # Create a query to remove a row with the given ID from the table
        query = tableModel.delete().where(tableModel.c.id == id)
        # Execute the query and commit the transaction
        session.execute(query)
        session.commit()
        return True
    return executeQuery(queryFunc, table, id)

def GetAllObjectsInModel(modelName):
    # Connect to database
    session, base = dl.GetSession()
    # If session or base is None, return error message
    if session is None or base is None:
        return False, 'Unable to connect to database'
    try:
    # Retrieve all rows from the specified database model
        rows = session.query(dl.GetModel(modelName))
    # If there are no rows, return error message
        if not rows:
            return False, 'The list is empty'
    # Return the rows
        return rows
    except (SQLAlchemyError, IntegrityError, ValueError, AssertionError, TypeError) as e:
    # If there is an error, rollback the session, print the error and return it
        session.rollback()
        print("Error:", e)
        return False, e
    finally:
    # Close the session
        session.close()

def GetAllFromTable(tableName):
    def queryFunc(session, base, tableName):
        # Construct the full table name
        realName = "public." + tableName
        # Get the table object for the specified table name
        tableObject = base.metadata.tables.get(realName)
        # Check if the table object exists
        if tableObject is None:
            return False, 'Error: Table not found'
        # Query the table object and return the results
        objects = session.query(tableObject).all()
        if not objects:
            return False, 'Error: The provided table is empty'
        return objects
    return executeQuery(queryFunc, tableName)

def GetTable(tableName):
    def queryFunc(session, base, tableName):
        # Construct the full table name (including schema) and use it to create a table object
        realName = "public." + tableName
        table = dl.CreateTableObject(realName, base.metadata)
        return table
    return executeQuery(queryFunc, tableName)


def GetAllOfColumnFromTable(tableName, columnName):
    def queryFunc(session, base, tableName, columnName):
        realName = "public." + tableName
        # Get the Table object for the specified table name
        table = base.metadata.tables.get(realName)
        for table_name in base.metadata.tables.keys():
            print(table_name)
        if table is None:
            return None, 'Table "{}" does not exist'.format(tableName)
        # Get the Column object for the specified column name
        column = table.columns.get(columnName)
        if column is None:
            return None, 'Column "{}" does not exist in table "{}"'.format(columnName, tableName)
        # Query the database to retrieve all values in the specified column
        result = session.query(column).all()
        return result
    return executeQuery(queryFunc, tableName, columnName)