from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class CalculatorApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=12, spacing=10)

        # डिस्प्ले स्क्रीन
        self.display = TextInput(
            multiline=False,
            readonly=True,
            halign='right',
            font_size=42,
            size_hint=(1, 0.22),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        main_layout.add_widget(self.display)

        # 5x4 का बटन्स लेआउट
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['00', '0', '.', '=']
        ]

        grid = GridLayout(cols=4, spacing=8, size_hint=(1, 0.78))

        # बटन्स को अलग-अलग रंगों के साथ जोड़ना
        for row in buttons:
            for label in row:
                btn = Button(text=label, font_size=26, bold=True)
                
                # कलर कोडिंग (RGBA format)
                if label in ['=', '+', '-', '*', '/']:
                    btn.background_color = (0.2, 0.6, 0.9, 1)  # नीला
                elif label in ['C', '⌫']:
                    btn.background_color = (0.9, 0.3, 0.3, 1)  # लाल
                else:
                    btn.background_color = (0.35, 0.35, 0.35, 1)  # डार्क ग्रे

                btn.bind(on_press=self.on_button_press)
                grid.add_widget(btn)

        main_layout.add_widget(grid)
        return main_layout

    def on_button_press(self, instance):
        text = instance.text

        if text == 'C':
            self.display.text = ''
        elif text == '⌫':
            self.display.text = self.display.text[:-1]
        elif text == '=':
            try:
                # % को Python के मॉड्यूलो ऑपरेटर या प्रतिशत की तरह हैंडल करना
                expression = self.display.text.replace('%', '/100')
                self.display.text = str(eval(expression))
            except Exception:
                self.display.text = 'Error'
        else:
            self.display.text += text

if __name__ == '__main__':
    CalculatorApp().run()
