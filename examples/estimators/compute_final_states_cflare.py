# -*- coding: utf-8 -*-
"""
Compute final states using CFLARE
---------------------------------

This examples show how to compute and plot final states using :class:`cellrank.tl.estimators.CFLARE`.
"""

import cellrank as cr

adata = cr.datasets.pancreas_preprocessed("../example.h5ad")
adata

# %%
# First, let us prepare the kernel using high-level pipeline and the :class:`cellrank.tl.estimators.CFLARE` estimator.
k = cr.tl.transition_matrix(
    adata, weight_connectivities=0.2, softmax_scale=4, show_progress_bar=False
)
g = cr.tl.estimators.CFLARE(k)

# %%
# Next, we need to compute the eigendecomposition of the transition matrix. By default we compute 20 left and right
# eigenvectors corresponding to the first 20 largest eigenvalues, sorted by their real part.
g.compute_eigendecomposition(k=20)

# %%
# For :class:`cellrank.tl.estimators.CFLARE`, there are 2 methods of how to choose the final states:
#
#     1. :meth:`cellrank.tl.estimators.CFLARE.set_final_states`
#     2. :meth:`cellrank.tl.estimators.CFLARE.compute_final_states`
#
# After successfully setting or compute the final states, we can compute the absorption probabilities,
# as shown here :ref:`sphx_glr_auto_examples_estimators_compute_abs_probs.py`.

# %%
# Set final states
# ^^^^^^^^^^^^^^^^
# :meth:`cellrank.tl.estimators.CFLARE.set_final_states` simply sets the final states manually - this
# can be useful if the final states are known beforehand.
#
# The states can be specified either as a categorical :class:`pandas.Series` where `NaN` values mark cells
# not belonging to any final state or a :class:`dict`, where keys correspond the names of the final states,
# and the values to the sequence of cell names or their indices.
#
# Below we set the final state called `'Alpha'` as all the cells from the `'Alpha``
# cluster under ``adata.obs['clusters']``.
g.set_final_states({"Alpha": adata[adata.obs["clusters"] == "Alpha"].obs_names})

# %%
# Compute final states
# ^^^^^^^^^^^^^^^^^^^^
# :meth:`cellrank.tl.estimators.CFLARE.compute_final_states` uses the previously computed left eigenvectors to obtain
# the recurrent states the right eigenvectors to do the clustering. For clustering, 3 options are available: `'kmeans'`,
# `'louvain'` or `'leiden'`. By default, we're only considering vectors based on the `eigengap`.
#
# As in :ref:`sphx_glr_auto_examples_estimators_compute_final_states_gpcca.py`., we can specify ``cluster_key``,
# which allows us to match the cluster labels stored under that key with the final states of the process.
# However, for :class:`cellrank.tl.estimators.CFLARE`, we have no way of controlling how many cells will be in each
# final state.
g.compute_final_states(method="kmeans", n_clusters_kmeans=3, cluster_key="clusters")

# %%
# Now that the final states have been either set or computed, we can visualize them in an embedding.
# All of the options seen in :ref:`sphx_glr_auto_examples_estimators_compute_metastable_states.py` also apply here -
# we can plot the final states in one plot or separately (parameter ``same_plot=``) but unlike
# in :ref:`sphx_glr_auto_examples_estimators_compute_final_states_gpcca.py`, we cannot plot the membership degrees,
# because they are nonexistent.

g.plot_final_states(same_plot=False)

# %%
# In general, we recommend :class:`cellrank.tl.estimators.GPCCA` to compute the final states. For more information,
# see here :ref:`sphx_glr_auto_examples_estimators_compute_final_states_gpcca.py`.
