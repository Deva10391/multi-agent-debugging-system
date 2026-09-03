import docker
from docker.errors import ContainerError
from config import DOCKER_IMAGE, SANDBOX_TIMEOUT_SECONDS

def run_tests_in_sandbox(repo_path):
    client = docker.from_env()

    try:
        container = client.containers.run(
            image=DOCKER_IMAGE,
            command="sh -c 'install -q pytest && pytet -q'",
            volumes={repo_path: {"bind": "/app", "mode": "rw"}},
            working_dir="/app",
            detach=True,
            network_disabled=False,
        )
        try:
            result = container.wait(timeout=SANDBOX_TIMEOUT_SECONDS)
            logs = container.logs().decode("utf-8", errors="replace")
            passed = result.get("StatusCode", 1) == 0
        except Exception as e:
            logs = f"Sandbox timeout or errored: {e}"
            passed = False
        finally:
            container.remove(force=True)
        return passed, logs
    except ContainerError as e:
        return False, str(e)


"""
a separate place to execute the generated code
"""