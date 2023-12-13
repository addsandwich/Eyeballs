"""
MIT License

Copyright (c) 2023 Christopher J. Watson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Purpose:
The Eyeballs module provides a collection of functions to create an easier method of video transfer with command
and control ports to enable rapid remote video solutions.

Required Libraries: https://github.com/opencv/opencv, https://github.com/yaml/pyyaml

"""
import yaml
import os
import VisualCortex
import Eyeball
import threading


class Eyeballs:
    def __init__(self, yaml_file_path='./servers.yaml'):
        self.server_node_config = []
        self.local_setup = {}
        self.load_yaml(yaml_file_path)
        self.cortex_list = []
        self.eyeball_list = []

    def load_yaml(self, yaml_file_path):
        try:
            # Check if the YAML file exists at the specified path
            if not os.path.isfile(yaml_file_path):
                raise FileNotFoundError(f"YAML file not found at '{yaml_file_path}'")

            # Load and process the YAML configuration
            with open(yaml_file_path, 'r') as file:
                config_data = yaml.safe_load(file)
                # Process the YAML data, for example:
                # Assuming the YAML contains server_node properties
                if 'servers' in config_data:
                    for server in list(config_data['servers'].keys()):
                        config_data['servers'][server]['name'] = server
                        self.server_node_config.append(config_data['servers'][server])
                else:
                    raise Exception('servers not defined in given yaml.')

                if 'local' in config_data:
                    self.local_setup = config_data['local']
                else:
                    raise Exception('local data not defined in given yaml.')

        except FileNotFoundError as e:
            # Handle the exception if the file is not found
            print(f"Error: {e}")
            # raise

        except yaml.YAMLError as e:
            # Handle YAML parsing errors if the file is not a valid YAML
            print(f"Error parsing YAML: {e}")
            # raise

    def start_cortex(self, server):
        new_cortex = VisualCortex.VisualCortex(self.server_node_config[server])
        thread = threading.Thread(target=new_cortex.run, args=(self.server_node_config[0],))
        self.cortex_list.append(thread)

    def get_cortex(self, server):
        new_cortex = VisualCortex.VisualCortex(self.server_node_config[server])
        return new_cortex

    def get_eyeball(self, server):
        new_eyeball = Eyeball.Eyeball(self.server_node_config[server])
        return new_eyeball

    def start_eyeball(self, server_node_config):
        new_eyeball = Eyeball(server_node_config)
        thread = threading.Thread(target=new_eyeball.run, args=(server_node_config,))
        self.eyeball_list.append(thread)

    def get_config(self):
        return self.server_node_config

    def get_local_setup(self):
        return self.local_setup


 # Example usage:
if __name__ == "__main__":
    eyeballs = Eyeballs()



