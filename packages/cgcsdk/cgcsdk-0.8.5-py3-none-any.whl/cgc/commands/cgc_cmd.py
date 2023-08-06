import click
import json

from cgc.commands.cgc_cmd_responses import cgc_status_response
from cgc.commands.resource.resource_cmd import resource_delete
from cgc.utils.requests_helper import call_api, EndpointTypes
from cgc.utils.click_group import CustomCommand
from cgc.utils.prepare_headers import get_api_url_and_prepare_headers
from cgc.utils.response_utils import retrieve_and_validate_response_send_metric
from cgc.telemetry.basic import telemetry_permission_set
from cgc.commands.compute.compute_responses import compute_logs_response


@click.command("rm", cls=CustomCommand)
@click.argument("name", type=click.STRING)
def cgc_rm(name: str):
    """
    Delete an app in user namespace
    """
    resource_delete(name)


@click.command("events", cls=CustomCommand)
@click.argument("app_name", type=click.STRING)
def resource_events(app_name: str):
    """Get events of given app"""
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/get_pod_events"
    metric = "resource.events"
    __payload = {"name": app_name}
    __res = call_api(
        request=EndpointTypes.get,
        url=url,
        headers=headers,
        data=json.dumps(__payload),
    )
    click.echo(
        compute_logs_response(retrieve_and_validate_response_send_metric(__res, metric))
    )


@click.command("status", cls=CustomCommand)
def cgc_status():
    """Lists available and used resources"""
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/status"
    metric = "resource.status"
    __res = call_api(
        request=EndpointTypes.get,
        url=url,
        headers=headers,
    )
    click.echo(
        cgc_status_response(retrieve_and_validate_response_send_metric(__res, metric))
    )


@click.command("telemetry", cls=CustomCommand)
def sending_telemetry_permission():
    """Changing permission for sending telemetry"""

    click.echo(
        f"Sending telemetry is now {'enabled' if telemetry_permission_set() else 'disabled'}"
    )
