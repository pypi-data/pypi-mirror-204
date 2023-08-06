"""Define a functions for modifying incoming data."""
from datetime import datetime, timedelta
import pytz
from .exceptions import RequestLimitReached, WebsocketException

TZ = pytz.timezone('Europe/Amsterdam')

ERRORS = {
    0: WebsocketException("Unknown command"),
    1: WebsocketException("Invalid Auth Token"),
    2: WebsocketException("Not authorized"),
    9: WebsocketException("Unknown error"),
    42: RequestLimitReached("Request limit reached")
}

SETTINGS = ['plug_and_charge', 'public_charging']

SMART_CHARGING = set()


def calculate_average_usage_from_phases(phases: tuple):
    """Get the average of the phases that are not 0."""
    used_phases = [p for p in phases if p]
    if len(used_phases):
        return round(sum(used_phases) / len(used_phases), 1)
    return 0


def calculate_total_kw(current: tuple, v_avg):
    """Calculate the total kW."""
    return round((sum(current) * v_avg / 1000), 2)


def create_datetime(timestamp: str):
    """Get a datetime object from an timestamp."""

    if timestamp == "":
        return None

    if '+' in timestamp:
        return datetime.strptime(timestamp, "%Y%m%d %H:%M:%S%z")

    time = datetime.strptime(timestamp, "%Y%m%d %H:%M:%S")
    time = TZ.localize(time)
    return time


def get_vehicle_status(vehicle_status_key: str):
    """Get the vehicle status."""
    statuses = {
        "A": "standby",
        "B": "vehicle_detected",
        "C": "ready",
        "D": "ready",
        "E": "no_power",
        "F": "vehicle_error",
    }

    return statuses[vehicle_status_key]


def get_exception(message: dict):
    """Return a defined error message or one from the server"""
    error = message["error"]
    message = message["message"]

    if error in ERRORS:
        return ERRORS[error]
    return WebsocketException(message)


def set_smart_charging(evse_id, smart_charging):
    """Add or discard evse_id in SMART_CHARGING"""
    if smart_charging:
        SMART_CHARGING.add(evse_id)
    else:
        SMART_CHARGING.discard(evse_id)


def handle_charge_points(message: dict):
    """Store the evse_id if it has smart charging enabled"""
    for charge_point in message["data"]:
        set_smart_charging(
            charge_point["evse_id"], charge_point["smart_charging"])


def set_current_left(message: dict, c_avg):
    """Set current_left"""
    max_usage = message["data"]["max_usage"]
    smart_charging_max_usage = message["data"]["smartcharging_max_usage"]

    if message["evse_id"] in SMART_CHARGING:
        message["data"]["current_left"] = smart_charging_max_usage - c_avg
    else:
        message["data"]["current_left"] = max_usage - c_avg


def handle_status(message: dict):
    """Transform status values and add others."""
    voltage1 = message["data"]["actual_v1"]
    voltage2 = message["data"]["actual_v2"]
    voltage3 = message["data"]["actual_v3"]

    v_avg = calculate_average_usage_from_phases((voltage1, voltage2, voltage3))
    message["data"]["avg_voltage"] = v_avg

    current1 = message["data"]["actual_p1"]
    current2 = message["data"]["actual_p2"]
    current3 = message["data"]["actual_p3"]

    c_avg = calculate_average_usage_from_phases(
        (current1, current2, current3))
    message["data"]["avg_current"] = c_avg

    set_current_left(message, c_avg)

    message["data"]["total_kw"] = calculate_total_kw((
        current1, current2, current3), v_avg)

    vehicle_status_key = message["data"]["vehicle_status"]
    message["data"]["vehicle_status"] = get_vehicle_status(vehicle_status_key)

    start_datetime = message["data"]["start_datetime"]
    new_start_datetime = create_datetime(start_datetime)

    stop_datetime = message["data"]["stop_datetime"]
    new_stop_datetime = create_datetime(stop_datetime)

    message["data"]["start_datetime"] = new_start_datetime
    message["data"]["stop_datetime"] = new_stop_datetime

    offline_since = message["data"]["offline_since"]
    message["data"]["offline_since"] = create_datetime(offline_since)


def handle_settings(message: dict):
    """Transform settings object"""
    for key in SETTINGS:
        message["data"][key] = message["data"][key]["value"]

    set_smart_charging(
        message['data']['evse_id'], message["data"]["smart_charging"])


def handle_grid(message: dict):
    """Add grid total and avg to a message."""
    if "CURRENT" in message.get('object'):
        message["data"] = {}
        message["data"]["grid_actual_p1"] = message.pop('grid_actual_p1')
        message["data"]["grid_actual_p2"] = message.pop('grid_actual_p2')
        message["data"]["grid_actual_p3"] = message.pop('grid_actual_p3')

    current1 = message["data"]["grid_actual_p1"]
    current2 = message["data"]["grid_actual_p2"]
    current3 = message["data"]["grid_actual_p3"]

    c_avg = calculate_average_usage_from_phases((current1, current2, current3))
    message["data"]["grid_avg_current"] = c_avg
    c_max = max(current1, current2, current3)
    message["data"]["grid_max_current"] = c_max


def handle_setting_change(message: dict):
    """Change result to a boolean."""
    message["result"] = "true" in message["result"]["setting"]
    message["object"] = message["object"].replace("STATUS_SET_", "")


def handle_session_messages(message: dict):
    """handle session messages."""

    object_name = message["object"].replace(
        "STATUS_", "").replace("RECEIVED_", "")

    if "STATUS" in message["object"] and message["error"]:
        name = object_name.lower()
        error = message['error'].lower()
        evse_id = message['evse_id']
        message["error"] = f"{name} {error} for chargepoint: {evse_id}"
    message["object"] = object_name


def get_dummy_message(evse_id):
    """Return a CH_STATUS message with the current time as start_datetime"""
    return {
        'object': 'CH_STATUS',
        'data': {'start_datetime': datetime.now(TZ), 'evse_id': evse_id, }
    }


def get_next_reset_delta():
    """Returns the timedelta to the next midnight"""
    now = datetime.now(TZ)
    return now.replace(
        hour=0,
        minute=0,
        second=30
    ) + timedelta(days=1) - now
