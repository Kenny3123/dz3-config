import sys
import json
from config_lang import ConfigLangParser

def main():
    parser = ConfigLangParser()
    source = sys.stdin.read()

    try:
        result = parser.parse(source)
        print(json.dumps(result, indent=4))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()