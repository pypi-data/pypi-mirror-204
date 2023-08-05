import logging
from enum import Enum
from typing import List, Dict

from google.protobuf.json_format import MessageToDict
from google.protobuf.struct_pb2 import Struct

from terrascope.sdk.builder.toi import Frequency


class DataType(Enum):
    PINGS = "pings"
    DEVICE_TRACKS = "device_tracks"
    DEVICE_VISITS = "device_visits"
    OPTICAL_IMAGERY = "optical_imagery"
    OBJECT_DETECTION = "object_detection"
    MULTICLASS_OBJECT_DETECTION = "multiclass_object_detection"
    SPOT_MOSAIC = "spot_mosaic"
    PSSCENE = "psscene"
    SKYSAT = "skysat"
    POPULATION = "population"
    PROXIMITY_ZONE_UDC = "proximity_zone_udc"
    HEURISTIC_JUMPS = "heuristic_jumps"
    NAVIGATIONAL_QUALITY_INDICATORS = "navigational_quality_indicators"
    GNSS_CLUSTERS = "gnss_clusters"
    CROP_CIRCLES = "crop_circles"
    TRACEABILITY_CLUSTERS = "traceability_clusters"
    TRACEABILITY_HEATMAP = "traceability_heatmap"
    UDC_HEATMAP = "unique_device_count_heatmap"
    UDC = "unique_device_count"


class DataSource(Enum):
    # Ping Sources
    GEOLOCATION = "geolocation_pings"
    SAFEGRAPH = "safegraph_pings"
    XMODE = "xmode_pings"
    CUEBIQ = "cuebiq_pings"
    BLOGWATCHER = "blogwatcher_pings"
    SPIRE = "spire_pings"
    SPIRE_NMEA = "spire-nmea_pings"
    CUEBIQ_WORKBENCH = "cuebiq-workbench_pings"
    WEJO = "wejo_pings"
    HAWKEYE360 = "hawkeye360_pings"
    OTONOMO = "otonomo_pings"
    ADSBX = "adsbx_pings"
    EXACTEARTH = "exact-earth_pings"
    EXACTEARTH_NMEA = "exact-earth_nmea-pings"

    # Imagery Sources
    IMAGERY = "imagery_imagery"
    PLANET_REORTHOTILE = "planet_REOrthoTile"
    PLANET_PSORTHOTILE = "planet_OSOrthoTile"
    PLANET_PSSCENE4BAND = "planet_PSScene4Band"
    PLANET_SKYSATSCENE = "planet_SkySatScene"
    PLANET_SKYSATCOLLECT = "planet_SkySatCollect"
    AIRBUS_SPOT7 = "airbus_SPOT7"
    AIRBUS_PHR1A = "airbus_PHR1A"
    AIRBUS_PHR1B = "airbus_PHR1B"


class ReleaseStatus(Enum):
    DEV = "DEV"
    QA = "QA"
    STAGE = "STAGE"
    PROD = "PROD"


class InterfaceType(Enum):
    SYNCHRONOUS_TASK_HTTP_WORKER = "SYNCHRONOUS_TASK_HTTP_WORKER"
    FILESYSTEM_TASK_WORKER = "FILESYSTEM_TASK_WORKER"
    NO_OP_WORKER = "NO_OP_WORKER"


class ParallelType(Enum):
    AOI = "AOI"
    TIME_RANGE = "TIME_RANGE"


class PermissionType(Enum):
    ALLOWED = 'Allowed'
    DISALLOWED = 'Disallowed'


