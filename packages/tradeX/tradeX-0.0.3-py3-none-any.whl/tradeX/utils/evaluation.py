from collections import defaultdict

import numpy as np


def far_at_k_hits(true_labels: np.ndarray, scores: np.ndarray, k_hits: float = 1000):
    """
    Finds the threshold for positive samples that corresponds to a specified FAR for each class in a multi-class
    classification problem, given the true labels and confidence scores.

    Parameters:
        true_labels (numpy.ndarray): An array of shape (n_samples,) containing the true labels for each sample.
        scores (numpy.ndarray): An array of shape (n_samples, n_classes) containing the confidence scores for each class
                                for each sample.
        far (float): The desired false alarm rate (FAR) for each class.

    Returns:
        thresholds (numpy.ndarray): An array of shape (n_classes,) containing the threshold that corresponds to the
                                     desired FAR for each class.
    """

    # Convert the true labels to one-hot encoding
    num_classes = scores.shape[1]

    # Initialize variables to keep track of the number of true negatives and false positives
    all_class_hits = defaultdict(list)
    all_class_far = defaultdict(list)
    all_threshold = defaultdict(list)
    for clz_id in range(num_classes):
        pred_scores = scores[:, clz_id]
        sorted_idx = pred_scores.argsort()
        sorted_score = pred_scores[sorted_idx]
        gts = true_labels[sorted_idx]
        for i in range(len(gts)):
            threshold = sorted_score[i]
            TP = np.count_nonzero(gts[i:] == clz_id)
            FP = np.count_nonzero(gts[i:] != clz_id)
            all_class_hits[clz_id].append(len(gts[i:]))
            all_class_far[clz_id].append(FP / ((len(gts[i:]) + 0.0000001)))
            all_threshold[clz_id].append(threshold)
    c = 1
    far, threshold = np.concatenate((all_class_hits[c], all_class_far[c], all_threshold[c])).reshape(3, -1)[1:, -1000]
    return far, threshold
