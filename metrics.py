import numpy as np
# from sacrebleu import sentence_chrf
from nltk.translate.chrf_score import sentence_chrf
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from Levenshtein import ratio as levenshtein_distance



def exact_match(prediction, expected):
    return float(prediction.strip() == expected.strip())


def chrf_score(prediction, expected):
    return sentence_chrf(prediction, expected)


def levenshtein_score(prediction, expected):
    return levenshtein_distance(prediction, expected)


def bleu_score(prediction, expected):
    smoothing = SmoothingFunction().method1
    return sentence_bleu([expected.split()], prediction.split(),
                         weights=(0.5, 0.5),
                         smoothing_function=smoothing)


def calculate_metrics(expecteds, predictions):
    metrics = {
        "exact_match": [],
        "chrf": [],
        "levenshtein": [],
        "bleu": []
    }

    for expected, prediction in zip(expecteds, predictions):
        metrics["exact_match"].append(exact_match(prediction, expected))
        metrics["chrf"].append(chrf_score(prediction, expected))
        metrics["levenshtein"].append(levenshtein_score(prediction, expected))
        metrics["bleu"].append(bleu_score(prediction, expected))

    return {k: np.mean(v) for k, v in metrics.items()}


with open("report.md") as f:
    lines = [line[line.find("\t"):].strip()
             for line in f if line.startswith(">")]

expecteds = lines[::2]
predictions = lines[1::2]

metrics = calculate_metrics(expecteds, predictions)

print("Average Metrics:")
for metric, value in metrics.items():
    print(f"{metric}: {value:.4f}")
