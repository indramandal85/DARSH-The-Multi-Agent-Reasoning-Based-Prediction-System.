# knowledge/document_parser.py
#
# WHAT THIS DOES:
# Reads any text document and prepares it for entity extraction.
# The key challenge: LLMs have token limits. A long document can't
# be sent as one prompt. We chunk it into overlapping pieces so
# no information gets cut off at a chunk boundary.

import os


def load_document(filepath: str) -> str:
    """
    Read a text file and return its content as a string.
    filepath: path to the file, e.g. "data/inputs/rbi_article.txt"
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"\nFile not found: {filepath}\n"
            f"Make sure the file exists in data/inputs/\n"
        )

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        raise ValueError(f"File is empty: {filepath}")

    print(f"  Loaded: {filepath}")
    print(f"  Size: {len(content)} characters")

    return content


def chunk_document(text: str, chunk_size: int = 800, overlap: int = 100) -> list:
    """
    Split a long document into overlapping chunks.

    Why overlapping? Because entities and relationships often span
    sentence boundaries. If we cut cleanly, we might split
    "RBI Governor Shaktikanta Das announced..." across two chunks
    and lose the connection between Das and RBI.

    chunk_size : characters per chunk (800 chars ≈ ~150 words — safe for LLM)
    overlap    : how many characters to repeat between adjacent chunks
                 so relationships crossing boundaries aren't lost

    Returns: list of text chunk strings
    """

    # If document is short enough, no chunking needed
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Don't cut mid-sentence — find the last period before the cut
        if end < len(text):
            last_period = text.rfind(".", start, end)
            if last_period > start + (chunk_size // 2):
                end = last_period + 1  # include the period

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move forward, but overlap so boundary relationships aren't lost
        start = end - overlap

    print(f"  Split into {len(chunks)} chunks "
          f"(chunk_size={chunk_size}, overlap={overlap})")

    return chunks


def parse_document(filepath: str) -> dict:
    """
    Main function: load a document and return it ready for extraction.

    Returns a dict with:
      filepath  : original file path
      filename  : just the filename
      full_text : the complete document text
      chunks    : list of text chunks ready for LLM processing
    """

    full_text = load_document(filepath)
    chunks = chunk_document(full_text)

    return {
        "filepath"  : filepath,
        "filename"  : os.path.basename(filepath),
        "full_text" : full_text,
        "chunks"    : chunks
    }


# ── SELF TEST ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print("\n" + "="*45)
    print("  TESTING document_parser.py")
    print("="*45)

    result = parse_document("data/inputs/rbi_article.txt")

    print(f"\n  Filename  : {result['filename']}")
    print(f"  Full text : {len(result['full_text'])} chars")
    print(f"  Chunks    : {len(result['chunks'])}")
    print(f"\n  First chunk preview:")
    print(f"  {result['chunks'][0][:200]}...")
    print("\n  ✓ document_parser.py working correctly.")