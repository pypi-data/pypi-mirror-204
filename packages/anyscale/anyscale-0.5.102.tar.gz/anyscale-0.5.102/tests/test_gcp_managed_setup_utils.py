from click import ClickException
import pytest

from anyscale.cli_logger import BlockLogger
from anyscale.utils.gcp_managed_setup_utils import (
    create_anyscale_aws_provider,
    create_workload_identity_pool,
)


@pytest.mark.parametrize(
    ("response", "expected_error_message"),
    [
        pytest.param(
            ("200 OK", "create_workload_identity_pool.json"), None, id="succeed",
        ),
        pytest.param(("409 conflict", None), "already exists", id="pool-exists",),
        pytest.param(("418 I'm a teapot", None), "Error occurred", id="error",),
    ],
)
def test_create_workload_identity_pool(
    setup_mock_server, response, expected_error_message, capsys
):
    factory, tracker = setup_mock_server
    mock_project_id = "anyscale-bridge-deadbeef"
    mock_project_number = "123456789"
    mock_pool_id = "mock-pool-id"
    display_name = "mock pool"
    description = "mock provider pool"
    tracker.reset({".*": [response]})
    if expected_error_message:
        with pytest.raises(ClickException) as e:
            create_workload_identity_pool(
                factory,
                mock_project_id,
                mock_pool_id,
                display_name,
                description,
                BlockLogger(),
            )
        e.match("Failed to create Workload Identity Provider Pool")
        _, err = capsys.readouterr()
        assert expected_error_message in err
    else:
        assert (
            create_workload_identity_pool(
                factory,
                mock_project_id,
                mock_pool_id,
                display_name,
                description,
                BlockLogger(),
            )
            == f"projects/{mock_project_number}/locations/global/workloadIdentityPools/{mock_pool_id}"
        )


@pytest.mark.parametrize(
    ("response", "expected_error_message"),
    [
        pytest.param(
            ("200 OK", "create_workload_identity_provider.json"), None, id="succeed",
        ),
        pytest.param(("409 conflict", None), "already exists", id="pool-exists",),
        pytest.param(("404 Not Found", None), "Error occurred", id="error",),
    ],
)
def test_create_anyscale_aws_provider(
    setup_mock_server, response, expected_error_message, capsys
):
    factory, tracker = setup_mock_server
    mock_project_id = "anyscale-bridge-deadbeef"
    mock_project_number = "123456789"
    mock_pool_id = "mock-pool-id"
    mock_provider_id = "mock-provider"
    mock_aws_account = "123456"
    tracker.reset({".*": [response]})
    if expected_error_message:
        with pytest.raises(ClickException) as e:
            create_anyscale_aws_provider(
                factory,
                mock_project_id,
                mock_pool_id,
                mock_provider_id,
                mock_aws_account,
                BlockLogger(),
            )
        e.match("Failed to create Anyscale AWS Workload Identity Provider")
        _, err = capsys.readouterr()
        assert expected_error_message in err
    else:
        assert (
            create_anyscale_aws_provider(
                factory,
                mock_project_id,
                mock_pool_id,
                mock_provider_id,
                mock_aws_account,
                BlockLogger(),
            )
            == f"projects/{mock_project_number}/locations/global/workloadIdentityPools/{mock_pool_id}/providers/{mock_provider_id}"
        )
