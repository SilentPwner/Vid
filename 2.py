# الخلية 2: تحليل وصف المستخدم
nlp = spacy.load("en_core_web_sm")

def parse_description(text):
    doc = nlp(text)
    verbs = []
    nouns = []
    background = ""
    
    # كلمات مفتاحية للخلفيات
    background_keywords = ['beach', 'park', 'room', 'forest', 'city', 'mountain']
    
    for token in doc:
        if token.pos_ == "VERB":
            verbs.append(token.lemma_)
        elif token.pos_ == "NOUN":
            nouns.append(token.text)
            if token.text in background_keywords:
                background = token.text
    
    return {
        "actions": verbs,
        "objects": nouns,
        "background": background
    }

# اختبار الدالة
user_input = "a man eating an apple on a beach"
parsed = parse_description(user_input)
print("Parsed Input:", parsed)