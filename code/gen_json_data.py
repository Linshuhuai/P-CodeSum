import os
import json

input_data_dir = "../data/h2o-3/text-davinci-003/data_10/data_"
output_data_dir = "./tmp.jsonl"


class ExampleIn(object):
    """A single training/test example."""

    def __init__(self,
                 query_idx=int,
                 exp_idx=list[int],
                 bleu=float,
                 rouge=float,
                 ):
        self.query_idx = query_idx
        self.exp_idx = exp_idx
        self.bleu = bleu
        self.rouge = rouge


class ExampleOut(object):
    """A single training/test example."""

    def __init__(self,
                 query_idx=int,
                 example_idx=list[int],
                 label=bool
                 ):
        self.query_idx = query_idx
        self.example_idx = example_idx
        self.label = label


def example_out_to_dict(out):
    return {
        "query_idx": out.query_idx,
        "example_idx": out.example_idx,
        "label": out.label
    }


def read_example_in(filename, data_num):
    """Read examples from filename."""
    examples = []
    with open(filename, encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if idx == data_num:
                avg_bleu = float(line[line.index(':') + 2:].split()[0])
                break
            query_idx = int(line[0:line.index('[') - 1])
            arr = line[line.index('[') + 1:line.index(']')]
            exp_idx = list(int(char) for char in arr.split(", "))
            bleu = float(line[line.index(']') + 2:].split()[0])
            rouge = float(line[line.index(']') + 2:].split()[1])
            examples.append(
                ExampleIn(
                    query_idx=query_idx,
                    exp_idx=exp_idx,
                    bleu=bleu,
                    rouge=rouge,
                )
            )
    return examples, avg_bleu


def main():
    fw = open(os.path.join(output_data_dir), 'w')
    for i in range(20, 30):
        examples, avg_bleu = read_example_in(input_data_dir + format(i) + "_10_25.jsonl", 25)
        for example in examples:
            exp = ExampleOut(
                query_idx=example.query_idx,
                example_idx=example.exp_idx,
                label=True if example.bleu >= avg_bleu else False
            )
            # write idx and bleu/rouge to files
            fw.write(json.dumps(exp, default=example_out_to_dict) + '\n')
    fw.close()


if __name__ == "__main__":
    main()
