import numpy as np
import xml.etree.ElementTree as ET
from owlready2 import get_ontology, sync_reasoner_pellet
from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from matplotlib import pyplot as plt
import networkx as nx

# Function for deep comparison of XML elements
def deep_compare_elements(elem1, elem2):
    if elem1.tag != elem2.tag or elem1.text != elem2.text or elem1.attrib != elem2.attrib or len(elem1) != len(elem2):
        return False
    for child1, child2 in zip(sorted(elem1, key=lambda x: x.tag), sorted(elem2, key=lambda x: x.tag)):
        if not deep_compare_elements(child1, child2):
            return False
    return True

# Function for calculating structural similarity
def structural_similarity(file1, file2):
    tree1, tree2 = ET.parse(file1), ET.parse(file2)
    return deep_compare_elements(tree1.getroot(), tree2.getroot())

# Function for advanced semantic comparison using Wu-Palmer similarity
def wu_palmer_similarity(word1, word2):
    synset1 = lesk(word_tokenize(word1), pos_tag(word_tokenize(word1)))
    synset2 = lesk(word_tokenize(word2), pos_tag(word_tokenize(word2)))

    if synset1 and synset2:
        return synset1.wup_similarity(synset2)
    else:
        return 0.0

def advanced_semantic_comparison(onto1, onto2):
    individuals_onto1 = set(onto1.individuals())
    individuals_onto2 = set(onto2.individuals())

    # Use Wu-Palmer similarity for semantic comparison
    semantic_scores = []
    for ind1 in individuals_onto1:
        for ind2 in individuals_onto2:
            word1 = ind1.name.lower()
            word2 = ind2.name.lower()
            similarity_score = wu_palmer_similarity(word1, word2)
            semantic_scores.append(similarity_score)

    # Average semantic scores
    average_semantic_score = np.nanmean(semantic_scores)

    return average_semantic_score

# Function for advanced isomeric comparison using graph isomorphism
def isomeric_comparison_advanced(onto1, onto2):
    sync_reasoner_pellet([onto1, onto2])

    individuals_onto1 = set(onto1.individuals())
    individuals_onto2 = set(onto2.individuals())

    # Convert individuals to graphs
    graph_onto1 = nx.Graph()
    graph_onto2 = nx.Graph()

    for ind in individuals_onto1:
        graph_onto1.add_node(ind.name)
        for prop in ind.get_properties():
            for value in prop[ind]:
                graph_onto1.add_edge(ind.name, value.name)

    for ind in individuals_onto2:
        graph_onto2.add_node(ind.name)
        for prop in ind.get_properties():
            for value in prop[ind]:
                graph_onto2.add_edge(ind.name, value.name)

    # Check for graph isomorphism
    isomorphic = nx.is_isomorphic(graph_onto1, graph_onto2)

    return 1.0 if isomorphic else 0.0

# Function for creating a detailed evaluation matrix
def create_detailed_evaluation_matrix(structural_score, semantic_score, isomeric_score):
    return np.array([
        ['Structural Similarity', structural_score],
        ['Semantic Similarity', semantic_score],
        ['Isomeric Comparison', isomeric_score]
    ])

# Function to plot the evaluation matrix
def plot_evaluation_matrix(matrix):
    labels, values = zip(*matrix)
    plt.bar(labels, values, color=['green', 'red', 'brown'])

    for i, value in enumerate(values):
        text_value = f'{int(value * 100)}%' if isinstance(value, (int, float)) else str(value)
        plt.text(i, value, text_value, ha='center', va='bottom')

    plt.xlabel('Evaluation Criteria')
    plt.ylabel('Scores')
    plt.title('Advanced OWL File Evaluation Matrix')
    plt.ylim(0, 1)
    plt.show()

# File paths
file1 = 'index.owl'
file2 = 'output.owl'
# Perform the comparisons
structural_score = structural_similarity(file1, file2)
onto1 = get_ontology(file1).load()
onto2 = get_ontology(file2).load()

# Use advanced semantic comparison
semantic_score = advanced_semantic_comparison(onto1, onto2)

# Add advanced isomeric comparison score
isomeric_score = isomeric_comparison_advanced(onto1, onto2)

# Print the scores
print(f'Average Semantic Score: {semantic_score}')
print(f'Numeric Score for Structural Similarity: {structural_score}')
print(f'Isomeric Score: {isomeric_score}')

# Create and plot the evaluation matrix
evaluation_matrix = create_detailed_evaluation_matrix(structural_score, semantic_score, isomeric_score)
plot_evaluation_matrix(evaluation_matrix)

