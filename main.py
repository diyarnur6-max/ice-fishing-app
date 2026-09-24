import json
import os
import random
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

ITEM_MAP = {
    'Red Fish': 'red_fish.png',
    'Orange Fish': 'orange_fish.png',
    'Blue Fish': 'blue_fish.png',
    'White Card': 'white_card.png',
    'Silver Card': 'silver_card.png',
}


class IceFishingPredictorApp(App):

  def build(self):
    self.spinning = False
    self.spin_time_left = 5.0

    root = BoxLayout(orientation='vertical', padding=20, spacing=15)

    # 1. العنوان
    self.title_label = Label(
        text='Ice Fishing - Predictor & Live API',
        font_size='22sp',
        bold=True,
        size_hint=(1, 0.1),
    )
    root.add_widget(self.title_label)

    # 2. عرض التنبؤ الحسابي (AI Prediction Display)
    self.prediction_label = Label(
        text='Prediction: Syncing API...',
        font_size='16sp',
        color=(0.2, 0.8, 1, 1),
        size_hint=(1, 0.1),
    )
    root.add_widget(self.prediction_label)

    # 3. عرض الصورة والنتيجة
    initial_img = 'wheel.png' if os.path.exists('wheel.png') else ''
    self.result_image = Image(source=initial_img, size_hint=(1, 0.4))

    self.result_text = Label(
        text='Press START SPIN to run round',
        font_size='18sp',
        size_hint=(1, 0.15),
    )
    root.add_widget(self.result_image)
    root.add_widget(self.result_text)

    # 4. زر Start
    self.spin_btn = Button(
        text='START SPIN (5s)',
        font_size='20sp',
        bold=True,
        size_hint=(1, 0.25),
        background_normal='',
        background_color=(0, 0.7, 0.3, 1),
    )
    self.spin_btn.bind(on_press=self.start_spin)
    root.add_widget(self.spin_btn)

    # تحديث التنبؤات المباشرة من live_game_data.json كل ثانية
    Clock.schedule_interval(self.update_prediction_from_api, 1.0)

    return root

  def update_prediction_from_api(self, dt):
    if os.path.exists('live_game_data.json'):
      try:
        with open('live_game_data.json', 'r') as f:
          data = json.load(f)
          pred = data.get('prediction', 'Analyzing...')
          self.prediction_label.text = f'🎯 Next Predicted: {pred}'
      except Exception:
        pass

  def start_spin(self, instance):
    if self.spinning:
      return

    self.spinning = True
    self.spin_btn.disabled = True
    self.spin_time_left = 5.0
    self.result_text.text = '🌀 Spinning with Live Algorithm...'

    Clock.schedule_interval(self.animate_spin, 0.1)

  def animate_spin(self, dt):
    self.spin_time_left -= dt

    if os.path.exists('wheel.png'):
      self.result_image.source = 'wheel.png'

    if self.spin_time_left > 0:
      self.spin_btn.text = f'Spinning... {self.spin_time_left:.1f}s'
    else:
      Clock.unschedule(self.animate_spin)
      self.show_final_result()

  def show_final_result(self):
    winner_key = random.choice(list(ITEM_MAP.keys()))

    if os.path.exists('live_game_data.json'):
      try:
        with open('live_game_data.json', 'r') as f:
          data = json.load(f)
          res = data.get('result_name', '')
          if res in ITEM_MAP:
            winner_key = res
      except Exception:
        pass

    winner_img = ITEM_MAP[winner_key]

    if os.path.exists(winner_img):
      self.result_image.source = winner_img
      self.result_image.reload()

    self.result_text.text = f'🎉 Result: {winner_key}'
    self.spin_btn.text = 'START SPIN AGAIN'
    self.spin_btn.disabled = False
    self.spinning = False


if __name__ == '__main__':
  IceFishingPredictorApp().run()
