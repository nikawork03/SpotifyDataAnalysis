import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


file_path = 'origins.csv'
data = pd.read_csv(file_path)


print("Initial Dataset Preview:")
print(data.head())
print("Dataset Columns:", data.columns)

# Step 1: Extract year from the 'Release Date' column
print("Extracting year from 'Release Date'...")
data['Release Date'] = pd.to_datetime(data['Release Date'], errors='coerce')  # Convert to datetime
data['year'] = data['Release Date'].dt.year

# Step 2: Expand the 'Genres' column
print("Processing genres...")
data['Genres'] = data['Genres'].fillna('').str.split(',')
data = data.explode('Genres')
data['Genres'] = data['Genres'].str.strip().str.lower()

# Step 3: Artist Popularity
print("Calculating artist popularity...")
artist_popularity = (
    data.groupby('Artist Name(s)')['Popularity']
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

plt.figure(figsize=(10, 6))
sns.barplot(data=artist_popularity, x='Popularity', y='Artist Name(s)', palette='Blues_r')
plt.title('Top 10 Artists by Average Popularity', fontsize=16)
plt.xlabel('Average Popularity', fontsize=12)
plt.ylabel('Artist', fontsize=12)
plt.tight_layout()
plt.savefig('artist_popularity.png')
plt.show()

# Step 4: Genre Distribution in Top 50 Songs
print("Calculating genre distribution for top 50 songs...")
top_50 = data.nlargest(50, 'Popularity')
genre_distribution_top = top_50['Genres'].value_counts()

plt.figure(figsize=(8, 8))
genre_distribution_top.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('Genre Distribution in Top 50 Songs', fontsize=16)
plt.ylabel('')
plt.tight_layout()
plt.savefig('genre_distribution_top_50.png')
plt.show()

# Step 5: Genre Distribution in Bottom 50 Songs
print("Calculating genre distribution for bottom 50 songs...")
bottom_50 = data.nsmallest(50, 'Popularity')
genre_distribution_bottom = bottom_50['Genres'].value_counts()

plt.figure(figsize=(8, 8))
genre_distribution_bottom.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('Genre Distribution in Bottom 50 Songs', fontsize=16)
plt.ylabel('')
plt.tight_layout()
plt.savefig('genre_distribution_bottom_50.png')
plt.show()

# Step 6: Danceability Comparison
print("Comparing danceability for top 50 vs bottom 50 songs...")
avg_danceability = pd.DataFrame({
    'Category': ['Top 50 Songs', 'Bottom 50 Songs'],
    'Average Danceability': [top_50['Danceability'].mean(), bottom_50['Danceability'].mean()]
})

plt.figure(figsize=(8, 6))
sns.barplot(data=avg_danceability, x='Category', y='Average Danceability', palette='Set3')
plt.title('Average Danceability: Top 50 vs Bottom 50 Songs', fontsize=16)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Average Danceability', fontsize=12)
plt.tight_layout()
plt.savefig('danceability_comparison.png')
plt.show()

# Step 7: Valence vs Energy Comparison
print("Plotting Valence vs Energy for Top and Bottom 50 Songs...")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=top_50, x='Valence', y='Energy', color='blue', label='Top 50 Songs')
sns.scatterplot(data=bottom_50, x='Valence', y='Energy', color='red', label='Bottom 50 Songs')
plt.title('Valence vs Energy: Top 50 vs Bottom 50 Songs', fontsize=16)
plt.xlabel('Valence', fontsize=12)
plt.ylabel('Energy', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('valence_vs_energy.png')
plt.show()

# Step 8: Tempo Distribution by Genre
print("Plotting tempo distribution by genre...")
top_genres = (
    data.groupby('Genres')['Popularity']
    .mean()
    .nlargest(10)
    .index
)
filtered_data = data[data['Genres'].isin(top_genres)]

plt.figure(figsize=(12, 8))
sns.violinplot(data=filtered_data, x='Genres', y='Tempo', palette='coolwarm')
plt.title('Tempo Distribution by Genre (Top 10 Genres)', fontsize=16)
plt.xlabel('Genre', fontsize=12)
plt.ylabel('Tempo', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('tempo_distribution_by_genre.png')
plt.show()

print("All visualizations generated and saved!")
