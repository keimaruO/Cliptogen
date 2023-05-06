import textwrap
import budoux

def wrap_text(text, max_length=14, max_lines=2):
    wrapped_lines = textwrap.wrap(text, width=max_length)
    
    if len(wrapped_lines) > max_lines:
        wrapped_lines = wrapped_lines[:max_lines - 1] + [''.join(wrapped_lines[max_lines - 1:])]
        
    return wrapped_lines

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

def sentence_parse_and_line_parse(text, max_line_length=15, max_lines=4):
    # 入力テキスト内のスペースを削除
    text = text.replace(" ", "")
    
    # budoux_parse_text を使用して改行されたテキストを生成
    parsed_text_list = budoux_parse_text(text, max_line_length)
    
    # 結果が最大行数を超えている場合、最後の行に残りのテキストを連結
    if len(parsed_text_list) > max_lines:
        parsed_text_list = parsed_text_list[:max_lines - 1] + [''.join(parsed_text_list[max_lines - 1:])]
    
    return parsed_text_list