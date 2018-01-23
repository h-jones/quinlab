import numpy as np
import os.path

def datatype_to_string(datatype):
    switcher = {
        0: "float32",
        1: "int32",
        2: "int16",
        3: "uint16",
        }
    return switcher.get(datatype, "invalid")

def spereadJanis(filename):
    """ Input:
     filename: full path name for file to be read
    
     Output:
     image: a matrix of size [xDim,yDim,NumFrames] with the pixels of the
       image. xDim and yDim are the x and y dimensions of the image. NumFrames
       is the number of frames the current spe file contains.
     xaxis: the wavelength axis of the image. Calculated from the calibration
       data of the spe file
     error_code: the error_code. >0 means everything is ok, <=0 means some
       problem arised.
     message: the error message. """

    error_code = 0
    message = "ERROR in function speread: corrupt header in file %s.\n" %filename

    # Open file
    if (os.path.isfile(filename)):
        file = open(filename,'rb')
    else:
        image = np.zeros((1,1,1), dtype='int')
        xaxis = 1
        error_code = -1
        message = "ERROR in function speread: file %s does not exist\n" %filename
        return (image,xaxis,error_code,message)
    # Read header
    Head = np.fromfile(file=file,dtype='uint16',count=2050)
    # Dimensions of image
    xDim = int(Head[21])
    yDim = int(Head[328])
    # Total # of pixels of the CCD detector
    xDimDet = Head[3]
    yDimDet = Head[9]
    # Experiment datatype
    # 0 = FLOATING POINT
    # 1 = LONG INTEGER
    # 2 = INTEGER
    # 3 = UNSIGNED INTEGER
    datatype = Head[54]
    # Total number of frames that the file contains
    file.seek(1446,0) #move pointer to read NumFrames
    NumFrames = int(np.fromfile(file,'int32',1))
    DataPoints = xDim*yDim*NumFrames
    
    # x-axis Calibration
    file.seek(3000,0); #move pointer to start of X calibration structure
    file.seek(101,1); #move pointer to polynom_order position
    polynom_order = int(np.fromfile(file,'uint8',1))
    calib_count = int(np.fromfile(file,'uint8',1))
    pixel_position = np.fromfile(file,'double',10)
    pixel_position = pixel_position[0:calib_count-1]
    calib_value = np.fromfile(file,'double',10)
    calib_value = calib_value[0:calib_count-1]
    polynom_coeff = np.fromfile(file,'double',6)
    xindex = np.arange(0,xDim)
    xaxis = polynom_coeff[0] + xindex*polynom_coeff[1] + pow(xindex,2)*polynom_coeff[2]
    
    # read in the image data
    file.seek(4100,0) # move  pointer to start of data
    datatype_str = datatype_to_string(datatype)
    if datatype_str != "invalid":
        image = np.fromfile(file,datatype_str,DataPoints)
        if (image.size >=DataPoints):
            error_code = 1
            message = ''
        else:
             error_code = -2
             message = 'ERROR in function speread: less data points than expected in file %s.\n' %filename
             file.close()
             return (image,xaxis,error_code,message)
    else:
        image = np.zeros((NumFrames,yDim,xDim),'int')
        error_code = -3
        message = 'ERROR in function speread: invalid datatype in file %s.\n' %filename
    file.close()
    image.shape = (NumFrames,yDim,xDim)
    return (image,xaxis,error_code,message)
