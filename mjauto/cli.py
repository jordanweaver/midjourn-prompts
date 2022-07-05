"""
To use: `python generate_prompts.py -n 5 -c red,purple -s 1,2,3,-1 -ro 1 -sd 5339 -ss 1`
"""
import random
import time

# FIXME: replace with CLI that looks in directory for .txt files
CATEGORIES = (
    'artists',
    'styles',
    'themes',
    'qualifiers',
)


def _read_wordbanks(*categories):
    banks = []
    for cat in categories:
        with open(f'{cat}.txt') as f:
            lines = f.readlines()
        banks.append([item.strip() for item in lines])

    return banks


def _build_prompt(colors, sizes, seed, randomorder):
    prompt = []
    elements = _read_wordbanks(*CATEGORIES)
    for el, size in zip(elements, sizes):
        if size == -1:
            size = random.randint(1, len(el))
        prompt.extend(random.sample(el, size))            

    if colors:
        prompt += colors

    for i, p in enumerate(prompt):
        if random.random() >= 0.5:
            prompt[i] = p + " :: "
        else:
            prompt[i] = p + " "

    if randomorder is not None:
        random.shuffle(prompt)

    prompt = "".join(prompt)
    prompt += f" --seed {seed}"

    return prompt


def _parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", default=10, type=int)
    parser.add_argument("-c", "--colors", default=None)
    parser.add_argument("-s", "--sizes", default="1,1,1,1")

    # Randomizes prompt order
    parser.add_argument("-ro", "--randomorder", default=0, type=int)
    parser.add_argument("-sd", "--seed", default=None)
    parser.add_argument("-ss", "--samesies", default=1, type=int)

    return parser.parse_args()


def _generate(args):
    colors = args.colors.split(',') if args.colors is not None else None
    if args.sizes is not None:
        sizes = [int(s) for s in args.sizes.split(',')]

    if args.seed is not None:
        seed = args.seed
    else:
        seed = random.randint(0, 2^32)

    # FIXME: change the filenames to include passed in CLI params
    with open(f'prompts_out-{int(time.time())}.txt', 'w') as file:
        for _ in range(args.number):
            if not args.samesies:
                seed = random.randint(0, 2^32)
            file.write(
                _build_prompt(colors, sizes, seed, args.randomorder) + "\n"
            )


def main():
    args = _parse_args()
    _generate(args)


if __name__ == "__main__":
    main()
