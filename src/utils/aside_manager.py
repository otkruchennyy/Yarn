import json
import os
import utils.helpers as helpers
import services.logger as log

"""Button click handler for aside - manages button states and contains basic logic"""
base_path = helpers.get_project_root()
btn_config_path = os.path.join(base_path, "config", "btn_settings_config.json")
data_btn_config = helpers.get_json_property(btn_config_path)
extra_panels_config_path = os.path.join(base_path, "config", "extra_panel.json")
data_extra_panels = helpers.get_json_property(extra_panels_config_path)


def save_config(path, data):
    """Save configuration to JSON file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

x = []
for name in data_btn_config:
    if name == "aside_is_open": continue
    x.append(data_btn_config[name])

if all(y == False for y in x):
    data_btn_config["btn_workspaces"] = True
    save_config(btn_config_path, data_btn_config)
del x

_main_widget = None
_panels = {}
_current_panel = None
extra_panel_reload_signal = None

def init_widget(widget_instance):
    """Initialize the main widget reference"""
    global _main_widget
    _main_widget = widget_instance

def register_panel(panel_name, panel_instance):
    """Register a panel by name for later access"""
    global _panels
    _panels[panel_name] = panel_instance


def control_sidebar_behavior(name):
    """Handle sidebar button click behavior"""
    helpers.get_json_property(btn_config_path, name)
    set_active_button(name)
    manage_panels_visibility(name)


def manage_panels_visibility(active_key):
    """Manage visibility of content panels based on active button"""
    global _panels, _current_panel
    
    # Hide current panel
    if _current_panel:
        _current_panel.hide()
    
    # Show new panel based on active button
    panel_name = _get_panel_name_by_button(active_key)
    if panel_name and panel_name in _panels:
        _panels[panel_name].show()
        _current_panel = _panels[panel_name]
    else:
        _current_panel = None

def _get_panel_name_by_button(button_name):
    """Map button names to panel names"""
    panel_mapping = {
        'btn_workspaces': 'workspaces',
        'btn_tools': 'tools', 
        'btn_plugins': 'plugins',
        'btn_settings': 'settings',
    } # 'btn_ExtraPanels': 'ExtraPanels'
    return panel_mapping.get(button_name)

def aside_state():
    """Toggle aside panel visibility"""
    global _main_widget
    data = helpers.get_json_property(btn_config_path)
    if data['aside_is_open']:
        hide_aside()
    else:
        show_aside()
    
    data['aside_is_open'] = not data['aside_is_open']
    save_config(btn_config_path, data)


def show_aside():
    """Show the aside panel and restore active content"""
    global _main_widget
    _main_widget.widget2.show()
    _main_widget.setFixedWidth(300)
    _main_widget.btn_toggle.setText("<<")
    
    # Show active panel when aside is opened
    active_btn = get_active_btn()
    if active_btn:
        manage_panels_visibility(active_btn)


def hide_aside():
    """Hide the aside panel and all content panels"""
    global _main_widget, _current_panel
    _main_widget.widget2.hide()
    _main_widget.setFixedWidth(50)
    _main_widget.btn_toggle.setText(">>")
    
    # Hide all panels when aside is closed
    if _current_panel:
        _current_panel.hide()
        _current_panel = None


def btn_workspaces_clicked():
    """Handle workspaces button click"""
    control_sidebar_behavior('btn_workspaces')


def btn_tools_clicked():
    """Handle tools button click"""
    control_sidebar_behavior('btn_tools')


def btn_plugins_clicked():
    """Handle plugins button click"""
    control_sidebar_behavior('btn_plugins')


def btn_settings_clicked():
    """Handle settings button click"""
    control_sidebar_behavior('btn_settings')

def btn_ExtraPanels_clicked():
    """Handle ExtraPanels button click"""
    handle_extra_panel_click("isOpen")
    reload_extra_panels()

def handle_extra_panel_click(button):
    """Click handler for buttons that trigger extra panels"""
    # for name in data_extra_panels:
    #     if name == "isOpen": continue
    #     elif button == name:
    #         if data_extra_panels[name] is True:
    data_extra_panels["isOpen"] = not data_extra_panels["isOpen"]
    #     else:
    #         data_extra_panels["isOpen"] = True
    #         data_extra_panels[name] = True
    # else: data_extra_panels[name] is False
    save_config(extra_panels_config_path, data_extra_panels)

def set_extra_panel_signal(signal):
    global extra_panel_reload_signal
    extra_panel_reload_signal = signal

def reload_extra_panels():
    if extra_panel_reload_signal:
        extra_panel_reload_signal.emit()
    else:
        log.debug("Extra panel signal not set yet")

def set_active_button(key): 
    """Keeps only one button active (set to true) among others"""

    with open(btn_config_path, "r", encoding="utf-8") as f:
        f_readfile = f.read()
        data = json.loads(f_readfile)

    for keyName in data:
        if keyName == 'aside_is_open': continue
        if keyName == key:
            if data[keyName] is True:
                if data["aside_is_open"] is True:
                    data['aside_is_open'] = False
                    hide_aside()
                else:
                    data['aside_is_open'] = True
                    show_aside()
            else:
                data['aside_is_open'] = True
                data[keyName] = True
                show_aside()
        else: data[keyName] = False
    save_config(btn_config_path, data)

def get_active_btn():
    """Get currently active button name"""
    data = helpers.get_json_property(btn_config_path)
    filtered = filter(lambda x: data[x] == True and x != 'aside_is_open', data)
    return next(filtered, None)