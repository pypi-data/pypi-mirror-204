from typing import Optional

import click

from dnastack.alpha.cli.workbench.utils import _get_workflow_client
from dnastack.alpha.client.workflow.models import WorkflowCreate, WorkflowVersionCreate, WorkflowSource
from dnastack.http.session import JsonPatch
from dnastack.alpha.client.workflow.utils import WorkflowSourceLoader
from dnastack.cli.helpers.command.decorator import command
from dnastack.cli.helpers.command.spec import ArgumentSpec
from dnastack.cli.helpers.exporter import to_json, normalize
from dnastack.cli.helpers.iterator_printer import show_iterator, OutputFormat
from dnastack.common.json_argument_parser import *


@click.group('versions')
def alpha_workflow_versions_command_group():
    """ Workflow Versions API """


@click.group('workflows')
def alpha_workflows_command_group():
    """ Workflows API """


def _get_author_patch(authors: str) -> Union[JsonPatch, None]:
    if authors == "":
        return JsonPatch(path="/authors", op="remove")
    elif authors:
        return JsonPatch(path="/authors", op="replace", value=authors.split(","))
    return None


def _get_description_patch(description: str) -> Union[JsonPatch, None]:
    if description == "":
        return JsonPatch(path="/description", op="remove")
    elif description:
        if get_argument_type(description) == RAW_FILE_PARAM_TYPE:
            description = read_file_content(description, RAW_FILE_PARAM_TYPE)
        return JsonPatch(path="/description", op="replace", value=description)
    return None


def _get_replace_patch(path: str, value: str) -> Union[JsonPatch, None]:
    if value:
        return JsonPatch(path=path, op="replace", value=value)
    return None


@command(alpha_workflows_command_group,
         'list',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='source',
                 arg_names=['--source'],
                 help='An optional flag to filter the results to only include workflows from the defined source',
                 as_option=True

             ),
             ArgumentSpec(
                 name='include_deleted',
                 arg_names=['--include-deleted'],
                 help='An optional flag to include deleted workflows in the list',
                 as_option=True

             ),
         ]
         )
def list_workflows(context: Optional[str],
                   endpoint_id: Optional[str],
                   namespace: Optional[str],
                   source: Optional[WorkflowSource],
                   include_deleted: Optional[bool] = False):
    """
    List workflows
    """
    workflows_client = _get_workflow_client(context, endpoint_id, namespace)
    show_iterator(output_format=OutputFormat.JSON,
                  iterator=workflows_client.list_workflows(source=source, include_deleted=include_deleted))


@command(alpha_workflows_command_group,
         'describe',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='include_deleted',
                 arg_names=['--include-deleted'],
                 help='An optional flag to include deleted workflows in the list',
                 as_option=True

             ),
         ]
         )
def describe_workflows(context: Optional[str],
                       endpoint_id: Optional[str],
                       namespace: Optional[str],
                       workflows: List[str],
                       include_deleted: Optional[bool] = False):
    """
    Describe one or more workflows
    """
    workflows_client = _get_workflow_client(context, endpoint_id, namespace)
    described_workflows = [workflows_client.get_workflow(workflow_id, include_deleted=include_deleted) for workflow_id
                           in workflows]
    click.echo(to_json(normalize(described_workflows)))


@command(alpha_workflows_command_group,
         'create',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='name',
                 arg_names=['--name'],
                 help='An optional flag to show set a workflow name. If omitted, the name within the workflow will be used',
                 as_option=True

             ),
             ArgumentSpec(
                 name='description',
                 arg_names=['--description'],
                 help='An optional flag to set a description for the workflow'
                      ' You can specify a file by prepending "=@" to a path: =@<path>',
                 as_option=True

             )
         ]
         )
def create_workflow(context: Optional[str],
                    endpoint_id: Optional[str],
                    namespace: Optional[str],
                    name: Optional[str],
                    description: Optional[str],
                    source_files: List[str]):
    """
    Create a new workflow from the supplied FILES

    The first file ending in ".wdl" will be treated as the entrypoint for the entire workflow
    becoming the "PRIMARY_DECSRIPTOR". If there are any local imports in a WDL file they will be dynamically resolved
    relative to the entrypoint.

    Files that are not WDL files may be included in the request and will have their file type set as follows:

     - files ending in ".json" will be set to type: "TEST_FILE"

     - files ending in any other extension will be set to type "OTHER"

    """

    workflows_client = _get_workflow_client(context, endpoint_id, namespace)
    workflow_source = WorkflowSourceLoader(source_files)

    if description and get_argument_type(description) == RAW_FILE_PARAM_TYPE:
        description = read_file_content(description, RAW_FILE_PARAM_TYPE)

    create_request = WorkflowCreate(
        name=name,
        description=description,
        files=workflow_source.loaded_files
    )

    result = workflows_client.create_workflow(workflow_create_request=create_request)
    click.echo(to_json(normalize(result)))


