#pip install pywebview
import webview
from pathlib import Path

def main():
    webview.create_window(
        "simple text",
        url=Path(Path(__file__).resolve() / "text.html").as_uri(),
        width=640,
        height=520,
        resizable=True
    )
    webview.start()

if __name__ == "__main__":
    main()