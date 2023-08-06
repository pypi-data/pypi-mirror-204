"""Main module."""
from astropy.io import fits
from astropy.table import Table
import numpy as np
import glob
import os
import tqdm
import warnings
import pdb
from copy import deepcopy

class splint:
    """
    Splint is the object for taking a multi-integration file and splitting it up
    """
    def __init__(self,inFile=None,outDir=None,overWrite=False,flipToDet=False,
                 detectorName=None,mirageSeedFile=False):
        """
        Initializes the objects
        
        Parameters
        ----------
        inFile: str
            A path for the file to split
        outDir: str
            The path to the output directory
        overWrite: bool
            Overwrite existing files?
        flipToDet: bool
            Flip to detector coordinates (provisional)?
        detectorName: str or None
            Give a detector name for flipping. If None, it is read from the header automatically
        mirageSeedFile: bool
            Is it a mirage seed file? This requires extra treatment for the differet parts of segments
        """
        self.inFile = inFile
        self.mirageSeedFile = mirageSeedFile
        
        if os.path.exists(self.inFile) == False:
            warnings.warn('No file found. {}'.format(self.inFile))
            self.nint = 0
        else:
            HDUList = fits.open(self.inFile)
            self.head = HDUList[0].header
            if self.mirageSeedFile == True:
                self.int_start_num = self.head['SEGINTST'] + 1 + self.head['PTINTSRT']
            elif ('INTSTART' not in self.head) & ('SEGINTST' in self.head):
                warnings.warn('INTSTART not found, trying SEGINTST')
                self.int_start_num = self.head['SEGINTST'] + 1
            elif 'INTSTART' in self.head:
                self.int_start_num = self.head['INTSTART']
            else:
                warnings.warn('INTSTART not found, setting the int start to 1')
                self.int_start_num = 1
            
            if self.mirageSeedFile == True:
                head1 = HDUList[1].header
                self.nint = head1['NAXIS4'] ## didn't find a better keyword
                self.nint_orig = self.head['EXPINT']
            elif 'INTEND' not in self.head:
                warnings.warn('INTEND not found, reverting to using NINTS')
                if 'NINTS' not in self.head:
                    warnings.warn('NINTS not found, trying SEGINTED')
                    self.nint = self.head['SEGINTED'] - self.int_start_num + 2  ## number in this file segment
                    self.nint_orig = self.head['EXPINT']
                else:
                    self.nint = self.head['NINTS']
                    self.nint_orig = self.nint
            elif self.head['INTEND'] == 0:
                warnings.warn('INTEND is 0, reverting to using NINTS')
                self.nint = self.head['NINTS']
                self.nint_orig = self.nint
            else:
                self.nint = self.head['INTEND'] - self.int_start_num + 1 ## number in this file segment
                self.nint_orig = self.head['NINTS'] ## original number of integrations in exposure
            
            if 'INT_TIMES' in HDUList:
                self.times_tab = Table(fits.getdata(self.inFile,extname='INT_TIMES'))#HDUList['INT_TIMES'].data)
            else:
                self.times_tab = Table()
        
        self.outDir = outDir
        if os.path.exists(self.outDir) == False:
            os.mkdir(self.outDir)
        
        self.overWrite = overWrite
        self.detectorName = detectorName
        self.flipToDet = flipToDet
        self.baseName = os.path.splitext(os.path.basename(self.inFile))[0]
        
    
    def split(self):
        
        origHDUList = fits.open(self.inFile)
        
        datCube = origHDUList['SCI'].data
        if 'ERR' in origHDUList:
            save_error=True
            errCube = origHDUList['ERR'].data
        else:
            save_error= False
        
        if 'DQ' in origHDUList:
            save_dq =True
            dqCube = origHDUList['DQ'].data
        else:
            save_dq = False
        
        for i in tqdm.tqdm(np.arange(self.nint)):

            if self.nint == 1:
                if len(datCube.shape) > 2:
                    _thisint = datCube[0]
                    if save_error == True:
                        _thiserr = errCube[0]
                    if save_dq == True:
                        _thisdq = dqCube[0]
                else:
                    _thisint = datCube
                    if save_error == True:
                        _thiserr = errCube
                    if save_dq == True:
                        _thisdq = dqCube
            else:
                _thisint = datCube[i]
                if save_error == True:
                    _thiserr = errCube[i]
                if save_dq == True:
                    _thisdq = dqCube[i]
            
            thisHeader=deepcopy(self.head)
            
            if self.flipToDet == True:
                outDat = flip_data(_thisint,self.head,detectorName=self.detectorName)
                thisHeader['FLIP2DET'] = (True,'Flipped to detector coordinates?')
            else:
                outDat = _thisint
                thisHeader['FLIP2DET'] = (False,'Flipped to detector coordinates?')
            
            tmpStr="{:05d}".format(i+self.int_start_num-1)
            outFile = "{}_I{}.fits".format(self.baseName,tmpStr)
            
            ## since we have split the ints, set nints to 1
            thisHeader['NINTS'] = 1
            thisHeader.insert("NINTS",("ON_NINT",i+self.int_start_num,"This is INT of TOT_NINT"),after=True)
            thisHeader.insert("ON_NINT",("TOT_NINT",self.nint_orig,"Total number of NINT in original exposure"),after=True)
            ## This is the number of ints in the file segment, which could be less than the total
            thisHeader.insert("TOT_NINT",("SEGNINT",self.nint,"Total number of NINT in the segment or file"),after=True)
            
            if len(self.times_tab) == self.nint:
                thisHeader.insert("TIME-OBS",("BJDMID",self.times_tab[i]['int_mid_BJD_TDB'],"Mid-integration time (MBJD_TDB)"),after=True)
                thisHeader.insert("BJDMID",("MJDSTART",self.times_tab[i]['int_start_MJD_UTC'],"Int start time (MJD_UTC)"),after=True)
                thisHeader.insert("MJDSTART", ("MJDMIDI",self.times_tab[i]['int_mid_MJD_UTC'],"Int mid time (MJD_UTC)"),after=True)
            
            thisHeader['NINTS'] = 1 # set nint to 1
            thisHeader.insert("NINTS",("NINT",1,"Number of ints"))
            thisHeader["COMMENT"] = 'Extracted from a multi-integration file by splintegrate'
            #thisheader["COMMENT"] = 'splintegrate version {}'.format(__version__)
            outHDU = fits.PrimaryHDU(outDat,header=thisHeader)
            outHDU.name = 'SCI'
            
            outHDUList = fits.HDUList(outHDU)
            
            if save_error == True:
                errHDU = fits.ImageHDU(_thiserr,origHDUList['ERR'].header)
                errHDU.name = 'ERR'
                outHDUList.append(errHDU)
            
            if save_dq == True:
                dqHDU = fits.ImageHDU(_thisdq,origHDUList['DQ'].header)
                dqHDU.name = 'DQ'
                outHDUList.append(dqHDU)
            
            outPath = os.path.join(self.outDir,outFile)
            if (os.path.exists(outPath) & (self.overWrite == False)):
                print("Found {}. Not overwriting".format(outPath))
            else:
                outHDUList.writeto(outPath,overwrite=self.overWrite)
            del outHDUList
        
        origHDUList.close()
        del origHDUList
        

