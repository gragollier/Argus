from slackclient import SlackClient
import yaml
from modules.HostMonitor import HostMonitor
from time import sleep

EVENT_LOOP_SLEEP = 60 * 5 # Sleep time for main event loop in seconds

def send_slack(client: SlackClient, channel: str, message: str):
    print(f"Sending message {message} to channel {channel}")
    client.api_call("chat.postMessage", channel=channel, text=message)


if __name__ == "__main__":
    print("Argus Started")

    config = yaml.safe_load(open('config.yaml'))
    slack_token = config['slack']['token']
    channel_id = config['slack']['channel_id']
    slack_client = SlackClient(slack_token)

    host_monitors = []
    for host_type in config['hosts']:
        host_config = config['hosts'][host_type]
        if host_type == 'm1000e':
            host_monitors.append(HostMonitor(host_config['hosts'], host_config['username'], host_config['password'], chassis=host_config['chassis'], fan_threshold=host_config['fan_threshold']))
        else:
            host_monitors.append(HostMonitor(host_config['hosts'], host_config['username'], host_config['password']))

    print("Starting main event loop")
    while True:
        sleep(EVENT_LOOP_SLEEP)
        for monitor in host_monitors:
            res = monitor.run()
            if len(res) != 0:
                message = '\n'.join(res)
                send_slack(slack_client, channel_id, message)