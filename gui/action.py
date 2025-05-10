from PyQt6.QtWidgets import QFileDialog

def open_file_dialog():
    file_path, _ = QFileDialog.getOpenFileName(
        None,  # Parent widget (can be `self` if inside a class)
        "Open File",  # Dialog title
        "",  # Starting directory (empty string means the default directory)
        "All Files (*)"  # File filters
    )
    if file_path:
        return file_path

