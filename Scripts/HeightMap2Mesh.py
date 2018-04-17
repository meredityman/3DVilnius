import bpy, sys, os
import bmesh
import mathutils
import math


spacing = 0.01
print_size = 0.10
print_thickness = 0.005
grid_size = 2
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
            
            
            x_pos = (2 * xi) * print_size + (xi * spacing) - (grid_size * print_size + ((grid_size - 1) * spacing)) / 2
            y_pos = (2 * yi) * print_size + (yi * spacing) - (grid_size * print_size + ((grid_size - 1) * spacing)) / 2        
            
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
                
            
            slot = mat.texture_slots.add()
            slot.texture = tex
            
            # Apply material to face
            bm = bmesh.new()
            bm.from_mesh(obj.data)        
            

            bm.faces.ensure_lookup_table() 
            top_face = bm.faces[0]        
            top_face.select = True
            
            obj.select = False
            
    print("Completed succesfully!")
    return

##########################################################



if __name__ == "__main__":
    run((0,0,0))