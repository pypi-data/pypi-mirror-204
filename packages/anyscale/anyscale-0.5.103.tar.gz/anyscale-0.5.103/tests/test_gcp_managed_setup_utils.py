from unittest.mock import Mock, patch

from click import ClickException
import pytest

from anyscale.cli_logger import BlockLogger
from anyscale.utils.gcp_managed_setup_utils import (
    create_anyscale_aws_provider,
    create_workload_identity_pool,
    delete_workload_identity_pool,
    get_anyscale_gcp_access_service_acount,
    get_project_number,
    get_workload_identity_pool,
    wait_for_operation_completion,
)


@pytest.mark.parametrize(
    ("response", "expected_error_message"),
    [
        pytest.param(("200 OK", "project_get.json"), None, id="succeed",),
        pytest.param(
            ("403 Forbidden", None),
            "Error occurred when trying to access the project",
            id="error",
        ),
    ],
)
def test_get_project_number(setup_mock_server, response, expected_error_message):
    factory, tracker = setup_mock_server
    mock_project_id = "anyscale-bridge-deadbeef"
    mock_project_name = "projects/112233445566"
    tracker.reset({".*": [response]})
    if expected_error_message:
        with pytest.raises(ClickException) as e:
            get_project_number(factory, mock_project_id)
            e.match(expected_error_message)
    else:
        assert get_project_number(factory, mock_project_id) == mock_project_name


@pytest.mark.parametrize(
    ("response", "expected_error_message", "pool_exists"),
    [
        pytest.param(
            ("200 OK", "get_workload_identity_pool.json"), None, True, id="succeed",
        ),
        pytest.param(("404 Not Found", None), None, False, id="NotFound"),
        pytest.param(
            ("403 Forbidden", None),
            "Failed to get Workload Identity Provider Pool.",
            True,
            id="error",
        ),
    ],
)
def test_get_workload_identity_pool(
    setup_mock_server, response, pool_exists, expected_error_message
):
    factory, tracker = setup_mock_server
    mock_project_id = "anyscale-bridge-deadbeef"
    mock_pool_id = "mock-pool-id"
    tracker.reset({".*": [response]})
    if expected_error_message:
        with pytest.raises(ClickException) as e:
            get_workload_identity_pool(factory, mock_project_id, mock_pool_id)
            e.match(expected_error_message)
    else:
        if pool_exists:
            assert (
                get_workload_identity_pool(factory, mock_project_id, mock_pool_id)
                == mock_pool_id
            )
        else:
            assert (
                get_workload_identity_pool(factory, mock_project_id, mock_pool_id)
                is None
            )


@pytest.mark.parametrize(
    ("response", "expected_error_message", "service_account_exists"),
    [
        pytest.param(("200 OK", "get_service_account.json"), None, True, id="succeed",),
        pytest.param(("404 Not Found", None), None, False, id="NotFound"),
        pytest.param(
            ("403 Forbidden", None), "Failed to get service account: ", True, id="error"
        ),
    ],
)
def test_get_anyscale_gcp_access_service_acount(
    setup_mock_server, response, service_account_exists, expected_error_message
):
    factory, tracker = setup_mock_server
    mock_service_account = (
        "anyscale-access@anyscale-bridge-deadbeef.iam.gserviceaccount.com"
    )
    tracker.reset({".*": [response]})
    if expected_error_message:
        with pytest.raises(ClickException) as e:
            get_anyscale_gcp_access_service_acount(factory, mock_service_account)
            e.match(expected_error_message)
    else:
        if service_account_exists:
            assert (
                get_anyscale_gcp_access_service_acount(factory, mock_service_account)
                == mock_service_account
            )
        else:
            assert (
                get_anyscale_gcp_access_service_acount(factory, mock_service_account)
                is None
            )


