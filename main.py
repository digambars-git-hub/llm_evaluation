# main.py
# entry point for running the eval tool
# (simple script to load chat + context, then run evaluator)

import argparse
import json
from evaluator import Evaluator


def load_json(path):
    # just reading json normally
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    # writes output file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--chat", required=True)
    p.add_argument("--context", required=True)
    p.add_argument("--out", default="report.json")
    args = p.parse_args()

    chat = load_json(args.chat)
    ctx = load_json(args.context)

    ev = Evaluator()
    res = ev.evaluate_chat(chat, ctx)

    save_json(res, args.out)
    print("Report saved to:", args.out)


if __name__ == "__main__":
    main()
