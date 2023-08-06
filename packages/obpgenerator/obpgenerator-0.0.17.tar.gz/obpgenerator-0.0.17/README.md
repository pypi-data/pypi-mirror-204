# Overview

This is a package to generate obp files which can e.g be used in Freemelt machines. The package is made to make it easy to implement new strategies for both line and point melting.  

# Installation

Install it by cloning the git reprository or from PyPi using:
```bash
pip install obpgenerator
```

# Code overview 

The code splits a component into three levels Shape, Layer, and Part.

Shape consists of one (or several) matplotlib paths which represents the area in the layer that should be manufactured. How this should be manufactured can be controlled by several parameters including:
- Resolution (distance between points in point melting)
- Melt strategy (can handle different versions of both line and point melting)
- Number of scans

Layer consist of one or more shapes. On this level you can change which order you want to scan the shapes and if you want to ramp manufacturing settings (successively increase/decrease e.g. energy input) between the scans of a shape

Part consist of one or more layers. On this level you can select layer height, scraper settings and other.

# Example

Example from examples/snake_cube.py where an svg file file is imported.

```bash
import obpgenerator

file_path1 = "examples\layer_nine_cubes.svg"
file_path2 = "examples\layer_15x15_cube.svg"

paths = obpgenerator.file_import.import_svg_layer(file_path2)
my_layer = obpgenerator.Layer.Layer()
my_layer.create_from_mplt_paths(paths)

my_layer.set_shapes(0.2)

manufacturing_settings = obpgenerator.manufacturing_settings.ManufacturingSetting()
manufacturing_settings.set_spot_size(0.1,lower=0.1,upper=1)
manufacturing_settings.set_beam_power(1500,lower=1000,upper=2000)
manufacturing_settings.set_scan_speed(1,lower=1,upper=2)
manufacturing_settings.set_dwell_time(100,lower=50,upper=150)
ramp_settings = dict(ramp_beam_power=1,ramp_dwell_time=0,ramp_scan_speed=0,ramp_spot_size=0)

my_layer.set_manufacturing_settings(manufacturing_settings)
my_layer.sorting_settings = ramp_settings
my_layer.set_melt_strategies("line_snake")
my_layer.set_nmb_of_scans(3)
my_layer.sorting_strategy = "ramp_manufacturing_settings"

my_layer.export_obp("output.obp")
```

# To package
- Delete old builds in the \dist folder 
- Update the version in the setup.cfg file
- run "python -m build"
- upload to pip with "twine uplaod dist/*"