@pytest.mark.parametrize(
    ("response", "expected_log_message"),
    [
        pytest.param(
            ("200 OK", "create_workload_identity_pool.json"), None, id="succeed",
        ),
        pytest.param(("409 conflict", None), "already exists", id="pool-exists",),
        pytest.param(("418 I'm a teapot", None), "Error occurred", id="error",),
    ],
)
def test_create_workload_identity_pool(
    setup_mock_server, response, expected_log_message, capsys
):
    factory, tracker = setup_mock_server
    mock_project_id = "anyscale-bridge-deadbeef"
    mock_project_number = "123456789"
    mock_pool_id = "mock-pool-id"
    display_name = "mock pool"
    description = "mock provider pool"
    tracker.reset({".*": [response]})
    if expected_log_message:
        with pytest.raises(ClickException) as e, patch.multiple(
            "anyscale.utils.gcp_managed_setup_utils",
            wait_for_operation_completion=Mock(),
        ):
            create_workload_identity_pool(
                factory,
                mock_project_id,
                mock_pool_id,
                BlockLogger(),
                display_name,
                description,
            )
        e.match("Failed to create Workload Identity Provider Pool")
        _, err = capsys.readouterr()
        assert expected_log_message in err

    else:
        with patch.multiple(
            "anyscale.utils.gcp_managed_setup_utils",
            wait_for_operation_completion=Mock(),
        ):
            assert (
                create_workload_identity_pool(
                    factory,
                    mock_project_id,
                    mock_pool_id,
                    BlockLogger(),
                    display_name,
                    description,
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
    mock_project_number = "123456789"
    mock_pool_id = f"projects/{mock_project_number}/locations/global/workloadIdentityPools/mock-pool-id"
    mock_provider_id = "mock-provider"
    mock_aws_account = "123456"
    mock_display_name = "mock provider"
    mock_org_id = "mock_org_id"
    tracker.reset({".*": [response]})
    if expected_error_message:
        with pytest.raises(ClickException) as e, patch.multiple(
            "anyscale.utils.gcp_managed_setup_utils",
            wait_for_operation_completion=Mock(),
        ):
            create_anyscale_aws_provider(
                factory,
                mock_org_id,
                mock_pool_id,
                mock_provider_id,
                mock_aws_account,
                mock_display_name,
                BlockLogger(),
            )
        e.match("Failed to create Anyscale AWS Workload Identity Provider")
        _, err = capsys.readouterr()
        assert expected_error_message in err
    else:
        with patch.multiple(
            "anyscale.utils.gcp_managed_setup_utils",
            wait_for_operation_completion=Mock(),
        ):
            assert (
                create_anyscale_aws_provider(
                    factory,
                    mock_org_id,
                    mock_pool_id,
                    mock_provider_id,
                    mock_aws_account,
                    mock_display_name,
                    BlockLogger(),
                )
                == f"{mock_pool_id}/providers/{mock_provider_id}"
            )


@pytest.mark.parametrize(
    ("response", "expected_log_message", "deletion_succeed"),
    [
        pytest.param(
            ("200 OK", "delete_workload_identity_pool.json"),
            "Deleted workload identity pool",
            True,
            id="succeed",
        ),
        pytest.param(
            ("403 Forbidden", None),
            "Error occurred when trying to delete workload identity pool",
            False,
            id="error1",
        ),
        pytest.param(
            ("404 Not Found", None),
            "Error occurred when trying to delete workload identity pool",
            False,
            id="error2",
        ),
    ],
)
def test_delete_workload_identity_pool(
    setup_mock_server, response, deletion_succeed, expected_log_message, capsys
):
    factory, tracker = setup_mock_server
    mock_project_number = "123456789"
    mock_pool_id = "mock-pool-id"
    mock_pool_name = f"projects/{mock_project_number}/locations/global/workloadIdentityPools/{mock_pool_id}"
    tracker.reset({".*": [response]})
    if deletion_succeed:
        with patch.multiple(
            "anyscale.utils.gcp_managed_setup_utils",
            wait_for_operation_completion=Mock(),
        ):
            delete_workload_identity_pool(
                factory, mock_pool_name, BlockLogger(),
            )
            _, log = capsys.readouterr()
            assert expected_log_message in log
    else:
        with pytest.raises(ClickException) as e, patch.multiple(
            "anyscale.utils.gcp_managed_setup_utils",
            wait_for_operation_completion=Mock(),
        ):
            delete_workload_identity_pool(
                factory, mock_pool_name, BlockLogger(),
            )
            e.match(expected_log_message)


@pytest.mark.parametrize("service_type", ["workload_identity_pool", "provider"])
@pytest.mark.parametrize(
    ("response", "expected_error_message"),
    [
        pytest.param(
            ("200 OK", "create_workload_identity_pool.json"),
            "did not complete within the timeout period",
            id="timeout",
        ),
        pytest.param(("200 OK", "operation_completed.json"), None, id="succeed",),
        pytest.param(
            ("200 OK", "operation_error.json"), "encountered an error", id="error",
        ),
    ],
)
def test_wait_for_operation_completion(
    setup_mock_server, response, expected_error_message, service_type
):
    factory, tracker = setup_mock_server
    mock_project_name = "projects/112233445566"
    mock_pool_id = "mock-pool-id"
    mock_provider_id = "mock-provider"
    if service_type == "workload_identity_pool":
        service = (
            factory.build("iam", "v1").projects().locations().workloadIdentityPools()
        )
        mock_operation_id = f"{mock_project_name}/locations/global/workloadIdentityPools/{mock_pool_id}/operations/mock_operation_id"
    elif service_type == "provider":
        service = (
            factory.build("iam", "v1")
            .projects()
            .locations()
            .workloadIdentityPools()
            .providers()
        )
        mock_operation_id = f"{mock_project_name}/locations/global/workloadIdentityPools/{mock_pool_id}/providers/{mock_provider_id}/operations/mock_operation_id"
    tracker.reset({".*": [response]})
    if expected_error_message:
        with patch.multiple(
            "anyscale.utils.gcp_managed_setup_utils.time",
            time=Mock(side_effect=[1, 1, None, None, 11]),  # only iterates once
            sleep=Mock(),
        ), pytest.raises(ClickException) as e:
            wait_for_operation_completion(
                service, mock_operation_id, "test", timeout=1, polling_interval=10
            )
            e.match(expected_error_message)
    else:
        with patch.multiple(
            "anyscale.utils.gcp_managed_setup_utils.time",
            time=Mock(side_effect=[1, 1, None, None, 11]),  # only iterates once
            sleep=Mock(),
        ):
            assert (
                wait_for_operation_completion(
                    service, mock_operation_id, "test", timeout=1, polling_interval=1
                )
                is None
            )
