from tree_sitter import Tree, Language, Parser

PYTHON_LANGUAGE = Language('/root/project/codex/method/ptuning/tree_sitter_utils/tree_sitter_build/my-languages.so', 'python')
py_parser = Parser()
py_parser.set_language(PYTHON_LANGUAGE)


def reprint_tree(tree: Tree):
    cursor = tree.walk()
    text = tree.text
    while True:
        if cursor.goto_first_child():
            continue
        start_idx = cursor.node.start_byte
        end_idx = cursor.node.end_byte
        yield bytes.decode(text[start_idx:end_idx])
        if cursor.goto_next_sibling():
            continue
        while True:
            if not cursor.goto_parent():
                return
            if cursor.goto_next_sibling():
                break


def remove_comment(tree: Tree):
    cursor = tree.walk()
    text = tree.text
    while True:
        if cursor.goto_first_child():
            continue
        start_idx = cursor.node.start_byte
        end_idx = cursor.node.end_byte
        yield bytes.decode(text[start_idx:end_idx])
        if cursor.goto_next_sibling():
            continue
        while True:
            if not cursor.goto_parent():
                return
            if cursor.goto_next_sibling():
                break


def get_func_name(tree: Tree):
    cursor = tree.walk()
    text = tree.text
    reached_root = False
    layer = 0
    while not reached_root:
        start_idx = cursor.node.start_byte
        end_idx = cursor.node.end_byte
        if (cursor.node.type == "identifier"
                and cursor.node.parent.type == "function_definition"):
            return bytes.decode(text[start_idx:end_idx])
        if cursor.goto_first_child():
            layer += 1
            continue
        if cursor.goto_next_sibling():
            continue
        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_root = True
                continue
            layer -= 1
            if cursor.goto_next_sibling():
                retracing = False


def get_params(tree: Tree):
    cursor = tree.walk()
    text = tree.text
    reached_root = False
    layer = 0
    while not reached_root:
        start_idx = cursor.node.start_byte
        end_idx = cursor.node.end_byte
        if cursor.node.type == "parameters" \
                and cursor.node.parent.type == "function_definition":
            return bytes.decode(text[start_idx:end_idx])
        if cursor.goto_first_child():
            layer += 1
            continue
        if cursor.goto_next_sibling():
            continue
        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_root = True
                continue
            layer -= 1
            if cursor.goto_next_sibling():
                retracing = False


def get_api_seq(tree: Tree):
    cursor = tree.walk()
    text = tree.text
    api_seq = []
    reached_root = False
    layer = 0
    while not reached_root:
        start_idx = cursor.node.start_byte
        end_idx = cursor.node.end_byte
        if cursor.node.type == "attribute" \
                and cursor.node.parent.type == "call":
            api_seq.append(bytes.decode(text[start_idx:end_idx]))
        if cursor.goto_first_child():
            layer += 1
            continue
        if cursor.goto_next_sibling():
            continue
        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_root = True
                continue
            layer -= 1
            if cursor.goto_next_sibling():
                retracing = False
    return api_seq


def get_variables(tree: Tree):
    cursor = tree.walk()
    text = tree.text
    var_seq = []
    reached_root = False
    layer = 0
    while not reached_root:
        start_idx = cursor.node.start_byte
        end_idx = cursor.node.end_byte
        if cursor.node.type == "identifier":
            var_seq.append(bytes.decode(text[start_idx:end_idx]))
        if cursor.goto_first_child():
            layer += 1
            continue
        if cursor.goto_next_sibling():
            continue
        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_root = True
                continue
            layer -= 1
            if cursor.goto_next_sibling():
                retracing = False
    return var_seq


def get_syntax_tree_0(src):
    src_str = ""
    src_tree = py_parser.parse(bytes(src, "utf8"))
    for tok in reprint_tree(src_tree):
        src_str = src_str + tok + " "
    return src_str


def get_func_signature_and_api_seq(src):
    src_tree = py_parser.parse(bytes(src, "utf8"))
    seq = ""
    for api in get_api_seq(src_tree):
        seq = seq + " " + api
    return get_func_name(src_tree) + get_params(src_tree) + seq


def get_no_comment(src):
    src_str = ""
    src_tree = py_parser.parse(bytes(src, "utf8"))
    for tok in remove_comment(src_tree):
        src_str = src_str + tok + " "
    return src_str


def get_func_api_var(src):
    src_tree = py_parser.parse(bytes(src, "utf8"))
    seq = ""
    for api in get_api_seq(src_tree):
        seq = seq + " " + api
    for var in get_variables(src_tree):
        seq = seq + " " + var
    return get_func_name(src_tree) + get_params(src_tree) + seq


code1 = "def run_instances(count, ec2_config, region, waitForSSH=True, tags=None):\n    ec2params = inheritparams(ec2_config, EC2_API_RUN_INSTANCE)\n    ec2params.setdefault('min_count', count)\n    ec2params.setdefault('max_count', count)\n\n    reservation = None\n    conn = ec2_connect(region)\n    try:\n        reservation = conn.run_instances(**ec2params)\n        log('Reservation: {0}'.format(reservation.id))\n        log('Waiting for {0} EC2 instances {1} to come up, this can take 1-2 minutes.'.format(len(reservation.instances), reservation.instances))\n        start = time.time()\n        time.sleep(1)\n        for instance in reservation.instances:\n            while instance.update() == 'pending':\n               time.sleep(1)\n               h2o_cmd.dot()\n\n            if not instance.state == 'running':\n                raise Exception('\\033[91m[ec2] Error waiting for running state. Instance is in state {0}.\\033[0m'.format(instance.state))\n\n        log('Instances started in {0} seconds'.format(time.time() - start))\n        log('Instances: ')\n        for inst in reservation.instances: log(\"   {0} ({1}) : public ip: {2}, private ip: {3}\".format(inst.public_dns_name, inst.id, inst.ip_address, inst.private_ip_address))\n        \n        if waitForSSH:\n            # kbn: changing to private address, so it should fail if not in right domain\n            # used to have the public ip address\n            wait_for_ssh([ i.private_ip_address for i in reservation.instances ])\n\n        # Tag instances\n        try:\n            if tags:\n                conn.create_tags([i.id for i in reservation.instances], tags)                        \n        except:\n            warn('Something wrong during tagging instances. Exceptions IGNORED!')\n            print sys.exc_info()\n            pass\n\n        return reservation\n    except:\n        print \"\\033[91mUnexpected error\\033[0m :\", sys.exc_info()\n        if reservation:\n            terminate_reservation(reservation, region)\n        raise"
code_tokens = ["def", "dedent", "(", "ind", ",", "text", ")", ":", "text2", "=", "textwrap", ".", "dedent", "(", "text", ")", "if", "ind", "==", "0", ":", "return", "text2", "indent_str", "=", "\" \"", "*", "ind", "return", "\"\\n\"", ".", "join", "(", "indent_str", "+", "line", "for", "line", "in", "text2", ".", "split", "(", "\"\\n\"", ")", ")"]
print(code1)
print(get_func_signature_and_api_seq(code1))
print(get_func_api_var(code1))
