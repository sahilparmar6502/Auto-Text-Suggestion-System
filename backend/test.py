import wikipediaapi  # Correct Wikipedia API library
from fastapi import FastAPI, Query
import requests

app = FastAPI()

# Wikipedia Setup
USER_AGENT = "app/1.0 (24mca040@nirmauni.ac.in)"  # Replace with your app name and email
wiki_wiki = wikipediaapi.Wikipedia(language="en",user_agent=USER_AGENT)
wiki_wiki.user_agent = USER_AGENT  

def get_wikipedia_summary(word):
    """Fetch a summary from Wikipedia."""
    page = wiki_wiki.page(word)
    if page.exists():
        return page.summary[:500]  # Return the first 500 characters
    return None  # Return None if the page doesn't exist

@app.get("/define/")
def get_definitions(word: str = Query(..., min_length=1, description="Word to define")):
    """Fetch definition from dictionary API or Wikipedia."""

    # Step 1: Try dictionary API
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        definitions = [definition["definition"] for meaning in data[0]["meanings"] for definition in meaning["definitions"]]
        return {"word": word, "definitions": definitions}

    # Step 2: Try Wikipedia
    wiki_definition = get_wikipedia_summary(word)
    if wiki_definition:
        return {"word": word, "definitions": [wiki_definition]}

    return {"word": word, "definitions": ["Definition not found."]}
