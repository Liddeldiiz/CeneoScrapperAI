def extractElement(ancestor, selector, attribute=None):
    try: 
        if attribute:
            return ancestor.select(selector).pop(0)[attribute].strip()
        else:
            return ancestor.select(selector).pop(0).text.strip()
        #feature = opinion.select(selector).pop(0).text.strip()
        #feature = opinion.select(selector).pop(0)[attribute].strip()
    except IndexError:
        #feature = None
        return None