class AlgorithmManifest:
    """
    This is a basic builder to help build a factories in a safe way instead of managing json configuration
    files. This includes all the methods to incrementally build out an algorithm manifest proto struct that can be
    used for an algorithm.

    REQUIRED Methods:
    The following methods have to be run in sequence. I don't have a better way to do this yet so for now we will just
    call these methods. Each time a new algorithm manifest is need use the following sequence.
    - metadata_required()
    - interface_required()
    - inputs_add_data_type(): can call this more than once, need AT LEAST 1
    - container_parameters_required()
    - outputs_add_data_types(): can call more than once, need AT LEAST 1

    """

    def __init__(self):
        self.__metadata = {
            "metadata": {}
        }
        self.__interface = {
            "interface": {}
        }
        self.__inputs = []
        self.container_parameters = {
            "container_parameters": {}
        }
        self.__parameters = {
            "parameters": []
        }
        self.__grouping = {
            "grouping": {}
        }
        self.__parallelization = {
            "parallelization": {
                "dimensions": [],
                "configuration": {}
            }
        }
        self.__restrictions = {
            "restrictions": {}
        }
        self.__outputs = {
            "outputs": {}
        }
        self.__performance_metrics = {
            "performance_metrics": {}
        }
        self.__manifest_version = {
            "manifest_version": "0.1.0"
        }
        self.__required = {
            "metadata": {
                "description": False,
                "version": False
            },
            "interface": {
                "interface_type": False
            },
            "inputs": False,
            "container_parameters": {
                "image": False,
                "command": False
            },
            "outputs": {
                "output_data_types": False,
                "observation_value_columns": False
            },
            "manifest_version": True

        }

    # Metadata
    def metadata_required(self, description: str, version: str):
        self.metadata_description(description=description)
        self.metadata_version(version=version)

    def manifest_version(self, manifest_version: str):
        self.__manifest_version['manifest_version'] = manifest_version
        self.__required['manifest_version'] = True

    def metadata_description(self, description: str):
        self.__metadata['metadata']['description'] = description
        self.__required['metadata']['description'] = True

    def metadata_version(self, version: str):
        self.__metadata['metadata']['version'] = version
        self.__required['metadata']['version'] = True

    def metadata_indicator(self, indicator: str):
        self.__metadata['metadata']['indicator'] = indicator

    def metadata_tags(self, tags: List):
        self.__metadata['metadata']['tags'] = tags

    # Interface
    def interface_required(self, interface_type: InterfaceType):
        self.interface_interface_type(interface_type=interface_type)

    def interface_interface_type(self, interface_type: InterfaceType):
        self.__interface['interface']["interface_type"] = interface_type.value
        self.__required['interface']['interface_type'] = True

    def interface_adapter(self, adapter: str):
        self.__interface['interface']['adapter'] = adapter

    # Inputs
    def inputs_add_data_type(self, data_type_name: DataType, **kwargs):
        """
        [REQUIRED]

        Adds data types this algorithm is allowed to have as inputs.

        :param data_type_name:
        :param kwargs:
        :return:
        """
        entry = {
            "data_type_name": data_type_name.value
        }
        if 'min_count' in kwargs.keys():
            entry['min_count'] = kwargs['min_count']
        if 'max_count' in kwargs.keys():
            entry['max_count'] = kwargs['max_count']
        if 'parameters' in kwargs.keys():
            entry['parameters'] = kwargs['parameters']

        self.__inputs.append(entry.copy())
        self.__required['inputs'] = True

    # Container Parameters
    def container_parameters_required(self, image: str, command: List):
        self.container_parameters_image(image=image)
        self.container_parameters_command(command=command)

    def container_parameters_image(self, image: str):
        self.container_parameters['container_parameters']['image'] = image
        self.__required['container_parameters']['image'] = True

    def container_parameters_command(self, command: List):
        self.container_parameters['container_parameters']['command'] = command
        self.__required['container_parameters']['command'] = True

    def container_parameters_resource_request(self, **kwargs):
        if 'resource_request' not in self.container_parameters['container_parameters'].keys():
            self.container_parameters['container_parameters']['resource_request'] = {}

        if 'gpu' in kwargs.keys():
            self.container_parameters['container_parameters']['resource_request']['gpu'] = kwargs['gpu']
        if 'memory_gb' in kwargs.keys():
            self.container_parameters['container_parameters']['resource_request']['memory_gb'] = kwargs['memory_gb']
        if 'cpu_millicore' in kwargs.keys():
            self.container_parameters['container_parameters']['resource_request']['cpu_millicore'] = kwargs['cpu_millicore']

    # Parameters
    def parameter_add(self, **kwargs):
        assert 'description' in kwargs.keys()
        entry = {}
        if 'name' in kwargs.keys():
            entry['name'] = kwargs['name']
        if 'type' in kwargs.keys():
            entry['type'] = kwargs['type']
        if 'unit' in kwargs.keys():
            entry['unit'] = kwargs['unit']
        if 'description' in kwargs.keys():
            entry['description'] = kwargs['description']
        if 'min' in kwargs.keys():
            entry['min'] = kwargs['min']
        if 'max' in kwargs.keys():
            entry['max'] = kwargs['max']
        if 'allowed_values' in kwargs.keys():
            entry['allowed_values'] = kwargs['allowed_values']
        if 'default' in kwargs.keys():
            entry['default'] = kwargs['default']

        self.__parameters['parameters'].append(entry.copy())

    # Grouping
    def grouping_frequency(self, frequency: str, value: int):
        assert isinstance(value, int)
        assert isinstance(frequency, str)
        self.__grouping['grouping']['frequency'] = frequency
        self.__grouping['grouping']['value'] = value

    # Parallelization
    def parallelization_add_dimension(self, and_set: List):
        self.__parallelization['parallelization']['dimensions'].append(and_set)

    def parallelization_add_configuration(self, config: Dict):
        self.__parallelization['parallelization']['configuration'].update(config)

    # Restrictions
    def restriction_spatial(self, permission_type: PermissionType,
                            overridable: bool,
                            geometry):
        self.__restrictions['spatial_restriction']['permission_type'] = permission_type
        self.__restrictions['spatial_restriction']['overridable'] = overridable
        self.__restrictions['spatial_restriction']['geometry'] = geometry

    def restriction_temporal_restriction(self, tois: List):
        self.__restrictions['temporal_restriction'] = tois

    def restriction_size(self):
        # TODO
        pass

    # Outputs
    def outputs_add_data_types(self, output_data_types: List, observation_value_columns: List, **kwargs):
        self.__outputs['outputs']['output_data_types'] = output_data_types
        self.__outputs['outputs']['observation_value_columns'] = observation_value_columns
        self.__required['outputs']['output_data_types'] = True
        self.__required['outputs']['observation_value_columns'] = True

    # Performance Metrics

    def get(self) -> Struct:
        """
        Description:

        Once your manifest is built, use this method to pass the manifest into your TerraScope API Calls.
        This will construct the proper format for that, and check that all the required fields are present.

        :return: An Algorithm Manifest
        """
        manifest = Struct()
        manifest.update(self.__metadata)
        manifest.update(self.__interface)
        manifest.update({"inputs": self.__inputs})
        manifest.update(self.container_parameters)
        manifest.update(self.__outputs)
        manifest.update(self.__manifest_version)

        if len(self.__performance_metrics) > 0:
            manifest.update(self.__parameters)
        if len(self.__grouping.keys()) > 0:
            manifest.update(self.__grouping)
        if (self.__parallelization['parallelization']['dimensions']
                or self.__parallelization['parallelization']['configuration']):
            manifest.update(self.__parallelization)
        if len(self.__restrictions.keys()) > 0:
            manifest.update(self.__restrictions)
        if len(self.__performance_metrics.keys()) > 0:
            manifest.update(self.__performance_metrics)

        for outer_key in self.__required.keys():
            if isinstance(outer_key, Dict):
                for inner_key in outer_key.keys():
                    if not self.__required[outer_key][inner_key]:
                        logging.info("[{} : {}] - was not set, and is required.".format(outer_key, inner_key))
                        assert self.__required[outer_key][inner_key]
            else:
                if not self.__required[outer_key]:
                    logging.info("[{}] - was not set, and is required.".format(outer_key))
                    assert self.__required[outer_key]

        return manifest


