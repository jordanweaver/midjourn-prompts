"""
Example usage: 
    mjauto -n 5 -p 1,2,3,-1 -d 1 -s 1 -sd 5339 -ss 1 -e " --sameseed"

See `mjauto --help` for more info.
"""
import glob
import random
import time


def _read_wordbanks():
    """Assumes CLI is run from the word banks directory. """
    paths = sorted(glob.glob("[0-9]*.txt"))
    banks = []
    for path in paths:
        with open(path) as bankfile:
            lines = bankfile.readlines()
        banks.append([item.strip() for item in lines])

    return banks


def _build_prompt(partials, seed, delineation, shuffle, extras, elements):
    prompt = []
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

    parser = argparse.ArgumentParser(
        description="Midjourney Prompt Generation CLI"
    )
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
    parser.add_argument(
        "-s", "--shuffle", 
        default=None, 
        help=("By default (None), all partials from categories will come in " 
              "the order they appear in the word banks directory. If set to 1, "
              "all of the partials are randomized before adding extras")
    )
    parser.add_argument(
        "-sd", "--seed", 
        default=None, 
        help="If provided, sets the seed for all of the prompts"
    )
    parser.add_argument(
        "-ss", "--samesies", 
        default=1, 
        type=int,
        help=("By default, sets the same random seed for all prompts if a " 
              "--seed isn't provided. If set to 0 and a --seed isn't "
              "provided, randomizes the seed for every prompt")
    )
    parser.add_argument(
        "-e", "--extras", 
        default=None,
        help="""
        Used to optionally add anything you want included with every
        prompt. Note: The argument should be encapsulated by double quotes
        and should almost definitely have a space at the beginning so that
        the parser doesn't strip out everything after the double --: 
        `-e " --sameseed"`
        """
    )

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

    # Read in word bank elements
    elements = _read_wordbanks()

    # FIXME: change the filenames to include passed in CLI params
    with open(f'prompts_out-{int(time.time())}.txt', 'w') as file:
        for _ in range(args.number):
            if not args.samesies:
                seed = random.randint(0, 2^32)

            prompt = _build_prompt(
                partials, seed, delineation, shuffle, extras, elements
            )
            file.write(f"{prompt}\n")


def main():
    args = _parse_args()
    _generate(args)


if __name__ == "__main__":
    main()
