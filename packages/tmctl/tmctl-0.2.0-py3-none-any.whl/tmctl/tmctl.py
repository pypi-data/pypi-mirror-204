import os
import sys

import fire
import logging
import yaml

from .controller import CommonOption, Catalog, Cluster, File, HelmChart, MountFile


class TMCtl(object):
    """Class Documentation"""

    def __init__(
        self, url=None, output=None, indent=4, log_level="WARNING", verbose=False
    ):
        self._config = self._init_config()

        admin_url = url or self._config["admin"]["url"]
        output = output or "json"
        indent = indent or 4

        common_option = CommonOption(admin_url=admin_url, output=output, indent=indent)

        self.catalog = Catalog(common_option)
        self.cluster = Cluster(common_option)
        self.helm_chart = HelmChart(common_option)
        self.file = File(common_option)
        self.mount = MountFile(common_option)

        log_config = self._config.get("logging", None) or {}
        self._init_logging(log_config, log_level, verbose)

    def _init_config(self):
        config = None
        try:
            config = yaml.load(open("./config.yaml", "r"), Loader=yaml.Loader)
        except Exception:
            pass

        if not config:
            try:
                home_directory = os.path.expanduser("~")
                config = yaml.load(
                    open(f"{home_directory}/.idp/config.yaml", "r"), Loader=yaml.Loader
                )
            except Exception:
                pass

        return config

    def _init_logging(self, log_config, log_level, verbose):
        handler = log_config.get("handler", "stdout")
        format = log_config.get("format", None)

        level = log_level

        if verbose:
            level = "DEBUG"

        root = logging.getLogger()
        root.setLevel(level)

        if handler:
            if handler == "stdout":
                handler = logging.StreamHandler(sys.stdout)
                handler.setLevel(level)
                if format:
                    handler.setFormatter(logging.Formatter(format))

                root.addHandler(handler)

        logging.debug("initializing logging object complete")

    def help(self):
        """Help message"""
        print("Help")


if __name__ == "__main__":
    fire.Fire(TMCtl)
