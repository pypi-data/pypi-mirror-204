"""Exec module for managing ServiceAccountKeys."""
from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext

__func_alias__ = {"list_": "list"}
RESOURCE_TYPE = "iam.projects.service_accounts.key"
RESOURCE_TYPE_FULL = "gcp.iam.projects.service_accounts.key"


async def list_(hub, ctx, sa_resource_id: str, project: str = None):
    r"""Lists every ServiceAccountKey that belongs to a specific project.

    Args:
        sa_resource_id(str):
            Resource id of the service account following the pattern projects/{project}/serviceAccounts/{id}.
        project(str, Optional):
            The resource name of the project associated with the service accounts.
    """
    execution_context = ExecutionContext(
        resource_type="iam.projects.service_accounts.key",
        method_name="list",
        method_params={"ctx": ctx, "name": sa_resource_id},
    )

    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def get(
    hub,
    ctx,
    project: str = None,
    service_account_id: str = None,
    key_id: str = None,
    resource_id: str = None,
):
    r"""Returns the specified ServiceAccountKey resource.

    Args:
        project(str, Optional):
            Project ID for this request.
        service_account_id(str, Optional):
            Email or unique_id of the service account in GCP.
        key_id(str, Optional):
            Id of the service account key in GCP.
        resource_id(str, Optional):
            An identifier of the service account key in idem. Defaults to None.
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    if service_account_id and key_id:
        project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
        resource_id = (
            f"projects/{project}/serviceAccounts/{service_account_id}/keys/{key_id}"
        )
    elif not resource_id:
        result["result"] = False
        result["comment"] = [
            f"gcp.iam.projects.service_accounts.key#get(): either service_account_id and key_id or resource_id"
            f" should be specified."
        ]
        return result

    execution_context = ExecutionContext(
        resource_type="iam.projects.service_accounts.key",
        method_name="get",
        method_params={"ctx": ctx, "name": resource_id},
    )

    ret = await hub.tool.gcp.generate.generic_exec.execute(execution_context)

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result


async def upload(hub, ctx, service_account_id: str, public_key_data: str):
    r"""Uploads the public key portion of a key pair that you manage, and associates the public key with a service account key.
    After you upload the public key, you can use the private key from the key pair as a service account key.

    Args:
        service_account_id(str):
            Resource id of the service account

        public_key_data(str):
            The public key to associate with the service account. Must be an RSA public key that is wrapped in an X.509 v3 certificate. Include the first line, -----BEGIN CERTIFICATE-----, and the last line, -----END CERTIFICATE-----. A base64-encoded string.

    Examples:
        .. code-block: sls

            random-name:
              exec.run:
              - path: gcp.iam.projects.service_accounts.key.upload
              - kwargs:
                  service_account_id: projects/{...}/serviceAccounts/{...}
                  public_key_data: <base64-encoded X.509 v3 certificate>
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    if not service_account_id:
        result["result"] = False
        result["comment"] = [
            f"{RESOURCE_TYPE_FULL}#upload(): service_account_id is required"
        ]
        return result

    if not public_key_data:
        result["result"] = False
        result["comment"] = [
            f"{RESOURCE_TYPE_FULL}#upload(): public_key_data is required"
        ]
        return result

    execution_context = ExecutionContext(
        resource_type=RESOURCE_TYPE,
        method_name="upload",
        method_params={
            "ctx": ctx,
            "name": service_account_id,
            "body": {"public_key_data": public_key_data},
        },
    )

    ret = await hub.tool.gcp.generate.generic_exec.execute(execution_context)

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result


async def disable(hub, ctx, resource_id: str):
    r"""Disable a ServiceAccountKey. A disabled service account key can be re-enabled.

    Args:
        resource_id(str):
            Resource id of the service account key

    Examples:
        .. code-block: sls

            random-name:
              exec.run:
              - path: gcp.iam.projects.service_accounts.key.disable
              - kwargs:
                  resource_id: projects/{...}/serviceAccounts/{...}/keys/{...}
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    if not resource_id:
        result["result"] = False
        result["comment"] = [f"{RESOURCE_TYPE_FULL}#disable(): resource_id is required"]
        return result

    execution_context = ExecutionContext(
        resource_type=RESOURCE_TYPE,
        method_name="disable",
        method_params={"ctx": ctx, "name": resource_id},
    )

    ret = await hub.tool.gcp.generate.generic_exec.execute(execution_context)

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result


async def enable(hub, ctx, resource_id: str):
    r"""Enable a ServiceAccountKey.

    Args:
        resource_id(str):
            Resource id of the service account key

    Examples:
        .. code-block: sls

            random-name:
              exec.run:
              - path: gcp.iam.projects.service_accounts.key.enable
              - kwargs:
                  resource_id: projects/{...}/serviceAccounts/{...}/keys/{...}
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    if not resource_id:
        result["result"] = False
        result["comment"] = [f"{RESOURCE_TYPE_FULL}#enable(): resource_id is required"]
        return result

    execution_context = ExecutionContext(
        resource_type=RESOURCE_TYPE,
        method_name="enable",
        method_params={"ctx": ctx, "name": resource_id},
    )

    ret = await hub.tool.gcp.generate.generic_exec.execute(execution_context)

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result
