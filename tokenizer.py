"""Dependency-free tokenizer for Klein's single-user, thinking-disabled template.

Uses the supplied Qwen vocabulary/merges. Unicode characters unknown to this
Python Unicode database are rejected rather than silently misclassified.
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT


def whitespace(c):
    # Unicode White_Space, unlike str.isspace's extra C0 separators.
    return c in "\t\n\v\f\r \x85\xa0\u1680\u2028\u2029\u202f\u205f\u3000" or "\u2000" <= c <= "\u200a"


def pieces(text):
    """Ordered scanner equivalent to the Qwen2 pre-tokenization alternatives."""
    i, n = 0, len(text)
    def letter(c):
        return unicodedata.category(c).startswith("L")
    def number(c):
        return unicodedata.category(c).startswith("N")
    while i < n:
        start = i
        match = re.match(r"(?i:'s|'t|'re|'ve|'m|'ll|'d)", text[i:])
        if match:
            i += len(match.group())
        elif letter(text[i]) or (text[i] not in "\r\n" and not number(text[i])
                                 and i+1 < n and letter(text[i+1])):
            i += 1
            while i < n and letter(text[i]):
                i += 1
        elif number(text[i]):
            i += 1
        else:
            j = i + 1 if text[i] == " " else i
            k = j
            while k < n and not whitespace(text[k]) and not letter(text[k]) and not number(text[k]):
                k += 1
            if k > j:
                while k < n and text[k] in "\r\n":
                    k += 1
                i = k
            else:
                k = i
                last_newline = -1
                while k < n and whitespace(text[k]):
                    if text[k] in "\r\n":
                        last_newline = k
                    k += 1
                if last_newline >= i:
                    i = last_newline + 1
                elif k == n:
                    i = k
                elif k - i > 1:
                    i = k - 1
                elif k > i:
                    i = k
                else:
                    raise ValueError("Unable to segment text at position %s" % i)
        yield text[start:i]


class NativeTokenizer:
    def __init__(self, directory=DATA):
        directory = Path(directory)
        self.vocab = json.loads((directory / "vocab.json").read_text(encoding="utf-8"))
        lines = (directory / "merges.txt").read_text(encoding="utf-8").splitlines()
        self.ranks = {tuple(line.split()): i for i, line in enumerate(lines[1:]) if line}
        config = json.loads((directory / "tokenizer_config.json").read_text(encoding="utf-8"))
        self.added = {}
        for key, token in config["added_tokens_decoder"].items():
            if any(token.get(flag) for flag in ("lstrip", "rstrip", "single_word", "normalized")):
                raise ValueError("Unsupported added-token configuration")
            self.added[token["content"]] = int(key)
        self.special_pattern = re.compile("(" + "|".join(re.escape(t) for t in
                                             sorted(self.added, key=len, reverse=True)) + ")")
        base = list(range(33, 127)) + list(range(161, 173)) + list(range(174, 256))
        extra = [b for b in range(256) if b not in base]
        self.byte_chars = dict(zip(base + extra, map(chr, base + list(range(256, 256 + len(extra))))))
        self.cache = {}

    def bpe(self, piece):
        if piece in self.cache:
            return self.cache[piece]
        word = tuple(self.byte_chars[b] for b in piece.encode("utf-8"))
        while len(word) > 1:
            best = min(zip(word, word[1:]), key=lambda pair: self.ranks.get(pair, float("inf")))
            if best not in self.ranks:
                break
            merged, i = [], 0
            while i < len(word):
                if i+1 < len(word) and (word[i], word[i+1]) == best:
                    merged.append(word[i] + word[i+1])
                    i += 2
                else:
                    merged.append(word[i])
                    i += 1
            word = tuple(merged)
        result = [self.vocab[w] for w in word]
        if len(self.cache) >= 8192:
            self.cache.clear()
        self.cache[piece] = result
        return result

    def encode(self, text):
        for c in text:
            if unicodedata.category(c) in ("Cn", "Cs"):
                raise ValueError("Unsupported Unicode character U+%04X in this Python runtime" % ord(c))
        ids = []
        for part in self.special_pattern.split(text):
            if part in self.added:
                ids.append(self.added[part])
            else:
                for piece in pieces(unicodedata.normalize("NFC", part)):
                    ids.extend(self.bpe(piece))
        return ids

    def tokenize(self, prompt):
        if not isinstance(prompt, str):
            raise TypeError("Prompt must be a string")
        if len(prompt) > 32768:
            raise ValueError("Prompt exceeds the tokenizer's 32768-character safety limit")
        text = "<|im_start|>user\n" + prompt + "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
        ids = self.encode(text)
        if len(ids) > 512:
            raise ValueError("Prompt exceeds 512 tokens after template; refusing silent truncation")
        count = len(ids)
        return {"prompt": prompt, "formatted_text": text, "input_ids": ids + [151643] * (512-count),
                "attention_mask": [1]*count + [0]*(512-count), "active_tokens": count}


def update_group(group):
    """Called in-process from the Nuke Group's button; no subprocess or ML imports."""
    tokenizer = NativeTokenizer()
    data = tokenizer.tokenize(group["prompt"].value())
    # Validate before touching either curve.
    for name, values in (("id_lut", data["input_ids"]), ("mask_lut", data["attention_mask"])):
        knob = group[name]
        knob.clearAnimated()
        knob.setAnimated()
        for index, value in enumerate(values):
            knob.setValueAt(float(value), index)
    group["token_status"].setValue("Encoded %s active tokens / 512" % data["active_tokens"])
    return data