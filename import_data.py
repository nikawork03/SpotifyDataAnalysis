import kagglehub

# Download latest version
path = kagglehub.dataset_download("michaellanurias/spotify-playlist-origins")

print("Path to dataset files:", path)