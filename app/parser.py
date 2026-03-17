import os

def parse_input(source: str) -> str:
    if os.path.isfile(source):
        with open(source, 'r', encoding='utf-8') as f:  
            content = f.read()
        extension = source.split('.')[-1].lower()
        if extension == 'md':
            file_type = 'markdown'
        elif extension == 'txt':
            file_type = 'text'  
        else:
            file_type = 'unknown' 
        
        return {
            "content": content,
            "type": file_type,
            "source": source
        }
    
    else:
         # Not a file, treat as direct input
        return {
            "content": source,
            "type": "text",
            "source": "raw_input"}
    