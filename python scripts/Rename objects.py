bl_info = {
    "name": "Auto Generic Rename + Symptom Renamer",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Two operators: one to rename all objects generically, one to auto-rename with !Symptoms."
}

import bpy
import re  # Import the regex module to handle pattern matching

class MESH_OT_rename_all_generic(bpy.types.Operator):
    """
    Renames all objects in each collection to something generic like 'TempObj_###'
    so you can start fresh with consistent naming.
    """
    bl_idname = "mesh.rename_all_generic"
    bl_label = "Rename All to Generic"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        counter = 1
        for collection in bpy.data.collections:
            for obj in collection.all_objects:
                if obj.type == 'MESH':
                    # Build a new generic name
                    new_name = f"TempObj_{counter:03d}"
                    obj.name = new_name
                    counter += 1

        self.report({'INFO'}, "All objects renamed to 'TempObj_###'.")
        return {'FINISHED'}


class MESH_OT_auto_rename(bpy.types.Operator):
    """
    Auto-Rename Meshes for Symptoms:
    For each collection, rename objects to 'CollectionName_originalName!Symptoms' 
    if a 'Symptoms' custom property is found.
    Ensures that only one '!Symptoms' suffix is present and names are unique.
    """
    bl_idname = "mesh.auto_rename"
    bl_label = "Auto-Rename for Symptoms"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Dictionary to keep track of counters for each unique combination
        name_counters = {}

        for collection in bpy.data.collections:
            group_prefix = collection.name  # e.g., "DriveBelt" or "Motor"

            for obj in collection.all_objects:
                if obj.type == 'MESH':
                    # Get symptoms from custom property
                    symptoms_str = obj.get("Symptoms", "").strip()

                    # Remove existing '!Symptoms' suffix if any
                    if '!' in obj.name:
                        base_name = obj.name.split('!', 1)[0]
                    else:
                        base_name = obj.name

                    # Remove any existing generic naming patterns like 'TempObj_###' or '_TempObj_###'
                    # This makes the underscore before TempObj_### optional
                    base_name = re.sub(r'_?TempObj_\d+', '', base_name)

                    # Replace spaces in the base name with underscores and remove trailing underscores
                    safe_obj_name = base_name.replace(" ", "_").strip('_')

                    if symptoms_str:
                        # Replace commas and spaces in symptoms with underscores
                        symptoms_cleaned = re.sub(r'[,\s]+', '_', symptoms_str)
                        base_new_name = f"{group_prefix}_{safe_obj_name}!{symptoms_cleaned}"
                    else:
                        base_new_name = f"{group_prefix}_{safe_obj_name}"

                    # Determine the key for the name_counters dictionary
                    # This key is unique per group_prefix, safe_obj_name, and symptoms_cleaned
                    key = base_new_name

                    # Initialize counter if key not present
                    if key not in name_counters:
                        name_counters[key] = 1
                        new_name = base_new_name  # First instance doesn't need a counter
                    else:
                        # Append counter to the prefix to ensure uniqueness
                        counter = name_counters[key]
                        if symptoms_str:
                            new_name = f"{group_prefix}_{safe_obj_name}_{counter:03d}!{symptoms_cleaned}"
                        else:
                            new_name = f"{group_prefix}_{safe_obj_name}_{counter:03d}"
                        name_counters[key] += 1  # Increment counter for next duplicate

                        # Ensure that the new name is indeed unique
                        while any(o.name == new_name for o in collection.all_objects):
                            counter = name_counters[key]
                            if symptoms_str:
                                new_name = f"{group_prefix}_{safe_obj_name}_{counter:03d}!{symptoms_cleaned}"
                            else:
                                new_name = f"{group_prefix}_{safe_obj_name}_{counter:03d}"
                            name_counters[key] += 1

                    # Assign the new unique name
                    obj.name = new_name

        self.report({'INFO'}, "Meshes auto-renamed for symptoms successfully.")
        return {'FINISHED'}


class MESH_PT_auto_rename_panel(bpy.types.Panel):
    """
    Panel that shows both buttons in the same UI category.
    """
    bl_label = "Mesh Renaming Tools"
    bl_idname = "MESH_PT_auto_rename_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Mesh Tools'  # The tab name in the N-panel (you can change if you like)

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.rename_all_generic", text="Rename All to Generic")
        layout.operator("mesh.auto_rename", text="Auto-Rename for Symptoms")


def register():
    bpy.utils.register_class(MESH_OT_rename_all_generic)
    bpy.utils.register_class(MESH_OT_auto_rename)
    bpy.utils.register_class(MESH_PT_auto_rename_panel)


def unregister():
    bpy.utils.unregister_class(MESH_PT_auto_rename_panel)
    bpy.utils.unregister_class(MESH_OT_auto_rename)
    bpy.utils.unregister_class(MESH_OT_rename_all_generic)


if __name__ == "__main__":
    register()