def flip_data(data,head,detectorName=None):
    """ This flips the detector coordinates from DMS to the Fitswriter way
    
    Perhaps using this module will make things easier in the future:
    https://github.com/spacetelescope/jwst/blob/master/jwst/fits_generator/create_dms_data.py
    
    Parameters
    ----------
    data: numpy array
        The input 2D array
    head: astropy.io.fits header
        Original
    
    Returns
    ----------
    """
    ndim = len(data.shape)
    if detectorName is None:
        if 'DETECTOR' not in head:
            raise Exception("Couldn't find detector name to know how to flip")
        else:
            detectorName = head['DETECTOR']
    if detectorName in ['NRCALONG','NRCA1','NRCA3','NRCB2','NRCB4']:
        if ndim == 2:
            return data[:,::-1]
        elif ndim == 3:
            return data[:,:,::-1]
        else:
            raise Exception("Don't know what to do with {} dimensions".format(ndim))
    elif detectorName in ['NRCBLONG','NRCA2','NRCA4','NRCB1','NRCB3']:
        if ndim == 2:
            return data[::-1,:]
        elif ndim == 3:
            return data[:,::-1,:]
        else:
            raise Exception("Don't know what to do with {} dimensions".format(ndim))
    else:
        raise NotImplementedError("Need to add this detector: {}".format(detectorName))

def get_fileList(inFiles):
    """
    Search a file list for a list of files
    
    Parameters
    ----------
    inFiles: str
        A search string (can contain * ) for the files to split
    """
    #self.nFile = len(self.fileList)
    return np.sort(glob.glob(inFiles))

def run_on_multiple(inFiles,**kwargs):
    fileList = get_fileList(inFiles)
    print("Splitting up {} original file(s)".format(len(fileList)))
    
    for oneFile in fileList:
        sp1 = splint(inFile=oneFile,**kwargs)
        
        sp1.split()
    
