import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('index', type=str)
    parser.add_argument('data', type=str)
    parser.add_argument('fout', type=str)
    args = parser.parse_args()
    with open(args.index, "r") as f_index:
        index = set(json.loads(f_index.readline().strip()))
    ans = {}
    with open(args.data, "r") as data, open(args.fout, "w") as fout:
        for line in data:
            row = json.loads(" ".join(line.split()[1:]))
            postal_code_tmp = row['properties'].get('postalcode', '0')
            if not postal_code_tmp:
                postal_code_tmp_int = 0
            else:
                postal_code_tmp_int = int(postal_code_tmp)
            if postal_code_tmp_int in index:
                ans[row['properties']['postalcode']] = row
        print(ans, file=fout, flush=True)


if __name__ == '__main__':
    main()
