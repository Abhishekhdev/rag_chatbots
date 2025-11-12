# utils/file_utils.py

from pathlib import Path

def save_uploaded_file(uploaded_file, save_dir):
    """
    Save a file uploaded through Streamlit or CLI.
    Returns the full path to the saved file.
    """
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    file_path = Path(save_dir) / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
