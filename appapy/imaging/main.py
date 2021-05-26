
from typing import List
from wand.image import Image

from appapy.common.text import find_and_replace

def create_png_from_svg(self, svg_path, png_path):
    self.log('Creating PNG render... {0}'.format(png_path))
    with Image(filename=svg_path) as original:
        with original.convert('png') as converted:
            converted.save(filename=png_path)

def social(self, svg_path, png_path, library):
    
    find_and_replace(svg_path, "!!library!!", library)
    create_png_from_svg(svg_path, png_path)

def execute(args: List[str]):   
    if args is None or len(args) == 0:
        raise ValueError(args)
    
    arg0 = args[0]
    
    if arg0 == "social":
        if len(args) != 3:
            raise ValueError(args)
                
        library = args[1]
        svg_path = args[2]
        png_path = svg_path.replace(".svg", ".png")
                
        social(svg_path, png_path, library)
    else:
        raise ValueError(args)