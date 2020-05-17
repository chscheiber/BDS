import re
from Data.punct import Punct


class Tweet:
    def __init__(self, text, date):
        self.text = text
        self.date = date
        self.clean()

    def __str__(self):
        return self.text

    def clean(self):
        self.cleaned_text = self.text.lower()
        self.cleaned_text = result = re.sub(r"http\S+", "", self.cleaned_text)
        self.cleaned_text = re.sub(r'\d+', '0', self.cleaned_text)

        punct = Punct().get_punct()
        for pun in punct:
            self.cleaned_text = self.cleaned_text.replace(pun, "")
        self.cleaned_text = re.sub(r'\s+', ' ', self.cleaned_text)
        self.cleaned_text.strip()
