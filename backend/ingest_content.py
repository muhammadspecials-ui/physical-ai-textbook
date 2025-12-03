"""
Content ingestion script for RAG chatbot.
Reads markdown files from docs/ and ingests them into Qdrant.
"""

import os
import re
from pathlib import Path
from qdrant_service import qdrant_service


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to end at a sentence boundary
        if end < len(text):
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n\n')
            boundary = max(last_period, last_newline)
            
            if boundary > chunk_size // 2:
                chunk = chunk[:boundary + 1]
                end = start + boundary + 1
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return chunks


def extract_metadata(content: str, filepath: str) -> dict:
    """Extract metadata from markdown frontmatter."""
    metadata = {
        'source': filepath,
        'title': os.path.basename(filepath).replace('.md', '').replace('-', ' ').title()
    }
    
    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
    
    return metadata


def ingest_markdown_files(docs_dir: str = '../docs'):
    """Ingest all markdown files from docs directory."""
    docs_path = Path(docs_dir)
    
    if not docs_path.exists():
        print(f"Error: {docs_dir} does not exist")
        return
    
    # Collect all markdown files
    md_files = list(docs_path.rglob('*.md'))
    print(f"Found {len(md_files)} markdown files")
    
    all_documents = []
    
    for md_file in md_files:
        print(f"Processing: {md_file}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata
        metadata = extract_metadata(content, str(md_file.relative_to(docs_path)))
        
        # Remove frontmatter from content
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Chunk the content
        chunks = chunk_text(content)
        
        # Create documents
        for i, chunk in enumerate(chunks):
            doc = {
                'text': chunk,
                'metadata': {
                    **metadata,
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                }
            }
            all_documents.append(doc)
    
    print(f"\nTotal chunks created: {len(all_documents)}")
    
    # Ingest into Qdrant
    print("Ingesting into Qdrant...")
    qdrant_service.create_collection()
    qdrant_service.add_documents(all_documents)
    
    print("✅ Ingestion complete!")


if __name__ == '__main__':
    ingest_markdown_files()
