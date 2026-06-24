from pathlib import Path

def main():
    # print(Path(__file__).parent)
    # f = open(Path(__file__).parent / "text.txt", "w")
    # f.write("Hello, World!\n")
    # f.close()
    url = Path(__file__).parent / "data" / "text.txt"
    with open(url, "w", encoding="utf-8") as 
        


if __name__ == "__main__":
    main()