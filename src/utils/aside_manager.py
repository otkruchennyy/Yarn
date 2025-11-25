import json
import os
import utils.helpers as helpers

"""Button click handler for aside - manages button states and contains basic logic"""

btn_config_path = os.path.join(helpers.get_project_root(), "config", "btn_settings_config.json")

def control_sidebar_behavior(name):
    helpers.get_json_property(btn_config_path, name)
    set_active_button(name)

_main_widget = None

def init_widget(widget_instance):
    global _main_widget
    _main_widget = widget_instance

def aside_state():
    global _main_widget
    data = helpers.get_json_property(btn_config_path)
    if data['aside_is_open']:
        hide_aside()
    else:
        show_aside()
    
    data['aside_is_open'] = not data['aside_is_open']
    save_config(btn_config_path, data)

def show_aside():
    global _main_widget
    _main_widget.widget2.show()
    _main_widget.setFixedWidth(300)
    _main_widget.btn_toggle.setText("<<")

def hide_aside():
    global _main_widget
    _main_widget.widget2.hide()
    _main_widget.setFixedWidth(50)
    _main_widget.btn_toggle.setText(">>")

def btn_workspaces_clicked():
    control_sidebar_behavior('btn_workspaces')
    # _main_widget.label2.setText("Workspaces")

def btn_tools_clicked():
    control_sidebar_behavior('btn_tools')
    # _main_widget.label2.setText("Tools")

def btn_plugins_clicked():
    control_sidebar_behavior('btn_plugins')
    # _main_widget.label2.setText("Plugins")

def btn_settings_clicked():
    control_sidebar_behavior('btn_settings')
    # _main_widget.label2.setText("Settings") load content

def set_active_button(key):
    """Keeps only one button active (set to true) among others"""
    with open(btn_config_path, "r", encoding="utf-8") as f:
        f_readfile = f.read()
        data = json.loads(f_readfile)
    for keyName in data:
        if keyName == 'aside_is_open': continue
        if keyName == key:
            if data['aside_is_open'] == True:
                if data[keyName] == True:
                    data['aside_is_open'] = not data['aside_is_open']
                    hide_aside()
                else:
                    data[keyName] = not data[keyName]
                save_config(btn_config_path, data)
            else:
                show_aside()
                data['aside_is_open'] = not data['aside_is_open']
                save_config(btn_config_path, data)
        else:
            data[keyName] = False

        save_config(btn_config_path, data)

def save_config(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_active_btn():
    data = helpers.get_json_property(btn_config_path)
    filtered = filter(lambda x: data[x] == True and x != 'aside_is_open', data)
    return next(filtered, None)