import bpy

def rename_objects_in_all_collections():
    # Iterate through all collections in the Blender file
    for collection in bpy.data.collections:
        # Initialize a counter for naming objects sequentially within each collection
        counter = 1
        
        # Iterate through each object in the current collection
        for obj in collection.objects:
            # Generate a new name using the collection's name, an underscore, and the counter
            new_name = f"{collection.name}_{counter}"
            
            # Rename the object
            obj.name = new_name
            
            # Increment the counter for the next object within the same collection
            counter += 1
        
        print(f"Renamed {counter - 1} objects in collection '{collection.name}'.")

rename_objects_in_all_collections()
