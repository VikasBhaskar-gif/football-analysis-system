# K=8 Macro Tactical State Reference Asset

This directory contains the retained reference configuration for the $K=8$ macro tactical state clustering discovered across 4 matches (8 halves, 4,800 snapshots) in the FOOTPASS dataset.

## Retained Files

- **`k8_cluster_summary.csv`**: Structural feature averages, centroid distributions, temporal run metrics, and recurrence across all 8 match halves.
- **`granularity_cluster_assignments.npz`**: Snapshot-by-snapshot cluster assignments for the 8 halves alongside cluster centers in the canonical 44-dimensional feature space.
- **`granularity_metrics.json`**: Full diagnostics, inertia, and silhouette measurements for the $K=8$ configuration.

## Discovered State Overview (K=8)

| State | Share (%) | Recurrence | Description |
|:---:|:---:|:---:|:---|
| **c0** | 4.3% | 3 matches / 3 halves | Deep defensive low block, high interaction density ($0.59$) |
| **c1** | 15.0% | 4 matches / 8 halves | Midfield balanced block, wide attacking shape ($0.85$ width) |
| **c2** | 10.9% | 4 matches / 8 halves | Left-flank congested build-up, asymmetric centroid displacement |
| **c3** | 12.6% | 3 matches / 3 halves | Pinned territorial low block (H2-specific settled sequence) |
| **c4** | 22.5% | 4 matches / 7 halves | Central midfield transition & circulation, compact structure |
| **c5** | 16.2% | 3 matches / 5 halves | High attacking territorial advance into final third |
| **c6** | 10.7% | 4 matches / 7 halves | Deep defensive line, low block absorption under opponent pressure |
| **c7** | 7.8% | 4 matches / 4 halves | Right-flank progression and wide corridor circulation |

*Note: This configuration is retained solely as an optional historical/comparative benchmark and is not the central architecture of the new coach-directed platform.*
