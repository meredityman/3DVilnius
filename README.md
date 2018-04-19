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

You should also make sure that blender can be called from the command line. Try typing:

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

Alternatively you can run the process in the background, without specifying a .blend file.

```
blender --background --python HeightMap2Mesh.py --  ../Data/Images/Vilnius.png ../Data/Models
```

## Options

You can specify a few options in the command line to control the output. View these like this.

```
blender --background --python HeightMap2Mesh.py --  -h
```

## Examples

![Default Output](Data/Renders/Example.png?raw=true "Default Output")

![Density Example](Data/Renders/Example-density.png?raw=true "Density Example")

![Displacement Example](Data/Renders/Example-displacement.png?raw=true "Displacement Example")

![Grid Size Example](Data/Renders/Example-grid.png?raw=true "Grid Size Example")

![Size Example](Data/Renders/Example-size.png?raw=true "Size Example")

![Thickness example](Data/Renders/Example-thickness.png?raw=true "Thickness example")

![Map Example](Data/Renders/Example-Map.png?raw=true "Map Example")

![Roads Example](Data/Renders/Example-Roads.png?raw=true "Roads Example")

![Reverse Example](Data/Renders/Example-Reverse.png?raw=true "Reverse Example")






