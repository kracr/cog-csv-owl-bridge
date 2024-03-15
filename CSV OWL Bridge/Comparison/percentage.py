from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# Function to read file content
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Read the contents of the two files
file1_content = read_file('output.owl')  # Replace 'path_to_file1' with the path to your first file
file2_content = read_file('index.owl')  # Replace 'path_to_file2' with the path to your second file

# Vectorize the file contents
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([file1_content, file2_content])

# Compute the Cosine Similarity
cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

# Plotting the similarity score
plt.figure(figsize=(6, 4))
plt.bar(['File Similarity'], [cosine_sim], color='blue')
plt.ylabel('Similarity Score')
plt.title('File Similarity Comparison')
plt.ylim(0, 1)
plt.show()

# Print the similarity in percentage
cosine_sim_percentage = cosine_sim * 100
print(f"File Similarity: {cosine_sim_percentage:.2f}%")
