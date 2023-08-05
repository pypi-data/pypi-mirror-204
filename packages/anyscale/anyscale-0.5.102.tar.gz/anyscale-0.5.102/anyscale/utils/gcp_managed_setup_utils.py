from click import ClickException
from googleapiclient.errors import HttpError

from anyscale.cli_logger import BlockLogger
from anyscale.utils.gcp_utils import GoogleCloudClientFactory


def create_workload_identity_pool(
    factory: GoogleCloudClientFactory,
    project_id: str,
    pool_id: str,
    display_name: str,
    description: str,
    logger: BlockLogger,
):
    """ Create a GCP Workload Identity Provider Pool. The functionality is not
    currently supported by GCP Deployment Manager.
    """
    # TODO (congding): 1) add default values to display_name and description 2) include service account info in description
    iam_service = factory.build("iam", "v1")

    parent = f"projects/{project_id}/locations/global"
    pool = {"displayName": display_name, "description": description}

    try:
        response = (
            iam_service.projects()
            .locations()
            .workloadIdentityPools()
            .create(parent=parent, workloadIdentityPoolId=pool_id, body=pool)
            .execute()
        )

        workload_identity_pool = response["name"].split("/operation")[0]
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
        raise ClickException("Failed to create Workload Identity Provider Pool")


def create_anyscale_aws_provider(
    factory: GoogleCloudClientFactory,
    project_id: str,
    pool_id: str,
    provider_id: str,
    aws_account_id: str,
    logger: BlockLogger,
):
    """ Create a GCP Workload Identity Provider for Anyscale cross account access.
    The functionality is notcurrently supported by GCP Deployment Manager.
    """
    # TODO (congding): add description/display name to provider
    # TODO (congding): make sure creating provider after the pool is created
    iam_service = factory.build("iam", "v1")

    parent = f"projects/{project_id}/locations/global/workloadIdentityPools/{pool_id}"
    provider = {"aws": {"accountId": aws_account_id}}

    try:
        response = (
            iam_service.projects()
            .locations()
            .workloadIdentityPools()
            .providers()
            .create(
                parent=parent, workloadIdentityPoolProviderId=provider_id, body=provider
            )
            .execute()
        )

        workload_identity_provider = response["name"].split("/operation")[0]
        logger.info(f"AWS provider created: {workload_identity_provider}")
        return workload_identity_provider
    except HttpError as e:
        if e.status_code == 409:
            logger.error(f"Provider {provider_id} already exists in pool {parent}.")
        else:
            logger.error(
                f"Error occurred when trying to build Workload Identity Provider Pool. Detailed: {e}"
            )
        raise ClickException("Failed to create Anyscale AWS Workload Identity Provider")
