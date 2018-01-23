import math
import glob
import re
import numpy as np
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import spereadNew as sperd

def spe2pngFFNew(directory='./'):
    dirname = directory
    #dirname = '070510/sample/';	#put directory name on top of output filenames
    pl = 770e-7
    ##########################################################
    ############# CHANGE THE RANGE OF WAVELENGTH #############
    offset_nm = 0	            #to raise the curve
    Snm=711.943 + offset_nm;    #Shorter wavelength displayed. center @770nm; 671.855(@730)681.875(@740)691.895(@750)701.915(@760)
    Lnm=827.815 + offset_nm;    #Longer wavelength displayed. center @770nm; 787.906(@730)797.855(@740)807.863(@750)817.842(@760)
    #########################################################
    #671.855(@730)681.875(@740)691.895(@750)701.915(@760)711.935(@770)721.955(@780)731.976(@790)
    #787.906(@730)797.855(@740)807.863(@750)817.842(@760)827.82(@770)837.798(@780)847.776(@790)
    #########################################################
    #########################################################
    anglelim = 50
    #klim=math.sin(anglelim*math.pi/180)*(2*math.pi/pl)
    filenames = glob.glob(dirname + '*.spe') 
    #filenames = glob.glob('*300gmm.spe') 
    num_files=len(filenames)

    # Acquire the background image
    background_filename = 'back.spe'
    (background_image,background_xaxis,error_code,message) = sperd.spereadJanis(background_filename)
    if (error_code == -1):
        print ('WARNING function spe2png_py: Background file %s not found in'
               ' directory %s.\n' %(background_filename,dirname))
        background_exists = 0
    elif (error_code <= 0):
        print(message)
        print('error code: %d.\n' %error_code)
        exit()
    else:
        background_exists = 1

    for file in filenames:
        input_filename = file
        #input_filename_up = filename.upper()
        # directory name + input filename for plot convenience
        dir_input_filename = dirname + input_filename
        png_filename = input_filename.rstrip('.spe').rstrip('.SPE') + '.png'
        png_filename_log = 'FFLog' + png_filename
        png_filename_sum = 'FF' + png_filename
        # ascii_filename = re.sub('.spe','.dat',input_filename)
        # filesize = filenames[i] #Not done, but is never used.
        (image, xaxis, error_code, message) = sperd.spereadJanis(input_filename)
        if (error_code <= 0):
            print(message)
            print('error code: %d.\n' %error_code)
            exit()
        if (background_exists):
            if (image.size == background_image.size):
                if (background_xaxis == xaxis):
                    image = image - background_image
                else:
                    print ('WARNING function spe2png_py: Background image',
                           '%s has different xaxis than %s.\n' %(background_image,
                                                                 input_filename))
            else:
                print ('WARNING function spe2png_py: Background image %s is of',
                       'different size than %s.\n' %(background_filename,
                                                     input_filename))

        # Angle (y-axis) calibration
        fobj = 4000     # objective focal length in um
        ypixsize = 20   # pixel size in um
        yindex = np.linspace(-199,200,400)
        yaxis = np.arcsin(ypixsize*yindex/fobj)*180/math.pi #degrees
        yk = (ypixsize*yindex/fobj)*2*math.pi/pl            #degrees

        # set display range for the spectral image
        xgap = abs(xaxis[0] - xaxis[1])/2
        iniIdx = min(np.where(abs(xaxis-Snm)<xgap))
        endIdx = max(np.where(abs(xaxis-Lnm)<xgap))
        if not iniIdx.any():
            iniIdx = 0
        else:
            iniIdx = np.amin(iniIdx)
        if not endIdx.any():
            endIdx = max(xaxis.shape)
        else:
            endIdx = np.amax(endIdx) + 1

        angle_correction = -0.4         # shift the center to right
        ygap = abs(yaxis[0]-yaxis[1])/2
        iniy = min(np.where(abs(yaxis+anglelim+angle_correction)<ygap))
        endy = max(np.where(abs(yaxis-anglelim+angle_correction)<ygap))
        if not iniy.any():
            iniy = 0
        else:
            iniy = np.amin(iniy)
        if not endy.any():
            endy = max(yaxis.shape)
        else:
            endy = np.amax(endy) + 1
    #    ykgap=abs(yk[0]-yk[1])/2
    #    iniyk=min(np.where(abs(yk+klim)<ykgap))
    #    endyk=max(np.where(abs(yk-klim)<ykgap))
    #    if not iniyk.any():
    #        iniyk = 0
    #    else:
    #        iniyk = np.amin(iniyk)
    #    if not endyk.any():
    #        endyk = max(yk.shape)
    #    else:
    #        endyk = np.amax(endyk) + 1
            
        # Region of interest for the figure
        #ROIx = xaxis[iniIdx:endIdx]
        #ROIy = yaxis[iniy:endy]     # +angle_correction
        #ROIyk = yk[iniyk:endyk]
        #ROIyk2 = np.sin(ROIy*math.pi/180)*2*math.pi/pl
        #ROIxeV = 1238.82/ROIx

        # definition of ROIimg (Region of Interest)
        ROIimg = image[:,iniy:endy,iniIdx:endIdx].reshape(endy-iniy,endIdx-iniIdx)
        #ROIimg = ROIimg / np.amax(ROIimg)      #intensity normalization
    #    clims = np.array([100, np.amax(ROIimg[50:300,750:1000])+1000])
        vmin = 100
        vmax = np.amax(ROIimg[50:300,750:1000])+1000
        imgplot = plt.imshow(ROIimg.astype(float), aspect='auto', cmap='jet', 
                             vmin = vmin, vmax = vmax, 
                             extent=[xaxis[iniIdx],xaxis[endIdx-1],
                                     yaxis[iniy],yaxis[endy-1]])
        #imgplot = plt.imshow(ROIimg, aspect='auto', cmap='jet')
    #    plt.colorbar()
        plt.ylabel('angle (degrees)')
        #plt.ylabel('pixel index')
        #plt.xlabel('Spatial Distance (um)')
        plt.xlabel('Wavelength (nm)')
        
        A = input_filename.partition('.')[0]
        A = '1/24/14 C3997.5' + A
        #plt.ylim(-199, 200)
        #plt.xlim(768.2, 772)
    #    plt.xlim(775, 790)
    #    plt.ylim(-40, 40)       #IMGs: x is for pixels, y: angle
        #axis square
        A = A.replace('_',' ')
        A = A.replace('p','.')
        plt.title(A)
        pylab.savefig(png_filename, bbox_inches='tight')
        plt.close()

if __name__ == '__main__':
    spe2pngFFNew()
        