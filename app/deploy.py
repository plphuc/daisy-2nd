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
import post_deployment_hook as post
import pre_deployment_hook as pre
import os, signal

env = os.environ.get("APP_ENV", "")

default_config_file = "dev.yaml"
# default_config_file = "dev_ec2.yaml"
if env == "prod":
    default_config_file = "prod.yaml"
    # default_config_file = "prod_prolific.yaml"
elif env == "test" or env == "sb":
    # default_config_file = "test.yaml"
    default_config_file = "test_prolific.yaml"


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
    pre.handle()
    task_dir = cfg.task_dir
    shared_state = SharedStaticTaskState()


    build_custom_bundle(
        task_dir,
        force_rebuild=cfg.mephisto.task.force_rebuild,
        post_install_script=cfg.mephisto.task.post_install_script,
    )

    try:
        shared_state.prolific_specific_qualifications = [
            {
                "name": "AgeRangeEligibilityRequirement",
                "min_age": 18,
                "max_age": 100,
            },
        ]
        operator.launch_task_run(cfg.mephisto, shared_state)
        operator.wait_for_runs_then_shutdown(skip_input=True, log_rate=30)
    finally:
        post.handle()

def shutdown(signum, frame):
    print('Caught SIGTERM, shutting down')
    # Finish any outstanding requests, then...
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, shutdown)
    main()