import json
from nbt import nbt
from PIL import Image
import math
import os
import sys

def read_nbt(filename):
    return nbt.NBTFile(filename, 'rb')


def write_nbt(filepath, nbtfile):
    nbtfile.write_file(filepath)
    print(f'Wrote {nbtfile} to {filepath}')


def load_blocks(filenames):
    for filename in filenames:
        jdata = json.load(open(os.getcwd() + 'block.json'))
        im = Image.open(os.getcwd() + f'/block/{filename}.png')
        rgb_im = im.convert('RGBA')
        
        clist = []
        for c in [(x, z) for x in range(im.size[0]) for z in range(im.size[1])]:
            rgb = rgb_im.getpixel(c)
            clist.append(rgb)
        
        r = int(sum([rgb[0] for rgb in clist]) / len(clist))
        g = int(sum([rgb[1] for rgb in clist]) / len(clist))
        b = int(sum([rgb[2] for rgb in clist]) / len(clist))
        a = int(sum([rgb[3] for rgb in clist]) / len(clist))
        fn = filename.replace('.png', '')
        jdata[fn.replace('_top', '')] = (r,g,b,a)

        with open('block.json', 'w+') as blockfile:
            json.dump(jdata, blockfile)

def to_schem(img_path):
    # Open file and convert to RGB
    im = Image.open(img_path)
    rgb_im = im.convert('RGBA')
    blockjson = json.load(open(os.getcwd() + '/py/block.json'))
    palette_blocks = []
    indices = {}
    # Creating palette
    palette = nbt.TAG_Compound()
    palette.name = 'Palette'

    # Iterating over each coordinate in the image
    for c in [(x, z) for x in range(im.size[0]) for z in range(im.size[1])]:
        # Get the color data from the pixel at coord c
        rgb = rgb_im.getpixel(c)

        # Getting the block with the closest color to the image pixel and
        # appending it to the palette list
        closest = min(blockjson, key=lambda k: math.dist(rgb, blockjson[k]))
        if closest not in palette_blocks:
            palette_blocks.append(closest)

            # The palette holds all the blocks that are used in a schematic. The field name
            # is the block name and the value is the index. This index is referenced in the 
            # BlockData field to identify which block is present at a given coord
            palette[f'minecraft:{closest}'] = nbt.TAG_Int(value=palette_blocks.index(closest))

        # Index blocks by x + z * Width + y * Width * Length. If we keep the same
        # order as the image coordinates the image comes out flipped and has holes.
        # (this may be fixed later)
        indices[c[0]+c[1]*im.size[0]+1*im.size[0]*im.size[1]] = palette_blocks.index(closest)

    # Initializing new NBT
    genfile = nbt.NBTFile()
    genfile.name = 'Schematic'

    # Setting basic NBT values
    genfile.tags.append(nbt.TAG_Int(name='Version', value=2))
    genfile.tags.append(nbt.TAG_Short(name='Width', value=im.size[0]))
    genfile.tags.append(nbt.TAG_Short(name='Height', value=1))
    genfile.tags.append(nbt.TAG_Short(name='Length', value=im.size[1]))
    genfile.tags.append(nbt.TAG_Int(name='DataVersion', value=2230))

    # Creating block data 
    blockdata = nbt.TAG_Byte_Array()
    blockdata.name = 'BlockData'

    # Set the palette length to length of the de-duped palette list
    genfile.tags.append(nbt.TAG_Int(name='PaletteMax', value=len(palette_blocks)))
    genfile.tags.append(palette)

    # A list of integers each referencing a block index from the palette is created
    # by sorting the indices dict. This list is then turned into a byte array as 
    # that is the type needed by the NBT file. This prevents the image from being
    # flipped.
    blockdata.value = bytearray([indices[i] for i in sorted(indices)])
    genfile.tags.append(blockdata)
    genfile.write_file(os.getcwd() + '/temp/upload1.schem')

    
    
    # return genfile

# print(sys.argv[1].replace('file://', ''))
try:
    to_schem(sys.argv[1].replace('file://', ''))
    print(True)
    sys.stdout.flush()
except:
    print(False)
    sys.stdout.flush()


# def to_image(nbtin):
#     # Create image object
#     img = Image.new('RGBA', (nbtin['Width'].value, nbtin['Length'].value))

#     # Load block-color mappings
#     blockjson = json.load(open('block.json'))

#     # Map palette index to RGB color vector
#     palette_dict = {nbtin['Palette'][t].value: blockjson[t.replace('minecraft:', '')] for t in nbtin['Palette']}

#     # Insert pixel data into image by referencing palette dict keys
#     img.putdata([tuple(palette_dict[b]) for b in nbtin['BlockData'].value])

#     return img