class AlgorithmConfiguration:

    def __init__(self):
        """
        This is an Algorithm Configuration Factory. The purpose is to simplify building an algo configuration struct.
        When creating an algorithm config, specifying a data source is required. Optionally, you may also specify
        modifications to algorithm parameters that were set in the algorithm manifest.

        Defaults:
            - Grouping Frequency: DAILY, 1
        """
        self.__required = {
            "data_sources": False,
            "grouping": False
        }
        self.__algorithm_parameters = {
            "parameters": {}
        }
        self.__grouping = {
            "grouping": {}
        }
        self.__parallelization_configuration = {
            "parallelization_configuration": {}
        }
        self.__data_sources = []
        # Set Default grouping frequency
        self.grouping_frequency(Frequency.DAILY, 1)

    def add_data_source(self, data_type: DataType, data_source: DataSource = None, data_parameters: Dict = None):

        data_type_exists = False
        for source in self.__data_sources:
            # Check if Data Type Element Exists
            if source['data_type_name'] == data_type.value:
                data_type_exists = True
                for source_id in source['data_source_ids']:
                    if source_id == data_source.value:
                        logging.info("data source [{}] already registered.".format(data_source))
                        return

        if not data_type_exists:
            self.__data_sources.append({
                "data_type_name": data_type.value,
                "data_source_ids": [data_source.value] if data_source else []
            })
        else:
            for source in self.__data_sources:
                if source['data_type_name'] == data_type.value and data_source:
                    source['data_source_ids'].append(data_source.value)

        if data_parameters is not None:
            for source in self.__data_sources:
                if source['data_type_name'] == data_type.value:
                    source['parameters'] = data_parameters

        self.__required['data_sources'] = True

    def add_algorithm_parameter(self, key: str, value):
        for param in self.__algorithm_parameters['parameters'].keys():
            if key == param:
                assert key != param

        self.__algorithm_parameters['parameters'][key] = value

    def update_parallelization_configuration(self, configuration: Dict):
        self.__parallelization_configuration['parallelization_configuration'].update(configuration)

    # Grouping
    def grouping_frequency(self, frequency: Frequency, value: int):
        assert isinstance(frequency, Frequency)
        assert isinstance(value, int)
        self.__grouping['grouping']['frequency'] = Frequency(frequency).name
        self.__grouping['grouping']['value'] = value
        self.__required['grouping'] = True

    def get(self) -> Struct:
        """
        Description:

        Once your manifest is built, use this method to pass the manifest into your TerraScope API Calls.
        This will construct the proper format for that, and check that all the required fields are present.

        :return: An Algorithm Configuration as struct_pb2.Struct
        """

        for key in self.__required.keys():
            if not self.__required[key]:
                logging.info("[{}] - was not set, and is required.".format(key))
                assert self.__required[key]

        algorithm_config = Struct()
        algorithm_config.update({"data_sources": self.__data_sources})
        algorithm_config.update(self.__algorithm_parameters)
        algorithm_config.update(self.__grouping)
        algorithm_config.update(self.__parallelization_configuration)

        MessageToDict(algorithm_config)
        return algorithm_config
