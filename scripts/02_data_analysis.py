import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# =======================================================
# 1. Environment Setup and Data Loading
# =======================================================
# Set professional plotting style for academic reporting
sns.set_theme(style="whitegrid", palette="muted")

processed_dir = "data/processed/"
data_path = os.path.join(processed_dir, "integrated_special_ed_data.csv")

# Load the finalized dataset
df = pd.read_csv(data_path)

# =======================================================
# 2. Analysis 1: Income vs. Per Pupil Spending (Regression)
# =======================================================
plt.figure(figsize=(10, 6))

# Generate a scatter plot with an automated linear regression line
sns.regplot(
    data=df, 
    x='Median_Household_Income', 
    y='Per_Pupil_Spending',
    scatter_kws={'alpha': 0.7, 'edgecolor': 'w', 's': 80},
    line_kws={'color': '#d62728', 'linewidth': 2}
)

plt.title('Economic Influence: Median Household Income vs. Per Pupil Spending', fontsize=14, pad=15)
plt.xlabel('Median Household Income (USD)', fontsize=12)
plt.ylabel('Per Pupil Educational Spending (USD)', fontsize=12)

plot1_path = os.path.join(processed_dir, "fig01_income_vs_spending.png")
plt.tight_layout()
plt.savefig(plot1_path, dpi=300)
plt.close()

# =======================================================
# 3. Model Evaluation: Elbow Method & Silhouette Score
# =======================================================
# Standardize features for distance-based clustering
features = ['Median_Household_Income', 'Per_Pupil_Spending']
X = df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

wcss = []
sil_scores = []
K_range = range(2, 10)

# Iterate through possible k values to find the optimal cluster count
for k in K_range:
    kmeans_eval = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans_eval.fit(X_scaled)
    wcss.append(kmeans_eval.inertia_)
    sil_scores.append(silhouette_score(X_scaled, kmeans_eval.labels_))

# Plot evaluation metrics on a dual-axis graph
fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot Elbow (WCSS)
color = 'tab:blue'
ax1.set_xlabel('Number of Clusters (k)', fontsize=12)
ax1.set_ylabel('Inertia / WCSS', color=color, fontsize=12)
ax1.plot(K_range, wcss, marker='o', color=color, linewidth=2)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(K_range)

# Plot Silhouette Score
ax2 = ax1.twinx()  
color = 'tab:red'
ax2.set_ylabel('Silhouette Score', color=color, fontsize=12)  
ax2.plot(K_range, sil_scores, marker='s', color=color, linestyle='--', linewidth=2)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Determining Optimal k: Elbow Method & Silhouette Score', fontsize=14, pad=15)
fig.tight_layout()  
eval_plot_path = os.path.join(processed_dir, "fig02_cluster_evaluation.png")
plt.savefig(eval_plot_path, dpi=300)
plt.close()

# =======================================================
# 4. Final K-Means Clustering & Visualization (k=3)
# =======================================================
# Apply K-Means with the optimal k=3
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

cluster_mapping = {
    1: 'Tier 3: Lower Income / Lower Spending',
    0: 'Tier 2: Mid Income / High Spending Outliers',
    2: 'Tier 1: Higher Income / Higher Spending'
}
df['Cluster_Label'] = df['Cluster'].map(cluster_mapping)

tier_order = [
    'Tier 1: Higher Income / Higher Spending',
    'Tier 2: Mid Income / High Spending Outliers',
    'Tier 3: Lower Income / Lower Spending'
]
color_palette = ['#d62728', '#2ca02c', '#1f77b4']

clustered_output = os.path.join(processed_dir, "clustered_integrated_dataset.csv")
df.to_csv(clustered_output, index=False)

# Generate final cluster scatter plot
plt.figure(figsize=(11, 7))
sns.scatterplot(
    data=df, 
    x='Median_Household_Income', 
    y='Per_Pupil_Spending', 
    hue='Cluster_Label',
    hue_order=tier_order,
    palette=color_palette,
    s=120,
    alpha=0.8,
    edgecolor='w'
)

# Add state abbreviations as text labels to the data points
for i in range(df.shape[0]):
    state_abbr = df['State'].iloc[i][:3].upper()
    plt.text(df['Median_Household_Income'].iloc[i] + 500, 
             df['Per_Pupil_Spending'].iloc[i], 
             state_abbr, 
             horizontalalignment='left', 
             size='small', color='black', alpha=0.6)

plt.title('State Segmentation: K-Means Clustering of Economic vs. Educational Investment', fontsize=14, pad=15)
plt.xlabel('Median Household Income (USD)', fontsize=12)
plt.ylabel('Per Pupil Educational Spending (USD)', fontsize=12)
plt.legend(title="State Profile (K-Means)", bbox_to_anchor=(1.02, 1), loc='upper left')

plot_cluster_path = os.path.join(processed_dir, "fig03_kmeans_clustering.png")
plt.tight_layout()
plt.savefig(plot_cluster_path, dpi=300, bbox_inches='tight')
plt.close()

# =======================================================
# 5. Statistical Correlation Extraction
# =======================================================
# Calculate Pearson correlation coefficients
corr_income_spending = df['Median_Household_Income'].corr(df['Per_Pupil_Spending'])
corr_needs_revenue = df['HI_Student_Count'].corr(df['Total_Revenue_Thousands'])

print(f"Correlation (Income & Spending): {corr_income_spending:.3f}")
print(f"Correlation (Needs & Revenue): {corr_needs_revenue:.3f}")