import logging
import re
from collections import defaultdict
from squad.core.models import SuiteMetadata, Test, KnownIssue, Status, ProjectStatus, Suite
from squad.core.utils import join_name
from squad.core.tasks import RecordTestRunStatus
from squad.plugins import Plugin as BasePlugin


logger = logging.getLogger()


class MCUResults(BasePlugin):
    name = "MCU test results"

    def postprocess_testrun(self, testrun):
        regex = re.compile("TEST (?P<test_unit>.*) (?P<test_case_id>.*)=(?P<measurement>.*)")
        issues = defaultdict(list)
        for issue in KnownIssue.active_by_environment(testrun.environment):
            issues[issue.test_name].append(issue)
        for line in  testrun.log_file.split('\n'):
            result = regex.search(line)
            if result:
                suite_slug = result.group("test_unit")
                # found a potential test result
                test_name = result.group("test_case_id")
                expected_result = testrun.metadata.get(test_name, None)
                if expected_result:
                    # found a matching key in metadata
                    test_result = False  # set fail as default
                    measurement = result.group("measurement")
                    if result.group("measurement") == str(expected_result):
                        # test pass
                        test_result = True
                    metadata, _ = SuiteMetadata.objects.get_or_create(suite=suite_slug, name=test_name, kind='test')
                    suite, _ = Suite.objects.get_or_create(slug=suite_slug, project=testrun.build.project, defaults={"metadata": metadata})
                    full_name = join_name(suite_slug, test_name)
                    test_issues = issues.get(full_name, [])
                    Test.objects.create(
                        test_run=testrun,
                        suite_id=suite.id,
                        metadata=metadata,
                        result=test_result,
                        log=line,
                        has_known_issues=bool(test_issues),
                        build=testrun.build,
                        environment=testrun.environment,
                    )

        Status.objects.filter(test_run=testrun).all().delete()
        testrun.status_recorded = False
        RecordTestRunStatus()(testrun)

        ProjectStatus.create_or_update(testrun.build)
