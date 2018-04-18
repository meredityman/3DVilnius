import bpy, sys, os, datetime, time
import bmesh
import mathutils
import math
import argparse



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

def loadHeightMap(path_to_image ):
    try:
        img = bpy.data.images.load(path_to_image )
        # Create image texture from image
        tex = bpy.data.textures.new("MHeight_Map", 'IMAGE')
        tex.image = img
        
        print("Height Map loaded")
        
        return tex

    except:
        raise NameError("Cannot load image %s" % realpath)

##########################################################

def createObjectMesh(xi, yi, i, properties):
        print_size = properties['print_size']
        spacing    = properties['spacing']
        grid_size  = properties['grid_size']
        print_thickness     = properties['print_thickness']
            
        # Create an empty mesh and the object.
        mesh = bpy.data.meshes.new('Mesh_' + str(i))
        obj  = bpy.data.objects.new('Mesh_' + str(i), mesh)
        vertex_group = obj.vertex_groups.new("top_verticies")
        
        bpy.context.scene.objects.link(obj)
        bpy.context.scene.objects.active = obj
        
        # Position Objects
        x_pos = xi * print_size + (xi * spacing) - ((grid_size - 1) * (print_size + spacing))/ 2 
        y_pos = yi * print_size + (yi * spacing) - ((grid_size - 1) * (print_size + spacing))/ 2 
        obj.location  = mathutils.Vector((x_pos, y_pos, 0.0))
        
        # Create cube mesh
        createCubeMesh(mesh, properties)
        assignUVs(xi, yi, obj, mesh, properties)

        return obj, mesh
    
    
##########################################################                              
def createCubeMesh(mesh, properties):
    print_size  = properties['print_size']
    print_thickness     = properties['print_thickness']

    
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)   
    bmesh.ops.scale(bm, vec = mathutils.Vector((print_size, print_size, print_thickness)), verts=bm.verts)                    
    bm.to_mesh(mesh)
    bm.free()
    
##########################################################
def assignUVs(xi, yi, obj, mesh, properties):
    grid_size  = properties['grid_size']
    grid_res  = properties['grid_res']
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bm = bmesh.from_edit_mesh(mesh)
    bm.faces.ensure_lookup_table() 
    top_face = bm.faces[5]
    
    deform_layer = bm.verts.layers.deform.active
    if deform_layer is None: deform_layer = bm.verts.layers.deform.new()
    
    vertex_group = obj.vertex_groups["top_verticies"]
    
    # Assigne UVs based on block position
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
    

    #Subdivide Top face
    top_face.select = True
    selected_edges = [edge for edge in bm.edges if edge.select]
    top_face.select = False

    subdivide_output = bmesh.ops.subdivide_edges(bm, edges=selected_edges, cuts=grid_res, use_grid_fill=True)
    bm.faces.ensure_lookup_table() 

    #Assign wieghts to vertex group

    
    prune_verts  = []
    adjust_verts = [] 
    for vert in subdivide_output["geom_inner"]:    
        if isinstance(vert, bmesh.types.BMVert):                    
            vert[deform_layer][vertex_group.index] = 1.0
            adjust_verts.append(vert)
       
    for vert in subdivide_output["geom_split"]:    
        if isinstance(vert, bmesh.types.BMVert):
            vert[deform_layer][vertex_group.index] = 0.0 
            prune_verts.append(vert)

    for edge in selected_edges:
        for vert in edge.verts:
            if isinstance(vert, bmesh.types.BMVert):
                vert[deform_layer][vertex_group.index] = 0.0
                prune_verts.append(vert)


    adjust_verts = list(set(adjust_verts) - set(prune_verts))
    sf = 1.0 + (2/grid_res)
    bmesh.ops.scale(bm, vec=mathutils.Vector((sf, sf, 1.0)), verts=adjust_verts)

    bmesh.update_edit_mesh(mesh) 
    
    bm.free() 
    
    bpy.ops.object.mode_set(mode='OBJECT')    

##########################################################
def applyDisplacement(obj, tex, properties):
    
    displace = obj.modifiers.new('Displace', 'DISPLACE')
    displace.vertex_group = "top_verticies"
    displace.mid_level = 0.0
    displace.texture_coords = "UV"
    displace.uv_layer = "UVMap"
    displace.direction = "Z"
    displace.texture = tex
    displace.strength  = properties['displace_strength'] 
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")

##########################################################                   
def cleanUpMesh(obj, mesh):
    obj.select = True
    bpy.ops.object.mode_set(mode='EDIT')    
    bpy.ops.mesh.normals_make_consistent(inside = False)
    bpy.ops.object.mode_set(mode='OBJECT')  
    obj.select = False
    
