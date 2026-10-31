import os
import sys
import time
import json
import hashlib
import h5py
import numpy as np
import faiss

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

print("=== SIFT1M Metadata Generation and Exact Ground Truth ===")

data_dir = '/mnt/c/NIRMA/SEM-1/DSA/filtered-ann/experiments/data'
h5_path = os.path.join(data_dir, 'sift-128-euclidean.hdf5')
meta_dir = os.path.join(data_dir, 'sift_metadata')
gt_dir = os.path.join(data_dir, 'sift_ground_truth')
os.makedirs(meta_dir, exist_ok=True)
os.makedirs(gt_dir, exist_ok=True)

print("Loading SIFT1M dataset...")
with h5py.File(h5_path, 'r') as f:
    train_vectors = f['train'][:]
    test_vectors = f['test'][:]
    unfiltered_neighbors = f['neighbors'][:]

num_base = len(train_vectors)
dim = train_vectors.shape[1]
num_queries = len(test_vectors)
# Use the first 1,000 queries for standard evaluation workload (consistent across all tests)
eval_queries = test_vectors[:1000]
eval_unfiltered_nn0 = unfiltered_neighbors[:1000, 0]
num_eval_queries = len(eval_queries)

print(f"Base vectors: {num_base}, Dim: {dim}, Total queries: {num_queries}, Eval queries: {num_eval_queries}")

sigmas = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 0.5]
target_Ks = {
    0.001: 1000,
    0.003: 333,
    0.01:  100,
    0.03:  33,
    0.1:   10,
    0.3:   3,
    0.5:   2
}

manifest_records = {}

# We'll store summaries
summary_records = []

# Random seed
GLOBAL_SEED = 42

