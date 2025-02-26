from pymongo import MongoClient
from bson.objectid import ObjectId


def get_mongodb_collection(mongodb_uri, db_name, collection_name):
    """
    Connects to a MongoDB collection and returns the collection reference.

    Parameters:
    - mongodb_uri: URI string to connect to MongoDB.
    - db_name: The name of the database.
    - collection_name: The name of the collection.

    Returns:
    - Reference to the collection in the database.
    """
    try:
        # Create MongoDB client
        client = MongoClient(mongodb_uri)

        # Obtain reference to the database
        db = client[db_name]

        # Obtain reference to the collection
        collection = db[collection_name]

        return client, collection
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {e}")
        return None




def consulta_varios_documentos( mongodb_uri, db_name, collection_name, query ):

	client, collection  = get_mongodb_collection(mongodb_uri, db_name, collection_name)
	cursor = collection.find(query) # Seleciona os documentos que correspondem à query de consulta
	docs = list( cursor )
	client.close()

	return docs



def consulta_um_unico_documento( mongodb_uri, db_name, collection_name, query ):

	client, collection = get_mongodb_collection(mongodb_uri, db_name, collection_name)
	documento = collection.find_one(query) # Seleciona os documentos que correspondem à query de consulta
	client.close()

	return documento
