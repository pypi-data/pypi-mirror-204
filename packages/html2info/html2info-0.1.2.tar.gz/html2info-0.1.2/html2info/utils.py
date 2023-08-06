from termcolor import colored
import json

def pretty_print_dict(data, color="cyan"):
    pretty_data = json.dumps(data, indent=2, ensure_ascii=False)
    print(colored(pretty_data, color))
