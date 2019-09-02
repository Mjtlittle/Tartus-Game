import pygame

# settings
game_name = 'Tartus'
font = 'freesansbold.ttf'#'OpenSans-Bold.ttf'
board_dimensions = (10,20)#(10,20)
border_width = 3
padding = 10

# colors
# pallet used: https://lospec.com/palette-list/sweetie-16
background_color = (26,28,44) #1a1c2c
middleground_color = (51,60,87) #333c57
foreground_color = (86,108,134) #566c86
secondary_color = (148,176,194) #94b0c2
primary_color = (244,244,244) #f4f4f4

pieces = [

    # T
    {
        'color':(197,87,239), #c557ef # custom color to fit the tetris colors
        'stages':[
            [(0,0),(1,0),(-1,0),(0,1)],
            [(0,0),(0,-1),(-1,0),(0,1)],
            [(0,0),(1,0),(0,-1),(-1,0)],
            [(0,0),(1,0),(0,-1),(0,1)],
            ],
        'centers':[(0.0, 0.5), (-0.5, 0.0), (0.0, -0.5), (0.5, 0.0)]
    },

    # dot, cause y not
    {
        'color': primary_color, #f4f4f4
        'stages':[[(0,0)]],
        'centers':[(0.0, 0.0)]
    },

    # half vertical, cause y not
    {
        'color': secondary_color, #94b0c2
        'stages':[[(0,0),(0,-1)],[(0,0),(1,0)]],
        'centers':[(0.0, -0.5),(0.5,0.0)]
    },

    # L
    {
        'color':(239,125,87), #ef7d57
        'stages':[
            [(0,0),(1,0),(-1,0),(1,1)],
            [(0,0),(0,-1),(0,1),(-1,1)],
            [(0,0),(1,0),(-1,0),(-1,-1)],
            [(0,0),(0,-1),(0,1),(1,-1)],
            ],
        'centers':[(0.0, 0.5), (-0.5, 0.0), (0.0, -0.5), (0.5, 0.0)]
    },

    # J
    {
        'color':(59,93,201), #3b5dc9
        'stages':[
            [(0,0),(1,0),(-1,0),(-1,1)],
            [(0,0),(0,-1),(0,1),(-1,-1)],
            [(0,0),(1,0),(-1,0),(1,-1)],
            [(0,0),(0,-1),(0,1),(1,1)],
            ],
        'centers':[(0.0, 0.5), (-0.5, 0.0), (0.0, -0.5), (0.5, 0.0)]
    },

    # O
    {
        'color':(255,205,117), #ffcd75
        'stages':[
            [(0,0),(1,0),(0,-1),(1,-1)],
            ],
        'centers':[(0.5, -0.5)]
    },

    # I
    {
        'color':(115,239,247), #73eff7
        'stages':[
            [(-1,0),(0,0),(1,0),(2,0)],
            [(0,1),(0,0),(0,-1),(0,-2)],
            ],
        'centers':[(0.5, 0.0), (0.0, -0.5)]
    },

    # S
    {
        'color':(167,240,112), #a7f070
        'stages':[
            [(0,0),(1,0),(0,1),(-1,1)],
            [(0,0),(-1,0),(-1,-1),(0,1)],
            [(0,0),(1,0),(0,1),(-1,1)],
            [(0,0),(0,1),(-1,0),(-1,-1)],
            ],
        'centers':[(0.0, 0.5), (-0.5, 0.0), (0.0, 0.5), (-0.5, 0.0)]
    },

    # Z
    {
        'color':(209,82,105), #d15269 # brightened the red
        'stages':[
            [(0,0),(-1,0),(0,1),(1,1)],
            [(0,0),(-1,0),(0,-1),(-1,1)],
            [(0,0),(-1,0),(0,1),(1,1)],
            [(0,0),(-1,0),(0,-1),(-1,1)]
            ],
        'centers':[(0.0, 0.5), (-0.5, 0.0), (0.0, 0.5), (-0.5, 0.0)]
    },

]

#
#  Piece Center Compilation Code
#  (used once for finding the centers)
#

'''
for piece in pieces:
    rotation_stage_centers = []
    for stage in piece['rotation_stages']:
        max_x = 0
        max_y = 0
        min_x = 0
        min_y = 0
        for x, y in stage:
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
        center = ((max_x+min_x)/2, (max_y+min_y)/2)
        rotation_stage_centers.append(center)
    print(rotation_stage_centers)
'''