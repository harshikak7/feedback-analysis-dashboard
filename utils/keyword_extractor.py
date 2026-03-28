from collections import Counter
import re


def extract_keywords(text_series):

    all_words = " ".join(text_series).lower()

    words = re.findall(r'\b\w+\b', all_words)

    return Counter(words).most_common(5)