import copy
import os
import sys

import numpy as np
from npp_materialslab_tools.dic.pydicGrid import grid

from ._pydic_support import (compute_disp_and_remove_rigid_transform,
                             compute_displacement)


class DICProcessorBatch:
    grid_list = [] # saving grid here
    def __init__(self, result_file, 
            interpolation='raw', 
            save_image=True, 
            scale_disp=4., scale_grid=25., 
            strain_type='cauchy', 
            rm_rigid_body_transform=True, 
            meta_info_file=None,
            unit_test_mode:bool = False):
        """* required argument:
        - the first arg 'result_file' must be a result file given by the init() function
        * optional named arguments ;
        - 'interpolation' the allowed vals are 'raw', 'spline', 'linear', 'delaunnay', 'cubic', etc... 
        a good value is 'raw' (for no interpolation) or spline that smooth your data.
        - 'save_image ' is True or False. Here you can choose if you want to save the 'disp', 'grid' and 
        'marker' result images
        - 'scale_disp' is the scale (a float) that allows to amplify the displacement of the 'disp' images
        - 'scale_grid' is the scale (a float) that allows to amplify the 'grid' images
        - 'meta_info_file' is the path to a meta info file. A meta info file is a simple csv file 
        that contains some additional data for each pictures such as time or load values.
        - 'strain_type' should be 'cauchy' '2nd_order' or 'log'. Default value is cauchy (or engineering) strains. You 
        can switch to log or 2nd order strain if you expect high strains. 
        - 'rm_rigid_body_transform' for removing rigid body displacement (default is true)
        """
        self.result_file = result_file
        self.interpolation = interpolation
        self.save_image = save_image
        self.scale_disp = scale_disp
        self.scale_grid = scale_grid
        self.strain_type = strain_type
        self.rm_rigid_body_transform = rm_rigid_body_transform
        self.meta_info_file = meta_info_file
        self.__unit_test_mode = unit_test_mode
        self.meta_info = {}

        if self.meta_info_file:
            self.read_meta_info_file()

    @property
    def grids(self)->list:
        """retuns the grid list. 

        Returns:
            _type_: _description_
        """        
        return self.grid_list
    
    def process_data(self):
        """main function for processing files
        """        
        self.grid_list = [] # saving grid here
        
        # read dic result file
        self.read_result_file()
        # compute displacement and strain
        for i, mygrid in enumerate(self.grid_list):
            self._process_single_grid(i, mygrid)
            # write image files
            if (self.save_image):
                self.write_image_files(mygrid)

            if not self.__unit_test_mode:
                # write result file
                mygrid.write_result()

            # add meta info to grid if it exists
            self.add_metadata_to_grid_object(mygrid)

    def add_metadata_to_grid_object(self, mygrid):
        """Adds metadata to grid object.

        Args:
            mygrid (_type_): _description_
        """        
        if (len(self.meta_info) > 0):
            img = os.path.basename(mygrid.image)
                #if not meta_info.has_key(img):
            if img not in self.meta_info.keys():
                print("warning, can't affect meta deta for image", img)
            else:
                mygrid.add_meta_info(self.meta_info.get(img))
                print('add meta info', self.meta_info.get(img))

    def write_image_files(self, mygrid):
        """write timage files (marked, displacement, grid)

        Args:
            mygrid (_type_): _description_
        """        
        win_size_x, win_size_y = self.win_size[0], self.win_size[1]
        mygrid.draw_marker_img()
        mygrid.draw_disp_img(self.scale_disp)
        mygrid.draw_grid_img(self.scale_grid)
        if win_size_x == 1 and win_size_y == 1 : 
            mygrid.draw_disp_hsv_img()

    def _process_single_grid(self, i:int, mygrid:grid):
        """_summary_

        Args:
            i (int): _description_
            mygrid (grid): I could use self.grid_list[i] instead of mygrid
        """        
        print("compute displacement and strain field of", self.image_list[i], "...")
        disp = None
        if self.rm_rigid_body_transform:
            print("remove rigid body transform")
            disp = compute_disp_and_remove_rigid_transform(self.point_list[i], self.point_list[0])
        else:
            print("do not remove rigid body transform")
            disp = compute_displacement(self.point_list[i], self.point_list[0])
        mygrid.add_raw_data(self.win_size, self.image_list[0], self.image_list[i], self.point_list[0], self.point_list[i], disp)
        
        self.disp_list.append(disp)
        mygrid.interpolate_displacement(self.point_list[0], disp, method=self.interpolation)

        if (self.strain_type == 'cauchy'):
            mygrid.compute_strain_field()
        elif (self.strain_type =='2nd_order'):
            mygrid.compute_strain_field_DA()
        elif (self.strain_type =='log'):
            mygrid.compute_strain_field_log()
        else:
            print("please specify a correct strain_type : 'cauchy', '2nd_order' or 'log'")
            print("exiting...")
            sys.exit(0)

    def plot_strain_map_with_id(self, id, strain_type:str):
        assert (id < len(self.grid_list) and id>0),  "id does not correspond to an image" 
        assert strain_type in ['xx', 'yy', 'xy'], "strain type should be one of ['xx', 'yy', 'xy']"
        tmp_grid = self.grid_list[id]
        if strain_type == 'xx':
            tmp_grid.plot_field(tmp_grid.strain_xx, 'xx strain')
        elif strain_type == 'yy':
            tmp_grid.plot_field(tmp_grid.strain_yy, 'yy strain')
        elif strain_type == 'xy':
            tmp_grid.plot_field(tmp_grid.strain_xy, 'xy strain')
        
    def read_meta_info_file(self):
        """ Read the meta info file and store the information in the meta_info dictionary.

        This function reads the meta info file specified by the `self.meta_info_file` attribute. The file
        should be in CSV format, with the first row as the header containing field names. The following
        rows should contain values corresponding to the field names. The function parses the file and
        stores the information in the `self.meta_info` dictionary, with the first value in each row as
        the key and the rest of the values as a dictionary.

        Example of meta info file format:
            time, load
            img_001, 0.1, 500
            img_002, 0.2, 520
            img_003, 0.3, 550

        The resulting self.meta_info dictionary will look like:
            {
                "img_001": {"time": 0.1, "load": 500},
                "img_002": {"time": 0.2, "load": 520},
                "img_003": {"time": 0.3, "load": 550},
            }
        """
        print('read meta info file', self.meta_info_file, '...')
        with open(self.meta_info_file) as f:
            lines = f.readlines()
            header = lines[0]
            field = header.split()
            for l in lines[1:-1]:
                val = l.split()
                if len(val) > 1:
                    dictionary = dict(zip(field, val))
                    self.meta_info[val[0]] = dictionary

    def read_result_file(self):
        """ Read the result file and extract the grid, point_list, image_list, and disp_list.

        This method reads the result file provided by the user, parses the contents of the file,
        and extracts the grid parameters, point_list, image_list, and disp_list from it. The
        extracted data is then stored as instance variables of the class for further processing.

        Args:
            self (object): The instance of the class for which the method is called.

        Attributes:
            win_size (tuple): A tuple containing the dimensions of the window size (win_size_x, win_size_y).
            point_list (list): A list of arrays containing the points extracted from the result file.
            image_list (list): A list of image names (strings) extracted from the result file.
            disp_list (list): A list of displacement values extracted from the result file.
            grid_list (list): A list of grids created from the parsed result file.

        """
        # first read grid
        with open(self.result_file) as f:
            head = f.readlines()[0:2]
        (xmin, xmax, xnum, win_size_x) = [float(x) for x in head[0].split()]
        (ymin, ymax, ynum, win_size_y) = [float(x) for x in head[1].split()]
        self.win_size = (win_size_x, win_size_y)
        
        grid_x, grid_y = np.mgrid[xmin:xmax:int(xnum)*1j, ymin:ymax:int(ynum)*1j]
        mygrid = grid(grid_x, grid_y, int(xnum), int(ynum))

        # the results
        self.point_list = []
        self.image_list = []
        self.disp_list = []

        # parse the result file
        with open(self.result_file) as f:
            res = f.readlines()[2:-1]
            for line in res:
                val = line.split('\t')
                self.image_list.append(val[0])
                point = []
                for pair in val[1:-1]:
                        (x,y) = [float(x) for x in pair.split(',')]
                        point.append(np.array([np.float32(x),np.float32(y)]))
                self.point_list.append(np.array(point))
                self.grid_list.append(copy.deepcopy(mygrid))
        f.close()