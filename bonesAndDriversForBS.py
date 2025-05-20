import bpy

# CONFIGURA ESTOS NOMBRES:
mesh_obj_name = "MiMesh"       # Reemplaza con el nombre de tu objeto con shape keys
armature_obj_name = "MiArmature"  # Reemplaza con el nombre de tu armature

# REFERENCIAS
mesh = bpy.data.objects[mesh_obj_name]
armature = bpy.data.objects[armature_obj_name]

# Entramos en modo de edición para crear los huesos
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='EDIT')
edit_bones = armature.data.edit_bones

# Limpiamos huesos anteriores (opcional)
# for b in armature.data.edit_bones:
#     if b.name.startswith("CTRL_"):
#         edit_bones.remove(b)

# Crear un hueso por shape key
bpy.ops.object.mode_set(mode='EDIT')
y_offset = 0
for i, key_block in enumerate(mesh.data.shape_keys.key_blocks):
    if key_block.name == "Basis":
        continue  # Saltamos el basis

    bone_name = f"CTRL_{key_block.name}"
    bone = edit_bones.new(bone_name)
    bone.head = (0, y_offset, 0)
    bone.tail = (0, y_offset, 0.2)
    y_offset += 0.3

# Volver al modo objeto
bpy.ops.object.mode_set(mode='POSE')

# Crear drivers en las shape keys
for key_block in mesh.data.shape_keys.key_blocks:
    if key_block.name == "Basis":
        continue

    driver = key_block.driver_add("value").driver
    driver.type = 'SCRIPTED'
    
    # Crear una variable que apunta al bone
    var = driver.variables.new()
    var.name = "ctrl"
    var.type = 'TRANSFORMS'
    
    targ = var.targets[0]
    targ.id = armature
    targ.bone_target = f"CTRL_{key_block.name}"
    targ.transform_type = 'LOC_Y'  # Puedes cambiar a ROT_X, SCALE_Z, etc.
    targ.transform_space = 'LOCAL_SPACE'

    # Mapeo directo (posición Y = valor shape key)
    driver.expression = "ctrl"

print("Huesos y drivers creados.")
