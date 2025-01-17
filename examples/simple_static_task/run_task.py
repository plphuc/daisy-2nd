#!/usr/bin/env python3

# Copyright (c) Meta Platforms and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from mephisto.tools.scripts import task_script
from omegaconf import DictConfig


@task_script(default_config_file="example_local_mock")
def main(operator, cfg: DictConfig) -> None:
    operator.launch_task_run(cfg.mephisto)
    operator.wait_for_runs_then_shutdown(skip_input=True, log_rate=30)


if __name__ == "__main__":
    main()
