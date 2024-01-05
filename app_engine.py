import requests
import spacy

# URL for fetching random story data
RANDOM_STORY_URL = "https://shortstories-api.onrender.com/"
# spacy.cli.download("en_core_web_lg")

class AppEngine:

    def __init__(self):
        self.difficulty = 2
        self.count_var = 0
        self.test_over = False
        self.random_text_var = ""



    def count(self):
        self.count_var += 1
        print(self.count_var)



    def check_test_over(self):
        if self.count_var >= self.difficulty:
            self.test_over = True


    def reset_count(self, event):
        self.count_var = 0

    def random_text(self):
        while True:
            response = requests.get(RANDOM_STORY_URL)
            story_data = response.json()
            if 1200 >= len(story_data.get("story", "")) >= 600:
                self.random_text_var = story_data["story"]
                return story_data

    def calculate_score(self, typed_text):
        """Takes the typed test as an input and calculates users words per minute, error count
        returns final score"""
        #Calculate percentage complete
        rdm_text_list = self.random_text_var.split(" ")
        typed_text_list = typed_text.split(" ")
        typed_text_list_clean = typed_text_list[0:len(typed_text_list) - 1]
        percentage_complete = len(typed_text_list_clean) / len(rdm_text_list) * 100

        #Calculate text similarity
        comparison_text = self.random_text_var[0:len(typed_text)]

        nlp = spacy.load("en_core_web_lg")
        text_1 = nlp(typed_text)
        text_2 = nlp(comparison_text)
        print(f"Text1: {text_1}")
        print(f"Text2: {text_2}")
        similarity_score = text_1.similarity(text_2)
        if similarity_score > 0.999:
            similarity_score = 1.0


        return percentage_complete, similarity_score