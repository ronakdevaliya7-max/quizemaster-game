import sys

def deduplicate_po(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    seen_msgids = set()
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('msgid '):
            msgid = line.strip()
            
            # Read msgid and msgstr block
            block = [line]
            j = i + 1
            while j < len(lines) and (lines[j].startswith('msgstr') or lines[j].startswith('"')):
                block.append(lines[j])
                j += 1
                
            if msgid not in seen_msgids and msgid != 'msgid ""':
                seen_msgids.add(msgid)
                new_lines.extend(block)
            elif msgid == 'msgid ""':
                # header
                new_lines.extend(block)
            else:
                # duplicate, do not add
                # also need to remove preceding empty lines or comments?
                # Actually, the duplicates added by update_translations.py didn't have #:, they just had empty line before
                if len(new_lines) > 0 and new_lines[-1].strip() == '':
                    new_lines.pop()
                    
            i = j
        else:
            new_lines.append(line)
            i += 1
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print(f"Deduplicated {filepath}")

if __name__ == '__main__':
    deduplicate_po('qgame/translations/hi/LC_MESSAGES/messages.po')
    deduplicate_po('qgame/translations/gu/LC_MESSAGES/messages.po')
