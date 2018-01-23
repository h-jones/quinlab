import glob
from matplotlib import image as mplimg
import spereadNew as sperd

def spe2pngraw(directory='./', file=''):
    dirname = directory
    filename = file
    
    input_filename = filename
    dir_input_filename = dirname + input_filename
    png_filename = input_filename.rstrip('.spe').rstrip('.SPE') + '.png'
    (image, xaxis, error_code, message) = sperd.spereadJanis(input_filename)
    mplimg.imsave(png_filename, image[0], cmap="gray")
                    
if __name__ == '__main__':
    spe2pngraw()
        