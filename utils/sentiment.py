from transformers import pipeline

#Load hugging face model
classifier=pipeline('sentiment-analysis',model='cardiffnlp/twitter-roberta-base-sentiment-latest')

def analyze_sentiment(text):
    try:
        if not isinstance(text,str):
            return 'Neutral',0
        if text.strip()=='':
            return 'Neutral',0
        
        result=classifier(text[:512])[0]
        label=result['label']
        score=round(result['score'],2)

        return label,score

    except Exception:
        return 'Neutral',0