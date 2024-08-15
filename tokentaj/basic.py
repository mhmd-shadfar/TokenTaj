from tokentaj.utils import find_max_pair, find_min_pair, merge_top_pair, count_pairs
import os
from pathlib import Path

class BasicTokenizer:

    def __init__(self) -> None:
        self.merges = {}
        self.vocabulary = {}

    def build_vocabulary(self, merges: dict) -> None:
        self.vocabulary = {i:bytes([i]) for i in range(256)}
        for k, v in merges.items():
            self.vocabulary[v] = self.vocabulary[k[0]] + self.vocabulary[k[1]]


    def train(self, text: str, vocabulary_size: int) -> None:
        num_merges = vocabulary_size - 256

        tokens = text.encode("utf-8")
        tokens = list(map(int, tokens))

        merges = {}
        vocabulary = {i:bytes([i]) for i in range(256)}

        for i in range(num_merges):
            pairs = count_pairs(tokens)
            max_pair = find_max_pair(pairs)
            tokens = merge_top_pair(tokens, max_pair, 256 + i)
            print(f"merging {max_pair} into a new token {256 + i}")

            merges[max_pair] = 256 + i
            vocabulary[256 + i] = vocabulary[max_pair[0]] + vocabulary[max_pair[1]]

        self.merges = merges
        self.vocabulary = vocabulary

    def decode(self, tokens: list[int]) -> str:
        text_byte = b"".join(self.vocabulary[token] for token in tokens)
        text = text_byte.decode("utf-8", errors="replace")

        return text

    def encode(self, text: str) -> list[int]:
        tokens = text.encode("utf-8")
        tokens = list(map(int, tokens))
        while len(tokens) >= 2:
            pairs = count_pairs(tokens)
            min_pair = find_min_pair(pairs, self.merges)
            if min_pair not in self.merges:
                break
            tokens = merge_top_pair(tokens, min_pair, self.merges[min_pair])


        return tokens

    def save(self, path: Path, file_name: str) -> None:
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + f"{file_name}.model", "w") as writer:
            writer.write(str(self.merges))

        print("merges saved")
    
    def load(self, path: Path, file_name: str) -> None:
        with open(path + f"{file_name}.model", "r") as reader:
            self.merges = eval(reader.read())

        self.build_vocabulary(self.merges)
        
        print("merges loaded")
