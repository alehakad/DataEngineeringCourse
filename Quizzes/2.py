from functools import reduce


# all words that have five or more letters reversed
def reverse_long_words(words_str: str) -> str:
    return " ".join([w if len(w) < 5 else w[::-1] for w in words_str.split(" ")])


def reverse_long_words_map(words_str: str) -> str:
    return reduce(
        lambda x, y: x + ' ' + y,
        map(lambda w: w if len(w) < 5 else w[::-1], words_str.split(" ")),
    )


if __name__ == "__main__":
    assert reverse_long_words("Stop gninnipS My sdroW!") == "Stop Spinning My !Words"
    assert reverse_long_words("Stop gninnipS My sdroW!") == reverse_long_words_map("Stop gninnipS My sdroW!")