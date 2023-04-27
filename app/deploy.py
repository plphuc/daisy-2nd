#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from mephisto.abstractions.blueprints.mixins.screen_task_required import (
    ScreenTaskRequired,
)
from mephisto.data_model.unit import Unit
from mephisto.operations.operator import Operator
from mephisto.tools.scripts import task_script, build_custom_bundle
from mephisto.abstractions.blueprints.abstract.static_task.static_blueprint import (
    SharedStaticTaskState,
)
from rich import print
from omegaconf import DictConfig
import os

env = os.environ.get("APP_ENV", "")

default_config_file = "example.yaml"
if env == "prod":
    default_config_file = "example_prod.yaml"
elif env == "test" or env == "sb":
    default_config_file = "example_test.yaml"


def my_screening_unit_generator():
    while True:
        yield {"text": "SCREENING UNIT: Press the red button", "is_screen": True}


def validate_screening_unit(unit: Unit):
    agent = unit.get_assigned_agent()
    if agent is not None:
        data = agent.state.get_data()
        print(data)
        if (
                data["outputs"] is not None
                and "rating" in data["outputs"]
                and data["outputs"]["rating"] == "bad"
        ):
            # User pressed the red button
            return True
    return False


def handle_onboarding(onboarding_data):
    if onboarding_data["outputs"]["success"] == True:
        return True
    return False


@task_script(default_config_file=default_config_file)
def main(operator: Operator, cfg: DictConfig) -> None:
    task_name = cfg.mephisto.task.get("task_name", None)

    is_using_screening_units = cfg.mephisto.blueprint["use_screening_task"]

    task_dir = cfg.task_dir

    build_custom_bundle(
        task_dir,
        force_rebuild=cfg.mephisto.task.force_rebuild,
        post_install_script=cfg.mephisto.task.post_install_script,
    )

    try:
        operator.launch_task_run(cfg.mephisto)
        operator.wait_for_runs_then_shutdown(skip_input=True, log_rate=30)
    finally:
        exec_parse_data_script()


def exec_parse_data_script():
    # run clean_up.sh script, the script is in the same directory as this file
    os.system(f"sh {os.path.dirname(os.path.realpath(__file__))}/clean_up.sh")


if __name__ == "__main__":
    main()
