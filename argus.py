from slackclient import SlackClient
import yaml
from modules import *
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


async def manage_ip_monitor(slack_client: SlackClient, channel: str, ip_monitor: IPMonitor, sleep_time: int):
    while True:
        try:
            res = ip_monitor.run()
            if len(res) != 0:
                message = '\n'.join(res)
                send_slack(slack_client, channel, message)
        except Exception as exception:
            send_slack(slack_client, channel, f"IPMonitor encountered an error: {exception}")
        await asyncio.sleep(sleep_time)


async def manage_http_monitor(slack_client: SlackClient, channel: str, https_monitors: list, sleep_time: int):
    while True:
        for monitor in https_monitors:
            try:
                res = monitor.run()
                if len(res) != 0:
                    message = '\n'.join(res)
                    send_slack(slack_client, channel, message)
            except Exception as exception:
                send_slack(slack_client, channel, f"HttpMonitor encountered an error: {exception}")
        await asyncio.sleep(sleep_time)

if __name__ == "__main__":
    print("Argus Started")

    config = yaml.safe_load(open('config.yaml'))
    slack_token = config['slack']['token']
    channel_id = config['slack']['channel_id']
    slack_client = SlackClient(slack_token)

    loop = asyncio.get_event_loop()

    if ('host_monitor' in config.keys() and 'hosts' in config['host_monitor'].keys()):
        host_monitors = HostMonitor.setup(config['host_monitor']['hosts'])
        loop.create_task(manage_host_monitor(slack_client, channel_id, host_monitors, config['host_monitor']['sleep_time']))
    if ('ip_monitor' in config.keys() and 'hosts' in config['ip_monitor'].keys()):
        ip_monitor = IPMonitor(config['ip_monitor']['hosts'])
        loop.create_task(manage_ip_monitor(slack_client, channel_id, ip_monitor, config['ip_monitor']['sleep_time']))
    if ('http_monitor' in config.keys() and 'monitors' in config['http_monitor'].keys()):
        http_monitors = HttpMonitor.setup(config['http_monitor']['monitors'].values())
        loop.create_task(manage_http_monitor(slack_client, channel_id, http_monitors, config['http_monitor']['sleep_time']))

    print("Starting main event loop")
    loop.run_forever()
            