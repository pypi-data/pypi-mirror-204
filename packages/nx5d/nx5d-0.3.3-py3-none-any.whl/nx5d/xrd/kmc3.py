#!/usr/bin/python3

#
#        nx5d - The NX5 Duct Tape
#        Copyright (C) 2022-2023 Florin Boariu
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        (at your option) any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

#from xrayutilities.io.spec import SPECFile

from silx.io.spech5 import SpecH5, SpecH5LazyNodeDataset, SpecH5NodeDataset
from silx.io.commonh5 import Group as H5Group, SoftLink as H5SoftLink
from h5py import File as H5File
from os import path
import tifffile
import numpy as np

'''
Provides a series of objects to mock an "ESRF dialect" of a HDF5-based Nexus
data file for X-ray diffraction experiments that are usable with `source.DataSource.

The "ESRF dialect" is essentially this:

  - There is 1D or 2D detector data ("images" or "frames").

  - The data is organized in "scans", i.e. images are oranized in series.
    One scan typically consists of several images with the same hard characteristics
    (i.e. same geometry), but taken under systematically differing external parameters:
    e.g. by "scanning" one or several parameter devices (angle? time delay?) and
    obtaining an image at each of the scan points.

  - The data format where the images are stored is a 3-dimensional block of NxWxH,
    where 'WxH' is the width/height of one frame, and 'N' is the number of frames
    in a scan. For a scan performed along a single paramter, each subsequent frame
    corresponds to a different parameter instance; for a scan taken along 2 parameters
    (e.g. inside a 2D parameter space), the scans are interleaved: there are actually
    (n*m)xWxH frames. This is still a 3D dataset with images of geometry WxH, but
    the first "chunk" of 'n' images are scanned along the first paramter and a specific
    'm' value (i.e. all have the same 'm'), the next chunk is scanned again along the
    whole N space but for a different 'm', and so on.

  - Besides detector data, there are also associated metadata -- e.g. the parameter
    arrays along which the scans took place. These are also Nx(...) data sets; in the
    simplest cases, they are 2D (parameter is scalar).

  - The both detector data and scan metadata are stored at specific "paths" within
    the data container. In HDF5 terminology, this is the literal HDF5 path within
    the file (e.g. "data/rayonix/detector"). We don't make any assumptions about
    the tree organisation (yes, typically it follows NX data format rules, but...).

  - A data container (i.e. a "file") can contain one or several scans. Each scan
    has a top-level subdirectory of its own.

  - Beyond data series (detector and metadata), there can also exist single scalar
    values setting the state for the entire experiment (e.g. "photon_energy", or
    "center_pixel", ...).

  - [FIXME: haven't decided yet whether top-level scalar metadata still needs to
    be embedded into a scan (i.e. is per-scan only), or can also be at the very
    top. I think ESRF has the former...]

The `source.DataSource` essentially uses the following HDF5 API elements:

  - Accessing of data using slicers and the indexing operator (`__getitem__`).

  - `__getitem__` access works both for selecting paths / subpaths, or selecting
    data containers within paths, or slicing parts of the data container itself,
    i.e. sub-access to limited parts of the images (i.e. only specific
    region-of-interests) via slicing. Examples:
    ```
      data["detector"] -> directory containing the "acme" subdirectory

      data["detector/acme"] -> directory, containing the "images" dataset
      data["detector"]["acme"] -> same as above

      data["detector/acme/images"] -> the dataset itself
      data["detector"]["acme"]["images"] -> same as above

      data["detector/acme/images"][3] -> image no. 3 from the dataset

      data["detector/acme/images"][3][60:160,60:160] -> a 100x100 pixel area centered
                                                        around pixel 110x110 of image no. 3

    ```

  - The HDF5 taxonomy (i.e. the '.attrs' dictionary

  - We're not using any HDF5 specific properties or Python attributes.

'''

