Estimate the true number of clusters for k-means clustering using the Cluster Consistency Criterion (CCC).

This algorithm follows the rationale that true cluster centres should be similar in random split-halves of the data. If too maby clusters are specified, the cluster centres will become driven by random sampling error.

The CCC implements this as follows. For each number of clusters, the data are split into random halves for a given number of splits (e.g., 20). For each split, a k-means cluster analysis is run on each half separately. The distances between most-similar cluster centres are summed. The similarity score is e^(-distance_sum). The mean similarity score over random splits is the score for the given number of clusters.

The best estimate of the true number of clusters is determined by where the improvement in score drops off, which occurs when the number of clusters becomes higher than the true number of clusters.

The file test.py gives an example and simulation script. Usage is:

O = teg_CCC.get_best_k_CCC(X)

where X is a 2D array of shape N_Observations x N_Variables. There is an optional argument for max_n_clusters, set to 10 by default. The output is a dictionary with the estimate of true cluster centres (best_n) as well as the similarity score per number of clusters (scores_per_n) and the associated number of clusters (n_vec).
