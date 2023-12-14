# Eyeballs Introduction 
A small python wrapper to openCV to help facilitate video transfer for robots.

# Eyeballs Module API Documentation

## Introduction

The `Eyeballs` module facilitates an easier method for video transfer by providing functions for command and control ports, enabling rapid remote video solutions.

### Required Libraries
- [OpenCV](https://github.com/opencv/opencv)
- [PyYAML](https://github.com/yaml/pyyaml)

## Eyeballs Class

The `Eyeballs` class manages video transfer functionalities and remote video solutions. Below are the methods available within this class:

### Initialization

#### `__init__(self, yaml_file_path='./servers.yaml')`
- **Description:** Initializes the Eyeballs class by loading YAML configuration for server nodes and local setup.
- **Parameters:**
  - `yaml_file_path` (optional): Path to the YAML file containing server configurations. Default: './servers.yaml'

### YAML Handling

#### `load_yaml(self, yaml_file_path)`
- **Description:** Loads and processes the YAML configuration for server nodes and local setup.
- **Parameters:**
  - `yaml_file_path`: Path to the YAML file containing server configurations.

### Cortex and Eyeball Management

#### `start_cortex(self, server)`
- **Description:** Starts a new VisualCortex instance based on the specified server configuration.
- **Parameters:**
  - `server`: Index of the server configuration to initialize VisualCortex.

#### `get_cortex(self, server)`
- **Description:** Retrieves a VisualCortex instance based on the specified server configuration.
- **Parameters:**
  - `server`: Index of the server configuration.

#### `get_eyeball(self, server)`
- **Description:** Retrieves an Eyeball instance based on the specified server configuration.
- **Parameters:**
  - `server`: Index of the server configuration.

#### `start_eyeball(self, server_node_config)`
- **Description:** Starts a new Eyeball instance based on the specified server node configuration.
- **Parameters:**
  - `server_node_config`: Configuration data for the server node.

### Configuration Retrieval

#### `get_config(self)`
- **Description:** Returns the server node configurations stored in the Eyeballs class.

#### `get_local_setup(self)`
- **Description:** Returns the local setup configuration stored in the Eyeballs class.

## Example Usage Class creation

```python

eyeballs_instance = Eyeballs('./servers.yaml')
```

## Example Usage VisualCortex(The computer without the camera) 

```python

vc = eyeballs_instance.get_cortex(0)
vc.get_video_stream()
```

## Example Usage Eyeball(The computer with the camera) 

```python

eye = eyeballs_instance.get_eyeball(0)
eye.get_video()
```
