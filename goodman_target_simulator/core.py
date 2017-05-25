#!/usr/bin/env python 
# -*- coding: utf8 -*-
"""


"""
from __future__ import absolute_import, division, print_function

import matplotlib as mpl
mpl.use('TkAgg')

import astropy.io.fits as pyfits
import numpy as np
import matplotlib.pyplot as plt
import pkg_resources

from astropy.modeling import models

__author__ = 'Bruno Quint'

class GoodmanTargetSimulator:

    pixel_scale = 0.15 # arcsec / pix

    def __init__(self,
                 filename=None,
                 targets_pos=[1000],
                 targets_int=[1.],
                 seeing=1.,
                 snr=1.,
                 show=False):
        """
        Parameters
        ----------
            filename (str) :
            targets_pos (indexable) :
            targets_int (indexable) :
            seeing (float) :
            snr (float) :
        """
        self.filename = filename
        self.targets_pos = targets_pos
        self.targets_int = targets_int
        self.seeing = seeing
        self.snr = snr
        self.show = show

    def run(self):

        # Convert the seeing measured in full-width at half maximum to stddev
        # and, then, from arcseconds to unbinned pixels.
        seeing = self.arcsec2px(self.seeing / 2.335)

        # Create the models
        my_models = models.Const1D(0)
        for (i, p)  in enumerate(self.targets_pos):
            peak_index = p
            peak_value = self.targets_int[i]
            my_models += models.Gaussian1D(mean=peak_index,
                                           amplitude=peak_value, stddev=seeing)

        # Get header
        h = self.goodman_header()

        # Create 1D data
        height = h['NAXIS2']
        x = np.arange(height)
        y = my_models(x)

        # From 1D to 2D
        width = h['NAXIS1']
        y = np.reshape(y, (1, height, 1))
        y = np.repeat(y, width, axis=2)

        # Create noise
        noise = np.random.randn(1, height, width) \
                * max(self.targets_int) / self.snr
        y += noise

        if self.show:
            self.display_results(y)

        # Write output file
        pyfits.writeto(self.filename, y, h, overwrite=True)


    def arcsec2px(self, x):
        """
        Return x in pixels.

        Parameters
        ----------
            x (float) : a value in arcseconds.

        Returns
        ------
            y (float) : the same value in number of pixels
        """
        return x / self.pixel_scale

    def display_results(self, data):
        """
        Simply display the resulting image.

        Parameters
        ----------
            data (ndarray) : 2D Array containinng the results.
        """
        fig, axs = plt.subplots(1, 1)

        axs.imshow(
            data[0], origin='lower', interpolation='nearest', cmap='Blues')

        axs.set_title(
            "Simulated Gaussians with SNR = {:.1f}".format(self.snr))

        axs.set_xlim(0, data.shape[2])
        axs.set_ylim(0, data.shape[1])
        axs.set_ylabel('Spatial direction [px]')
        axs.set_xlabel('Spectral direction [px]')

        plt.show()

    @staticmethod
    def goodman_header(camera=0):
        """
        Get a sample of the Goodman Header.

        Parameters
        ----------
            camera (int) : an index representing which camera to be taken as
            example - 0: Old blue camera, 1: New blue camera, 2: Red camera.

        Returns
        -------
            h (astropy.io.fits.Header) : a sample instance of the header.
        """

        # Select what is the source of the data
        if camera == 0:
            filename = 'sample_data/sample_blue_camera.fits'
        elif camera == 1:
            raise NotImplemented(
                "I don't have a sample for the new blue camera yet.")
        elif camera == 2:
            raise NotImplemented("I don't have a sample for the red camera yet.")

        # Read and deliver header
        filename = pkg_resources.resource_filename(
            'goodman_target_simulator', filename)
        h = pyfits.getheader(filename)

        for key in h.keys():
            if 'PARAM' in key:
                del h[key]

        return h


if __name__ == '__main__':
    gts = GoodmanTargetSimulator(
        filename="dummy.fits",
        targets_pos=[1000, 1500],
        targets_int=[10., 5],
        seeing=1.,
        snr=100,
        show=True
    )
    gts.run()