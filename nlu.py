import json
import re
import string

def load_intents(json_path):
    """
    Loads intents from JSON and creates a mapping of word -> intent_tag.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        intent_map = {}
        for intent in data['intents']:
            tag = intent['tag']
            for pattern in intent['patterns']:
                    words = tokenize(preprocess(pattern))
                    # Filter noise/stopwords from patterns so generic question words
                    # (e.g. 'कौन', 'कब') do not get mapped to specific intents.
                    filtered_words = filter_noise(words)
                    for word in filtered_words:
                        intent_map[word] = tag
        return intent_map
    except Exception as e:
        print(f"Error loading intents: {e}")
        return {}

def preprocess(text):
    """
    Lowercase, remove punctuation, strip whitespace.
    """
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    # Remove punctuation using translation table
    # Include common English and Hindi punctuation keys if needed, but standard string.punctuation handles standard ASCII
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

def tokenize(text):
    """
    Split by whitespace.
    """
    return text.split()

def filter_noise(tokens):
    """
    Remove stopwords and short words.
    """
    STOPWORDS = {
        # Romanized
        "hai", "h", "ko", "se", "ka", "ki", "ke", "me", "mein", 
        "aur", "tathaa", "evam", "kyon", "kya", "kab", "kaise", 
        "kahan", "jab", "tab", "ab", "abhi", "bhi", "toh", "hi", 
        "ji", "sir", "madam", "sunie", "suno", "hey", "hello", "hi", 
        "kuch", "kuchh", "ek", "do", "teen", "char", "paanch", 
        "batao", "dikhao", "karo", "do", "de", "lo", "le", "baje",
        
        # Devanagari
        "है", "ह", "को", "से", "का", "की", "के", "में", "मे",
        "और", "तथा", "एवं", "क्यों", "क्या", "कब", "कैसे",
        "कहाँ", "जब", "तब", "अब", "अभी", "भी", "तो", "ही",
        "जी", "सर", "मैडम", "सुनिए", "सुनो", "हे", "हेलो", "हाय",
        "कुछ", "एक", "दो", "तीन", "चार", "पांच",
        "बताओ", "दिखाओ", "करो", "दो", "दे", "लो", "ले", "बजे"
    }
    
    filtered = []
    for t in tokens:
        if t in STOPWORDS:
            continue
        if len(t) < 2: 
            continue
        filtered.append(t)
    return filtered

def get_levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return get_levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def detect_intent(text, intent_map):
    """
    1. Preprocess & Tokenize
    2. Filter Noise
    3. Match (Exact then Fuzzy)
    """
    clean_text = preprocess(text)
    tokens = tokenize(clean_text)
    clean_tokens = filter_noise(tokens)
    
    # 1. Exact Match
    for token in clean_tokens:
        if token in intent_map:
            return intent_map[token]
            
    # 2. Fuzzy Match (Levenshtein <= 1)
    for token in clean_tokens:
        for keyword, tag in intent_map.items():
            dist = get_levenshtein_distance(token, keyword)
            if dist <= 1:
                return tag
                
    return None

def fallback_to_llm(text):
    """
    Generate a concise response using the LLM.
    """
    prompt = f"""
    आप एक हिंदी वॉयस असिस्टेंट हैं।
    कृपया केवल उपयोगकर्ता के प्रश्न का उत्तर दें।
    किसी भी उपयोगकर्ता या सहायक लेबल का उपयोग न करें।
    
    {text}
    """

    # Example LLM call (adjust parameters as needed)
    result = llm(
        prompt=prompt,
        max_tokens=50,  # Limit response length
        temperature=0.7,  # Adjust creativity
        top_p=0.9
    )

    # Return only the response text
    return result.strip() if result else "मुझे समझ नहीं आया।"
