import os
import streamlit as st
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser 


# Model (API key from environment)
model = ChatGroq(
    groq_api_key=os.getenv('GROQ_API_KEY'),
    model="llama-3.3-70b-versatile"
)



def recommand1(movie_name):
  prompt = PromptTemplate(
      template="Based on the movie {movie_name}, suggest top 5 similar movies for the user. Format your response as a numbered list.",
      input_variables=['movie_name'])
  parser = StrOutputParser()

  movie = prompt | model | parser

  result = movie.invoke({'movie_name': movie_name})
  return movie_list(result)


def movie_list(result):
  movies = []
  # Parse the result to extract movie names
  lines = result.split('\n')
  for line in lines:
    line = line.strip()
    # Skip empty lines and non-numbered lines
    if line and (line[0].isdigit() or line.startswith('-')):
      # Remove numbering and clean up
      movie_name = line.split('.', 1)[-1].strip() if '.' in line else line.lstrip('- ').strip()
      if movie_name:
        movies.append(movie_name)
  return movies if movies else [result]  # Return list of movies or the full result if parsing fails


# Streamlit UI
st.title("🎬 Movie Recommendation System")
st.write("Enter a movie name to get top 5 similar movie recommendations")

movie_name = st.text_input("Enter a movie name:", placeholder="e.g., The Matrix")

if st.button("Get Recommendations"):
    if movie_name:
        with st.spinner("Finding similar movies..."):
            recommendations = recommand1(movie_name)
        
        st.success("Here are your recommendations:")
        for i, movie in enumerate(recommendations, 1):
            st.write(f"{i}. {movie}")
    else:

        st.warning("Please enter a movie name")
