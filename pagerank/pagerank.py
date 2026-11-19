
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)

    print(f"PageRank Results from Sampling (n = {SAMPLES})")

    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)

    print("PageRank Results from Iteration")

    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """

    pages = dict()

    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue

        with open(os.path.join(directory, filename), encoding="utf-8") as f:
            contents = f.read()

            links = re.findall(
                r'<a\s+(?:[^>]*?)href="([^"]*)"',
                contents
            )

            pages[filename] = set(links) - {filename}

    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next.
    """

    pages = list(corpus.keys())
    total_pages = len(pages)

    links = corpus[page]

    if not links:
        links = set(pages)

    probabilities = {}

    for p in pages:
        probabilities[p] = (1 - damping_factor) / total_pages

        if p in links:
            probabilities[p] += damping_factor / len(links)

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values by sampling pages according to the
    transition model.
    """

    pages = list(corpus.keys())

    counts = {page: 0 for page in pages}

    current_page = random.choice(pages)

    for _ in range(n):

        counts[current_page] += 1

        probabilities = transition_model(
            corpus,
            current_page,
            damping_factor
        )

        current_page = random.choices(
            list(probabilities.keys()),
            weights=list(probabilities.values())
        )[0]

    ranks = {}

    for page in pages:
        ranks[page] = counts[page] / n

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values by iteratively updating PageRank values
    until convergence.
    """

    pages = list(corpus.keys())
    total_pages = len(pages)

    ranks = {
        page: 1 / total_pages
        for page in pages
    }

    while True:

        new_ranks = {}

        for page in pages:

            rank = (1 - damping_factor) / total_pages

            for other_page in pages:

                links = corpus[other_page]

                if not links:
                    links = set(pages)

                if page in links:
                    rank += (
                        damping_factor
                        * ranks[other_page]
                        / len(links)
                    )

            new_ranks[page] = rank

        converged = all(
            abs(new_ranks[page] - ranks[page]) < 0.001
            for page in pages
        )

        ranks = new_ranks

        if converged:
            break

    return ranks


if __name__ == "__main__":
    main()
