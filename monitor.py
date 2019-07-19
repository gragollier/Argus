from slackclient import SlackClient
import yaml
from modules.HostMonitor import HostMonitor
from time import sleep
import asyncio

def send_slack(client: SlackClient, channel: str, message: str):
    print(f"Sending message {message} to channel {channel}")
    client.api_call("chat.postMessage", channel=channel, text=message)


async def manage_host_monitor(slack_client: SlackClient, channel: str, host_monitors: list, sleep_time: int):
    while True:
        await asyncio.sleep(sleep_time)
        for monitor in host_monitors:
            try:
                res = monitor.run()
                if len(res) != 0:
                    message = '\n'.join(res)
                    send_slack(slack_client, channel, message)
            except Exception as exception:
                send_slack(slack_client, channel, f"HostMonitor encountered an error: {exception}")


if __name__ == "__main__":
    print("Argus Started")

    config = yaml.safe_load(open('config.yaml'))
    slack_token = config['slack']['token']
    channel_id = config['slack']['channel_id']
    slack_client = SlackClient(slack_token)

    loop = asyncio.get_event_loop()

    host_monitors = HostMonitor.setup(config['host_monitor']['hosts'])

    print("Starting main event loop")
    # Register monitoring tasks
    loop.create_task(manage_host_monitor(slack_client, channel_id, host_monitors, config['host_monitor']['sleep_time']))
    loop.run_forever()
            