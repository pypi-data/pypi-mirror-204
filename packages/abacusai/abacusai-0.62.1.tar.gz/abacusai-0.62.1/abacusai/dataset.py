from typing import Union

from .api_class import ParsingConfig
from .dataset_column import DatasetColumn
from .dataset_version import DatasetVersion
from .refresh_schedule import RefreshSchedule
from .return_class import AbstractApiClass


class Dataset(AbstractApiClass):
    """
        A dataset reference

        Args:
            client (ApiClient): An authenticated API Client instance
            datasetId (str): The unique identifier of the dataset.
            sourceType (str): The source of the Dataset. EXTERNAL_SERVICE, UPLOAD, or STREAMING.
            dataSource (str): Location of data. It may be a URI such as an s3 bucket or the database table.
            createdAt (str): The timestamp at which this dataset was created.
            ignoreBefore (str): The timestamp at which all previous events are ignored when training.
            ephemeral (bool): The dataset is ephemeral and not used for training.
            lookbackDays (int): Specific to streaming datasets, this specifies how many days worth of data to include when generating a snapshot. Value of 0 indicates leaves this selection to the system.
            databaseConnectorId (str): The Database Connector used.
            databaseConnectorConfig (dict): The database connector query used to retrieve data.
            connectorType (str): The type of connector used to get this dataset FILE or DATABASE.
            featureGroupTableName (str): The table name of the dataset's feature group
            applicationConnectorId (str): The Application Connector used.
            applicationConnectorConfig (dict): The application connector query used to retrieve data.
            incremental (bool): If dataset is an incremental dataset.
            isDocumentset (bool): If dataset is a documentset.
            extractBoundingBoxes (bool): Signifies whether to extract bounding boxes out of the documents. Only valid if is_documentset if True.
            mergeFileSchemas (bool): If the merge file schemas policy is enabled.
            latestDatasetVersion (DatasetVersion): The latest version of this dataset.
            schema (DatasetColumn): List of resolved columns.
            refreshSchedules (RefreshSchedule): List of schedules that determines when the next version of the dataset will be created.
    """

    def __init__(self, client, datasetId=None, sourceType=None, dataSource=None, createdAt=None, ignoreBefore=None, ephemeral=None, lookbackDays=None, databaseConnectorId=None, databaseConnectorConfig=None, connectorType=None, featureGroupTableName=None, applicationConnectorId=None, applicationConnectorConfig=None, incremental=None, isDocumentset=None, extractBoundingBoxes=None, mergeFileSchemas=None, schema={}, refreshSchedules={}, latestDatasetVersion={}):
        super().__init__(client, datasetId)
        self.dataset_id = datasetId
        self.source_type = sourceType
        self.data_source = dataSource
        self.created_at = createdAt
        self.ignore_before = ignoreBefore
        self.ephemeral = ephemeral
        self.lookback_days = lookbackDays
        self.database_connector_id = databaseConnectorId
        self.database_connector_config = databaseConnectorConfig
        self.connector_type = connectorType
        self.feature_group_table_name = featureGroupTableName
        self.application_connector_id = applicationConnectorId
        self.application_connector_config = applicationConnectorConfig
        self.incremental = incremental
        self.is_documentset = isDocumentset
        self.extract_bounding_boxes = extractBoundingBoxes
        self.merge_file_schemas = mergeFileSchemas
        self.schema = client._build_class(DatasetColumn, schema)
        self.refresh_schedules = client._build_class(
            RefreshSchedule, refreshSchedules)
        self.latest_dataset_version = client._build_class(
            DatasetVersion, latestDatasetVersion)

    def __repr__(self):
        return f"Dataset(dataset_id={repr(self.dataset_id)},\n  source_type={repr(self.source_type)},\n  data_source={repr(self.data_source)},\n  created_at={repr(self.created_at)},\n  ignore_before={repr(self.ignore_before)},\n  ephemeral={repr(self.ephemeral)},\n  lookback_days={repr(self.lookback_days)},\n  database_connector_id={repr(self.database_connector_id)},\n  database_connector_config={repr(self.database_connector_config)},\n  connector_type={repr(self.connector_type)},\n  feature_group_table_name={repr(self.feature_group_table_name)},\n  application_connector_id={repr(self.application_connector_id)},\n  application_connector_config={repr(self.application_connector_config)},\n  incremental={repr(self.incremental)},\n  is_documentset={repr(self.is_documentset)},\n  extract_bounding_boxes={repr(self.extract_bounding_boxes)},\n  merge_file_schemas={repr(self.merge_file_schemas)},\n  schema={repr(self.schema)},\n  refresh_schedules={repr(self.refresh_schedules)},\n  latest_dataset_version={repr(self.latest_dataset_version)})"

    def to_dict(self):
        """
        Get a dict representation of the parameters in this class

        Returns:
            dict: The dict value representation of the class parameters
        """
        return {'dataset_id': self.dataset_id, 'source_type': self.source_type, 'data_source': self.data_source, 'created_at': self.created_at, 'ignore_before': self.ignore_before, 'ephemeral': self.ephemeral, 'lookback_days': self.lookback_days, 'database_connector_id': self.database_connector_id, 'database_connector_config': self.database_connector_config, 'connector_type': self.connector_type, 'feature_group_table_name': self.feature_group_table_name, 'application_connector_id': self.application_connector_id, 'application_connector_config': self.application_connector_config, 'incremental': self.incremental, 'is_documentset': self.is_documentset, 'extract_bounding_boxes': self.extract_bounding_boxes, 'merge_file_schemas': self.merge_file_schemas, 'schema': self._get_attribute_as_dict(self.schema), 'refresh_schedules': self._get_attribute_as_dict(self.refresh_schedules), 'latest_dataset_version': self._get_attribute_as_dict(self.latest_dataset_version)}

    def create_version_from_file_connector(self, location: str = None, file_format: str = None, csv_delimiter: str = None, merge_file_schemas: bool = None, parsing_config: Union[dict, ParsingConfig] = None):
        """
        Creates a new version of the specified dataset.

        Args:
            location (str): External URI to import the dataset from. If not specified, the last location will be used.
            file_format (str): File format to be used. If not specified, the service will try to detect the file format.
            csv_delimiter (str): If the file format is CSV, use a specific CSV delimiter.
            merge_file_schemas (bool): Signifies if the merge file schema policy is enabled.
            parsing_config (ParsingConfig): Custom config for dataset parsing.

        Returns:
            DatasetVersion: The new Dataset Version created.
        """
        return self.client.create_dataset_version_from_file_connector(self.dataset_id, location, file_format, csv_delimiter, merge_file_schemas, parsing_config)

    def create_version_from_database_connector(self, object_name: str = None, columns: str = None, query_arguments: str = None, sql_query: str = None):
        """
        Creates a new version of the specified dataset.

        Args:
            object_name (str): The name/ID of the object in the service to query. If not specified, the last name will be used.
            columns (str): The columns to query from the external service object. If not specified, the last columns will be used.
            query_arguments (str): Additional query arguments to filter the data. If not specified, the last arguments will be used.
            sql_query (str): The full SQL query to use when fetching data. If present, this parameter will override object_name, columns, and query_arguments.

        Returns:
            DatasetVersion: The new Dataset Version created.
        """
        return self.client.create_dataset_version_from_database_connector(self.dataset_id, object_name, columns, query_arguments, sql_query)

    def create_version_from_application_connector(self, object_id: str = None, start_timestamp: int = None, end_timestamp: int = None):
        """
        Creates a new version of the specified dataset.

        Args:
            object_id (str): The ID of the object in the service to query. If not specified, the last name will be used.
            start_timestamp (int): The Unix timestamp of the start of the period that will be queried.
            end_timestamp (int): The Unix timestamp of the end of the period that will be queried.

        Returns:
            DatasetVersion: The new Dataset Version created.
        """
        return self.client.create_dataset_version_from_application_connector(self.dataset_id, object_id, start_timestamp, end_timestamp)

    def create_version_from_upload(self, file_format: str = None):
        """
        Creates a new version of the specified dataset using a local file upload.

        Args:
            file_format (str): File format to be used. If not specified, the service will attempt to detect the file format.

        Returns:
            Upload: Token to be used when uploading file parts.
        """
        return self.client.create_dataset_version_from_upload(self.dataset_id, file_format)

    def snapshot_streaming_data(self):
        """
        Snapshots the current data in the streaming dataset.

        Args:
            dataset_id (str): The unique ID associated with the dataset.

        Returns:
            DatasetVersion: The new Dataset Version created by taking a snapshot of the current data in the streaming dataset.
        """
        return self.client.snapshot_streaming_data(self.dataset_id)

    def set_column_data_type(self, column: str, data_type: str):
        """
        Set a Dataset's column type.

        Args:
            column (str): The name of the column.
            data_type (str): The type of the data in the column. Refer to the [guide on data types](https://api.abacus.ai/app/help/class/DataType) for more information. Note: Some ColumnMappings may restrict the options or explicitly set the DataType.

        Returns:
            Dataset: The dataset and schema after the data type has been set.
        """
        return self.client.set_dataset_column_data_type(self.dataset_id, column, data_type)

    def set_streaming_retention_policy(self, retention_hours: int = None, retention_row_count: int = None, ignore_records_before_timestamp: int = None):
        """
        Sets the streaming retention policy.

        Args:
            retention_hours (int): Number of hours to retain streamed data in memory.
            retention_row_count (int): Number of rows to retain streamed data in memory.
            ignore_records_before_timestamp (int): The Unix timestamp (in seconds) to use as a cutoff to ignore all entries sent before it
        """
        return self.client.set_streaming_retention_policy(self.dataset_id, retention_hours, retention_row_count, ignore_records_before_timestamp)

    def get_schema(self):
        """
        Retrieves the column schema of a dataset.

        Args:
            dataset_id (str): Unique string identifier of the dataset schema to look up.

        Returns:
            DatasetColumn: List of column schema definitions.
        """
        return self.client.get_dataset_schema(self.dataset_id)

    def refresh(self):
        """
        Calls describe and refreshes the current object's fields

        Returns:
            Dataset: The current object
        """
        self.__dict__.update(self.describe().__dict__)
        return self

    def describe(self):
        """
        Retrieves a full description of the specified dataset, with attributes such as its ID, name, source type, etc.

        Args:
            dataset_id (str): The unique ID associated with the dataset.

        Returns:
            Dataset: The dataset.
        """
        return self.client.describe_dataset(self.dataset_id)

    def list_versions(self, limit: int = 100, start_after_version: str = None):
        """
        Retrieves a list of all dataset versions for the specified dataset.

        Args:
            limit (int): The maximum length of the list of all dataset versions.
            start_after_version (str): The ID of the version after which the list starts.

        Returns:
            DatasetVersion: A list of dataset versions.
        """
        return self.client.list_dataset_versions(self.dataset_id, limit, start_after_version)

    def attach_to_project(self, project_id: str, dataset_type: str):
        """
        [DEPRECATED] Attach a dataset to the project.

        Use this method to attach a dataset that is already in the organization to another project. The dataset type is required to let the AI engine know what type of schema should be used.


        Args:
            project_id (str): Unique identifier of the project to attach the dataset to.
            dataset_type (str): Enum string representing the dataset type, associated with the use case of the project. Refer to the [Use Case Documentation](https://api.abacus.ai/app/help/useCases) for the supported dataset types per use case.

        Returns:
            Schema: An array of column descriptions.
        """
        return self.client.attach_dataset_to_project(self.dataset_id, project_id, dataset_type)

    def remove_from_project(self, project_id: str):
        """
        [DEPRECATED] Removes the dataset with the specified dataset from the project.

        Args:
            project_id (str): Unique string identifier of the project.
        """
        return self.client.remove_dataset_from_project(self.dataset_id, project_id)

    def delete(self):
        """
        Deletes the specified dataset from the organization.

        Args:
            dataset_id (str): Unique string identifier of the dataset to delete.
        """
        return self.client.delete_dataset(self.dataset_id)

    def wait_for_import(self, timeout=900):
        """
        A waiting call until dataset is imported.

        Args:
            timeout (int, optional): The waiting time given to the call to finish, if it doesn't finish by the allocated time, the call is said to be timed out.

        """
        latest_dataset_version = self.describe().latest_dataset_version
        if not latest_dataset_version:
            from .client import ApiException
            raise ApiException(409, 'This dataset does not have any versions')
        self.latest_dataset_version = latest_dataset_version.wait_for_import(
            timeout=timeout)
        return self

    def wait_for_inspection(self, timeout=None):
        """
        A waiting call until dataset is completely inspected.

        Args:
            timeout (int, optional): The waiting time given to the call to finish, if it doesn't finish by the allocated time, the call is said to be timed out.
        """
        latest_dataset_version = self.describe().latest_dataset_version
        if not latest_dataset_version:
            from .client import ApiException
            raise ApiException(409, 'This dataset does not have any versions')
        self.latest_dataset_version = latest_dataset_version.wait_for_inspection(
            timeout=timeout)
        return self

    def get_status(self):
        """
        Gets the status of the latest dataset version.

        Returns:
            str: A string describing the status of a dataset (importing, inspecting, complete, etc.).
        """
        return self.describe().latest_dataset_version.status

    def describe_feature_group(self):
        """
        Gets the feature group attached to the dataset.

        Returns:
            FeatureGroup: A feature group object.
        """
        return self.client.describe_feature_group_by_table_name(self.feature_group_table_name)

    def create_refresh_policy(self, cron: str):
        """
        To create a refresh policy for a dataset.

        Args:
            cron (str): A cron style string to set the refresh time.

        Returns:
            RefreshPolicy: The refresh policy object.
        """
        return self.client.create_refresh_policy(self.feature_group_table_name, cron, 'DATASET', dataset_ids=[self.id])

    def list_refresh_policies(self):
        """
        Gets the refresh policies in a list.

        Returns:
            List[RefreshPolicy]: A list of refresh policy objects.
        """
        return self.client.list_refresh_policies(dataset_ids=[self.id])
