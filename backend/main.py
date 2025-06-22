from fastapi import FastAPI, Query
from trie import Trie
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import openai  # Install via `pip install openai`
import wikipediaapi

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific frontend URL for security
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

trie = Trie()

# Load words from words.txt into the Trie
def load_words_from_file():
    file_path = os.path.join(os.path.dirname(__file__), "words.txt")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip()
            if word:
                trie.insert(word)

load_words_from_file()

@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}

@app.get("/suggest/")
def get_suggestions(prefix: str = Query(..., min_length=1, description="Prefix to search for")):
    suggestions = trie.find_words_with_prefix(prefix)

    if len(suggestions) == 0:
        suggestions = trie.find_closest_match(prefix)
        suggestions = [word for count,word in suggestions]

    return {"prefix": prefix, "suggestions": suggestions}

    

# @app.get("/define/")
# def get_definitions(word: str = Query(..., min_length=1, description="Word to define")):
#     url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         data = response.json()
#         definitions = [definition["definition"] for meaning in data[0]["meanings"] for definition in meaning["definitions"]]
#         return {"word": word, "definitions": definitions}
    
#     return {"word": word, "error": "Definition not found"}



# Set your OpenAI API Key


USER_AGENT = "app/1.0 (24mca040@nirmauni.ac.in)"  # Replace with your app name and email
wiki_wiki = wikipediaapi.Wikipedia(language="en",user_agent=USER_AGENT)
wiki_wiki.user_agent = USER_AGENT  

# if page.exists():
#     print("Title:", page.title)
#     print("Summary:", page.summary[:500])  # Print first 500 characters of summary
# else:
#     print("Page not found")

def get_wikipedia_summary(word):
    """Fetch a summary from Wikipedia."""
    page = wiki_wiki.page(word)
    if page.exists():
        return page.summary[:500]  # Return the first 500 characters
    return None  # Return None if the page doesn't exist

def get_ai_generated_definition(word):
    """Generate a definition using OpenAI's GPT model."""
    prompt = f"Define the term '{word}' in a simple and clear way."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" for better results
            messages=[{"role": "user", "content": prompt}]
        )
        definition = response["choices"][0]["message"]["content"]
        return definition
    except Exception as e:
        return "AI definition service is currently unavailable."
    


# @app.get("/define/")
# def get_definitions(word: str = Query(..., min_length=1, description="Word to define")):

#     """Fetch definition from dictionary API, Wikipedia, or AI as fallback."""
    
#     # Step 1: Try dictionary API
#     url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         data = response.json()
#         definitions = [definition["definition"] for meaning in data[0]["meanings"] for definition in meaning["definitions"]]
#         return {"word": word, "definitions": definitions}

#     # Step 2: Try Wikipedia for proper nouns, places, and company names
#     wiki_definition = get_wikipedia_summary(word)
#     if wiki_definition:
#         return {"word": word, "definitions": [wiki_definition]}

#     # Step 3: Use AI-generated definition as the final fallback
#     ai_definition = get_ai_generated_definition(word)
#     return {"word": word, "definitions": [ai_definition]}

@app.get("/define/")
def get_definitions(word: str = Query(..., min_length=1, description="Word to define")):
    """Fetch definition from dictionary API or Wikipedia."""

    # Step 1: Try dictionary API
    # url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    # response = requests.get(url)

    # if response.status_code == 200:
    #     data = response.json()
    #     definitions = [definition["definition"] for meaning in data[0]["meanings"] for definition in meaning["definitions"]]
    #     return {"word": word, "definitions": definitions}

    # Step 2: Try Wikipedia
    wiki_definition = get_wikipedia_summary(word)
    if wiki_definition:
        return {"word": word, "definitions": [wiki_definition]}

    return {"word": word, "definitions": ["Definition not found."]}