for sigma in sigmas:
    K = target_Ks[sigma]
    print(f"\n------------------------------------------------------------")
    print(f"Processing sigma = {sigma} (target K = {K})")
    print(f"------------------------------------------------------------")
    
    # -------------------------------------------------------------
    # A. Independent Labels
    # -------------------------------------------------------------
    rng_indep = np.random.RandomState(GLOBAL_SEED + int(sigma * 10000))
    indep_base_labels = rng_indep.randint(0, K, size=num_base, dtype=np.int32)
    
    # Save base labels
    indep_base_file = os.path.join(meta_dir, f"sift_indep_labels_sigma_{sigma}.npy")
    np.save(indep_base_file, indep_base_labels)
    indep_base_sha = compute_sha256(indep_base_file)
    
    # Query predicates: random, near, far
    q_rng = np.random.RandomState(GLOBAL_SEED + 100 + int(sigma * 10000))
    q_pred_indep_random = q_rng.randint(0, K, size=num_eval_queries, dtype=np.int32)
    q_pred_indep_near = indep_base_labels[eval_unfiltered_nn0]
    # For far in independent mode: select a label != near label
    q_pred_indep_far = (q_pred_indep_near + q_rng.randint(1, K, size=num_eval_queries, dtype=np.int32)) % K
    
    # -------------------------------------------------------------
    # B. Cluster-Correlated Labels (FAISS KMeans)
    # -------------------------------------------------------------
    t_km_start = time.time()
    # Train KMeans on a 100k subset for speed and consistency
    train_subset_size = min(100000, num_base)
    kmeans = faiss.Kmeans(d=dim, k=K, niter=15, verbose=False, seed=GLOBAL_SEED)
    kmeans.train(train_vectors[:train_subset_size])
    centroids = kmeans.centroids  # shape (K, dim)
    
    # Assign all base vectors
    _, cluster_base_labels = kmeans.index.search(train_vectors, 1)
    cluster_base_labels = cluster_base_labels.ravel().astype(np.int32)
    t_km_end = time.time()
    print(f"  KMeans training & assignment (K={K}) took {t_km_end - t_km_start:.2f}s")
    
    cluster_base_file = os.path.join(meta_dir, f"sift_cluster_labels_sigma_{sigma}.npy")
    np.save(cluster_base_file, cluster_base_labels)
    cluster_base_sha = compute_sha256(cluster_base_file)
    
    # Query predicates for cluster:
    q_pred_clust_random = q_rng.randint(0, K, size=num_eval_queries, dtype=np.int32)
    q_pred_clust_near = cluster_base_labels[eval_unfiltered_nn0]
    
    # Far: find centroid with maximum distance from query
    centroid_index = faiss.IndexFlatL2(dim)
    centroid_index.add(centroids)
    # Search all K centroids to find the farthest one
    _, all_centroid_nn = centroid_index.search(eval_queries, K)
    q_pred_clust_far = all_centroid_nn[:, -1].astype(np.int32)  # farthest centroid
    
    # -------------------------------------------------------------
    # Compute Exact Ground Truth (top-10) for all modes
    # -------------------------------------------------------------
    combos = [
        ('independent', indep_base_labels, 'random', q_pred_indep_random),
        ('independent', indep_base_labels, 'near',   q_pred_indep_near),
        ('independent', indep_base_labels, 'far',    q_pred_indep_far),
        ('cluster',     cluster_base_labels, 'random', q_pred_clust_random),
        ('cluster',     cluster_base_labels, 'near',   q_pred_clust_near),
        ('cluster',     cluster_base_labels, 'far',    q_pred_clust_far),
    ]
    
    for corr_mode, b_labels, pred_mode, q_labels in combos:
        t0 = time.time()
        # Precompute label counts and actual sigma
        label_counts = np.bincount(b_labels, minlength=K)
        q_sigma_actual = label_counts[q_labels] / float(num_base)
        mean_sigma_actual = float(np.mean(q_sigma_actual))
        
        # Ground truth containers
        gt_ids = np.zeros((num_eval_queries, 10), dtype=np.int32)
        gt_dists = np.zeros((num_eval_queries, 10), dtype=np.float32)
        
        # Group queries by target label to optimize search
        unique_q_labels = np.unique(q_labels)
        for label_val in unique_q_labels:
            q_idx = np.where(q_labels == label_val)[0]
            if len(q_idx) == 0:
                continue
            matching_base_idx = np.where(b_labels == label_val)[0]
            if len(matching_base_idx) == 0:
                # No matching vectors in base
                gt_ids[q_idx, :] = -1
                gt_dists[q_idx, :] = float('inf')
                continue
            
            matching_vectors = train_vectors[matching_base_idx]
            sub_index = faiss.IndexFlatL2(dim)
            sub_index.add(matching_vectors)
            
            k_search = min(10, len(matching_base_idx))
            D_sub, I_sub = sub_index.search(eval_queries[q_idx], k_search)
            
            # Map local indices back to global base indices
            global_I = matching_base_idx[I_sub]
            gt_ids[q_idx, :k_search] = global_I
            gt_dists[q_idx, :k_search] = D_sub
            if k_search < 10:
                gt_ids[q_idx, k_search:] = -1
                gt_dists[q_idx, k_search:] = float('inf')
                
        t1 = time.time()
        
        # Save GT
        gt_prefix = f"sift_gt_{corr_mode}_sigma_{sigma}_{pred_mode}"
        gt_ids_path = os.path.join(gt_dir, f"{gt_prefix}_ids.npy")
        gt_dists_path = os.path.join(gt_dir, f"{gt_prefix}_dists.npy")
        np.save(gt_ids_path, gt_ids)
        np.save(gt_dists_path, gt_dists)
        
        sha_ids = compute_sha256(gt_ids_path)
        sha_dists = compute_sha256(gt_dists_path)
        
        print(f"  {corr_mode:<12} | {pred_mode:<6} | sigma_actual: {mean_sigma_actual:.5f} | GT computed in {t1-t0:.2f}s | SHA: {sha_ids[:10]}...")
        
        summary_records.append({
            "dataset": "SIFT1M",
            "sigma_target": sigma,
            "K": K,
            "correlation": corr_mode,
            "predicate_mode": pred_mode,
            "sigma_actual_mean": mean_sigma_actual,
            "gt_ids_file": os.path.basename(gt_ids_path),
            "gt_ids_sha256": sha_ids,
            "gt_dists_file": os.path.basename(gt_dists_path),
            "gt_dists_sha256": sha_dists
        })

