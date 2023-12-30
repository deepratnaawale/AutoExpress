from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.slider import Slider
from kivy.uix.button import Button  # Import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window


class InputWidget(BoxLayout):  # Use FloatLayout instead of FormLayout
    def __init__(self, **kwargs):
        super(InputWidget, self).__init__(**kwargs)

        input_grid = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        positive_quality_layout = BoxLayout(
            orientation="horizontal", spacing=5, height=30
        )

        self.positive_quality = CheckBox()
        positive_quality_layout.add_widget(self.positive_quality)
        self.positive_quality_label = Label(text="Use Quality Prompt")
        positive_quality_layout.add_widget(self.positive_quality_label)
        input_grid.add_widget(positive_quality_layout)

        negative_quality_layout = BoxLayout(
            orientation="horizontal", spacing=5, height=30
        )
        self.negative_quality = CheckBox()
        negative_quality_layout.add_widget(self.negative_quality)
        self.negative_quality_label = Label(text="Use Negative Quality Prompt")
        negative_quality_layout.add_widget(self.negative_quality_label)
        input_grid.add_widget(negative_quality_layout)

        # Create a horizontal BoxLayout for "Prompt" elements
        prompt_layout = BoxLayout(orientation="horizontal", spacing=5, height=30)
        prompt_layout.add_widget(Label(text="Prompt"))
        self.prompt_input = TextInput(
            multiline=False,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            do_wrap=True,
            hint_text="(Optional) Enter Character specific eye and lips (only) details here.",
        )
        prompt_layout.add_widget(self.prompt_input)
        input_grid.add_widget(prompt_layout)

        neg_prompt_layout = BoxLayout(orientation="horizontal", spacing=5, height=30)
        neg_prompt_layout.add_widget(Label(text="Negative Prompt"))
        self.negative_prompt_input = TextInput(
            multiline=False,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text="(Optional) Enter Negative Prompt here",
        )
        neg_prompt_layout.add_widget(self.negative_prompt_input)
        input_grid.add_widget(neg_prompt_layout)

        sampling_method_layout = BoxLayout(
            orientation="horizontal", spacing=5, height=30
        )
        sampling_method_layout.add_widget(Label(text="Sampling Method"))

        self.sampling_method_dropdown = DropDown()

        sampling_methods = ["DPM++ 2M Karras", "Method 2", "Method 3"]

        for method in sampling_methods:
            btn = Button(
                text=method,
                size_hint_y=None,
                height=30,
                background_color=(0.1, 0.1, 0.1, 1),
            )
            btn.bind(
                on_release=lambda btn: self.sampling_method_dropdown.select(btn.text)
            )
            self.sampling_method_dropdown.add_widget(btn)
            # Bind a function to update the button text when an item is selected
            btn.bind(on_release=self.update_sampling_method_text)

        self.sampling_method_button = Button(text="DPM++ 2M Karras", height=30)
        self.sampling_method_button.bind(on_release=self.sampling_method_dropdown.open)

        sampling_method_layout.add_widget(self.sampling_method_button)
        input_grid.add_widget(sampling_method_layout)

        seed_dropdown_layout = BoxLayout(orientation="horizontal", spacing=5, height=30)
        seed_dropdown_layout.add_widget(Label(text="Seed"))

        self.seed_dropdown = DropDown()
        seeds = ["-1", "constant"]
        for seed in seeds:
            btn = Button(
                text=seed,
                size_hint_y=None,
                height=30,
                background_color=(0.1, 0.1, 0.1, 1),
            )
            btn.bind(on_release=lambda btn: self.seed_dropdown.select(btn.text))
            self.seed_dropdown.add_widget(btn)
            btn.bind(on_release=self.update_seed_text)

        self.seed_button = Button(text="-1", height=30)
        self.seed_button.bind(on_release=self.seed_dropdown.open)

        seed_dropdown_layout.add_widget(self.seed_button)
        input_grid.add_widget(seed_dropdown_layout)

        # Create text inputs for slider values
        self.width_text = TextInput(
            hint_text="Width Value",
            multiline=False,
            height=30,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
        )
        self.width_text.bind(on_text_validate=self.on_width_text_enter)

        self.height_text = TextInput(
            hint_text="Height Value",
            multiline=False,
            height=30,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
        )
        self.height_text.bind(on_text_validate=self.on_height_text_enter)

        self.cfg_scale_text = TextInput(
            hint_text="CFG Scale Value",
            multiline=False,
            height=30,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
        )
        self.cfg_scale_text.bind(on_text_validate=self.on_cfg_scale_text_enter)

        self.denoising_strength_text = TextInput(
            hint_text="Denoising Strength Value",
            multiline=False,
            height=30,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
        )
        self.denoising_strength_text.bind(
            on_text_validate=self.on_denoise_strength_text_enter
        )

        # Create sliders with default values and bind to text inputs
        self.width_slider = Slider(
            min=0, max=2048, step=1, value=512, cursor_size=(25, 25)
        )
        self.width_slider.bind(value=self.on_width_slider_value)
        self.on_width_slider_value(
            self.width_slider, self.width_slider.value
        )  # Initialize text input value

        self.height_slider = Slider(
            min=0, max=2048, step=1, value=768, cursor_size=(25, 25)
        )
        self.height_slider.bind(value=self.on_height_slider_value)
        self.on_height_slider_value(
            self.height_slider, self.height_slider.value
        )  # Initialize text input value

        self.cfg_scale_slider = Slider(
            min=0, max=30, step=0.5, value=7, cursor_size=(25, 25)
        )
        self.cfg_scale_slider.bind(value=self.on_cfg_scale_slider_value)
        self.on_cfg_scale_slider_value(
            self.cfg_scale_slider, self.cfg_scale_slider.value
        )  # Initialize text input value

        self.denoising_strength_slider = Slider(
            min=0, max=1, step=0.05, value=0.5, cursor_size=(25, 25)
        )
        self.denoising_strength_slider.bind(
            value=self.on_denoising_strength_slider_value
        )
        self.on_denoising_strength_slider_value(
            self.denoising_strength_slider, self.denoising_strength_slider.value
        )  # Initialize text input value

        # Add widgets to the grid
        width_slider_layout = BoxLayout(orientation="horizontal", spacing=5, height=30)
        width_slider_layout.add_widget(Label(text="Width"))
        width_slider_layout.add_widget(self.width_slider)
        width_slider_layout.add_widget(self.width_text)
        input_grid.add_widget(width_slider_layout)

        height_slider_layout = BoxLayout(orientation="horizontal", spacing=5, height=30)
        height_slider_layout.add_widget(Label(text="Height"))
        height_slider_layout.add_widget(self.height_slider)
        height_slider_layout.add_widget(self.height_text)
        input_grid.add_widget(height_slider_layout)

        cfg_scale_slider_layout = BoxLayout(
            orientation="horizontal", spacing=5, height=30
        )
        cfg_scale_slider_layout.add_widget(Label(text="CFG Scale"))
        cfg_scale_slider_layout.add_widget(self.cfg_scale_slider)
        cfg_scale_slider_layout.add_widget(self.cfg_scale_text)
        input_grid.add_widget(cfg_scale_slider_layout)

        denoising_strength_slider_layout = BoxLayout(
            orientation="horizontal", spacing=5, height=30
        )
        denoising_strength_slider_layout.add_widget(Label(text="Denoising Strength"))
        denoising_strength_slider_layout.add_widget(self.denoising_strength_slider)
        denoising_strength_slider_layout.add_widget(self.denoising_strength_text)
        input_grid.add_widget(denoising_strength_slider_layout)

        generate_button_layout = BoxLayout(
            orientation="horizontal", spacing=5, height=30
        )
        generate_button = Button(
            text="Generate Expressions",
            size_hint_y=None,
            height=30,
            background_color=(0.56, 0.93, 0.56, 1),
            color=(1, 1, 1, 1),
        )

        generate_button.bind(on_release=self.send_params)
        generate_button_layout.add_widget(generate_button)

        input_grid.add_widget(generate_button_layout)

        self.add_widget(input_grid)

    def send_params(self, instance):
        params = {
            "use_quality": self.positive_quality.active,
            "use_negative_quality": self.negative_quality.active,
            "prompt": self.prompt_input.text,
            "negative_prompt": self.negative_prompt_input.text,
            "sampler": self.sampling_method_button.text,
            "seed": self.seed_button.text,
            "width": self.width_text.text,
            "height": self.height_text.text,
        }

        print(params)
        return params

    def update_seed_text(self, instance):
        # Update the button text with the selected item
        self.seed_button.text = instance.text

    def update_sampling_method_text(self, instance):
        # Update the button text with the selected item
        self.sampling_method_button.text = instance.text

        # Function to show tooltip

    def on_width_text_enter(self, instance):
        # Update slider value when Enter is pressed in text input
        try:
            value = int(self.width_text.text)
            if 0 <= value <= 2048:  # Assuming these are the min and max for the slider
                self.width_slider.value = value
            else:
                print("Value out of range. Please enter a number between 0 and 2048.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def on_height_text_enter(self, instance):
        # Update slider value when Enter is pressed in text input
        try:
            value = int(self.height_text.text)
            if 0 <= value <= 2048:  # Assuming these are the min and max for the slider
                self.height_slider.value = value
            else:
                print("Value out of range. Please enter a number between 0 and 2048.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def on_cfg_scale_text_enter(self, instance):
        # Update slider value when Enter is pressed in text input
        try:
            value = float(self.cfg_scale_text.text)
            if 0 <= value <= 30:  # Assuming these are the min and max for the slider
                self.cfg_scale_slider.value = value
            else:
                print("Value out of range. Please enter a number between 0 and 30.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def on_denoise_strength_text_enter(self, instance):
        # Update slider value when Enter is pressed in text input
        try:
            value = float(self.denoising_strength_text.text)
            if 0 <= value <= 1:  # Assuming these are the min and max for the slider
                self.denoising_strength_slider.value = value
            else:
                print("Value out of range. Please enter a number between 0 and 2048.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def on_width_slider_value(self, instance, value):
        # Update text input when slider value changes
        self.width_text.text = str(int(value))

    def on_height_slider_value(self, instance, value):
        self.height_text.text = str(int(value))

    def on_cfg_scale_slider_value(self, instance, value):
        self.cfg_scale_text.text = str(round(value, 2))

    def on_denoising_strength_slider_value(self, instance, value):
        self.denoising_strength_text.text = str(round(value, 2))
