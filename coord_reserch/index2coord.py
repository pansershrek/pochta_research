
import argparse
import json
from collections import Counter
import requests

url = "<GEOCODER URL>"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fin", type=str)
    parser.add_argument("fout", type=str)
    args = parser.parse_args()
    with open(args.fin, "r") as f:
        data = json.load(f)
    ans = {}
    cnt = Counter()
    kek = 0
    print(len(data))
    exit(0)
    with open(args.fout, "w") as f:
        for key, value in data.items():
            q = f"{value['country']} "
            if value.get('locality', ''):
                q += f"город {value['locality']} "
            else:
                q += f"{value['region']} "
                if value['region'][-1] == "я":
                    q += "область "
            if value.get('street', ''):
                q += f"улица {value['street']} "
                if value.get('housenum', ''):
                    q += f"{value['housenum']}"
            f_url = f"{url+q}".strip()
            r = requests.get(f_url)
            try:
                ans[key] = r.json()["results"][0]["coordinates"]
            except BaseException as e:
                print("ignore")
                kek += 1
                pass
        json.dump(ans, f, ensure_ascii=False)
        print("Invalid", kek)

if __name__ == "__main__":
    main()
