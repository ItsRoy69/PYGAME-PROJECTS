'''Import'''
import os


'''Images'''
IMAGEPATHS = {
    'pig': [
        os.path.join(os.getcwd(), 'resources/images/pig_1.png'),
        os.path.join(os.getcwd(), 'resources/images/pig_2.png'),
        os.path.join(os.getcwd(), 'resources/images/pig_damaged.png'),
    ],
    'bird': [
        os.path.join(os.getcwd(), 'resources/images/bird.png'),
    ],
    'wall': [
        os.path.join(os.getcwd(), 'resources/images/wall_horizontal.png'),
        os.path.join(os.getcwd(), 'resources/images/wall_vertical.png'),
    ],
    'block': [
        os.path.join(os.getcwd(), 'resources/images/block.png'),
        os.path.join(os.getcwd(), 'resources/images/block_destroyed.png'),
    ]
}
'''Fonts'''
FONTPATH = {
    'Comic_Kings': os.path.join(os.getcwd(), 'resources/fonts/Comic_Kings.ttf'),
    'arfmoochikncheez': os.path.join(os.getcwd(), 'resources/fonts/arfmoochikncheez.ttf'),
}
'''Audio'''
BGMPATH = os.path.join(os.getcwd(), 'resources/audios/bgm.ogg')
'''Screen'''
SCREENSIZE = (1200, 700)
'''fps'''
FPS = 60
'''Background Color'''
BACKGROUND_COLOR = (51, 51, 51)