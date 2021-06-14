
import json

DATA_FILENAME = "out.json"

def read_json(path: str):
  with open(path, "r") as f:
    return json.loads(f.read())

def main():
  functions = read_json(DATA_FILENAME)
  for func in functions:
    print(func["PLpgSQL_function"])

if __name__ == "__main__":
  main()