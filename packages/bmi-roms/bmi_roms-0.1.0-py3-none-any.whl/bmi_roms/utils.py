# -*- coding: utf-8 -*-
import os
import xarray as xr
import numpy as np
from datetime import datetime

from .errors import DataError


class RomsData:

    """Access data and metadata in a ROMS data file."""

    def __init__(self, filename=None, download=False):
        """Make a RomsData object.
        Parameters
        ----------
        filename : str, optional
            Path or URL (e.g., OPeNDAP data url) to the file to open.

        download : bool, optional
            Indicate whether to download and save the data as a netCDF file with the provided URL
        """

        self._filename = None
        self._data = None
        self._var_list = None
        self._grid_list = None
        self._var_info = None
        self._grid_info = None
        self._time_info = None
        self._dim_info = None
        self._download_file = None

        if filename is not None:
            self.open(filename, download)

    @property
    def data(self):
        return self._data

    @property
    def filename(self):
        return self._filename

    @property
    def grid_info(self):
        return self._grid_info

    @property
    def dim_info(self):
        return self._dim_info

    @property
    def var_info(self):
        return self._var_info

    @property
    def time_info(self):
        return self._time_info

    @property
    def download_file(self):
        return self._download_file

    def open(self, filename, download=False):

        """Load a ROMS data file into a xarray DataArray.
        Parameters.
        ----------
        filename : str
            Path or URL to the file to open.

        download : bool
            Indicate whether to download and save the data as a netCDF file with the provided URL

        """
        # load data
        self._filename = filename
        self._data = xr.open_dataset(self._filename, decode_cf=False)

        # save data
        if download:
            if not os.path.isfile(filename):
                time_info = datetime.now().strftime('%d%m%YT%H%M%S')
                file_name = 'romsdata_{}.nc'.format(time_info)
                file_path = os.path.join(os.getcwd(), file_name)
                self._data.to_netcdf(file_path)
                self._download_file = file_path

        # get var and grid list
        self._get_var_grid_list()

        return self.data

    def get_grid_info(self):
        if self._filename is not None:
            # get dim info
            dim_info = self._get_dim_info()

            # get grid info
            try:
                grid_info = {}
                for index, dim in enumerate(self._grid_list):
                    if len(dim) > 1:  # suppose dim is 2-3D (exclude time dim)
                        x_name = dim[-1]
                        y_name = dim[-2]
                        z_name = dim[-3] if len(dim) > 2 else None

                        grid_info[index] = {

                            'type': "rectilinear",
                            'shape': tuple([self.data.dims[dim_name] for dim_name in dim]),
                            'grid_spacing': (dim_info[y_name]['spacing_y'], dim_info[x_name]['spacing_x']) if z_name is None else
                                            (dim_info[z_name]['spacing_z'], dim_info[y_name]['spacing_y'],
                                             dim_info[x_name]['spacing_x']),
                            'grid_origin': (dim_info[y_name]['origin_y'], dim_info[x_name]['origin_x']) if z_name is None else
                                           (dim_info[z_name]['origin_z'], dim_info[y_name]['origin_y'],
                                            dim_info[x_name]['origin_x']),
                            'grid_x': dim_info[x_name]['grid_x'],
                            'grid_y': dim_info[y_name]['grid_y'],
                            'grid_z': dim_info[z_name]['grid_z'] if z_name is not None else 0,
                        }
                    elif len(dim) == 1:
                        pass  # TODO support scalar value (1D)

                self._grid_info = grid_info

            except Exception:
                raise DataError('Failed to get the grid information for {} from the dataset.'.format(dim))

        return self.grid_info

    def get_time_info(self):
        if self._filename is not None:
            try:
                # identify time dim name and suppose there is only one time dimension used for all variables
                if self._time_list:
                    time_name = set(self._time_list).pop()
                else:
                    time_name = 'ocean_time'

                # time values are float in BMI time function
                time_var = self._data.coords[time_name]
                time_info = {
                    'start_time': float(time_var.values[0]),
                    'time_step': 0.0 if len(time_var.values) == 1 else
                    float(time_var.values[1] - time_var.values[0]),
                    'end_time': float(time_var.values[-1]),
                    'total_steps': len(time_var.values),
                    'time_units': time_var.units,
                    'calendar': time_var.calendar,
                    'time_value': time_var.values.astype('float'),
                }

                self._time_info = time_info

            except Exception:
                raise DataError('Failed to get the time information from the dataset.')

        return self.time_info

    def get_var_info(self):
        if self._filename is not None:
            var_info = {}
            try:
                for var_name, grid_id in self._var_list:
                    var = self._data.data_vars[var_name]
                    var_info[var.long_name] = {
                        'var_name': var_name,
                        'dtype':  str(var.dtype),
                        'itemsize': var.values.itemsize,
                        'nbytes': var.values[0].nbytes if len(var.dims) >= 3 else var.values.nbytes,  # current time step nbytes
                        'units': var.units if 'units' in var.attrs else 'N/A',
                        'location': 'node',
                        'grid_id': grid_id,
                    }

                self._var_info = var_info

            except Exception:
                raise DataError('Failed to get the variable information for {} from the dataset.'.format(var_name))

        return self.var_info

    def _get_var_grid_list(self):
        if self._filename is not None:
            var_list = []
            grid_list = []
            time_list = []

            # get var, grid, and time list
            for var_name in self._data.data_vars.keys():
                var_obj = self._data.data_vars[var_name]

                if len(var_obj.shape) in [3, 4]:  # get var with 3-4 dims
                    var_list.append(var_name)
                    var_dims = var_obj.dims[1:]
                    if var_dims not in grid_list:
                        grid_list.append(var_dims)
                    time_list.append(var_obj.dims[0])

                elif len(var_obj.shape) == 2:
                    var_dims = var_obj.dims
                    dim_names = [name.split('_')[0] for name in var_dims]
                    if dim_names == ['eta', 'xi']:  # var with 2 dims and defined with geolocation
                        var_list.append(var_name)
                        if var_dims not in grid_list:
                            grid_list.append(var_dims)

                # elif len(var_obj.shape) == 1: #TODO support scalar value
                #     var_list.append(var_name)
                #     if 'scalar' not in grid_list:
                #         grid_list.append('scalar')

            # assign grid id to var list
            for index, var_name in enumerate(var_list):
                var_obj = self._data.data_vars[var_name]
                var_dims = var_obj.dims if len(var_obj.shape) == 2 else var_obj.dims[1:]
                var_list[index] = [var_name, grid_list.index(var_dims)]

            self._grid_list = tuple(grid_list)
            self._var_list = tuple(var_list)
            self._time_list = tuple(time_list)

    def _get_dim_info(self):
        # get unique dim names
        dim_list = list(set([item for sublist in self._grid_list for item in sublist]))

        # get dim info
        if dim_list:
            dim_info = {}
            for dim_name in dim_list:
                if 's_' in dim_name:
                    grid_z = np.arange(0, self._data.dims[dim_name], dtype=float)  # value represent layer index number
                    dim_info[dim_name] = {
                        'grid_z': grid_z,
                        'origin_z': grid_z[0],
                        'spacing_z': 1.0,
                    }

                elif 'xi_' in dim_name:
                    if dim_name.replace('xi', 'x') in self._data.data_vars.keys():
                        coor_var = dim_name.replace('xi', 'x')
                        grid_x = self._data.data_vars[coor_var].values[0, :]
                        dim_info[dim_name] = {
                            'grid_x': grid_x,
                            'origin_x': grid_x[0],
                            'spacing_x': grid_x[1] - grid_x[0],
                        }
                    elif dim_name.replace('xi', 'lon') in self._data.data_vars.keys():
                        coor_var = dim_name.replace('xi', 'lon')
                        grid_x = np.arange(0, self._data.data_vars[coor_var].shape[1], dtype=float)  # index value
                        dim_info[dim_name] = {
                            'grid_x': grid_x,
                            'origin_x': grid_x[0],
                            'spacing_x': 1.0,
                        }

                elif 'eta_' in dim_name:
                    if dim_name.replace('eta', 'y') in self._data.data_vars.keys():
                        coor_var = dim_name.replace('eta', 'y')
                        grid_y = self._data.data_vars[coor_var].values[:, 0]
                        dim_info[dim_name] = {
                            'grid_y': grid_y,
                            'origin_y': grid_y[0],
                            'spacing_y': grid_y[1] - grid_y[0],
                        }

                    elif dim_name.replace('eta', 'lat') in self._data.data_vars.keys():
                        coor_var = dim_name.replace('eta', 'lat')
                        grid_y = np.arange(0, self._data.data_vars[coor_var].shape[0], dtype=float)  # index value
                        dim_info[dim_name] = {
                            'grid_y': grid_y,
                            'origin_y': grid_y[0],
                            'spacing_y': 1.0,
                        }

                elif 'Nbed' == dim_name:
                    grid_z = np.arange(0, self._data.dims['Nbed'], dtype=float)
                    dim_info[dim_name] = {
                        'grid_z': grid_z,  # value represent layer index number
                        'origin_z': grid_z[0],
                        'spacing_z': 1.0,
                    }

            self._dim_info = dim_info

        else:
            raise DataError('Failed to get the dimension information from the dataset.')

        return self.dim_info


