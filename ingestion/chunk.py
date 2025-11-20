import re
import tiktoken


enc = tiktoken.get_encoding("cl100k_base")

def chunk_markdown(md, max_tokens=500):
    md = re.sub(r"(?=\*\*[A-Z])", r"\n", md)
    sections = re.split(r"(?:^|\n)(?=\*\*[A-Z][A-Za-z\s&]+\*\*)", md) #split before headings
    sections = [s for s in sections if s.strip()] # remove empty items
    chunks = []
    buf = []
    tot_token = 0
    
    for sec in sections:
        sec_token = len(enc.encode(sec))
        if tot_token + sec_token > max_tokens:
            chunks.append("".join(buf))
            buf, tot_token = [sec], sec_token
        else:
            buf.append(sec)
            tot_token += sec_token
            
    if buf:
        chunks.append("".join(buf))
        
    print(f"Total chunks created: {len(chunks)}")
    return chunks