##########################################################                   
def renderImage(path_to_render_folder):
    scene = bpy.context.scene

    lamp_data = bpy.data.lamps.new(name="Light", type='POINT')
    lamp_object = bpy.data.objects.new(name="Light", object_data=lamp_data)
    scene.objects.link(lamp_object)
    lamp_object.location = (-0.4, 0.0, 0.2)
    
    camera_data = bpy.data.cameras.new(name="Camera")
    camera_object = bpy.data.objects.new(name="Camera", object_data=camera_data)
    scene.objects.link(camera_object)
    camera_object.location = (0.4, 0.0, 0.3)
    camera_object.rotation_euler = mathutils.Euler((0.3 * math.pi, 0.0, 0.5 * math.pi), 'XYZ')
                  
    scene.camera = camera_object
    render_name = 'render_' + str(time.time()) + '.jpg' 
	
    target_file = os.path.join(path_to_render_folder,  render_name)
    
    
    bpy.context.scene.render.filepath = target_file
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 720
    bpy.ops.render.render( write_still=True )      

########################################################## 
def export(obj, xi, yi, path_to_models_folder):
    obj.select = True
    
    if not os.path.exists(path_to_models_folder):
        os.makedirs(path_to_models_folder)
	
    file_name = 'block_' + str(xi) + '_' +str(yi) + '.obj'
    target_file = os.path.join(path_to_models_folder, file_name )

    bpy.ops.export_scene.obj(   filepath=target_file, 
                                use_selection=True,
                                use_triangles=True,
                                use_materials = False
                                
                            )
    obj.select = False

##########################################################
def processArgs():
	argv = sys.argv
	if "--" not in argv:
		argv = []
	else:
	   argv = argv[argv.index("--") + 1:]

	## set the prog name to match real usage
	parser = argparse.ArgumentParser(
		description = 'Run blender in background mode',
		prog = "blender -b -P "+__file__+" --",
	)	
	parser.add_argument('image',  action = FullPaths,
					help='Path to the heightmap image')
					
	parser.add_argument('models',  action = FullPaths,
					help='Directory in which models will be placed')

	parser.add_argument('--render',  metavar='R', action = FullPaths,
					help='If set, the script will render a preview to this directory')
	
	parser.add_argument('--print_size', type=float, default=10,
					help='Size of block in cm')
					
	parser.add_argument('--print_thickness', type=float, default=0.5,
					help='Base thickness of block in cm')

	parser.add_argument('--grid_size', type=int, default=3,
					help='Number of blocks per row/column')
					
	parser.add_argument('--grid_res', type=int, default=50,
					help='Resolution top face on mesh')
					
	parser.add_argument('--displace_strength', type=float, default=0.06,
					help='Displace strength. THis is how height hills will rise abouve the base')
					
	try:
		args = parser.parse_args(argv)
		print(args)
				
		properties = {}		
		properties['print_size']        = args.print_size / 100		
		properties['spacing']           = properties['print_size'] * 0.1		
		properties['print_thickness']   = args.print_thickness / 100
		properties['grid_size']         = args.grid_size
		properties['grid_res']          = args.grid_res   
		properties['displace_strength'] = args.displace_strength

		properties['path_to_image'] = args.image
		properties['path_to_models_folder'] = args.models
		properties['path_to_render_folder'] =  args.render

	
		return properties		
		
	except SystemExit as e:
		exit()
		
		
##########################################################
class FullPaths(argparse.Action):
	"""Expand user- and relative-paths"""
	def __call__(self, parser, namespace, values, option_string=None):
		setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))

##########################################################

def run(origin):

    properties = processArgs()
    
    print("Starting...")

    delete_scene_objects()

    scene = bpy.context.scene
    
    tex = loadHeightMap(properties['path_to_image'])
    
    # Create cubes
    i =  0
    for xi in range(0, properties['grid_size'] ):
            
        for yi in range(0, properties['grid_size']):
            i = i + 1
            print("Making block " + str(i))
    
            #Set up objects and meshes
            obj, mesh = createObjectMesh(xi, yi, i, properties)
            
            # Apply displacement  
            applyDisplacement(obj, tex, properties)
            
            # Clean up 
            cleanUpMesh(obj, mesh)
                        
            # Export 
            export(obj, xi, yi, properties['path_to_models_folder'])
            
    if(properties['path_to_render_folder']):
        renderImage(properties['path_to_render_folder'])
    
    print("Completed succesfully!")
    return

##########################################################



if __name__ == "__main__":
	
    run((0,0,0))