# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
from contrast.extern.wrapt import register_post_import_hook

import contrast
from contrast.agent import scope
from contrast.agent.middlewares.route_coverage.common import build_route
from contrast.agent.middlewares.route_coverage.flask_routes import create_routes
from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import build_and_apply_patch
from contrast.utils.decorators import fail_quietly

from contrast.agent.assess.rules.config import (
    FlaskSessionAgeRule as QuartSessionAgeRule,
    FlaskSecureFlagRule as QuartSecureFlagRule,
    FlaskHttpOnlyRule as QuartHttpOnlyRule,
)

from contrast.extern import structlog as logging

MODULE_NAME = "quart"

logger = logging.getLogger("contrast")


def build_full_dispatch_request_patch(orig_func, patch_policy):
    del patch_policy

    async def full_dispatch_request_patch(self, *args, **kwargs):
        try:
            result = await orig_func(self, *args, **kwargs)
        finally:
            do_first_request_analysis(self)
            do_quart_route_observation(self, *args, **kwargs)
        return result

    return full_dispatch_request_patch


@fail_quietly("Failed to run first-request Quart analysis")
@scope.with_contrast_scope
def do_first_request_analysis(quart_instance):
    from contrast.agent import agent_state

    if not agent_state.is_first_request():
        return

    do_quart_config_scanning(quart_instance)
    do_quart_route_discovery(quart_instance)


@fail_quietly("Failed to run Quart config scanning rules")
def do_quart_config_scanning(quart_instance):
    logger.debug("Running Quart config scanning rules")
    QuartSessionAgeRule().apply(quart_instance)
    QuartSecureFlagRule().apply(quart_instance)
    QuartHttpOnlyRule().apply(quart_instance)


@fail_quietly("unable to perform Quart route discovery")
def do_quart_route_discovery(quart_instance):
    from contrast.agent import agent_state

    discovered_routes = create_routes(quart_instance)
    agent_state.get_routes().update(discovered_routes)
    logger.debug(
        "Discovered the following Quart routes: %s",
        [f"{route.verb} {route.url}" for route in discovered_routes.values()],
    )


@fail_quietly("unable to perform Quart route observation")
@scope.with_contrast_scope
def do_quart_route_observation(quart_instance, *args, **kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None:
        return

    logger.debug("Performing quart route observation")

    quart_ctx = args[0] if len(args) > 0 else kwargs.get("request_context")
    if not quart_ctx:
        logger.debug(
            "unable to get quart ctx for route observation. args: %s, kwargs: %s",
            args,
            kwargs,
        )
        return

    endpoint = getattr(quart_ctx.request.url_rule, "endpoint", None)
    view_func = quart_instance.view_functions.get(endpoint)
    if view_func is None:
        logger.debug("did not find endpoint for quart route observation")
        return

    context.view_func = view_func
    context.view_func_str = build_route(view_func.__name__, view_func)
    logger.debug("Observed Quart route: %s", context.view_func_str)


def patch_quart(quart_module):
    build_and_apply_patch(
        quart_module.Quart,
        "full_dispatch_request",
        build_full_dispatch_request_patch,
    )


def register_patches():
    register_post_import_hook(patch_quart, MODULE_NAME)


def reverse_patches():
    quart_module = sys.modules.get(MODULE_NAME)
    if not quart_module:
        return

    patch_manager.reverse_patches_by_owner(quart_module.Quart)
