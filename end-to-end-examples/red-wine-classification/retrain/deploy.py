import argparse
import logging

from servicefoundry import Build, Job, PythonBuild, Resources, Schedule

logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser()
parser.add_argument(
    "--workspace_fqn", type=str, required=True, help="fqn of the workspace to deploy to"
)
parser.add_argument(
    "--model_version_fqn",
    type=str,
    required=True,
    help="fqn of the model which you want to retrain",
)
args = parser.parse_args()

# servicefoundry uses this specification to automatically create a Dockerfile and build an image,
python_build = PythonBuild(
    python_version="3.9",
    command="python retrain.py",
)
env = {
    "TFY_HOST": os.getenv('TFY_HOST', default='https://app.truefoundry.com'),
    "TFY_API_KEY": os.getenv('TFY_API_KEY'),
    "MLF_MODEL_VERSION_FQN": args.model_version_fqn
}
job = Job(
    name="red-wine-retrain",
    image=Build(build_spec=python_build),
    env=env,
    resources=Resources(
        cpu_request=1, cpu_limit=1.5, memory_request=1000, memory_limit=1500
    ),
    trigger=Schedule(schedule="0 0 * * 0"),
)
job.deploy(workspace_fqn=args.workspace_fqn)
