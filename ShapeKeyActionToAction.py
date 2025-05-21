import bpy

# ========== CONFIGURA ESTOS DATOS ==========
mesh_name = "Head"                    # Nombre del objeto con shape keys
armature_name = "rig"           # Nombre del armature con huesos controladores
target_action_name = "Talking"    # Nombre de la Action que quieres modificar (cuerpo + expresiones)
shape_key_action_name = "BS_Talking"   # Nombre de la Action que contiene la animación de las shape keys
bone_axis_index = 1  # 0=X, 1=Y, 2=Z
# ===========================================

mesh = bpy.data.objects[mesh_name]
armature = bpy.data.objects[armature_name]
target_action = bpy.data.actions.get(target_action_name)
shape_key_action = bpy.data.actions.get(shape_key_action_name)

if not mesh or not armature or not target_action or not shape_key_action:
    raise Exception("Asegúrate de que los nombres del mesh, armature y acciones existen correctamente.")

# Aseguramos que el armature tenga la Action asignada
armature.animation_data_create()
armature.animation_data.action = target_action

# Transferencia de cada FCurve de shape key a su hueso controlador correspondiente
for fcurve in shape_key_action.fcurves:
    data_path = fcurve.data_path

    # Asegurarse de que es una animación de shape key
    if not data_path.startswith('key_blocks["'):
        continue

    shape_key_name = data_path.split('"')[1]
    bone_name = f"CTRL_{shape_key_name}"
    if bone_name not in armature.pose.bones:
        print(f" Saltando '{shape_key_name}': No se encontró el hueso '{bone_name}'")
        continue

    # Crear o encontrar la FCurve correspondiente en la acción principal
    bone_path = f'pose.bones["{bone_name}"].location'
    index = bone_axis_index

    # Buscar si ya existe esa fcurve (para evitar duplicados)
    existing_fcurve = None
    for fc in target_action.fcurves:
        if fc.data_path == bone_path and fc.array_index == index:
            existing_fcurve = fc
            break

    if not existing_fcurve:
        existing_fcurve = target_action.fcurves.new(data_path=bone_path, index=index, action_group=bone_name)

    # Copiar los keyframes
    for keyframe in fcurve.keyframe_points:
        frame = keyframe.co.x
        value = keyframe.co.y

        new_key = existing_fcurve.keyframe_points.insert(frame, value)
        new_key.interpolation = keyframe.interpolation

print(f" Shape keys de '{shape_key_action_name}' transferidas a huesos en la acción '{target_action_name}'.")
