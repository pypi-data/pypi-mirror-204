def KDS1():
    print("""
    
Write MongoDB query to :
1) Create, display and drop Database 
2) Create, display and drop Collection
3) Insert, display, update and delete a document

1)Create, display and drop Database
 Create a database 
 Syntax: use database_name 
 Display databases 
 Syntax: show dbs 
 Drop database 
 Syntax: db.database_name.drop()

2) Create, display and drop Collection
 Create a collection 
 Syntax : db.createCollection(“collection_name”)
 Display Collections 
 Syntax: show collections
 Drop Collection 
 Syntax: db.collection_name.drop()

3) Insert, display, update and delete a document

 Insert a document ( insertOne )
 Syntax: db.collection_name.insert({“name”})
 Insert more than one document ( insertMany ) 
 Syntax: db.collection_name.insertMany({“name1”}, {“name2”})
 Display documents 
 Syntax: db.collection_name.find() 
 Delete a document 
 Syntax: db.collection_name.remove({“deletion_criteria”}) 

    
    """)