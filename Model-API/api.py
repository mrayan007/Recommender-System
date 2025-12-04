from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import pickle
import scipy.sparse
import pandas as pd
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load the saved TF-IDF vectorizer and matrix
try:
    with open("recommender.pkl", "rb") as f:
        tfidf = pickle.load(f)
    X = scipy.sparse.load_npz("recommender_X.npz")
except Exception as e:
    raise RuntimeError(f"Error loading model or matrix: {e}")

# Load the dataset
DATA_PATH = Path("Data/vkm-dataset.csv")
try:
    df = pd.read_csv(DATA_PATH, sep=None, engine="python")
except Exception as e:
    raise RuntimeError(f"Error loading dataset: {e}")

# Define input schema
class RecommendationRequest(BaseModel):
    interests_text: str
    study_credits: Optional[int] = None
    preferred_location: Optional[str] = None
    preferred_level: Optional[str] = None
    max_difficulty: Optional[float] = None
    num_recommendations: int = 5

# Define output schema
class RecommendationResponse(BaseModel):
    recommendations: list
    
# Helper function to find the correct column name
def get_column_name(possible_names, df):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

# Update the recommend function
def recommend(
    profile: RecommendationRequest,
    k: int = 10,
    alpha: float = 0.7,
    beta: float = 0.2,
    gamma: float = 0.1
) -> pd.DataFrame:
    if not np.isclose(alpha + beta + gamma, 1.0):
        raise ValueError("alpha + beta + gamma must sum to 1.0.")

    # Transform the profile's interests text into a vector
    p_vec = tfidf.transform([profile.interests_text])
    content_scores = cosine_similarity(p_vec, X).flatten()

    # Placeholder for popularity scores (set to 0 if unavailable)
    pop_scaled = pd.Series(0.0, index=df.index)

    # Dynamically find the module title column
    title_col = get_column_name(["module_title", "title", "name"], df)

    rows = []
    for idx, row in df.iterrows():
        c_score = float(content_scores[idx])
        pop_score = float(pop_scaled.loc[idx])
        final_score = alpha * c_score + beta * 0.0 + gamma * pop_score  # Simplified for now

        rows.append({
            "module_title": row.get(title_col, "Unknown Title"),
            "final_score": final_score,
        })

    rec_df = pd.DataFrame(rows).sort_values("final_score", ascending=False).head(k).reset_index(drop=True)
    return rec_df

# API endpoint to get recommendations
@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):
    try:
        recommendations = recommend(request, k=request.num_recommendations)
        return RecommendationResponse(recommendations=recommendations.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")