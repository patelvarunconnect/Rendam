"""Create a sample product-review dataset (data/reviews.csv) and a file of new reviews to test.

The sample data lets the project run out of the box. For a real-world model, replace
data/reviews.csv with a larger dataset (for example Amazon or Flipkart reviews from Kaggle)
that has the columns: review, sentiment (positive / negative).
"""
import random
from pathlib import Path

import pandas as pd

random.seed(7)
DATA_DIR = Path(__file__).parent / "data"

PRODUCTS = [
    "phone", "headphones", "laptop", "shoes", "smartwatch", "mixer grinder", "backpack", "keyboard",
    "power bank", "bluetooth speaker", "water bottle", "t-shirt", "kurta", "earbuds", "trimmer", "charger",
]
POSITIVE = [
    "works perfectly", "is excellent value for money", "has amazing build quality", "exceeded my expectations",
    "is very comfortable to use", "has great battery life", "looks premium and stylish", "is worth every rupee",
    "arrived quickly and well packed", "has superb sound quality", "is fast and reliable", "is exactly as described",
    "is very easy to use", "has a solid finish", "is the best purchase I made this year",
]
NEGATIVE = [
    "stopped working after a week", "is a complete waste of money", "has very poor build quality",
    "is not as described", "heats up too much", "has terrible battery life", "broke within a few days",
    "arrived damaged", "is very uncomfortable", "has awful sound quality", "is slow and keeps hanging",
    "looks cheap and flimsy", "is overpriced for what you get", "has a bad smell and poor stitching",
    "was missing parts in the box",
]
POS_OPENERS = ["Loved it!", "Highly recommended.", "Very happy with this.", "Great product.", "Five stars.", ""]
NEG_OPENERS = ["Very disappointed.", "Do not buy.", "Not happy at all.", "Worst product.", "One star.", ""]
POS_CLOSERS = ["Will buy again.", "Thank you seller!", "Totally satisfied.", "Go for it.", ""]
NEG_CLOSERS = ["Returning it.", "Customer support did not help.", "Regret buying this.", "Avoid it.", ""]


def review(label):
    product = random.choice(PRODUCTS)
    if label == "positive":
        parts = [random.choice(POS_OPENERS), f"The {product} {random.choice(POSITIVE)}"]
        if random.random() < 0.5:
            parts[-1] += f" and {random.choice(POSITIVE)}"
        parts[-1] += "."
        parts.append(random.choice(POS_CLOSERS))
    else:
        parts = [random.choice(NEG_OPENERS), f"The {product} {random.choice(NEGATIVE)}"]
        if random.random() < 0.5:
            parts[-1] += f" and {random.choice(NEGATIVE)}"
        parts[-1] += "."
        parts.append(random.choice(NEG_CLOSERS))
    return " ".join(p for p in parts if p)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    rows = [{"review": review(label), "sentiment": label} for label in ["positive", "negative"] * 400]
    random.shuffle(rows)
    pd.DataFrame(rows).drop_duplicates("review").to_csv(DATA_DIR / "reviews.csv", index=False)

    test = [{"review": review(random.choice(["positive", "negative"]))} for _ in range(40)]
    pd.DataFrame(test).to_csv(DATA_DIR / "new_reviews_to_test.csv", index=False)
    print(f"Saved {len(rows)} training reviews and {len(test)} test reviews to {DATA_DIR}")


if __name__ == "__main__":
    main()
