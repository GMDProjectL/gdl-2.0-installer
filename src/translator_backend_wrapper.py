from PySide6.QtCore import QObject, Slot, Signal, Property

from src.translator_backend import TranslatorBackend


class TranslatorBackendWrapper(QObject):
    languageChanged = Signal()

    def __init__(self):
        super().__init__()
        self._translator = TranslatorBackend()
        self._current_language = "en"

    @Property(str, notify=languageChanged)
    def language(self):
        return self._current_language

    @language.setter
    def language(self, code):
        if self._current_language == code:
            return
        
        self._current_language = code
        self._translator.change_language(code)
        
        self.languageChanged.emit()

    @Slot(str, str, result=str)
    def translate(self, text, trigger=""): 
        return self._translator.translate(text)