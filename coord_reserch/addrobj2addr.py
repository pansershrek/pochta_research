
import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fin", type=str)
    parser.add_argument("fout", type=str)
    args = parser.parse_args()
    with open(args.fin, "rb") as f:
        data = eval(f.readline())
    ans = {}
    with open(args.fout, "w") as f:
        for key, value in data.items():
            ans[key] = value["properties"]["address"]
        json.dump(ans, f, ensure_ascii=False)
if __name__ == "__main__":
    main()

