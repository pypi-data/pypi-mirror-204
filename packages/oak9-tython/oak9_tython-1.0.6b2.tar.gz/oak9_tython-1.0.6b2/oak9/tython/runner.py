import json
import os
import sys
from io import StringIO
from typing import Protocol, runtime_checkable, Set, Optional, List
from core.services.tython_api_service import TythonApiService
from core.bp_metadata_utils.customer_blueprint_repo import CustomerBlueprintRepo
from core.bp_metadata_utils.python_source_file_utils import get_blueprint_classes
from core.types import Finding, Configuration
import core.utilities as Utilities

@runtime_checkable
class SupportsValidation(Protocol):
    def validate(self) -> Set[Finding]:
        """
        Entry point into component's validation logic
        """


class Runner:

    @staticmethod
    def run(validation_target: SupportsValidation):
        return validation_target.validate()


def main(argv):
    stdout = sys.stdout
    sys.stdout = runner_stdout = StringIO()

    args_path = None
    findings = set()

    try:

        if len(argv) > 0:
            args_path = argv[0]
        else:
            sys.stderr.write("Configuration path was not provided.")
            sys.exit(1)
        
        config = None
        try:
            args_file = open(args_path)
            args_obj = json.load(args_file)
            args_file.close()
            Utilities.verify_config_arguments(args_obj)
            config = Configuration(**args_obj)
        except:
            raise Exception("Runner arguments not found or could not be understood.")
                
        runner = Runner()

        blueprint_repo = CustomerBlueprintRepo(config.blueprint_package_path)

        # TODO: make this conditional on a CLI command
        # blueprint_repo.print_blueprint_summary()

        environment_id = TythonApiService.get_default_environment(config)
        request_id = TythonApiService.build_app(config, environment_id)
        runner_inputs = TythonApiService.fetch_graph_data(config, environment_id, request_id)

        # get all blueprint classes
        # TODO: filter out import of base Blueprint class
        blueprint_classes = []
        for path in blueprint_repo.blueprint_file_paths:
            blueprint_classes.extend(get_blueprint_classes(path))

        # Run each blueprint
        for blueprint in blueprint_classes:
            customer_blueprint = blueprint[1](graph=runner_inputs)
            # TODO: check usage guidelines to see if findings should be reported
            findings = runner.run(customer_blueprint)
            
        if config.mode == "apply" and findings:
            TythonApiService.apply_findings(config, findings, environment_id, request_id)
        
        sys.exit(0)

    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)

    finally:
        Utilities.persist_runner_output(args_path, runner_stdout, findings)
        sys.stdout = stdout


if __package__ == "":
    # Resulting path is the name of the wheel itself
    path = os.path.dirname(__file__)
    sys.path.insert(0, path)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
