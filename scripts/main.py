import re

class TextAnalyzer:
    def __init__(self, text):
        self.text = text
        self.special_chars = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~±÷×€£¥¢₹₽₴«»„"''"'’…·•¶§©®™°µ†‡◊"
        self.numbers = '0123456789'
    
    def clean_text(self): # чистка текста (спец. символы)
        return ''.join(char for char in self.text if char not in self.special_chars)
            
    def remove_spaces(self): # чистка текста (пробелы)
        return self.text.replace(' ', '')

    def remove_numbers(self): # чистка текста (цифры)
        return ''.join(char for char in self.text if char not in self.numbers)

    def all_transforms(self): # все вышеперечисленные
       return self.remove_spaces(self.remove_numbers(self.clean_text()))

    def split_sentences(self): # разделение на предложения
        pattern = r'(?<=[.!?])\s+(?=[А-ЯA-Z])|(?<=[.!?])$'
        sentences = re.split(pattern, self.text)
        return [s.strip() for s in sentences if s.strip()]

    def split_words(self): # разделение на слова
        cleaned = self.remove_numbers(self.clean_text())
        return [word for word in cleaned.split() if word]

    def count_chars(self): # подсчёт символов (с пробелами и со всеми трансформациями)
        return len(self.all_transforms()), len(self.text)
    
    def aux_count_chars(self): # подсчёт символов каждого преобразования
        return len(self.clean_text()), len(self.remove_numbers()), len(self.remove_spaces())

    def count_words(self): # подсчёт слов
        return len(self.split_words())

    def count_sentences(self): # подсчёт предложений
        return len(self.split_sentences())

    def extract_emails(self): # поиск email-адресов
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return set(re.findall(email_pattern, self.text))

    def extract_urls(self): # извлечение ссылок extract_urls()
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*\??[/\w\.-=&%]*|www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[/\w\.-]*\??[/\w\.-=&%]*'
        return set(re.findall(url_pattern, self.text))

    def extract_context(self, search_target): # поиск предложений, содержащих искомую строку
        escaped_target = re.escape(search_target)
        pattern = fr'[^.!?]*{escaped_target}[^.!?]*[.!?]'
        return re.findall(pattern, self.text)

    def sentence_index_range(self, search_target): # возвращает количество и позиции всех вхождений строки 
        mentions = []
        start = 0
        while True:
            pos = self.text.find(search_target, start)
            if pos == -1:
                break
            mentions.append(pos)
            start = pos + 1
        return len(mentions), mentions
    
        def extract_urls_context(self): # поиск предложений с использованием url
            return 0


# поиск телефонных номеров extract_phone_numbers()

# print(all_transforms(userInput))
# print(split_sentences(userInput))