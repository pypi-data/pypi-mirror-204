import json
from utils import import_yaml_cfg


class DictReader:
    def __init__(self, data_cfg):
        self.config = import_yaml_cfg(data_cfg)
        print(self.config)

    def get_cfg_from_name(self, file_name):
        return self.config["FILES"][file_name]

    def iterate_dict(self, obj, cfg, return_list=False):
        new_dict = {}
        """Walk through a dictionary of dicts and lists and return list of relevant items."""
        if type(obj) is dict:
            for key, value in obj.items():
                if type(value) in [dict, list]:
                    if key == cfg['LIST'] and return_list:
                        return value
                    self.iterate_dict(value, cfg, return_list)
                elif not return_list:
                    if key in cfg["ATTRIBUTES"].values():
                        new_dict_key = [i for i in cfg["ATTRIBUTES"] if cfg["ATTRIBUTES"][i] == key][0]
                        new_dict[new_dict_key] = value
        return new_dict
        # elif type(obj) is list:
        #     for i, element in enumerate(obj):
        #         if type(element) in [dict, list]:
        #             self.iterate_dict(element, cfg, return_list)
        # else:
        #     raise ValueError

    def get_items(self, file_dict, identifier):
        cfg = self.config[identifier]
        obj = self.iterate_dict(file_dict, cfg, return_list=True)
        db_items = []
        for element in obj:
            item = self.iterate_dict(element, cfg)
            if not db_items.__contains__(item):
                db_items.append(item)
        return db_items


if __name__ == "__main__":
    def import_json():
        with open('config/ProcessGraph1_2.json') as json_file:
            data = json.load(json_file)
        return data

    wrapper = DictReader(data_cfg="config/task.yaml")
    file = import_json()
    db_item = wrapper.get_items(file, 'TASK')
    print("next")