'''
Experiment configuration template to use with `nx5d.xrd.data.ExperimentSetup`.
Contains goniometer and detector layout for the Pilatus detector, as well
as HDF5 addresses for the goniometer and detector angles.
'''
ExperimentTemplate = {
    "goniometerAxes": ('x+', 'y+', 'z+'),
    
    "detectorTARAxes": ("x+", None, None),
    
    "imageAxes": ("x-", "z-"),
    "imageSize": (195, 487),
    "imageCenter": (90, 245),

    # This could also be used instead of 'imageChannelSize' below.
    # It's the same physical quantity, but in degrees/channel
    # instead of relative length.
    "imageChannelSpan": None,

    "imageDistance": "@{positioners}/PilatusYOffset",
    "imageChannelSize": (0.172, 0.172), # same unit as imageDistance (mm)
    
    "sampleFaceUp": 'z+',
    "beamDirection": (0, 1, 0),
    
    "sampleNormal": (0, 0, 1),
    
    "beamEnergy": "@{positioners}/monoE",

    "goniometerAngles": {
        'theta': "@{positioners}/Theta",
        'chi':   "@{positioners}/Chi",
        'phi':   "@{positioners}/Phi" },

    "detectorTARAngles": {
        'azimuth': "@{positioners}/TwoTheta",
    }
}

class SpecH5LazyTiffNode(SpecH5LazyNodeDataset):
    '''
    Implements a NodeDataset that lazily loads a list of TIFF files,
    specified as a path format that relies on an index variable.
    '''
    def __init__(self, *args, tiffPathFmt="{frameidx}.tiff", numFrames=0, **kwargs):
        super().__init__(*args, **kwargs)
        self._tiff_path_fmt = tiffPathFmt
        self._tiff_frames_no = int(numFrames)


    def _create_data(self):
        #data = []
        #for i in range(self._tiff_frames_no):
        #    data.append( tifffile.imread(self._tiff_path_fmt.format(frameidx=i)) )
        #return np.array(data)
        return np.array([tifffile.imread(self._tiff_path_fmt.format(frameidx=i)) \
                         for i in range(self._tiff_frames_no)])


    def __getitem__(self, item):
        '''
        Apparently we can optimize this so that only a single file is
        loaded if not already initialized (...so we don't have to load
        the whole bunch for single-frame access). In that case, `item`
        is the index of the file, and all we have to do is plug it
        into the name formatter.

        OTOH the ESRF H5 library is slow af in specific instances (e.g.
        when doing itermittend slicing a 3D dataset from HDF5.) Not sure if
        this is a problem of HDF5 or of some ESRF trickery. So we might keep
        an eye on this (...in case it's something like this).
        '''
        if not self._is_initialized: 
            try:            
                idx = None
                slc = None
                if isinstance(item, int):
                    idx = item
                    slc = None
                else:
                    idx, slc = item
                    assert isinstance(idx, int)

                # Access the frame from 'idx'
                p = self._tiff_path_fmt.format(index=item)
                frame = np.array([tifffile.imread(p)])

                # ...and possibly a sub-slice ('None' is the same as [:])
                return frame[slc]

            except:
                pass

        return super().__getitem__(item)

    

