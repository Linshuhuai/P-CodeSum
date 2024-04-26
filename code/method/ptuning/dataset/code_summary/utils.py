import json
import logging
import numpy as np
from tree_sitter_utils.build_tree import get_func_signature_and_api_seq
from tree_sitter_utils.build_tree import get_func_api_var
from tree_sitter_utils.build_tree import get_no_comment

logger = logging.getLogger(__name__)


def read_examples(filename, data_num, task):
    read_example_dict = {
        'summarize': read_summarize_examples,
    }
    return read_example_dict[task](filename, data_num)


def calc_stats(examples, tokenizer=None, is_tokenize=False):
    avg_src_len = []
    avg_trg_len = []
    avg_src_len_tokenize = []
    avg_trg_len_tokenize = []
    for ex in examples:
        if is_tokenize:
            avg_src_len.append(len(ex.source.split()))
            avg_trg_len.append(len(str(ex.target).split()))
            avg_src_len_tokenize.append(len(tokenizer.tokenize(ex.source)))
            avg_trg_len_tokenize.append(len(tokenizer.tokenize(str(ex.target))))
        else:
            avg_src_len.append(len(ex.source.split()))
            avg_trg_len.append(len(str(ex.target).split()))
    if is_tokenize:
        logger.info("Read %d examples, avg src len: %d, avg trg len: %d, max src len: %d, max trg len: %d",
                    len(examples), np.mean(avg_src_len), np.mean(avg_trg_len), max(avg_src_len), max(avg_trg_len))
        logger.info("[TOKENIZE] avg src len: %d, avg trg len: %d, max src len: %d, max trg len: %d",
                    np.mean(avg_src_len_tokenize), np.mean(avg_trg_len_tokenize), max(avg_src_len_tokenize),
                    max(avg_trg_len_tokenize))
    else:
        logger.info("Read %d examples, avg src len: %d, avg trg len: %d, max src len: %d, max trg len: %d",
                    len(examples), np.mean(avg_src_len), np.mean(avg_trg_len), max(avg_src_len), max(avg_trg_len))


class Example(object):
    """A single training/test example."""

    def __init__(self,
                 idx,
                 source,
                 target,
                 path,
                 url=None,
                 task='',
                 sub_task=''
                 ):
        self.idx = idx
        self.source = source
        self.target = target
        self.path = path
        self.url = url
        self.task = task
        self.sub_task = sub_task


def read_summarize_examples(filename, data_num):
    """Read examples from filename."""
    examples = []
    with open(filename, encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line = line.strip()
            js = json.loads(line)
            if 'idx' not in js:
                js['idx'] = idx
            # code = ' '.join(js['code_tokens']).replace('\n', ' ')
            # code = ' '.join(code.strip().split())
            # nl = ' '.join(js['docstring_tokens']).replace('\n', '')
            # nl = ' '.join(nl.strip().split())
            # code = js['code'].replace('\n', '\\n')
            # this is ts1
            # code = get_func_signature_and_api_seq(js['code']).replace('\n', '\\n')
            # this is ts2
            # code = get_func_api_var(js['code']).replace('\n', '\\n')
            # this is ts0
            code = get_no_comment(js['code']).replace('\n', '\\n')
            nl = js['docstring'].replace('\n', '\\n')
            path = js['path']
            examples.append(
                Example(
                    idx=idx,
                    source=code,
                    target=nl,
                    path=path,
                )
            )
            if idx + 1 == data_num:
                break
    return examples


def largest_same_string(str1, str2):
    str1, str2 = (str2, str1) if len(str1) > len(str2) else (str1, str2)
    res = 0
    for i in range(0, len(str1)):
        if str2[i] == str1[i]:
            res = res + 1
        else:
            break
    return res


def find_k_largest(nums, k):
    for i in range(len(nums)-1):
        for j in range(len(nums)-1-i):
            if nums[j] > nums[j+1]:
                nums[j+1], nums[j] = nums[j], nums[j+1]
    return nums[len(nums)-k]


def choice(k, input_list):
    ans_list = []
    rest = len(input_list)
    praise = k
    for i in input_list:
        if np.random.rand() < (praise / rest):
            ans_list.append(i)
            praise -= 1
        rest -= 1
    return ans_list



