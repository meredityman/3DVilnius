import bpy, sys, os
import bmesh
import mathutils
import math


spacing = 0.0
print_size = 0.10
print_thickness = 0.005
grid_size = 3
grid_res  = 50
displace_strength = 0.05
path_to_image = "D:\Documents\Blender\\3DVilnius\Data\Images\Vilnius.png"

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

    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)

##########################################################

def run(origin):
    print("Starting...")

    delete_scene_objects()

    try:
        img = bpy.data.images.load(path_to_image )
    except:
        raise NameError("Cannot load image %s" % realpath)


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
            
            # Create cube mesh
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
            
         
            # Create image texture from image
            tex = bpy.data.textures.new("Material_" + str(i), 'IMAGE')
            tex.image = img              
            
            # Apply material to face
            vertex_group = obj.vertex_groups.new("top_verticies")
            bpy.ops.object.mode_set(mode = 'EDIT')
            
            bm = bmesh.from_edit_mesh(mesh)
            bm.faces.ensure_lookup_table() 
            top_face = bm.faces[5]
            
            uv_layer = bm.loops.layers.uv.verify()        
            
            
            step = 1 / grid_size;
            x0   = xi * step
            x1   = (xi + 1) * step
            y0   = yi * step
            y1   = (yi + 1) * step
            
            
            top_face.loops[0][uv_layer].uv = tuple([x1, y1])
            top_face.loops[1][uv_layer].uv = tuple([x0, y1])
            top_face.loops[2][uv_layer].uv = tuple([x0, y0])
            top_face.loops[3][uv_layer].uv = tuple([x1, y0 ])
            

            # Split mesh
            top_face.select = True

            selected_edges = [edge for edge in bm.edges if edge.select]

            deform_layer = bm.verts.layers.deform.active
            if deform_layer is None: deform_layer = bm.verts.layers.deform.new()
            

            subdivide_output = bmesh.ops.subdivide_edges(bm, edges=selected_edges, cuts=grid_res, use_grid_fill=True)
                        
            for vert in subdivide_output["geom_inner"]:    
                if isinstance(vert, bmesh.types.BMVert):
                    vert[deform_layer][vertex_group.index] = 1.0
           
           for vert in subdivide_output["geom_split"]:    
                if isinstance(vert, bmesh.types.BMVert):
                    vert[deform_layer][vertex_group.index] = 0.0 
            
            for edge in selected_edges:
                for vert in edge.verts:
                    if isinstance(vert, bmesh.types.BMVert):
                        vert[deform_layer][vertex_group.index] = 0.0
            
                
            bmesh.update_edit_mesh(mesh) 
            bpy.ops.object.mode_set(mode='OBJECT')    

            bm.free()          
            
            displace = obj.modifiers.new('Displace', 'DISPLACE')
            displace.vertex_group = "top_verticies"
            displace.mid_level = 0.0
            displace.texture_coords = "UV"
            displace.uv_layer = "UVMap"
            displace.direction = "Z"
            displace.texture = tex
            displace.strength  = displace_strength 
            
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")
            
            
    print("Completed succesfully!")
    return

##########################################################



if __name__ == "__main__":
    run((0,0,0))