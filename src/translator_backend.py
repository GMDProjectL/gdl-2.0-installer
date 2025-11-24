import json
import os

class TranslatorBackend:
    def __init__(self, language='en'):
        self.change_language(language)

    def load_translations(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        translations_path = os.path.join(base_path, '..', 'translations', f'{self.language}.json')
        try:
            with open(translations_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except Exception as e:
            print(f"Error loading translations: {e}")
            self.translations = {}
    
    def change_language(self, language):
        self.language = language
        self.translations = {}
        self.load_translations()

    def translate(self, text):
        return self.translations.get(text, text)