@command(alpha_workflows_command_group,
         "delete",
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='force',
                 arg_names=['--force'],
                 help='Force the deletion without prompting for confirmation.',
                 as_option=True,
                 default=False
             ),
         ]
         )
def delete_workflow(context: Optional[str],
                    endpoint_id: Optional[str],
                    namespace: Optional[str],
                    workflow_id: str,
                    force: Optional[bool] = False):
    """
    Delete an existing workflow
    """
    workflows_client = _get_workflow_client(context, endpoint_id, namespace)
    workflow = workflows_client.get_workflow(workflow_id)
    if not force and not click.confirm(
            f'Do you want to delete "{workflow.name}"?'):
        return

    workflows_client.delete_workflow(workflow.internalId, workflow.etag)
    click.echo("Deleted...")


@command(alpha_workflows_command_group,
         "update",
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='name',
                 arg_names=['--name'],
                 help='The new name of the workflow',
                 as_option=True
             ),
             ArgumentSpec(
                 name='description',
                 arg_names=['--description'],
                 help='The new description of the workflow in markdown format.'
                      ' You can specify a file by prepending "=@" to a path: =@<path>. To'
                      ' unset the description the value should be ""',
                 as_option=True
             ),
             ArgumentSpec(
                 name='authors',
                 arg_names=['--authors'],
                 help='List of authors to update. This value can be a comma separated list, a file or JSON literal',
                 as_option=True
             ),
         ]
         )
def update_workflow(context: Optional[str],
                    endpoint_id: Optional[str],
                    namespace: Optional[str],
                    workflow_id: str,
                    name: Optional[str],
                    description: Optional[str],
                    authors: Optional[str]):
    """
    Update an existing workflow
    """
    workflows_client = _get_workflow_client(context, endpoint_id, namespace)
    workflow = workflows_client.get_workflow(workflow_id)

    patch_list = [
        _get_replace_patch("/name", name),
        _get_description_patch(description),
        _get_author_patch(authors)
    ]
    patch_list = [patch for patch in patch_list if patch]

    if patch_list:
        workflow = workflows_client.update_workflow(workflow_id, workflow.etag, patch_list)
        click.echo(to_json(normalize(workflow)))
    else:
        raise ValueError("Must specify at least one attribute to update")


@command(alpha_workflow_versions_command_group,
         'list',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='workflow',
                 arg_names=['--workflow', ],
                 help='The workflow id to add the version to.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='include_deleted',
                 arg_names=['--include-deleted'],
                 help='An optional flag to include deleted workflows in the list',
                 as_option=True

             ),
         ]
         )
def list_versions(context: Optional[str],
                  endpoint_id: Optional[str],
                  namespace: Optional[str],
                  workflow: str,
                  include_deleted: Optional[bool] = False
                  ):
    """
    List the available versions for the given workflow
    """
    workflows_client = _get_workflow_client(context, endpoint_id, namespace)
    show_iterator(output_format=OutputFormat.JSON,
                  iterator=workflows_client.list_workflow_versions(workflow_id=workflow,
                                                                   include_deleted=include_deleted))


@command(alpha_workflow_versions_command_group,
         'describe',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='workflow',
                 arg_names=['--workflow', ],
                 help='The workflow id to add the version to.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='include_deleted',
                 arg_names=['--include-deleted'],
                 help='An optional flag to include deleted workflows in the list',
                 as_option=True

             ),
         ]
         )
def describe_version(context: Optional[str],
                     endpoint_id: Optional[str],
                     namespace: Optional[str],
                     workflow: str,
                     versions: List[str],
                     include_deleted: Optional[bool] = False
                     ):
    """
    Describe one or more workflow versions for the given workflow
    """
    workflows_client = _get_workflow_client(context, endpoint_id, namespace)
    click.echo(to_json(normalize(
        [workflows_client.get_workflow_version(workflow_id=workflow, version_id=version_id,
                                               include_deleted=include_deleted) for version_id in versions]
    )))


@command(alpha_workflow_versions_command_group,
         "delete",
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='force',
                 arg_names=['--force'],
                 help='Force the deletion without prompting for confirmation.',
                 as_option=True,
                 default=False
             ),
             ArgumentSpec(
                 name='workflow_id',
                 arg_names=['--workflow'],
                 help='The id of the workflow',
                 as_option=True
             ),
         ]
         )
