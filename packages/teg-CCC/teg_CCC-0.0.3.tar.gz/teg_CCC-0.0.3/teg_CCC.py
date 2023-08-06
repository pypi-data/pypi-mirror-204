import numpy as np
from sklearn.cluster import KMeans

def get_kmeans(Xsub, n_clusters):
    km = KMeans(n_clusters=n_clusters, random_state=0, n_init="auto").fit(Xsub)
    return km.cluster_centers_

def get_sim_centres(centres1, centres2):
    distances = []
    for ic1 in range(centres1.shape[0]):
        newrow = []
        for ic2 in range(centres2.shape[0]):
            dv = centres1[ic1] - centres2[ic2]
            d = np.sqrt(np.sum(dv**2))
            newrow.append(d)
        distances.append(newrow)
    D = np.array(distances)
    dist_per_cluster = []
    for ic1 in range(D.shape[0]):
        v = D[ic1, :]
        i_closest = np.argmin(v)
        dist_per_cluster.append(v[i_closest])
        D[:, i_closest] = np.inf
    d_overall = np.sum(dist_per_cluster)
    sim = np.exp(-d_overall)
    return sim

def get_sim_clusters(X1, X2, n_clusters):
    centres1 = get_kmeans(X1, n_clusters)
    centres2 = get_kmeans(X2, n_clusters)
    sim = get_sim_centres(centres1, centres2)
    return sim

def get_sim_score(X, n_clusters, n_iters=10):
    sim_score_vec = []
    for i_iter in range(n_iters):
        nObs = X.shape[0]
        rng = np.random.default_rng()
        indices = rng.choice(range(nObs), size=nObs, replace=False)
        half = np.floor(len(indices) / 2).astype(int)
        X1 = X[indices[:half], :]
        X2 = X[indices[(half + 1):], :]
        sim_score_this = get_sim_clusters(X1, X2, n_clusters)
        sim_score_vec.append(sim_score_this)
    sim_score = np.mean(np.array(sim_score_vec))
    return sim_score

def run_over_n_clusters(X, max_n_clusters):
    scores_per_n = []
    n_vec = []
    for n_clusters in range(1, max_n_clusters):
        this_sim_score = get_sim_score(X, n_clusters)
        scores_per_n.append(this_sim_score)
        n_vec.append(n_clusters)
    scores_per_n = np.array(scores_per_n)
    n_vec = np.array(n_vec)
    return scores_per_n, n_vec

def get_best_k_CCC(X, max_n_clusters=10):
    scores_per_n, n_vec = run_over_n_clusters(X, max_n_clusters)
    d_scores_per_n = np.diff(scores_per_n)
    ind_best_n = np.argmin(d_scores_per_n)
    best_n = n_vec[ind_best_n]
    Output = {}
    Output['best_n'] = best_n
    Output['scores_per_n'] = scores_per_n
    Output['n_vec'] = n_vec
    return Output
