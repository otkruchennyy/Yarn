import os


class helpers_costomize:
    def __init__(self):
        self.themes_dir = 'resources/themes/'
        self.fonts_dir = 'resources/fonts/'

        self.available_themes = {}
        self.available_fonts = {}

        for filename in os.listdir(self.themes_dir):
            if filename.endswith('.json'):
                theme_name = os.path.splitext(filename)[0]
                full_path = os.path.join(self.themes_dir, filename)
                self.available_themes[theme_name] = full_path


        for filename in os.listdir(self.fonts_dir):
            if filename.endswith('.json'):
                font_name = os.path.splitext(filename)[0]
                full_path = os.path.join(self.themes_dir, filename)
                self.available_themes[font_name] = full_path

    def get_theme_fonts(self):
        return list(self.available_fonts.keys())

    def apply_theme_from_json(self, theme_name):
        import json
        path = self.available_themes[theme_name]

        with open(path, 'r') as f:
            theme_data = json.load(f)

        instructions = {}
        for property_name, value in theme_data.items():
            instructions[property_name] = value

        return instructions

    def apply_fonts_from_json(self, font_name):
        import json
        path = self.available_fonts[font_name]

        with open(path, 'r') as f:
            font_data = json.load(f)

        instructions = {}
        for property_name, value in font_data.items():
            instructions[property_name] = value

        return instructions