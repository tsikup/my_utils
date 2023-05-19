import glob
import json
import os
import random
from pathlib import Path
from typing import Union

import yaml
from dotmap import DotMap
from natsort import os_sorted


def create_dirs(dirs):
    """
    dirs - a list of directories to create if these directories are not found
    :param dirs:
    """
    for dir_ in dirs:
        Path(dir_).mkdir(parents=True, exist_ok=True)


def get_config_from_json(json_file):
    """
    Get the config from a json file
    :param json_file:
    :return: config(namespace) or config(dictionary)
    """
    # parse the configurations from the config json file provided
    with open(json_file, "r") as config_file:
        config_dict = json.load(config_file)

    # convert the dictionary to a namespace using bunch lib
    config = DotMap(config_dict)

    return config, config_dict


def get_config_from_yaml(yaml_file):
    """
    Get the config from a yaml file
    :param yaml_file:
    :return: config(namespace) or config(dictionary)
    """
    # parse the configurations from the config json file provided
    with open(yaml_file, "r") as config_file:
        config_dict = yaml.load(config_file, Loader=yaml.Loader)

    # convert the dictionary to a namespace using bunch lib
    config = DotMap(config_dict)

    return config, config_dict


def get_config(file_path):
    if file_path.endswith(".yaml") or file_path.endswith(".yml"):
        return get_config_from_yaml(file_path)
    elif file_path.endswith(".json"):
        return get_config_from_json(file_path)


def process_config(
    file: Union[Path, str],
    name: str,
    output_dir: Union[Path, str],
    fold: int = None,
    mkdirs=True,
    config_copy=True,
    version: int = None,
):
    print("Processing config..")
    config, _ = get_config(file)

    config.exp.name = name

    if config.trainer.seed is None:
        config.trainer.seed = random.randint(0, 2**32 - 1)

    config.filename = file

    config.dataset.train_folder = os.path.join(
        config.dataset.train_folder, f"{fold}_fold/train"
    )
    config.dataset.val_folder = os.path.join(
        config.dataset.val_folder, f"{fold}_fold/val"
    )

    if config.exp.name:
        base_dir = os.path.join(output_dir, config.exp.name)
        if fold is not None:
            base_dir = os.path.join(base_dir, f"{fold}_fold")
        config.experiment_dir = base_dir
        config.callbacks.tensorboard_log_dir = os.path.join(base_dir, "logs/")

        new_version = 0
        if os.path.exists(config.callbacks.tensorboard_log_dir):
            # Get experiment version
            if not config.trainer.version and version is None:
                version = os_sorted(
                    glob.glob(
                        os.path.join(config.callbacks.tensorboard_log_dir, "version_*")
                    )
                )
                if len(version) > 0:
                    new_version = int(os.path.basename(version[-1]).split("_")[-1]) + 1
            elif version is None:
                new_version = config.trainer.version
            else:
                new_version = version
        config.callbacks.checkpoint_dir = os.path.join(
            base_dir, "checkpoints", f"version_{new_version}"
        )

        config.callbacks.backup_dir = os.path.join(base_dir, "backup/")
        if config.mode == "train":
            config.results.performance_dir = os.path.join(base_dir, "results/online")
            config_dir = config.callbacks.checkpoint_dir.replace(
                "/checkpoints/", "/configs/"
            )
            config.callbacks.config_dir = config_dir
            if mkdirs:
                create_dirs(
                    [
                        config.callbacks.tensorboard_log_dir,
                        config.callbacks.checkpoint_dir,
                        config.results.performance_dir,
                        config_dir,
                    ]
                )
            if config_copy:
                with open(
                    os.path.join(config_dir, Path(file).stem + ".json"), "w"
                ) as f:
                    json.dump(dict(config), f)

        elif config.mode == "eval":
            dirname = os.path.dirname(
                os.path.dirname(os.path.dirname(config.tester.checkpoint_path))
            )
            checkpoint = os.path.basename(config.tester.checkpoint_path)
            config.results.performance_dir = os.path.join(
                dirname, "results", "offline", checkpoint
            )
            if mkdirs:
                create_dirs([config.results.performance_dir])
            if config_copy:
                with open(
                    os.path.join(config.results.performance_dir, "config.json"), "w"
                ) as f:
                    json.dump(dict(config), f)

    return config
