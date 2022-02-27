import re, sqlite3, random
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import BallTree
from sklearn.base import BaseEstimator
from sklearn.pipeline import make_pipeline


db_name = 'Buddy optimize'

with sqlite3.connect(f"{db_name}.db") as conn:  
	csr = conn.cursor()
	csr.execute("SELECT context FROM data")

	questions = [question[0] for question in csr.fetchall()]

vectorizer = TfidfVectorizer()
vectorizer.fit(questions)
matrix_big = vectorizer.transform(questions)

transform = len(questions)
if len(questions) > 256:
	transform = 256

svd = TruncatedSVD(n_components=transform)
svd.fit(matrix_big)
matrix_small = svd.transform(matrix_big)


def softmax(x):
	proba = np.exp(-x)
	return proba / sum(proba)

class NeighborSampler(BaseEstimator):
	def __init__(self, k=1, temperature=1.0):
		self.k = k
		self.temperature = temperature

	def fit(self, X, y):
		self.tree_ = BallTree(X)
		self.y_ = np.array(y)

	def predict(self, X, random_state=None):
		distances, indices = self.tree_.query(X, return_distance=True, k=self.k)

		result = []
		for distance, index in zip(distances, indices):
			result.append(np.random.choice(index, p=softmax(distance * self.temperature)))

		return self.y_[result]

ns = NeighborSampler()
ns.fit(matrix_small, [i+1 for i in range(len(questions))])
pipe = make_pipeline(vectorizer, svd, ns)

del matrix_big, matrix_small, ns, svd, vectorizer


def clear_text(text):        
    text = re.sub(r'[^\w-]+', ' ', text.lower().replace('ё', 'е'))
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def response(pipe, question):
	answer_id = pipe.predict([clear_text(question)])[0]
	with sqlite3.connect(f"{db_name}.db") as conn:  
		csr = conn.cursor()
		csr.execute(f"SELECT reply FROM data WHERE id = {answer_id}")
		answer = csr.fetchone()[0]
	return answer

if __name__ == "__main__":
	while True:
		print(random.choice(response(pipe, question=input('>>')).split('//')))


#print(matrix_big.shape)
#print(matrix_small.shape)
#print(svd.explained_variance_ratio_.sum())


