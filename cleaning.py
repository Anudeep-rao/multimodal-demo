def clean_text(text: str) -> str:
    abbreviations = {
        "BD": "twice daily",
        "TDS": "three times daily",
        "OD": "once daily",
        "HS": "at bedtime"
    }

    for short, full in abbreviations.items():
        text = text.replace(short, full)

    return text