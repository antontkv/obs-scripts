import obspython as obs
from datetime import datetime

record_for = 60
record_interval = 540

def timestamp():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def start(props, prop):
    global record_interval
    global record_for

    obs.script_log(obs.LOG_INFO, f"{timestamp()} | Recording starts in {record_interval} seconds.")
    obs.timer_add(start_recording, record_interval * 1000)

def stop(props, prop):
    obs.script_log(obs.LOG_INFO, f"{timestamp()} | Stopping all timers.")
    obs.obs_frontend_recording_stop()
    obs.timer_remove(start_recording)
    obs.timer_remove(stop_recording)

def start_recording():
    obs.script_log(obs.LOG_INFO, f"{timestamp()} | Starting recording.")
    obs.timer_remove(start_recording)
    obs.obs_frontend_recording_start()
    obs.timer_add(stop_recording, record_for * 1000)

def stop_recording():
    obs.script_log(obs.LOG_INFO, f"{timestamp()} | Stopping recording.")
    obs.timer_remove(stop_recording)
    obs.obs_frontend_recording_stop()
    obs.timer_add(start_recording, record_interval * 1000)

def script_update(settings):
    global record_for
    global record_interval

    record_for = obs.obs_data_get_int(settings, "record_for")
    record_interval = obs.obs_data_get_int(settings, "record_interval")

    obs.timer_remove(start_recording)
    obs.timer_remove(stop_recording)

def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "record_for", 60)
    obs.obs_data_set_default_int(settings, "record_interval", 540)

def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_int(props, "record_for", "Record for (seconds)", 5, 3600, 1)
    obs.obs_properties_add_int(props, "record_interval", "Record Interval (seconds)", 5, 3600, 1)
    obs.obs_properties_add_button(props, "start_button", "Start", start)
    obs.obs_properties_add_button(props, "stop_button", "Stop", stop)

    return props

def script_description():
    return "Start and stop recording at the specified interval."
