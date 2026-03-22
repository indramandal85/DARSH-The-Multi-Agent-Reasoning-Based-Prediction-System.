import os
import re
import subprocess
from pathlib import Path


ALLOWED_EXTENSIONS = {"txt", "md", "pdf"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def normalize_uploaded_file(file_storage, upload_folder: str) -> dict:
    os.makedirs(upload_folder, exist_ok=True)

    original_name = file_storage.filename or "uploaded_document.txt"
    source_ext = (original_name.rsplit(".", 1)[1].lower() if "." in original_name else "txt")
    source_path = _write_source_file(file_storage, upload_folder, original_name)

    if source_ext == "pdf":
        text_content = _extract_pdf_text(source_path)
    else:
        with open(source_path, "rb") as handle:
            raw = handle.read()
        text_content = _decode_text(raw)

    normalized_text = _normalize_content(text_content, source_ext)
    if not normalized_text.strip():
        raise ValueError("Uploaded file could not be converted into usable text.")

    normalized_name = _normalized_filename(original_name)
    normalized_path = os.path.join(upload_folder, normalized_name)
    with open(normalized_path, "w", encoding="utf-8") as handle:
        handle.write(normalized_text)

    return {
        "filename": normalized_name,
        "display_filename": original_name,
        "source_filepath": source_path,
        "filepath": normalized_path,
        "word_count": len(normalized_text.split()),
        "source_format": source_ext,
    }


def _write_source_file(file_storage, upload_folder: str, original_name: str) -> str:
    source_dir = os.path.join(upload_folder, "originals")
    os.makedirs(source_dir, exist_ok=True)

    safe_name = _unique_name(source_dir, original_name)
    source_path = os.path.join(source_dir, safe_name)
    file_storage.save(source_path)
    return source_path


def _decode_text(raw: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _normalize_content(content: str, source_ext: str) -> str:
    text = content.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", " ")

    if source_ext == "md":
        text = _strip_markdown(text)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def _strip_markdown(text: str) -> str:
    cleaned = text
    cleaned = re.sub(r"```.*?```", " ", cleaned, flags=re.S)
    cleaned = re.sub(r"`([^`]*)`", r"\1", cleaned)
    cleaned = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"\1", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", cleaned)
    cleaned = re.sub(r"^\s{0,3}#{1,6}\s*", "", cleaned, flags=re.M)
    cleaned = re.sub(r"^\s*>\s?", "", cleaned, flags=re.M)
    cleaned = re.sub(r"^\s*[-*+]\s+", "", cleaned, flags=re.M)
    cleaned = re.sub(r"^\s*\d+\.\s+", "", cleaned, flags=re.M)
    cleaned = cleaned.replace("**", "").replace("__", "").replace("*", "").replace("_", "")
    return cleaned


def _extract_pdf_text(filepath: str) -> str:
    extractors = [
        ["mdls", "-name", "kMDItemTextContent", "-raw", filepath],
        ["textutil", "-convert", "txt", "-stdout", filepath],
        ["strings", "-n", "6", filepath],
    ]

    for cmd in extractors:
        try:
            proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
        except FileNotFoundError:
            continue

        output = (proc.stdout or "").strip()
        if not output or output == "(null)":
            continue

        if cmd[0] == "strings":
            output = _clean_strings_output(output)

        if len(output.split()) >= 40:
            return output

    raise ValueError("PDF text extraction failed on this system. Try exporting the PDF to text or markdown first.")


def _clean_strings_output(text: str) -> str:
    lines = []
    for line in text.splitlines():
        clean = line.strip()
        if len(clean) < 4:
            continue
        if clean.startswith("%PDF") or clean.startswith("endobj"):
            continue
        lines.append(clean)
    return "\n".join(lines)


def _normalized_filename(original_name: str) -> str:
    path = Path(original_name)
    stem = re.sub(r"[^a-zA-Z0-9_-]+", "_", path.stem).strip("_") or "document"
    ext = path.suffix.lower().lstrip(".")
    if ext in {"txt", "md"}:
        candidate = f"{stem}.txt"
    else:
        candidate = f"{stem}_{ext}.txt"
    return candidate


def _unique_name(directory: str, filename: str) -> str:
    path = Path(filename)
    stem = re.sub(r"[^a-zA-Z0-9_-]+", "_", path.stem).strip("_") or "upload"
    suffix = path.suffix.lower()
    candidate = f"{stem}{suffix}"
    counter = 1
    while os.path.exists(os.path.join(directory, candidate)):
        candidate = f"{stem}_{counter}{suffix}"
        counter += 1
    return candidate