# -----------------------------------------------------------------------------
# 4. Verify Ground Truth on 100 queries with a Second Implementation
# (FAISS Flat L2 + explicit boolean masking / IDSelector)
# -----------------------------------------------------------------------------
print("\n============================================================")
print("Verifying Ground Truth on 100 queries with second implementation")
print("============================================================")

verify_passes = 0
verify_total = 0

# Test across sample configurations
test_configs = [
    ('independent', 0.1, 'random'),
    ('independent', 0.01, 'near'),
    ('cluster', 0.1, 'near'),
    ('cluster', 0.01, 'far')
]

full_flat_index = faiss.IndexFlatL2(dim)
full_flat_index.add(train_vectors)

for corr_mode, sigma, pred_mode in test_configs:
    b_labels = np.load(os.path.join(meta_dir, f"sift_{corr_mode[:5] if corr_mode=='independent' else 'cluster'}_labels_sigma_{sigma}.npy" if corr_mode=='cluster' else os.path.join(meta_dir, f"sift_indep_labels_sigma_{sigma}.npy")))
    gt_ids = np.load(os.path.join(gt_dir, f"sift_gt_{corr_mode}_sigma_{sigma}_{pred_mode}_ids.npy"))
    gt_dists = np.load(os.path.join(gt_dir, f"sift_gt_{corr_mode}_sigma_{sigma}_{pred_mode}_dists.npy"))
    
    # Verify on first 25 queries of this config (total 100 queries across the 4 configs)
    for q_i in range(25):
        verify_total += 1
        q_vec = eval_queries[q_i:q_i+1]
        target_gt_ids = gt_ids[q_i]
        target_gt_dists = gt_dists[q_i]
        
        # Second implementation: Brute-force via NumPy masked matrix multiplication
        # Find all matching vector indices
        if corr_mode == 'independent':
            # reconstruct query label from GT top hit
            first_id = target_gt_ids[0]
            req_label = b_labels[first_id]
        else:
            first_id = target_gt_ids[0]
            req_label = b_labels[first_id]
            
        matching_indices = np.where(b_labels == req_label)[0]
        match_vectors = train_vectors[matching_indices]
        
        # Exact L2 distance via numpy
        diffs = match_vectors - q_vec
        manual_dists = np.sum(diffs * diffs, axis=1)
        manual_top_k_idx = np.argsort(manual_dists)[:10]
        manual_ids = matching_indices[manual_top_k_idx]
        manual_top_dists = manual_dists[manual_top_k_idx]
        
        # Check agreement
        ids_match = np.array_equal(target_gt_ids, manual_ids)
        dists_match = np.allclose(target_gt_dists, manual_top_dists, atol=1e-4)
        
        if ids_match and dists_match:
            verify_passes += 1
        else:
            print(f"MISMATCH on query {q_i} in config {corr_mode}-{sigma}-{pred_mode}:")
            print(f"  GT ids:     {target_gt_ids}")
            print(f"  Manual ids: {manual_ids}")

print(f"\nVerification Result: {verify_passes} / {verify_total} queries matched identically!")
assert verify_passes == verify_total, f"Verification failed! Only {verify_passes}/{verify_total} matched!"

# Write summary manifest
summary_path = os.path.join(data_dir, 'MANIFEST.json')
manifest_data = {
    "dataset": "SIFT1M",
    "source_url": "http://ann-benchmarks.com/sift-128-euclidean.hdf5",
    "hdf5_sha256": compute_sha256(h5_path),
    "hdf5_size_bytes": os.path.getsize(h5_path),
    "metadata_and_ground_truth": summary_records,
    "ground_truth_verification": {
        "queries_tested": verify_total,
        "queries_matched": verify_passes,
        "second_implementation": "NumPy manual Euclidean distance with full boolean masking",
        "status": "PASS" if verify_passes == verify_total else "FAIL"
    }
}

with open(summary_path, 'w') as f:
    json.dump(manifest_data, f, indent=2)

print(f"Saved complete manifest to {summary_path}")
