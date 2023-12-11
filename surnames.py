import re


# Dictionary of regex pattern keys and return values
patterns = {
        # pattern for McKenzie, MacKenzie, McDonald, MacDonald, McIntyre, MacIntyre, et al
    r'(.*)(ma?c)(.*)': lambda match: match.group(1).capitalize() + match.group(2).capitalize() + match.group(3).title(),
        # pattern for del, de la, et al
    r'(.*)(de(?:\s?la|\s?l)?\s)(\w.*)$': lambda match: match.group(1).capitalize() + match.group(2).lower() + match.group(3).title(),
        # pattern for cultural names beginning with 'Di' and ending with either 'o' or 'i'
    r'(.*)(di)(\w+[oi])$': lambda match: match.group(1).capitalize() + match.group(2).title() + match.group(3).title(),
        # pattern for non-whitespace-separated middle names, i.e. Vander, Vonder, et al
    r'(.*)(v[ao]n[a-z]+\s)(\w+)': r'\1\2\3',
        # pattern for compound middle names, i.e. van Buren, von der Beek, et al
    r'(.*)(van(?:der)?|von der)(\s?\w+)$': lambda match: match.group(1).title() + match.group(2).lower() + match.group(3).title(),

        # pattern for Jr and Sr suffixes, with or without trailing period
    r'(.*)(jr|sr)\.?$': r'\1\2.',
        # pattern last names with apostrophe after first character, with or without intercedent spacing
    r'^(\w.*)([a-z]\'\s?)(\w+)': r'\1\2\3',
        # pattern for names with Roman numeral suffixes
    r'(.*)(\b[ixv]{1,}\b)(.*)': r'\1\2\3',

}


def transform_name(name):
    for pattern, replacement in patterns.items():
        if re.match(pattern, name, flags=re.IGNORECASE):
            # Check if the replacement is a lambda function
            if callable(replacement):
                return replacement(re.match(pattern, name))
            else:
                # Apply the replacement with backreferences
                transformed_name = re.sub(pattern, replacement, name, flags=re.IGNORECASE)

                # Special case for Roman numeral handling
                # if pattern == r'(\b\w+) (\w+) (i?(x|v)|v?i{,3})$':
                if pattern == r'(.*)(\b[ixv]{1,}\b)(.*)':
                    parts = transformed_name.rsplit(' ', 1)
                    parts[0] = parts[0].title()  # Leading parts in Title case
                    parts[1] = parts[1].upper()  # Roman numeral in Uppercase
                    return ' '.join(parts)
                else:
                    return transformed_name.title()

    return name.title()  # Return the name as-is if no pattern matches


names = ["sean o'donnell", "vincent d'onofrio", "dietrich o' malley",
         'douglas macarthur', 'alex mckenzie',
         'carlos de la cruz', 'rosa del rio', 'paul lo duca',
         'carlos de la cruz jr',
         'ronald acuña jr.', 'james preston sr.', 'william charles iii', 'patrick surtain iv',
         'martin van buren', 'johnny vander meer', 'james von der beek',
         'catherine zeta-jones', 'rebecca st. james',
         'leonardo dicaprio', 'al di meola', 'enrico de luca',
         "d'angelo williams", 'j.r.r. tolkein', 'f. scott fitzgerald', 'george h.w. bush',
         "Sebastian Alejandro Torres y García",
        #  "Alessandro Giovanni DeLuca-Carbone Fiorentini",
        #  "Isabelle Marie-Thérèse Chantal DuBois-Lafontaine de Clermont",
         ]


if __name__ == '__main__':

    for name in names:
        print(transform_name(name))
