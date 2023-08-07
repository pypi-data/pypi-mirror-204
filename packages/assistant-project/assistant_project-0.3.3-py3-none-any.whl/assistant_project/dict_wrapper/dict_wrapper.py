import json
from .utils import import_yaml_cfg


class DictReader:
    def __init__(self, data_cfg):
        # Read from yaml if not already as dict
        self.config = data_cfg if data_cfg is dict else import_yaml_cfg(data_cfg)
        print(self.config)

    def get_cfg_from_name(self, file_name):
        return self.config["FILES"][file_name]

    def iterate_dict(self, obj, cfg, return_list=False, prekey=""):
        new_dict = {}
        """Walk through a dictionary of dicts and lists and return list of relevant items."""
        if type(obj) is dict:
            for key, value in obj.items():
                if type(value) in [dict, list]:
                    if (prekey+'.' + key).__contains__(cfg['LIST']) and return_list:
                        return value
                    self.iterate_dict(value, cfg, return_list, prekey=(prekey + '.' + key))
                elif not return_list:
                    contained = [x for x in cfg["ATTRIBUTES"].values() if (prekey+'.' + key).__contains__(x)]
                    if contained:
                        new_dict_key = list(cfg["ATTRIBUTES"].keys())[list(cfg["ATTRIBUTES"].values()).index(contained[0])]
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

