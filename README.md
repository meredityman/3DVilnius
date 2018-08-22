# 3DVilnius

This blender script will produce a series of .obj files in a grid from a hight map image

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

All you need to use this script is Blender. You can find instructions for installing blender [here](https://www.blender.org/download/)

### Installing

Just clone this repository onto you machines either using the clone button at the top of this page or:

```
git clone https://github.com/meredityman/3DVilnius.git
```

You should also make sure that blender can be called from the command line.

```
blender -v
```

If you get an error you should make sure to add it to your path.

### Basic Usage

You can run python script in an existing blender file. This will enable you to check the output.

```
cd Scripts

blender ..\Blender\Example.blend --python HeightMap2Mesh.py --  ../Data/Images/Vilnius.png ../Data/Models

```

Alternatively you can run the process in the background, without specifying a .blend file. Then the programmer with run placing .obj files in the specified directory, in this case /Data/Models

```
blender --background --python HeightMap2Mesh.py --  ../Data/Images/Vilnius.png ../Data/Models
```

The default output should look something like this.

![Default Output](Data/Renders/Example.png?raw=true "Default Output")

### Sourcing Data

The elevation data used in these examples was taken from the [Copernicus Land Monitoring Service - EU-DEM](https://www.eea.europa.eu/data-and-maps/data/copernicus-land-monitoring-service-eu-dem).

## Options

You can specify a few options in the command line to control the output. You can view these like this.

```
blender --background --python HeightMap2Mesh.py --  -h
```

### Changing the input image

```
blender --background --python HeightMap2Mesh.py --  ../Data/Images/Vilnius-Map.png ../Data/Models
```

![Map Example](Data/Renders/Example-Map.png?raw=true "Map Example")

```
blender --background --python HeightMap2Mesh.py --  ../Data/Images/Vilnius-Roads.png ../Data/Models
```

![Roads Example](Data/Renders/Example-Roads.png?raw=true "Roads Example")

### Render an image

```
blender --background --python HeightMap2Mesh.py --  ../Data/Images/Vilnius.png ../Data/Models --render ../Data/Renders
```

### Adjust the mesh density

```
blender --background --python HeightMap2Mesh.py --  ../Data/Images/Vilnius.png ../Data/Models --mesh_density 0.5
```

![Density Example](Data/Renders/Example-density.png?raw=true "Density Example")

### Adjust displacement

```
blender --background --python HeightMap2Mesh.py --  ../Data/Images/Vilnius.png ../Data/Models --displace_strength 50
```

![Displacement Example](Data/Renders/Example-displacement.png?raw=true "Displacement Example")


### Adjust the grid

```
blender --background --python HeightMap2Mesh.py --  ../Data/Images/Vilnius.png ../Data/Models --grid_size 2
```

![Grid Size Example](Data/Renders/Example-grid.png?raw=true "Grid Size Example")


### Adjust the size

```
blender --background --python HeightMap2Mesh.py --  ../Data/Images/Vilnius.png ../Data/Models --print_size 5
```

![Size Example](Data/Renders/Example-size.png?raw=true "Size Example")

### Adjust the base thickness

```
blender --background --python HeightMap2Mesh.py --  ../Data/Images/Vilnius.png ../Data/Models --print_thickness 15
```

![Thickness example](Data/Renders/Example-thickness.png?raw=true "Thickness example")



### Reversing the print

```
blender --background --python HeightMap2Mesh.py --  ../Data/Images/Vilnius-Roads.png ../Data/Models --reverse
```

![Reverse Example](Data/Renders/Example-Reverse.png?raw=true "Reverse Example")






