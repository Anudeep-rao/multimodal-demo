def simplify_prescription(text: str) -> str:
    """
    Simplifies medical abbreviations into patient-friendly English.
    """

    # Common medical abbreviations
    replacements = {
        "BD": "two times a day",
        "TDS": "three times a day",
        "OD": "once a day",
        "HS": "at night",
        "Tab": "tablet",
        "Cap": "capsule",
        "mg": "mg"
    }

    words = text.split()
    simplified_words = []

    for word in words:
        clean_word = word.strip()

        # Case-insensitive match
        upper_word = clean_word.upper()

        if upper_word in replacements:
            simplified_words.append(replacements[upper_word])
        else:
            simplified_words.append(clean_word)

    simplified_text = " ".join(simplified_words)

    # Improve structure
    simplified_text = simplified_text.replace(" x ", " for ")

    # Remove accidental extra spaces
    simplified_text = simplified_text.strip()

    # Capitalize first letter only (clean output)
    if simplified_text:
        simplified_text = simplified_text[0].upper() + simplified_text[1:]

    # Add full stop only if not already present
    if not simplified_text.endswith("."):
        simplified_text += "."

    return simplified_text