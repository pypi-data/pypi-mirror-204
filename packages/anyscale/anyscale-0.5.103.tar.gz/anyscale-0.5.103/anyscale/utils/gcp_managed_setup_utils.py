import time
from typing import Any

from click import ClickException
from google.api_core.exceptions import Forbidden, NotFound, PermissionDenied
from googleapiclient.errors import HttpError

from anyscale.cli_logger import BlockLogger
from anyscale.utils.gcp_utils import GoogleCloudClientFactory


def get_project_number(factory: GoogleCloudClientFactory, project_id: str):
    project_client = factory.resourcemanager_v3.ProjectsClient()
    try:
        project = project_client.get_project(name=f"projects/{project_id}")
        return project.name  # format: "/projects/{project_number}"
    except (NotFound, PermissionDenied, Forbidden) as e:
        raise ClickException(
            f"Error occurred when trying to access the project {project_id}: {e}"
        )


def get_workload_identity_pool(
    factory: GoogleCloudClientFactory, project_id: str, pool_id: str,
):
    workload_identity_pool_client = (
        factory.build("iam", "v1").projects().locations().workloadIdentityPools()
    )

    try:
        workload_identity_pool_client.get(
            name=f"projects/{project_id}/locations/global/workloadIdentityPools/{pool_id}"
        ).execute()
        return pool_id
    except HttpError as e:
        if e.status_code == 404:
            # workload identity pool not found
            return None
        else:
            raise ClickException(f"Failed to get Workload Identity Provider Pool. {e}")


def get_anyscale_gcp_access_service_acount(
    factory: GoogleCloudClientFactory, anyscale_access_service_account: str,
):
    service_account_client = factory.build("iam", "v1").projects().serviceAccounts()

    try:
        service_account_client.get(
            name=f"projects/-/serviceAccounts/{anyscale_access_service_account}"
        ).execute()
        return anyscale_access_service_account
    except HttpError as e:
        if e.status_code == 404:
            # service account not found
            return None
        else:
            raise ClickException(f"Failed to get service account: {e}")


def create_workload_identity_pool(
    factory: GoogleCloudClientFactory,
    project_id: str,
    pool_id: str,
    logger: BlockLogger,
    display_name: str = "a workload identity pool",
    description: str = "a workload identity pool",
):
    """ Create a GCP Workload Identity Provider Pool. The functionality is not
    currently supported by GCP Deployment Manager.
    """
    workload_identity_pool_client = (
        factory.build("iam", "v1").projects().locations().workloadIdentityPools()
    )

    parent = f"projects/{project_id}/locations/global"
    pool = {"displayName": display_name, "description": description}

    try:
        create_workload_identity_pool_operation = workload_identity_pool_client.create(
            parent=parent, workloadIdentityPoolId=pool_id, body=pool
        ).execute()

        wait_for_operation_completion(
            workload_identity_pool_client,
            create_workload_identity_pool_operation["name"],
            description="creating workload identity provider pool",
        )

        workload_identity_pool = create_workload_identity_pool_operation["name"].split(
            "/operation"
        )[0]
        logger.info(f"Workload Identity Pool created: {workload_identity_pool}")
        return workload_identity_pool
    except HttpError as e:
        if e.status_code == 409:
            logger.error(
                f"Provider Pool {pool_id} already exists in project {project_id}."
            )
        else:
            logger.error(
                f"Error occurred when trying to build Workload Identity Provider Pool. Detailed: {e}"
            )
        raise ClickException("Failed to create Workload Identity Provider Pool. ")


def create_anyscale_aws_provider(
    factory: GoogleCloudClientFactory,
    organization_id: str,
    pool_id: str,
    provider_id: str,
    aws_account_id: str,
    display_name: str,
    logger: BlockLogger,
):
    """ Create a GCP Workload Identity Provider for Anyscale cross account access.
    The functionality is notcurrently supported by GCP Deployment Manager.
    """
    provider_client = (
        factory.build("iam", "v1")
        .projects()
        .locations()
        .workloadIdentityPools()
        .providers()
    )

    parent = pool_id
    provider = {
        "aws": {"accountId": aws_account_id},
        "name": provider_id,
        "displayName": display_name,
        "description": "provider for Anyscale access",
        "attributeMapping": {
            "attribute.aws_role": "assertion.arn.contains('assumed-role') ? assertion.arn.extract('{account_arn}assumed-role/') + 'assumed-role/' + assertion.arn.extract('assumed-role/{role_name}/') : assertion.arn",
            "google.subject": "assertion.arn",
            "attribute.arn": "assertion.arn",
        },
        "attributeCondition": f"google.subject.startsWith('arn:aws:sts::{aws_account_id}:assumed-role/gcp_if_{organization_id}')",
    }

    try:
        response = provider_client.create(
            parent=parent, workloadIdentityPoolProviderId=provider_id, body=provider
        ).execute()
        wait_for_operation_completion(
            provider_client,
            response["name"],
            description="creating workload identity provider",
        )
        workload_identity_provider = response["name"].split("/operation")[0]
        logger.info(f"Anyscale provider created: {workload_identity_provider}")
        return workload_identity_provider
    except HttpError as e:
        if e.status_code == 409:
            logger.error(f"Provider {provider_id} already exists in pool {parent}.")
        else:
            logger.error(
                f"Error occurred when trying to build Workload Identity Provider Pool. Detailed: {e}"
            )
        raise ClickException("Failed to create Anyscale AWS Workload Identity Provider")


def delete_workload_identity_pool(
    factory: GoogleCloudClientFactory, pool_name: str, logger: BlockLogger
):
    service = factory.build("iam", "v1").projects().locations().workloadIdentityPools()

    # we can directly delete the pool even if there're providers in it
    try:
        delete_pool_operation = service.delete(name=pool_name).execute()
        wait_for_operation_completion(
            service,
            delete_pool_operation["name"],
            "deleting workload identity provider pool",
        )
        logger.info(f"Deleted workload identity pool: {pool_name}")
    except HttpError as e:
        raise ClickException(
            f"Error occurred when trying to delete workload identity pool {pool_name}: {e}. Please delete the resources by yourself."
        )


def wait_for_operation_completion(
    service: Any,
    operation_id: str,
    description: str = "Operation",
    timeout: int = 300,
    polling_interval: int = 3,
) -> None:
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_operation = service.operations().get(name=operation_id).execute()
        if current_operation.get("done", False):
            if "error" in current_operation:
                raise ClickException(
                    f"{description} encountered an error: {current_operation['error']}"
                )
            break
        time.sleep(polling_interval)
    else:
        raise ClickException(
            f"{description} did not complete within the timeout period ({timeout}s)"
        )
