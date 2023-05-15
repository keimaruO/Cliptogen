import budoux

def budoux_parse_text(text, max_length=14):
    budoux_parser = budoux.load_default_japanese_parser()
    parsed_text_list = []
    while len(text) > 0:
        parsed_text = ""
        overflow_text = ""
        for budoux_parsed_text in budoux_parser.parse(text):
            if max_length > len(parsed_text + budoux_parsed_text):
                parsed_text += budoux_parsed_text
            elif len(parsed_text) == 0 and len(budoux_parsed_text) > max_length:
                parsed_text = budoux_parsed_text[0:max_length]
                overflow_text += budoux_parsed_text[max_length:]
            else:
                overflow_text += budoux_parsed_text
        parsed_text_list.append(parsed_text)
        text = overflow_text
    return parsed_text_list
