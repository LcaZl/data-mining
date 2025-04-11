# Route Optimization and Recommendation System

This project was developed for the **Data Mining course** at the **University of Trento**. It tackles a real-world logistics problem where truck drivers frequently diverge from the standard delivery routes assigned by their company.

The system aims to:
1. **Propose new optimized standard routes** based on driver behavior.
2. **Recommend personalized standard routes** to individual drivers to minimize deviations.
3. **Generate ideal per-driver routes** that best align with historical behavior.

### Project Structure

- `data/` – Synthetic datasets including drivers, trips, and route definitions
- `src/` – Core source code: encoding, clustering, recommendation, evaluation
- `output/` – Final outputs: JSON files, similarity matrices, evaluation scores
- `notebooks/` – Jupyter notebooks for experiments, testing, and visualizations
- `requirements.txt` – Python dependencies
- `README.md` – Project description and documentation

## Features

- Synthetic data generation (cities, trips, merchandise types and quantities)
- Encoding of trips and driver behaviors
- Dimensionality reduction via PCA
- Clustering with KMeans and KMedoids to identify better standard routes
- Utility matrix construction and collaborative filtering for driver-route matching
- Top-5 recommendations of standard routes per driver
- Greedy generation of ideal routes for each driver
- Evaluation through cosine and Jaccard similarity metrics

## Algorithms & Techniques

- **Clustering**: KMeans, KMedoids, SSE, Silhouette, Davies-Bouldin Index
- **Collaborative Filtering**: User-based filtering on route preferences
- **Encoding**: One-hot encoding with quantity and order information
- **Similarity Measures**: Cosine and Jaccard similarity
- **Dimensionality Reduction**: PCA
- **Greedy Search**: Constructing personalized optimal routes

## Datasets

All data is **synthetically generated** to simulate real-world logistics behavior:
- 20–50 standard routes
- Up to 60,000 actual route variations
- Each route is a sequence of trips: `<city_from, city_to, {merchandise_type: quantity}>`

Input files:
- `actual.json` – Actual routes executed by drivers
- `standard.json` – Company-assigned standard routes and corresponding drivers

## Outputs

- `recStandard.json` – Recommended standard routes (updated company suggestions)
- `driver.json` – Top 5 standard route suggestions per driver (minimizing deviation)
- `perfectRoute.json` – Ideal reconstructed route per driver based on preferences

## Key Concepts

- Learning from deviations to inform better route planning
- Combining clustering, collaborative filtering, and greedy search
- Bridging logistics optimization with behavioral patterns

## Authors

- Luca Zanolo — [luca.zanolo@unitn.it](mailto:luca.zanolo@unitn.it)
- Kaleem Ullah — [kaleemullah.ullah@unitn.it](mailto:kaleemullah.ullah@unitn.it)
- Yishak Tadele Nigatu — [yishaktadele.nigatu@unitn.it](mailto:yishaktadele.nigatu@unitn.it)
- Hafiz Muhammad Ahmed — [hafizmuhammad.ahmed@unitn.it](mailto:hafizmuhammad.ahmed@unitn.it)

