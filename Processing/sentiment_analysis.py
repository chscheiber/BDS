from textblob import TextBlob


class Classifier:
    def __init__(self):
        pass

    def __get_subjectivity(self, text):
        return TextBlob(text).sentiment.subjectivity

    def __get_polarity(self, text):
        return TextBlob(text).sentiment.polarity

    def get_classified_df(self, df):
        df['Subjectivity'] = df['cleaned_text'].apply(self.__get_subjectivity)
        df['Polarity'] = df['cleaned_text'].apply(self.__get_polarity)
        return df