def delete_workflow_version(context: Optional[str],
                            endpoint_id: Optional[str],
                            namespace: Optional[str],
                            workflow_id: str,
                            version_id: str,
                            force: Optional[bool] = False):
    """
    Delete an existing workflow version
    """
    workflows_client = _get_workflow_client(context, endpoint_id, namespace)
    workflow = workflows_client.get_workflow(workflow_id)
    version = workflows_client.get_workflow_version(workflow_id, version_id)
    if not force and not click.confirm(
            f'Do you want to delete "{version.versionName}" from workflow "{workflow.name}"?'):
        return

    workflows_client.delete_workflow_version(workflow_id, version_id, version.etag)
    click.echo("Deleted...")


@command(alpha_workflow_versions_command_group,
         'create',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='workflow',
                 arg_names=['--workflow', ],
                 help='The workflow id to add the version to.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='name',
                 arg_names=['--name'],
                 help='The version name to create',
                 as_option=True
             ),
             ArgumentSpec(
                 name='description',
                 arg_names=['--description'],
                 help='An optional description for the workflow version in markdown format.'
                      ' You can specify a file by prepending "=@" to a path: =@<path>',
                 as_option=True
             )
         ]
         )
def add_version(context: Optional[str],
                endpoint_id: Optional[str],
                namespace: Optional[str],
                workflow: str,
                name: str,
                description: Optional[str],
                source_files: List[str]):
    """
    Add a new version to an existing workflow from the supplied FILES

    The first file ending in ".wdl" will be treated as the entrypoint for the entire workflow
    becoming the "PRIMARY_DECSRIPTOR". If there are any local imports in a WDL file they will be dynamically resolved
    relative to the entrypoint.

    Files that are not WDL files may be included in the request and will have their file type set as follows:

     - files ending in ".json" will be set to type: "TEST_FILE"

     - files ending in any other extension will be set to type "OTHER"

    """
    workflows_client = _get_workflow_client(context, endpoint_id, namespace)
    workflow_source = WorkflowSourceLoader(source_files)

    if description and get_argument_type(description) == RAW_FILE_PARAM_TYPE:
        description = read_file_content(description, RAW_FILE_PARAM_TYPE)

    create_request = WorkflowVersionCreate(
        versionName=name,
        description=description,
        files=workflow_source.loaded_files
    )

    result = workflows_client.create_version(workflow_id=workflow, workflow_version_create_request=create_request)
    click.echo(to_json(normalize(result)))


@command(alpha_workflow_versions_command_group,
         "update",
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='An optional flag to define the namespace to connect to. By default, the namespace will be '
                      'extracted from the users credentials.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='version_name',
                 arg_names=['--name'],
                 help='The new name of the workflow version',
                 as_option=True
             ),
             ArgumentSpec(
                 name='description',
                 arg_names=['--description'],
                 help='The new description of the workflow version in markdown format.'
                      ' You can specify a file by prepending "=@" to a path: =@<path>. To'
                      ' unset the description the value should be ""',
                 as_option=True
             ),
             ArgumentSpec(
                 name='authors',
                 arg_names=['--authors'],
                 help='List of authors to update. This value can be a comma separated list',
                 as_option=True
             ),
             ArgumentSpec(
                 name='workflow_id',
                 arg_names=['--workflow'],
                 help='The id of the workflow',
                 as_option=True
             ),
         ]
         )
def update_workflow_version(context: Optional[str],
                            endpoint_id: Optional[str],
                            namespace: Optional[str],
                            workflow_id: str,
                            version_id: str,
                            version_name: Optional[str],
                            description: Optional[str],
                            authors: Optional[str]):
    """
    Update an existing workflow
    """
    workflows_client = _get_workflow_client(context, endpoint_id, namespace)
    workflow_version = workflows_client.get_workflow_version(workflow_id, version_id)

    patch_list = [
        _get_replace_patch("/versionName", version_name),
        _get_description_patch(description),
        _get_author_patch(authors)
    ]
    patch_list = [patch for patch in patch_list if patch]

    if patch_list:
        workflow_version = workflows_client.update_workflow_version(workflow_id, version_id, workflow_version.etag,
                                                                    patch_list)
        click.echo(to_json(normalize(workflow_version)))
    else:
        raise ValueError("Must specify at least one attribute to update")


alpha_workflows_command_group.add_command(alpha_workflow_versions_command_group)
