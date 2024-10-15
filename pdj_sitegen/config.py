from pdj_sitegen.build import Config

if __name__ == '__main__':
    import sys
    fmt: str = sys.argv[1] if len(sys.argv) > 1 else 'yaml'
    config: Config = Config()
    config_str: str = config.as_str(fmt)
    print(config_str)