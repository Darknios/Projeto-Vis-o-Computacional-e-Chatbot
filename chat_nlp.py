import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class AnimalNLP:
    def __init__(self, csv_path="FAQ.csv"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # carregar base (FAQ.csv)
        self.kb = pd.read_csv(csv_path, encoding='latin1', sep=';')


        self.questions = self.kb["question"].tolist()
        self.answers = self.kb["answer"].tolist()

        # gerar embeddings
        self.embeddings = self.model.encode(self.questions, convert_to_numpy=True)

    def answer(self, user_message, detected_animal=None):
        user_emb = self.model.encode([user_message], convert_to_numpy=True)
        sims = cosine_similarity(user_emb, self.embeddings).flatten()

        idx = sims.argmax()
        best_score = sims[idx]

        if best_score < 0.40:
            return f"Não encontrei uma resposta exata, mas posso te contar algo sobre {detected_animal}!"

        return self.answers[idx]
