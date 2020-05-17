class Punct:
    def __init__(self):
        self.punct = {'💁', '[', '’', '~', '💪', '📚', '🏡', '-', '🐣', '🇺', '”', '̶', '\u200a', ';', '🍕', ' ', '!', '%', ',',
         '👇', '®', '🌈', '?', '🏽', '=', '💨', '✅', '✔', ')', '|', '‘', '\xa0', '🗽', '&', '🏼', '¿', '…', '🎓', '👉',
         '❌', '🎧', '👈', '🚂', '+', '🤖', '👎', '→', '¡', '🤔', '️', '👸', '@', '🇸', ':', '“', '•', '🏿', '🏻', '👀',
         '👏', '—', ']', '✓', '"', '\u200b', '🎤', '\n', '.', '(', '$', '❤', '⬇', '#', '👍', "'", '/', '*', '🏾', '–',
         '👿', '\\xe0\\x0\\x0'}
        self.punct.remove(' ')  # keep spaces
        #self.punct.remove('#')  # keep hashtags
        self.punct.remove('@')  # keep mentions
        #self.punct.remove('\')  # keep single quotes (in order to retain I'm, isn't, etc.)

    def get_punct(self):
        return self.punct
