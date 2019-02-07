import numpy as np
import settings

learn_options = {
    "V": "CD33",
    "adaboost_CV": False,
    "adaboost_loss" : "ls",
    "algorithm_hyperparam_search" : "grid",
    "allowed_category" : None, # "Mismatch", # "Insertion",
    "alpha": np.array([1.0e-3]),
    "annotation position one-hot": False,
    "annotation_decoupled_onehot" : ["pos", "let", "transl"], # decouple the CFD features into letters and position
    "annotation_onehot" : True, # featurize like CFD
    "azimuth_feat" : None, # was: ["WT"]
    "azimuth_score_in_stacker": False,
    "cv": "stratified",
    "fit_intercept" : True,
    "guide_seq_full": True,
    "guideseq_version": 2,
    "haeussler_version": 1,
    "include_NGGX_interaction": False,
    "include_Tm": False,
    "include_azimuth_score": None, # All of them ["WT","MUT","DELTA"]
    "include_gene_position": False,
#   "kde_normalize_guideseq": False,
    "left_right_guide_ind": [4,27,30], # 21-mer
    "models": ["AdaBoost"],
    "mutation_type" : False,
    "n_folds" : 10,
    "normalize_features" : False, "class_weight": None,
    "nuc_features_WT": False, "include_pi_nuc_feat": False,
    "num_proc": 28, # 1
    "order": 1,
    "phen_transform": "kde_cdf",
    "post-process Platt": False,
    "reload guideseq": False,
    "renormalize_guideseq": True, # 6/30/2017 - per Jennifer, changed back to True after latest experiments
    "seed": settings.default_random_seed,
    "testing_non_binary_target_name": "ranks",
    "training_metric": "spearmanr",
    "use_mut_distances": False,
}
