import json
import importlib.resources as res

json_preset_path = res.files("lpd8mk2.presets")


def _load_presets():
    preset_list = []
    with res.as_file(json_preset_path) as json_preset_path_file:
        json_files = json_preset_path_file.glob("*json")
        for json_file in json_files:
            with open(json_file) as f:
                preset_list.append(json.load(f))
    return preset_list


presets: list[dict] = _load_presets()
