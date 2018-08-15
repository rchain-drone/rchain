import logging
import pytest
import docker
import tools.random as random

docker_client = docker.from_env()

import collections
RChain = collections.namedtuple("RChain", ["network", "bootstrap", "peers"])


def create_network():
    network_name = f"rchain-{random.random_string(5)}"

    docker_client.networks.create(network_name, driver="bridge")

    return network_name

def remove_resources_by_network(network_name):
    """Remove resources by network name."""

    containers = docker_client.containers.list(all=True, filters={"name":f".{network_name}"})
    for container in containers:
        logging.info("=" * 100)
        logging.info(f"Docker container logs for {container.name}:")
        logging.info("=" * 100)
        logs = container.logs().decode('utf-8').splitlines()
        for log_line in logs:
            logging.info(f"{container.name}: {log_line}")

        logging.info("=" * 100)

    logging.info(f"Removing resources for docker network {network_name}")

    for container in containers:
        logging.info(f"Remove container {container.name}")
        container.remove(force=True, v=True)

    for network in docker_client.networks.list():
        if network_name == network.name:
            print(f"removing {network.name}")
            network.remove()

    logging.info("Remove unused volumes")
    docker_client.volumes.prune()

@pytest.fixture
def docker_network():
    logging.info("Setup")

    network_name = create_network()

    yield network_name

    logging.info("Teardown")
    remove_resources_by_network(network_name)

Config = collections.namedtuple( "Config",
                                 [
                                     "peer_count",
                                     "bootstrap_startup_timeout",
                                     "network_converge_timeout"
                                 ])
@pytest.fixture
def config(request):
    peer_count = int(request.config.getoption("--peer-count"))
    return Config(peer_count = peer_count,
                bootstrap_startup_timeout = 60,
                network_converge_timeout = 200
                )