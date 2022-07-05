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


def _build_prompt(partials, seed, delineation, shuffle, extras):
    prompt = []
    elements = _read_wordbanks(*CATEGORIES)
    for el, partial in zip(elements, partials):
        if partial == -1:
            partial = random.randint(1, max(1, min(-(partial), len(el))))
        prompt.extend(random.sample(el, partial))            

    for i, p in enumerate(prompt):
        if delineation == -1:
            if random.random() >= 0.5:
                prompt[i] = p + " :: "
            else:
                prompt[i] = p + " "
        elif delineation == 0:
            prompt[i] = p + " "
        elif delineation == 1:
            prompt[i] = p + " :: "

    if shuffle is not None:
        random.shuffle(prompt)

    if extras:
        prompt += extras

    prompt = "".join(prompt)
    prompt += f" --seed {seed}"

    return prompt


def _parse_args():
    import argparse

    parser = argparse.ArgumentParser(description="Midjourney Prompt Generation CLI")
    parser.add_argument(
        "-n", "--number", 
        default=10, 
        type=int, 
        help="The number of prompts to generate."
    )
    parser.add_argument(
        "-p", "--partials", 
        default="1,1,1,1", 
        help=("Sets the number of partials to pull from each category. "
              "If set to less than 0, the size will be randomized with a max "
              "equal to -(number provided)")
    )
    parser.add_argument(
        "-d", "--delineation", 
        default=-1, 
        type=int,
        help=("Controls the prompt delineators. By default (-1), prompts "
              "are randomly hard separated (with ::) If set to 0, there will "
              "be no separation at all. If set to 1, every partial will be "
              "hard separated (i.e. no separation or hard separated with ::)")
    )

    # By default (None), all partials from categories will come in the order they appear in the Categories List
    # If set to 1, all of the partials are randomized before adding extras
    parser.add_argument("-s", "--shuffle", default=None)
    # If provided, sets the seed for all of the prompts
    parser.add_argument("-sd", "--seed", default=None)
    # By default, sets the same random seed for all prompts if a --seed isn't provided
    # If set to 0 and a --seed isn't provided, randomizes the seed for every prompt
    parser.add_argument("-ss", "--samesies", default=1, type=int)
    # Used to optionally add anything you want included with every prompt
    # Note: The argument should be encapsulated by double quotes and should almost definitely have a space
        # at the beginning so that the parser doesn't strip out everything after the double --
        # Ex: `-e " --sameseed"`
    parser.add_argument("-e", "--extras", default=None)

    return parser.parse_args()


def _generate(args):
    
    # Clean CLI inputs
    if args.partials is not None:
        partials = [int(s) for s in args.partials.split(',')]
    if args.seed is not None:
        seed = args.seed
    else:
        seed = random.randint(0, 2^32)
    shuffle = args.shuffle
    extras = args.extras.split(',') if args.extras is not None else None
    delineation = args.delineation

    # FIXME: change the filenames to include passed in CLI params
    with open(f'prompts_out-{int(time.time())}.txt', 'w') as file:
        for _ in range(args.number):
            if not args.samesies:
                seed = random.randint(0, 2^32)
            file.write(
                _build_prompt(partials, seed, delineation, shuffle, extras) + "\n"
            )


def main():
    args = _parse_args()
    _generate(args)


if __name__ == "__main__":
    main()
