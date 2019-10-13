from slackclient import SlackClient
import yaml
from modules import *
from time import sleep
from typing import List
import asyncio


def send_slack(client: SlackClient, channel: str, message: str):
    print(f"Sending message {message} to channel {channel}")
    client.api_call("chat.postMessage", channel=channel, text=message)


async def manage_module(slack_client: SlackClient, channel: str, host_monitors: List[BaseModule], sleep_time: int):
    while True:
        await asyncio.sleep(sleep_time)
        for monitor in host_monitors:
            try:
                res = monitor.run()
                if len(res) != 0:
                    message = '\n'.join(res)
                    send_slack(slack_client, channel, message)
            except Exception as exception:
                send_slack(slack_client, channel, f"{monitor.__class__.__name__} encountered an error: {exception}")


if __name__ == "__main__":
    print("Argus Started")

    config = yaml.safe_load(open('config.yaml'))
    slack_token = config['slack']['token']
    channel_id = config['slack']['channel_id']
    slack_client = SlackClient(slack_token)

    loop = asyncio.get_event_loop()

    modules = {
        'host_monitor': HostMonitor,
        'ip_monitor': IPMonitor,
        'http_monitor': HttpMonitor
        }

    for (module_name, module_class) in modules.items():
        if module_name in config.keys():
            monitors = module_class.setup(config[module_name]['monitors'])
            loop.create_task(manage_module(slack_client, channel_id, monitors, config[module_name]['sleep_time']))

    print("Starting main event loop")
    loop.run_forever()
