# -*- coding: utf-8 -*-
from __future__ import absolute_import

import io
import json
import os

ENV_PROJECT_ID = "UQ_PROJECT_ID"


def _repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, ".."))


def config_dir():
    return os.path.join(_repo_root(), "config")


def projects_dir():
    return os.path.join(config_dir(), "projects")


def active_project_file():
    return os.path.join(config_dir(), "active_project.txt")


def _read_text(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_nested(mapping, keys, default=None):
    cur = mapping
    for key in keys:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur


def resolve_active_project_id(default_project_id="original"):
    env_project_id = os.getenv(ENV_PROJECT_ID)
    if env_project_id and env_project_id.strip():
        return env_project_id.strip()

    selector_path = active_project_file()
    if os.path.isfile(selector_path):
        project_id = _read_text(selector_path).strip()
        if project_id:
            return project_id

    return default_project_id


def _project_json_path(project_id):
    return os.path.join(projects_dir(), "{}.json".format(project_id))


def load_project_profile(project_id=None):
    resolved_id = project_id or resolve_active_project_id()
    profile_path = _project_json_path(resolved_id)

    if not os.path.isfile(profile_path):
        raise RuntimeError(
            "Project profile not found for '{}' at {}".format(resolved_id, profile_path)
        )

    with io.open(profile_path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    conversation_cfg = profile.get("conversation") or {}
    prompt_rel_path = conversation_cfg.get("system_prompt_path")
    if prompt_rel_path:
        prompt_path = os.path.join(config_dir(), prompt_rel_path)
        if not os.path.isfile(prompt_path):
            raise RuntimeError("system_prompt_path does not exist: {}".format(prompt_path))
        conversation_cfg["system_prompt"] = _read_text(prompt_path).strip()
        profile["conversation"] = conversation_cfg

    profile["_project_id"] = resolved_id
    profile["_profile_path"] = profile_path
    profile["_config_dir"] = config_dir()
    return profile


def load_active_project_profile(default_project_id="original"):
    return load_project_profile(resolve_active_project_id(default_project_id))
