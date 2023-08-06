import numpy as np
import pandas as pd
import scanpy as sc

from starfysh import LOGGER
from .utils import (get_adata_wsig,
                    get_windowed_library,
                    get_sig_mean,
                    znorm_sigs,
                    get_anchor_spots,
                    get_alpha_min
                   )


class VisiumArguments:
    """
    Loading Visium AnnData, perform preprocessing, library-size smoothing & Anchor spot detection

    Parameters
    ----------
    adata : AnnData
        annotated visium count matrix

    adata_norm : AnnData
        annotated visium count matrix after normalization & log-transform

    gene_sig : pd.DataFrame
        list of signature genes for each cell type. (dim: [S, Cell_type])

    map_info : pd.DataFrame
        Spatial information of histology image paired with visium
    """

    def __init__(
        self,
        adata,
        adata_norm,
        gene_sig,
        map_info,
        img=None,
        **kwargs
    ):

        self.adata = adata
        self.adata_norm = adata_norm
        self.gene_sig = gene_sig
        self.img = img
        self.map_info = map_info

        self.params = {
            'n_anchors': 60,
            'patch_r': 13,
            'vlow': 10,
            'vhigh': 95,
            'window_size': 30,
            'z_axis': 0
        }

        # Update parameters for library smoothing & anchor spot identification
        for k, v in kwargs.items():
            if k in self.params.keys():
                self.params[k] = v

        # Filter out signature genes X listed in expression matrix
        LOGGER.info('Filtering signatures not highly variable...')
        self.adata = get_adata_wsig(adata, gene_sig)
        self.adata_norm = get_adata_wsig(adata_norm, gene_sig)

        # Get smoothed library size
        LOGGER.info('Smoothing library size by taking averaging with neighbor spots...')
        log_lib = np.log1p(self.adata.X.sum(1))
        self.log_lib = np.squeeze(np.asarray(log_lib)) if log_lib.ndim > 1 else log_lib
        self.win_loglib = get_windowed_library(self.adata,
                                               map_info,
                                               self.log_lib,
                                               window_size=self.params['window_size']
                                              )

        # Retrieve & Z-norm signature gexp
        LOGGER.info('Retrieving & normalizing signature gene expressions...')
        self.sig_mean = get_sig_mean(self.adata,
                                     gene_sig,
                                     self.log_lib)
        self.sig_mean_znorm = znorm_sigs(self.sig_mean, z_axis=self.params['z_axis'])

        # Get anchor spots
        LOGGER.info('Identifying anchor spots (highly expression of specific cell-type signatures)...')
        anchor_info = get_anchor_spots(self.adata,
                                       self.sig_mean_znorm,
                                       v_low=self.params['vlow'],
                                       v_high=self.params['vhigh'],
                                       n_anchor=self.params['n_anchors']
                                      )
        self.pure_spots, self.pure_dict, self.pure_idx = anchor_info
        self.alpha_min = get_alpha_min(self.sig_mean, self.pure_dict) # Calculate alpha mean

    def get_adata(self):
        """Return adata after preprocessing & HVG gene selection"""
        return self.adata, self.adata_norm

    def get_anchors(self):
        """Return indices of anchor spots for each cell type"""
        anchors_df = pd.DataFrame.from_dict(self.pure_dict, orient='columns')
        return anchors_df.applymap(
            lambda x:
            np.where(self.adata.obs.index == x)[0][0] # TODO: make sure adata.obs index is formatted as "location_i"
        )