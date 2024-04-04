import bpy

def move_meshes_to_main_collection():
    main_collection = bpy.data.collections.get("main")
    if main_collection is None:
        main_collection = bpy.data.collections.new("main")
        bpy.context.scene.collection.children.link(main_collection)

    # Get all collections in the scene
    all_collections = bpy.data.collections
    
    # Loop through each collection
    for collection in all_collections:
        # Skip the "main" collection
        if collection.name != "main":
            # Move objects from other collections to the main collection
            for obj in collection.objects:
                main_collection.objects.link(obj)
            # Unlink the collection
            bpy.data.collections.remove(collection)

# Call the function to move meshes to the main collection and remove other collections
move_meshes_to_main_collection()