class SpecTiffH5(SpecH5):
    '''
    Mocks a HDF5 file using the Spec H5 module from Silx.

    In addition the "regular" `slix.io.spech5.SpecH5` functionality, after loading the
    SPEC file, this module also injects lazy-loading nodes for the TIFF files
    correspondng to a typical KMC3 setup.
    '''

    def __init__(self, *args, instrumentName="pilatus",
                 framePathFmt='{dirname}/{instr}/S{scannr:05}/{basename}_{scannr}_{frameidx}.tif',
                 **kwargs):
        '''
        Parameters:

          - `instrument`: A name/label for the instrument. For one, this is used to compile
            the location of where to insert the data from the external TIFF files (as
            specified by `tiffInsertFmt` and `tiffLinkFmt`); for another, this is used
            to determine the location of the TIFF files on disk relative to the
            SPEC file (as specified by `scanPathFmt`).
        
          - `framePathFmt`: format for the image scan filepath.

          - `scanIndexNameFmt`: string formatting that ties the scan number (on disk)
            and scan name (in teh SpecH5 naming) together.

         All string formatters can make use of any or all of the following variables:
        
           - `{dirname}`: folder-only component of the spec file name
        
           - `{basename}`: base name the SPEC file, with the last component after a dot
             (typically ".spec" removed

           - `{scannr}`: scan number; this is typically an integer, assigned by "the
             algorithm", and typically starting with 1 for the first scan

           - `{scanidx}`: scan index; this is an integer starting with 0 and designating
             the cosecutive index value of the scan.

           - `{frameidx}`: the index (starting with 0) of the frame being processed
             (i.e. the TIFF file).

        In addition to the explicit parameters, we also use the following positional
        parameters from `args`:

           - `filename` (position 0): the path of the SPEC file to read
        
        '''
        super().__init__(*args, **kwargs)
        
        self._specBaseName = '.'.join(path.basename(self.filename).split('.')[:-1]) \
            or path.base(self.filename)
        self._specDirName = path.abspath(path.dirname(self.filename))

        for scanName in self.keys():
            
            scan = self[scanName]
            scanNr, foo = scanName.split('.')

            tiffPartialFmt = framePathFmt.format(**{
                "basename": self._specBaseName,
                "dirname": self._specDirName,
                "scannr": int(scanNr),
                "instr": instrumentName,
                "scanidx": "{scanidx}",
                "frameidx": "{frameidx}"
            })
            
            self._adopt_scan(scan, instrumentName, tiffPartialFmt)

            self._enter_cnt = 0
            self._enter_data = None


    def __enter__(self, *args, **kwargs):
        '''
        Opening / closing a SpecTiffH5 is pretty expensive. We usually want to
        employ with-guards (enter/exit) when doing that, but the original SpecH5
        does not support "nested" guards (i.e. entering/exitting multiple
        times on the same object).

        This is an extension to do just that. (Need to check if h5py.File supports
        this... the original Python open() / file object definitely does.)
        '''
        if self._enter_cnt == 0:
            self._enter_data = super().__enter__(*args, **kwargs)
        self._enter_cnt += 1
        return self._enter_data


    def __exit__(self, *args, **kwargs):
        if self._enter_cnt > 0:
            self._enter_cnt -= 1
        if self._enter_cnt == 0:
            super().__exit__(*args, **kwargs)


    def _adopt_scan(self, scanObj, instrumentName, tiffFormat):

        measRoot = scanObj['measurement']
        instrRoot = scanObj['instrument']
        posnrs = instrRoot['positioners']
        

        # Let's hope they're all the same... :-)
        numFrames = 0
        #print("Positioners:", posnrs.keys())
        for p in posnrs.keys():
            #print("Positioner:", p, "length", posnrs[p].size)
            numFrames = max(numFrames, posnrs[p].size)

        # place data inside "instrument/<name>/data"
        instrRoot.add_node(H5Group(parent=instrRoot, name=instrumentName,
                                   attrs={'NX_class': 'NXinstrument'} ))
        instrObj = instrRoot[instrumentName]

        instrObj.add_node(SpecH5LazyTiffNode(tiffPathFmt=tiffFormat,
                                             numFrames=numFrames,
                                             name="data",
                                             parent=instrObj))

        # create a link inside "measurement" that points to "instrument/<name>/data"
        link_target = instrObj.name.replace('measurement', 'instrument')
        measRoot.add_node(H5SoftLink(name=instrumentName,
                                     path=link_target + "/data",
                                     parent=measRoot))

        
def test_kmc3nx():
    
    k = Kmc3NxMocker(specFile="/var/home/specuser/tmp/nxdata/231-cw7-12083-roessle.spc/"
                     "231-cw7-12083-roessle.spec", scanNr=3)

    for f in k.dataFiles:
        assert path.isfile(f)
