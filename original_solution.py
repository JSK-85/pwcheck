def getPasswordStrength(passwords, common_words):
    result = []
    
    for pwd in passwords:
        # Rule 4: Length < 6
        if len(pwd) < 6:
            result.append("weak")
            continue
        
        # Rule 2: Consists ONLY of numerical digits (0-9)
        if pwd.isdigit():
            result.append("weak")
            continue
        
        # Rule 3: Consists ONLY of uppercase letters (A-Z) or ONLY of lowercase letters (a-z)
        if pwd.isupper() or pwd.islower():
            result.append("weak")
            continue
        
        # Rule 1: Contains a substring that matches a word from common_words list
        contains_common = False
        for word in common_words:
            if word in pwd:
                contains_common = True
                break
        
        if contains_common:
            result.append("weak")
            continue
        
        # If none of the weak conditions are met
        result.append("strong")
        
    return result
