import argparse


class ArgumentLoader:

    def __init__(self, config_data: dict = None):
        self.config_data = config_data

    def get_value(self, key: str, default=None):
        return self.config_data.get(key, default)

    @staticmethod
    def load(load_dict: list = None):
        if load_dict is None:
            return ArgumentLoader({})
        else:
            parser = argparse.ArgumentParser(allow_abbrev=True)
            for key in load_dict:
                if key.startswith("--"):
                    parser.add_argument(f"{key}", help=key, nargs="?",
                                        default=argparse.SUPPRESS)
                else:
                    parser.add_argument(f"{key}", help=key, nargs="?",
                                        default=argparse.OPTIONAL)
            (known, _) = parser.parse_known_args()
            config_data = vars(known)
            print(config_data)
            return ArgumentLoader(config_data)
