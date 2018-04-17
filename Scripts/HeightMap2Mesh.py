import bpy, sys, os
import bmesh
import mathutils
import math


spacing = 0.01
print_size = 0.10
print_thickness = 0.005
grid_size = 3
grid_res  = 10
displace_strength = 0.3
path_to_image = ""

##########################################################

def delete_scene_objects(scene=None):
    """Delete a scene and all its objects."""
    #
    # Sort out the scene object.
    if scene is None:
        # Not specified: it's the current scene.
        scene = bpy.context.screen.scene
    else:
        if isinstance(scene, str):
            # Specified by name: get the scene object.
            scene = bpy.data.scenes[scene]
        # Otherwise, assume it's a scene object already.
    #
    # Remove objects.
    for object_ in scene.objects:
        bpy.data.objects.remove(object_, True)
    #
    # Remove scene.
    # bpy.data.scenes.remove(scene, True)

##########################################################

def run(origin):
    print("Starting...")

    delete_scene_objects()

    scene = bpy.context.scene
    # Create cubes
    i =  0
    for xi in range(0, grid_size ):
            
        for yi in range(0, grid_size):
            i = i + 1
            print("Making block " + str(i))

            
        
            # Create an empty mesh and the object.
            mesh = bpy.data.meshes.new('Mesh_' + str(i))
            obj  = bpy.data.objects.new('Mesh_' + str(i), mesh)

            # Add the object into the scene.
            scene.objects.link(obj)
            scene.objects.active = obj
            obj.select = True
            
            # Cread cube mesh
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)
            
            
            x_pos = xi * print_size + (xi * spacing) - (grid_size * print_size + ((grid_size - 1) * spacing)) / 2
            y_pos = yi * print_size + (yi * spacing) - (grid_size * print_size + ((grid_size - 1) * spacing)) / 2        
            
            bmesh.ops.scale(bm, vec = mathutils.Vector((print_size, print_size, print_thickness)), verts=bm.verts)
            bmesh.ops.translate(bm, vec = mathutils.Vector((x_pos, y_pos, 0.0)), verts=bm.verts)
            
            bm.to_mesh(mesh)
            bm.free()
            
            # Make new material
            mat = bpy.data.materials.new(name=("Material_" + str(i)))
            obj.data.materials.append(mat)    
            
            
            realpath = "D:\Documents\Blender\\3DVilnius\Data\Images\Vilnius.png"
            try:
                img = bpy.data.images.load(realpath)
            except:
                raise NameError("Cannot load image %s" % realpath)
         
            # Create image texture from image
            tex = bpy.data.textures.new("Material_" + str(i), 'IMAGE')
            tex.image = img              
            
            # Apply material to face
            vertex_group = obj.vertex_groups.new("top_verticies")
            bpy.ops.object.mode_set(mode = 'EDIT')
            
            bm = bmesh.from_edit_mesh(mesh)
            bm.faces.ensure_lookup_table() 
            top_face = bm.faces[5]        
            top_face.select = True    
            
            # Assgin Material
            bpy.ops.object.material_slot_assign()
            
            # Split mesh
            selected_edges = [edge for edge in bm.edges if edge.select]

            deform_layer = bm.verts.layers.deform.active
            if deform_layer is None: deform_layer = bm.verts.layers.deform.new()

            subdivide_output = bmesh.ops.subdivide_edges(bm, edges=selected_edges, cuts=grid_res, use_grid_fill=True)
            
            for vert in subdivide_output["geom_inner"]:    
                if isinstance(vert, bmesh.types.BMVert):

                    vert[deform_layer][vertex_group.index] = 1.0
                
            
                
            bmesh.update_edit_mesh(mesh) 
            bpy.ops.object.mode_set(mode='OBJECT')    

            bm.free()          
            
            displace = obj.modifiers.new('Displace_' + str(i), 'DISPLACE')
            displace.vertex_group = "top_verticies"
            displace.direction = "Z"
            displace.texture = tex
            displace.strength  = displace_strength 
            
            
            
    print("Completed succesfully!")
    return

##########################################################



if __name__ == "__main__":
    run((0,0,0))