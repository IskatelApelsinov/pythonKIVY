import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_READ_UNCOMMITTED
import kivy
import random
from kivy.graphics import *
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.graphics import Color, Rectangle
from kivy.config import Config

# Глобальные настройки
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 50)
Config.set('graphics', 'top',  50)
Config.write()
height_screen = 600
width_screen = 1200
Window.size = (width_screen, height_screen)
Window.fullscreen = 0
Window.minimum_width = width_screen
Window.minimum_height = height_screen
Window.maximum_width = width_screen
Window.maximum_height = height_screen

Window.clearcolor = (51 / 255, 51 / 255, 51 / 255, 1)#(255 / 255, 186 / 255, 3 / 255, 1)
Window.Title = "Для Работников Паспортного Стола"
App.title = 'ПРИЛОЖЕНИЕ ДРПС'

#Config.set('graphics', 'width', '640')
#Config.set('graphics', 'height', '480')

red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]


# class PageLayout(PageLayout):
#     """
#     Define class PageLayout here
#     """
#
#     def __init__(self, **kwargs):
#         # The super function in Python can be
#         # used to gain access to inherited methods
#         # which is either from a parent or sibling class.
#         super(PageLayout, self).__init__(**kwargs)
#
#         # btn1 = Button(text='Page 1', background_color = [1, 1, 1, 1])
#         #
#         #
#         # self.add_widget(btn1)


# Builder.load_string('''
# <SelectableLabel>:
#     # Draw a background to indicate selection
#     canvas.before:
#         Color:
#             rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
#         Rectangle:
#             pos: self.pos
#             size: self.size
# <RV>:
#     viewclass: 'SelectableLabel'
#     SelectableRecycleBoxLayout:
#         default_size: None, dp(56)
#         default_size_hint: 1, None
#         size_hint_y: None
#         height: self.minimum_height
#         orientation: 'vertical'
#         multiselect: True
#         touch_multiselect: True
# ''')
# class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
#                                  RecycleBoxLayout):
#     ''' Adds selection and focus behaviour to the view. '''
# class SelectableLabel(RecycleDataViewBehavior, Label):
#     ''' Add selection support to the Label '''
#     index = None
#     selected = BooleanProperty(False)
#     selectable = BooleanProperty(True)
#     def refresh_view_attrs(self, rv, index, data):
#         ''' Catch and handle the view changes '''
#         self.index = index
#         return super(SelectableLabel, self).refresh_view_attrs(
#             rv, index, data)
#     def on_touch_down(self, touch):
#         ''' Add selection on touch down '''
#         if super(SelectableLabel, self).on_touch_down(touch):
#             return True
#         if self.collide_point(*touch.pos) and self.selectable:
#             return self.parent.select_with_touch(self.index, touch)
#     def apply_selection(self, rv, index, is_selected):
#         ''' Respond to the selection of items in the view. '''
#         self.selected = is_selected
#         if is_selected:
#             print("selection changed to {0}".format(rv.data[index]))
#         else:
#             print("selection removed for {0}".format(rv.data[index]))
# class RV(RecycleView):
#     def __init__(self, **kwargs):
#         super(RV, self).__init__(**kwargs)
#         self.data = [{'text': str(x)} for x in range(100)]
# class TestApp(App):
#     def build(self):
#         return RV()




class CustomGraphics(App):
    def SetBG(layout, **options):
        with layout.canvas.before:
                if 'bg_color' in options:
                    bg_rgba = options['bg_color']
                    if len(bg_rgba) == 4:
                        Color(bg_rgba[0], bg_rgba[1], bg_rgba[2], bg_rgba[3])
                    elif len(bg_rgba) == 3:
                        Color(bg_rgba[0], bg_rgba[1], bg_rgba[2])
                    else:
                        Color(0,0,0,1)
                layout.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
                def update_rect(instance, value):
                    instance.bg_rect.pos = instance.pos
                    instance.bg_rect.size = instance.size
                # listen to size and position changes
                layout.bind(pos=update_rect, size=update_rect)







class MainApp(App):


    def build(self):
        colors = [red, green, blue, purple]



        self.proverka_nal_table = 0
        #self.proverla_autor = 0
        self.page_layout = PageLayout()



        self.textperv = Label(text='', font_size = 12)


        #self.page_layout.add_widget(self.textperv)
        self.autorizacion = self.autorizac()


        try:
            self.page_layout.add_widget(self.autorizacion)

        except (Exception, Error) as error:
            layout = BoxLayout(orientation='horizontal')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()








        self.layout = BoxLayout(padding = 0)
        self.layout.background_color = [255 / 255, 186 / 255, 3 / 255, 1]

        print(self.layout.background_color)
        self.layout.opacity = 0
        self.layout.disabled = 1


        self.text = Label(text = 'privet', font_size = 12)

        # self.txt = TextInput(hint_text='Write syda', size_hint=(1.5, 0.1))
        # self.txt.bind(text=self.on_text)
        # self.layout.add_widget(self.txt)


        self.table = [['a', 'b'], ['c', 'd']]






        # for i in range(5):
        #     current_table = BoxLayout(orientation = 'vertical')
        #     for j in range(7):
        #         if i == 0:
        #                 self.btn_cre = Button(text='Создать\nзадание', background_color=[255 / 255, 204 / 255, 51 / 255, 1],
        #                                       font_size=12)
        #                 self.btn_cre.bind(on_press=self.on_press_button)
        #                 self.levyistolb.add_widget(self.btn_cre)
        #
        #             if i == 1:
        #                 self.btn_done = Button(text='Завершить\nзадание', background_color=[255 / 255, 204 / 255, 51 / 255, 1],
        #                                        font_size=12)
        #                 self.btn_done.bind(on_press=self.on_press_button)
        #                 self.levyistolb.add_widget(self.btn_done)
        #             if i == 2:
        #                 self.btn_chng = Button(text='Поменять\nисполнителя\nзадания',
        #                                        background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn_chng.bind(on_press=self.on_press_button)
        #                 self.levyistolb.add_widget(self.btn_chng)
        #             if i == 3:
        #                 self.btn_take = Button(text='Взять\nзадание', background_color=[255 / 255, 204 / 255, 51 / 255, 1],
        #                                        font_size=12)
        #                 self.btn_take.bind(on_press=self.on_press_button)
        #                 self.levyistolb.add_widget(self.btn_take)
        #
        #
        #
        #
        #         if j == 1:
        #             if i == 0:
        #                 self.btn_cre = Button(text='Создать\nзадание', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn_cre.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn_cre)
        #
        #             if i == 1:
        #                 self.btn_done = Button(text='Завершить\nзадание', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn_done.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn_done)
        #             if i == 2:
        #                 self.btn_chng = Button(text='Поменять\nисполнителя\nзадания', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn_chng.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn_chng)
        #             if i == 3:
        #                 self.btn_take = Button(text='Взять\nзадание', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn_take.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn_take)
        #             if i == 4:
        #                 #self.btn = Button(text='', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn = Label(text='', font_size=12)
        #                 #self.btn.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn)
        #
        #
        #         if j == 6:
        #             if i == 0:
        #                 self.btn_exit = Button(text='Выйти из\nприложения', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn_exit.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn_exit)
        #             if i == 1:
        #                 self.btn_reg = Button(text='Регистрация\nнового\nпользователя', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn_reg.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn_reg)
        #             if i == 2:
        #                 self.btn_enter_c = Button(text='Ввести команду\nSQL', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn_enter_c.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn_enter_c)
        #             if i == 3:
        #                 self.btn_prov = Button(text='PROVERKA', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn_prov.bind(on_press=self.on_press_button)
        #                 #self.btn = Label(text='', font_size=12)
        #                 current_table.add_widget(self.btn_prov)
        #             if i == 4:
        #                 self.btn_join_an_bd = Button(text='Подключение\nк другой\nбазе данных', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn_join_an_bd.bind(on_press=self.on_press_button)
        #                 #self.btn = Label(text='', font_size=12)
        #                 current_table.add_widget(self.btn_join_an_bd)
        #
        #
        #         # self.textik = Label(text='', font_size=12)
        #         # current_table.add_widget(self.textik)
        #         if j == 100:
        #             if i == 2:
        #                 self.btn = Button(text='COLOR', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn)
        #             if i == 1:
        #                 self.btn = Button(text='CLOSE TABLE', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn)
        #             if i == 3:
        #                 self.btn = Button(text='PROVERKA', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn)
        #             if i == 0:
        #                 self.btn = Button(text='PROVERKA', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn)
        #             if i == 4:
        #                 self.btn = Button(text='PROVERKA', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn)
        #
        #         if j == 2:
        #             if i == 0:
        #                 self.btn_find = Button(text='Поиск по\nатрибутам', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn_find.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn_find)
        #
        #             if i == 2:
        #                 self.btn_show = Button(text='Просмотр\nсвоих\nзаданий', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 #self.btn = Label(text='', font_size=12)
        #                 self.btn_show.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn_show)
        #             if i == 3:
        #                 # self.btn = Button(text='', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn = Label(text='', font_size=12)
        #                 # self.btn.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn)
        #             if i == 4:
        #                 # self.btn = Button(text='', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
        #                 self.btn = Label(text='', font_size=12)
        #                 # self.btn.bind(on_press=self.on_press_button)
        #                 current_table.add_widget(self.btn)
        #
        #         if j == 5 or j == 3:
        #             self.textik = Label(text='', font_size=12)
        #             current_table.add_widget(self.textik)
        #
        #         # if i == 1 and j == 2:
        #         #     self.textik.text = 'proverka'
        #         #     print(self.textik.text)
        #
        #     self.layout.add_widget(current_table)


        self.page_layout.add_widget(self.layout)


        return self.page_layout
     #   return self.layout
    def on_press_button(self, instance):

        try:
            #print('otm')
            if self.connection:
                self.connection.commit()
        except (Exception, Error) as error:
            print(error)

        button_text = instance.text
        print('Вы нажали на кнопку!', button_text)
        if button_text == 'Button #1':
            self.cursor.execute('SELECT * from zadanie')
            record = self.cursor.fetchall()
            print("Результат", record)
        if button_text == 'Закрыть\nсоединение':
            try:
                if self.connection:
                    self.cursor.close()
                    self.connection.commit()
                    self.connection.close()
                    print("Соединение с PostgreSQL закрыто")
            except (Exception, Error) as error:
                print(error)
                content = Button(text='Хорошо')
                popup = Popup(content=content, auto_dismiss=False, title='Что то не так',
                              size_hint=(None, None), size=(0.5 * height_screen, 0.25 * width_screen))
                content.bind(on_press=popup.dismiss)
                popup.open()

        if button_text == 'Ввести команду\nSQL':
            layout = BoxLayout(orientation = "vertical")
            self.txt = TextInput(hint_text='Write syda', size_hint=(1, 0.8))
            self.txt.bind(text=self.on_text)
            # self.layout.add_widget(self.txt)
            niz_layout = BoxLayout(orientation = 'horizontal')
            vihod = Button(text = 'Отмена')
            content = Button(text='Ввести команду')
            content.bind(on_press = self.on_press_button)
            niz_layout.add_widget(content)
            niz_layout.add_widget(vihod)
            layout.add_widget(self.txt)
            niz_layout.size_hint_max_y = 0.05 * height_screen
            layout.add_widget(niz_layout)

            popup = Popup(content=layout, auto_dismiss=False, title='Введите команду',
                          size_hint=(None, None), size=(0.9 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            vihod.bind(on_press = popup.dismiss)
            content.bind(on_press=popup.dismiss)
            # open the popup
            popup.open()
        if button_text == 'Открыть\nтаблицу':

            #print('otm')
            #content = Button(text='Хорошо')
            #popup = Popup(content=content, auto_dismiss=False, title='Не надо',
            #              size_hint=(None, None), size=(0.5 * height_screen, 0.25 * width_screen))
            #content.bind(on_press=popup.dismiss)
            #popup.open()
            #
            #
            # print(self.proverka_nal_table)
            # print('GOPA')
            # #cursor.execute(self.txt.text)
            # if self.proverka_nal_table == 0:
            #     self.cursor.execute('Select * from zadanie')
            #     record = self.cursor.fetchall()
            #     new_record = [[0]*len(record) for _ in range(len(record[0]))]
            #
            #     for i in range(len(record)):
            #         for j in range(len(record[0])):
            #             new_record[j][i] = record[i][j]
            #     self.table_create(new_record)
            # else:
            #     content = Button(text='Понятно!')
            #     popup = Popup(content=content, auto_dismiss=False, title='Закройте предыдущую таблицу',
            #                    size_hint=(None, None), size=(0.25 * height_screen, 0.25 * width_screen))
            #
            #     # bind the on_press event of the button to the dismiss function
            #     content.bind(on_press=popup.dismiss)
            #
            #     # open the popup
            #     popup.open()
            try:
                layout = BoxLayout(orientation='vertical')
                niz_layout = BoxLayout(orientation = 'horizontal')
                nadpis = Label(text='Какую таблицу нужно открыть?', font_size=14)
                content = Button(text='Отмена', font_size=14)
                zadanie = Button(text = 'zad')
                clienty = Button(text = 'clie')
                rabotniki = Button(text = 'rab')
                niz_layout.add_widget(zadanie)
                niz_layout.add_widget(clienty)
                niz_layout.add_widget(rabotniki)
                layout.add_widget(nadpis)
                layout.add_widget(niz_layout)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Просмотр таблицы',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                zadanie.bind(on_press=self.enter_the_table)
                zadanie.bind(on_press=popup.dismiss)
                clienty.bind(on_press=self.enter_the_table)
                clienty.bind(on_press=popup.dismiss)
                rabotniki.bind(on_press=self.enter_the_table)
                rabotniki.bind(on_press=popup.dismiss)
                popup.open()


            except (Exception, Error) as error:
                layout = BoxLayout(orientation='vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text=textik, font_size=24)
                content = Button(text='Хорошо', font_size=24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()

        if button_text == 'MAKE WHAT':
            print(instance)
            #self.pageTable = FloatLayout(size=(300, 300))
            button = Button(
                text='Hello world',
                size_hint=(.5, .25),
                pos=(20, 20))
            #self.pageTable.add_widget(button)
            #self.pageTable.add_widget(self.text)
        if button_text == 'COLOR':
            self.layout.background_color = [1,1,1,1]
            print(self.layout.background_color)
        if button_text == 'CLOSE TABLE':
            self.page_layout.remove_widget(self.main_tablica)
            self.proverka_nal_table = 0
            self.page_layout.add_widget(self.layout)
        if button_text == 'Зайти под другим\nпользователем':


            layout = BoxLayout(orientation="vertical")
            self.txt_log = TextInput(hint_text='LOGIN', size_hint=(1, 0.8))
            self.txt_log.multiline = 0
            self.txt_pass = TextInput(hint_text='PASSWORD', size_hint=(1, 0.8))
            self.txt_pass.multiline = 0
            self.txt_pass.foreground_color = [0, 0, 0, 0]
            self.txt_pass.allow_copy = 0
            # self.layout.add_widget(self.txt)
            niz_layout = BoxLayout(orientation = 'horizontal')
            vihod = Button(text = 'Отмена')
            content = Button(text='Авторизоваться ')
            content.bind(on_press=self.on_press_button)
            niz_layout.add_widget(content)
            niz_layout.add_widget(vihod)
            layout.add_widget(self.txt_log)
            layout.add_widget(self.txt_pass)
            layout.add_widget(niz_layout)

            popup = Popup(content=layout, auto_dismiss=False, title='Повторите авторизацию',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.25 * height_screen))
            # bind the on_press event of the button to the dismiss function
            vihod.bind(on_press=popup.dismiss)
            content.bind(on_press=popup.dismiss)
            # open the popup
            popup.open()
        if button_text == 'Выйти из\nприложения':

            try:
                print(self.autorizac())

                if self.connection:
                    self.cursor.close()

                    self.connection.close()
                    print("Соединение с PostgreSQL закрыто")

                self.root_window.close()

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
                self.root_window.close()
        if button_text == 'Авторизоваться':
            self.proverka_autor = 0
            if self.vvod_login.text == 'postgres' or self.vvod_pass.text == '':
                self.vvod_login.text = ''
                self.vvod_pass.text = ''
            self.enter_the_bd(self.vvod_login.text, self.vvod_pass.text, 'pasport_stol')
            self.vvod_login.text = ''
            self.vvod_pass.text = ''
            print('a')

            # if self.vvod_login.text == '' and self.vvod_pass.text == '':
            #     self.proverka_autor = 1
            if self.proverka_autor == 1:



                self.layout.opacity = 1
                self.layout.disabled = 0
                self.page_layout.remove_widget(self.autorizacion)
                #self.start()
                self.proverka_polz()


            # self.autorizacion.disabled = 1
            # self.autorizacion.opacity = 0
        if button_text == 'Авторизоваться ':
            self.proverka_autor = 0
            if self.txt_log.text == 'postgres' or self.txt_pass.text == '':
                self.txt_log.text = ''
                self.txt_pass.text = ''


            self.enter_the_bd(self.txt_log.text, self.txt_pass.text, 'pasport_stol')
            self.txt_log.text = ''
            self.txt_pass.text = ''
            print('kk')
            if self.proverka_autor == 1:
                content = Button(text='Успешно')
                popup = Popup(content=content, auto_dismiss=False, title='Авторизация',
                               size_hint=(None, None), size=(0.25 * height_screen, 0.25 * width_screen))
                content.bind(on_press=popup.dismiss)

                popup.open()
                self.proverka_polz()
            if self.proverka_autor == 0:
                print('pprov')
                content = Button(text='Безуспешно')
                popup = Popup(content=content, auto_dismiss=False, title='Авторизация',
                               size_hint=(None, None), size=(0.25 * height_screen, 0.25 * width_screen))
                content.bind(on_press=popup.dismiss)
                popup.open()

        if button_text == 'PROVERKA':
            self.proverka_polz()


        if button_text == 'Подключение\nк другой\nбазе данных':
            print('join another bd')

            try:
                niz_lalout = BoxLayout(orientation='horizontal')
                lalout = BoxLayout(orientation='vertical')
                self.login = TextInput(hint_text='Логин', size_hint=(1, 0.8))
                self.password = TextInput(hint_text='Пароль', size_hint=(1, 0.8))
                self.password.allow_copy = 0
                self.password.foreground_color = [0, 0, 0, 0]
                self.database = TextInput(hint_text='Название БД', size_hint=(1, 0.8))
                self.host = TextInput(hint_text='Адрес', size_hint=(1, 0.8))
                self.port = TextInput(hint_text='Порт', size_hint=(1, 0.8))
                ok = Button(text='Подключиться')
                otmena = Button(text='Отмена')
                lalout.add_widget(self.login)
                lalout.add_widget(self.password)
                lalout.add_widget(self.database)
                lalout.add_widget(self.host)
                lalout.add_widget(self.port)
                niz_lalout.add_widget(ok)
                niz_lalout.add_widget(otmena)
                lalout.add_widget(niz_lalout)
                popup = Popup(content=lalout, auto_dismiss=False, title='Подключится к другой БД',
                              size_hint=(None, None), size=(0.8 * width_screen, 0.6 * height_screen))
                #ok.bind(on_press = self.self.enter_the_bd_and_serv(instance, login.text, password.text, database.text, host.text, port.text))
                ok.bind(on_press = self.enter_the_bd_and_serv)
                ok.bind(on_press=popup.dismiss)
                otmena.bind(on_press=popup.dismiss)
                popup.open()

            except (Exception, Error) as error:
                layout = BoxLayout(orientation = 'vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text = textik, font_size = 24)
                content = Button(text = 'Хорошо',font_size = 24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()


        if button_text == 'Ввести команду':
            try:
                print(self.cursor.fetchall)
                self.cursor.execute(self.txt.text)          #update clienty set age = 21 where age = 22
                print(self.cursor)

                if self.cursor:
                    if self.proverka_nal_table:   #== 0:
                        try:
                            record = self.cursor.fetchall()
                            header = self.cursor.description
                            for row in record:
                                print(row)
                            self.table_create(record, header)
                        except (Exception, Error) as error:
                            layout = BoxLayout(orientation='vertical')
                            textik = 'Ошибка: ' + str(error)
                            nadpis = Label(text=textik, font_size=24)
                            content = Button(text='Хорошо', font_size=24)
                            layout.add_widget(nadpis)
                            layout.add_widget(content)
                            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                            # bind the on_press event of the button to the dismiss function
                            content.bind(on_press=popup.dismiss)
                            content.bind(on_press = self.autorollback)
                            popup.open()
                    else:
                        content = Button(text='Понятно!')
                        popup = Popup(content=content, auto_dismiss=False, title='Закройте предыдущую таблицу',
                                      size_hint=(None, None), size=(0.25 * height_screen, 0.25 * width_screen))

                        # bind the on_press event of the button to the dismiss function
                        content.bind(on_press=popup.dismiss)

                        # open the popup
                        popup.open()

            except (Exception, Error) as error:
                layout = BoxLayout(orientation = 'vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text = textik, font_size = 24)
                content = Button(text = 'Хорошо',font_size = 24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()
            #self.nadpis.text = record

        if button_text == 'Узнать имя\nпользователя':
            try:
                self.cursor.execute('select current_user')
                otvet = ['Ваш логин: ' + self.cursor.fetchall()[0][0]][0]
                print(otvet[0])
                label = Label(text=otvet)
                layot = BoxLayout(orientation = 'vertical')
                layot.add_widget(label)
                content = Button(text='Понятно')
                layot.add_widget(content)
                popup = Popup(content=layot, auto_dismiss=False, title='Имя пользователя',
                              size_hint=(None, None), size=(0.5 * height_screen, 0.25 * width_screen))
                content.bind(on_press=popup.dismiss)
                popup.open()


            except (Exception, Error) as error:
                layout = BoxLayout(orientation='vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text=textik, font_size=24)
                content = Button(text='Хорошо', font_size=24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()

        if button_text == 'Отменить\nоперации':
            try:
                print('otm')
                self.connection.rollback()
                content = Button(text='Хорошо')
                popup = Popup(content=content, auto_dismiss=False, title='Отмена операций',
                              size_hint=(None, None), size=(0.5 * height_screen, 0.25 * width_screen))
                content.bind(on_press=popup.dismiss)
                popup.open()


            except (Exception, Error) as error:
                layout = BoxLayout(orientation='vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text=textik, font_size=24)
                content = Button(text='Хорошо', font_size=24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()
        if button_text == 'Подтвердить\nоперации':

            try:
                print('podt')
                self.connection.commit()
                content = Button(text='Хорошо')
                popup = Popup(content=content, auto_dismiss=False, title='Подтверждение операций',
                              size_hint=(None, None), size=(0.5 * height_screen, 0.25 * width_screen))
                content.bind(on_press=popup.dismiss)
                popup.open()

            except (Exception, Error) as error:
                layout = BoxLayout(orientation='vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text=textik, font_size=24)
                content = Button(text='Хорошо', font_size=24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()
        if button_text == 'Создать\nзадание':

            niz_lalout = BoxLayout(orientation = 'horizontal')
            lalout = BoxLayout(orientation = 'vertical')
            self.nazv_zad = TextInput(hint_text='Название задания', size_hint=(1, 0.8))
            self.prioritet_zad = TextInput(hint_text='Приоритет задания', size_hint=(1, 0.8))
            self.text_zad = TextInput(hint_text='Описание задания', size_hint=(1, 0.8))
            self.srok_zad = TextInput(hint_text='Срок задания', size_hint=(1, 0.8))
            self.id_clienta = TextInput(hint_text='Введите ID клиента', size_hint=(1, 0.8))
            self.id_clienta.input_filter = 'float'
            ok = Button(text='Создать')
            otmena = Button(text = 'Отмена')
            lalout.add_widget(self.nazv_zad)
            lalout.add_widget(self.prioritet_zad)
            lalout.add_widget(self.text_zad)
            lalout.add_widget(self.srok_zad)
            lalout.add_widget(self.id_clienta)
            niz_lalout.add_widget(ok)
            niz_lalout.add_widget(otmena)
            lalout.add_widget(niz_lalout)
            popup = Popup(content=lalout, auto_dismiss=False, title='Создать задание',
                          size_hint=(None, None), size=(0.8 * width_screen , 0.6 * height_screen))
            ok.bind(on_press = self.create_zadanie)
            ok.bind(on_press=popup.dismiss)
            otmena.bind(on_press=popup.dismiss)
            popup.open()

        if button_text == 'Завершить\nзадание':

            try:
                zapros = 'select distinct id_zad, nazwanie_zad, status_zadaniya ' \
                         'from rabotniki inner join zadanie on rabotniki.id_rab=zadanie.id_ispolnitel_zadaniya ' \
                         'or rabotniki.id_rab=zadanie.id_avtor_zadaniya ' \
                         'where id_ispolnitel_zadaniya=(select id_rab from rabotniki where login = current_user) ' \
                         'or id_avtor_zadaniya = (select id_rab from rabotniki where login = current_user) '
                print(zapros)
                self.cursor.execute(zapros)
                record = self.cursor.fetchall()
                layout = BoxLayout(orientation = 'vertical')
                niz_layout = BoxLayout(orientation = 'horizontal')
                self.vvod = TextInput(hint_text='Поле для ввода ID', size_hint=(1, 0.8))
                print(record)

                for stroka in record:
                    strocha = 'ID = ' + str(stroka[0]) + ' Название: ' + str(stroka[1]) + " Статус: " + str(stroka[2])
                    print(strocha)
                    nadpis = Label(text = strocha, font_size = 13)
                    layout.add_widget(nadpis)


                layout.add_widget(self.vvod)
                zaversh = Button(text = 'Завершить')
                content = Button(text='Отмена')
                niz_layout.add_widget(zaversh)
                niz_layout.add_widget(content)
                layout.add_widget(niz_layout)
                popup = Popup(content=layout, auto_dismiss=False, title='Завершение задания',
                              size_hint=(None, None), size=(0.75 * width_screen, 0.65 * height_screen))
                zaversh.bind(on_press = self.zaversh_zad)
                zaversh.bind(on_press = popup.dismiss)
                content.bind(on_press=popup.dismiss)
                popup.open()


            except (Exception, Error) as error:
                layout = BoxLayout(orientation = 'vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text = textik, font_size = 24)
                content = Button(text = 'Хорошо',font_size = 24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()

        if button_text == 'Поменять\nисполнителя\nзадания':

            try:
                self.cursor.execute('select current_user')
                logi = self.cursor.fetchall()[0][0]
                self.cursor.execute(
                    '''Select rolname from pg_roles where pg_has_role((select current_user), oid, 'member') and rolname not in (select current_user)''')
                vyvod = self.cursor.fetchall()
                print(vyvod)
                rolename = vyvod[0][0]
                # b =[j for i in vyvod for j in i][0]
                print(rolename)
                print(logi)
                zapros = ''
                if logi == 'postgres':
                    # self.cursor.execute(
                    #     '''Select rolname from pg_roles where pg_has_role((select current_user), oid, 'member') and rolname not in (select current_user)''')
                    # vyvod = self.cursor.fetchall()
                    # print(vyvod)
                    # rolename = vyvod[0][0]
                    # # b =[j for i in vyvod for j in i][0]
                    # print(rolename)

                    zapros = 'select id_zad, nazwanie_zad, status_zadaniya, id_ispolnitel_zadaniya ' \
                             'from rabotniki inner join zadanie on rabotniki.id_rab=zadanie.id_avtor_zadaniya '
                if logi != 'postgres' :

                    if rolename == 'manager' or rolename == 'administrator25':
                        zapros = 'select id_zad, nazwanie_zad, status_zadaniya, id_ispolnitel_zadaniya ' \
                                 'from rabotniki inner join zadanie on rabotniki.id_rab=zadanie.id_avtor_zadaniya '


                    if rolename == 'starprog':
                        # self.cursor.execute(
                        #     '''Select rolname from pg_roles where pg_has_role((select current_user), oid, 'member') and rolname not in (select current_user)''')
                        # vyvod = self.cursor.fetchall()
                        # print(vyvod)
                        # rolename = vyvod[0][0]
                        # # b =[j for i in vyvod for j in i][0]
                        # print(rolename)


                        zapros = 'select distinct id_zad, nazwanie_zad, status_zadaniya, id_ispolnitel_zadaniya ' \
                                 'from rabotniki inner join zadanie on rabotniki.id_rab=zadanie.id_avtor_zadaniya ' \
                                 'where id_ispolnitel_zadaniya=(select id_rab from rabotniki where login = current_user) ' \
                                 'or id_avtor_zadaniya = (select id_rab from rabotniki where login = current_user) '
                print(zapros)
                self.cursor.execute(zapros)
                record = self.cursor.fetchall()
                layout = BoxLayout(orientation = 'vertical')
                nadpis = Label(text = 'Выберите задание, щелкнув по ID')
                layout.add_widget(nadpis)
                #niz_layout = BoxLayout(orientation = 'horizontal')
                print(record)

                popup = Popup(content=layout, auto_dismiss=False, title='Смена исполнителя задания',
                              size_hint=(None, None), size=(0.8 * width_screen, 0.65 * height_screen))

                for stroka in record:
                    nadpis = BoxLayout(orientation = 'horizontal')
                    strocha = ' Название: ' + str(stroka[1]) + " Статус: " + str(stroka[2]) + '\n' + ' Исполнитель: ' + str(stroka[3])
                    print(strocha)
                    # 'ID = ' + str(stroka[0]) +
                    levaya = Button(text = str(stroka[0]))
                    levaya.size_hint_max_x = 0.1 * width_screen
                    pravaya = Label(text = strocha, font_size = 13)
                    nadpis.add_widget(levaya)
                    nadpis.add_widget(pravaya)
                    levaya.bind(on_press=popup.dismiss)
                    levaya.bind(on_press = self.vybrat_ispolnitelya)
                    layout.add_widget(nadpis)


                zaversh = Button(text = 'Отменить')
                layout.add_widget(zaversh)
                #layout.add_widget(niz_layout)
                print('oshib')


                zaversh.bind(on_press = popup.dismiss)
                popup.open()


            except (Exception, Error) as error:
                layout = BoxLayout(orientation = 'vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text = textik, font_size = 24)
                content = Button(text = 'Хорошо',font_size = 24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()



        if button_text == 'Взять\nзадание':

            try:



                layout = BoxLayout(orientation='vertical')
                verh_layout = BoxLayout(orientation='horizontal')
                nadpis = Label(text = 'Выберите приоритет задания', font_size = 15)
                visokiy = Button(text = 'Высокий')
                sredniy = Button(text = 'Средний')
                nizkiy = Button(text = 'Низкий')

                # stroka.lower()

                content = Button(text = 'Отмена')
                verh_layout.add_widget(nizkiy)
                verh_layout.add_widget(sredniy)
                verh_layout.add_widget(visokiy)

                layout.add_widget(nadpis)
                layout.add_widget(verh_layout)
                layout.add_widget(content)

                #self.cursor.execute(zapros)
                #record = self.cursor.fetchall()

                popup = Popup(content = layout, auto_dismiss=False, title='Взять задание',
                              size_hint=(None, None), size=(0.5 * height_screen, 0.45 * width_screen))
                nizkiy.bind(on_press=popup.dismiss)
                nizkiy.bind(on_press = self.vsyat_zadanie)
                sredniy.bind(on_press=popup.dismiss)
                sredniy.bind(on_press = self.vsyat_zadanie)
                visokiy.bind(on_press = self.vsyat_zadanie)
                visokiy.bind(on_press=popup.dismiss)
                content.bind(on_press=popup.dismiss)
                popup.open()



            except (Exception, Error) as error:
                layout = BoxLayout(orientation = 'vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text = textik, font_size = 24)
                content = Button(text = 'Хорошо',font_size = 24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()

        if button_text == 'Поиск по \nатрибутам':
            try:

                sovsem_niz = BoxLayout(orientation = 'horizontal')
                sovsem_niz.size_hint_max_y = 0.04 * height_screen
                layout = BoxLayout(orientation = 'vertical')
                niz_layout = BoxLayout(orientation = 'vertical')
                self.imya = TextInput(hint_text='Введите имя', size_hint=(1, 0.8))
                self.imya.multiline = False
                self.familia = TextInput(hint_text='Введите фамилию', size_hint=(1, 0.8))
                self.familia.multiline = False
                self.otchestvo = TextInput(hint_text='Введите отчество', size_hint=(1, 0.8))
                self.otchestvo.multiline = False
                vihod = Button(text='Отмена')
                podtverdit = Button(text='Найти')
                if (self.parent_group()[1]) == 'sotr_pasp_st':
                    podtverdit.bind(on_press = self.poisk_po_atr_rus)
                if (self.parent_group()[1]) == 'sotr_migr':
                    podtverdit.bind(on_press = self.poisk_po_atr_nerus)

                sovsem_niz.add_widget(podtverdit)
                sovsem_niz.add_widget(vihod)
                niz_layout.add_widget(self.imya)
                niz_layout.add_widget(self.familia)
                niz_layout.add_widget(self.otchestvo)
                layout.add_widget(niz_layout)

                layout.add_widget(sovsem_niz)
                popup = Popup(content= layout, auto_dismiss=False, title='Поиск по атрибутам',
                              size_hint=(None, None), size=( 0.45 * width_screen, 0.3 * height_screen))
                vihod.bind(on_press=popup.dismiss)
                podtverdit.bind(on_press = popup.dismiss)
                popup.open()


            except (Exception, Error) as error:
                layout = BoxLayout(orientation='vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text=textik, font_size=24)
                content = Button(text='Хорошо', font_size=24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()



        # if button_text == 'Поиск по\nатрибутам':
        #     try:
        #
        #
        #         layout = BoxLayout(orientation = 'vertical')
        #         niz_layout = BoxLayout(orientation = 'horizontal')
        #         textik = Label(text = 'Выберите нужный атрибут' , font_size = 15)
        #         btn_gorod = Button(text = 'Город')
        #         btn_fio = Button(text = 'ФИО')
        #         vihod = Button(text='Отмена')
        #         niz_layout.add_widget(btn_gorod)
        #         niz_layout.add_widget(btn_fio)
        #         niz_layout.add_widget(vihod)
        #         layout.add_widget(textik)
        #         layout.add_widget(niz_layout)
        #         popup = Popup(content= layout, auto_dismiss=False, title='Поиск по атрибутам',
        #                       size_hint=(None, None), size=(0.5 * height_screen, 0.45 * width_screen))
        #         btn_fio.bind(on_press=self.vybor_atr)
        #         btn_fio.bind(on_press=popup.dismiss)
        #         btn_gorod.bind(on_press = self.vybor_atr)
        #         btn_gorod.bind(on_press=popup.dismiss)
        #         vihod.bind(on_press=popup.dismiss)
        #         popup.open()
        #
        #
        #     except (Exception, Error) as error:
        #         layout = BoxLayout(orientation='vertical')
        #         textik = 'Ошибка: ' + str(error)
        #         nadpis = Label(text=textik, font_size=24)
        #         content = Button(text='Хорошо', font_size=24)
        #         layout.add_widget(nadpis)
        #         layout.add_widget(content)
        #         popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
        #                       size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
        #         # bind the on_press event of the button to the dismiss function
        #         content.bind(on_press=popup.dismiss)
        #         popup.open()


        if button_text == 'Просмотр\nсвоих\nзаданий':

            try:
                # print('otm')
                # content = Button(text='Хорошо')
                # popup = Popup(content=content, auto_dismiss=False, title='Не надо',
                #               size_hint=(None, None), size=(0.5 * height_screen, 0.25 * width_screen))
                # content.bind(on_press=popup.dismiss)
                # popup.open()
                zapros = 'select distinct id_zad, nazwanie_zad, prioritet, status_zadaniya, date_sozdaniya, period_wypolneniya ' \
                         'from rabotniki inner join zadanie on rabotniki.id_rab=zadanie.id_ispolnitel_zadaniya ' \
                         'or rabotniki.id_rab=zadanie.id_avtor_zadaniya ' \
                         'where id_ispolnitel_zadaniya=(select id_rab from rabotniki where login = current_user) ' \
                         'or id_avtor_zadaniya = (select id_rab from rabotniki where login = current_user) '
                print(zapros)
                self.cursor.execute(zapros)
                record = self.cursor.fetchall()
                # new_record = [[0] * len(record) for _ in range(len(record[0]))]
                #
                # for i in range(len(record)):
                #     for j in range(len(record[0])):
                #         new_record[j][i] = record[i][j]
                # self.table_create(new_record)
                self.table_create(record)

            except (Exception, Error) as error:
                layout = BoxLayout(orientation='vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text=textik, font_size=14)
                content = Button(text='Хорошо', font_size=24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()



        if button_text == 'Регистрация\nнового\nпользователя':
            print('reg')

            try:
                text = Label(text='Выберите отдел и\nпродолжите регистрацию', font_size=24)
                lalout = BoxLayout(orientation='vertical')
                mfc = Button(text='Администратор')
                pasport = Button(text = 'Сотрудник паспортного стола')
                migr = Button(text= 'Сотрудник отдела по миграции')
                otmena = Button(text='Отмена')
                lalout.add_widget(text)
                lalout.add_widget(mfc)
                lalout.add_widget(pasport)
                lalout.add_widget(migr)
                lalout.add_widget(otmena)
                popup = Popup(content=lalout, auto_dismiss=False, title='Регистрация нового пользователя',
                              size_hint=(None, None), size=(0.6 * width_screen, 0.6 * height_screen))
                mfc.bind(on_press = self.reg_new_polzovat)
                mfc.bind(on_press=popup.dismiss)
                pasport.bind(on_press = self.reg_new_polzovat)
                pasport.bind(on_press=popup.dismiss)
                migr.bind(on_press = self.reg_new_polzovat)
                migr.bind(on_press=popup.dismiss)
                otmena.bind(on_press=popup.dismiss)
                popup.open()

            except (Exception, Error) as error:
                layout = BoxLayout(orientation = 'vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text = textik, font_size = 24)
                content = Button(text = 'Хорошо',font_size = 24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(0, 6 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()

        if button_text == 'Взаимодействие с\nтаблицей':
            try:
                layout = BoxLayout(orientation='vertical')
                niz_layout = BoxLayout(orientation = 'vertical')
                nadpis = Label(text='Выберите нужное действие', font_size=24)
                nadpis.size_hint_max_y =0.1 * height_screen
                content = Button(text='Отмена', font_size=14) #background_color=[255 / 255, 104 / 255, 51 / 255, 1])
                content.size_hint_max_y = 0.1 * height_screen
                layout.add_widget(nadpis)

                popup = Popup(content=layout, auto_dismiss=False, title='Взаимодействие с таблицей',
                              size_hint=(None, None), size=(0.4 * width_screen, 0.8 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)

                btn_prosm = Button(text = 'Посмотреть отдельную запись',on_press = popup.dismiss)
                btn_prosm.bind(on_press = self.zap_deistv)
                niz_layout.add_widget(btn_prosm)
                btn_izm = Button(text = 'Изменить отдельную запись',on_press = popup.dismiss)
                btn_izm.bind(on_press = self.zap_deistv)
                niz_layout.add_widget(btn_izm)
                btn_del = Button(text = 'Удалить отдельную запись',on_press = popup.dismiss)
                btn_del.bind(on_press = self.zap_deistv)
                niz_layout.add_widget(btn_del)
                btn_add = Button(text = 'Добавить новую запись',on_press = popup.dismiss)
                btn_add.bind(on_press = self.zap_add)
                niz_layout.add_widget(btn_add)

                if self.otkryto_predstavlenie == 1:
                    niz_layout.remove_widget(btn_izm)
                    niz_layout.remove_widget(btn_del)
                    niz_layout.remove_widget(btn_add)
                # print(self.superheader, self.supertable, self.supername_table)
                #
                # for slovo in self.superheader:
                #     #print(slovo)
                #     knoka = Button(text = slovo[0])
                #     #zadanie.bind(on_press=self.enter_the_table)
                #     knoka.bind(on_press=popup.dismiss)
                #     niz_layout.add_widget(knoka)

                layout.add_widget(niz_layout)
                layout.add_widget(content)


                popup.open()


            except (Exception, Error) as error:
                layout = BoxLayout(orientation='vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text=textik, font_size=24)
                content = Button(text='Хорошо', font_size=24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()

        if button_text == 'Удаление \nгражданина \nиз базы':
            try:

                self.proverka_polz()
                #print(instance.text)
                layout = BoxLayout(orientation='vertical')
                niz_layout = BoxLayout(orientation = 'horizontal')
                content = Button(text='Отмена', font_size=18)
                content.size_hint_max_y = 0.03 * height_screen
                popup = Popup(content=layout, auto_dismiss=False, title='Удалить гражданина из базы',
                              size_hint=(None, None), size=(0.5 * width_screen, 0.5 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)

                for zap in self.supertable:
                    #print(zap[0])
                    btn = Button(text = str(zap[0]), font_size = 14, on_press = popup.dismiss)
                    btn.size_hint_min_x = 0.01 * width_screen
                    if (self.parent_group()[1]) == 'sotr_pasp_st':
                        btn.bind(on_press=self.delete_all_inf_rus)
                    if (self.parent_group()[1]) == 'sotr_migr':
                        btn.bind(on_press = self.delete_all_inf_nerus)

                    niz_layout.add_widget(btn)


                olg_layout = BoxLayout(orientation = 'vertical')
                zapis_layout = BoxLayout(orientation = 'vertical')
                niz_layout.add_widget(olg_layout)
                niz_layout.add_widget(zapis_layout)
                layout.add_widget(niz_layout)

                knopki_layout = BoxLayout(orientation = 'horizontal')
                knopki_layout.add_widget(content)
                layout.add_widget(knopki_layout)


                popup.open()

            except (Exception, Error) as error:
                layout = BoxLayout(orientation = 'vertical')
                textik = 'Ошибка: ' + str(error)
                nadpis = Label(text = textik, font_size = 24)
                content = Button(text = 'Хорошо',font_size = 24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                              size_hint=(None, None), size=(0, 6 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()

    def on_text(self, instance, value):
        print('The widget', instance, 'have:', value)
        return value

    def table_create(self, table, header):
        if self.proverka_nal_table == 1:
            self.mestodlyainfi.remove_widget(self.main_tablica)

        self.main_tablica = BoxLayout(orientation='vertical')
        self.supertable = table
        self.superheader = header

        #print(header, len(header))
        oglav = BoxLayout(orientation = 'horizontal')
        for i in header:
            textus = self.perevodchik(i[0])
            stolb = Label(text=textus, font_size=13, color= [1, 1, 1, 1])   #[153 / 255, 153 / 255, 153 / 255, 1])
            CustomGraphics.SetBG(stolb, bg_color=[84 / 255, 47 / 255, 58 / 255, 1])
            stolb.outline_color = [1, 1, 1, 1]
            oglav.add_widget(stolb)
            oglav.padding = 1
            oglav.size_hint_min_y = 0.1 * height_screen
        self.main_tablica.add_widget(oglav)
        count = 0
        count_str = 0
        lene = len(table)
        kol_str = lene // 8
        # print(lene)
        # print(kol_str)
        # print(lene % 8)
        count = 0
        if kol_str > -1:
            for row in table:
                if count == 8:
                     break
                tablica = BoxLayout()
                for label in row:
                    if type(label) is str and len(label.strip()) > 15:
                        new_label = self.perenos_stroki(label.strip())
                        # print(label.strip(), len(new_label))
                        # a = (new_label[:(len(new_label) // 2 // 2)])
                        # b = (new_label[(len(new_label) // 2 // 2):])
                        # # print(a)
                        # # print(b)
                        # new_label = (a + '\n' + b)
                        # print(' '.join(map(str, new_label)))
                    else:
                        if type(label) is str:
                            new_label = label.strip()
                        else:
                            new_label = label
                    # print(new_label)
                    # print(new_label)
                    new_label = self.perevodchik(str(new_label))
                    textik = Label(text=str(new_label), font_size=13, color=[1, 1, 1, 1], padding = (1,0))
                    CustomGraphics.SetBG(textik, bg_color=[84 / 255, 47 / 255, 58 / 255, 0.75])

                    tablica.add_widget(textik)
                tablica.padding = (1, 1)

                self.main_tablica.add_widget(tablica)
                count += 1



            layout = BoxLayout(orientation='horizontal')
            self.str_label = Button(text = '1', background_color=[255 / 255, 204 / 255, 51 / 255, 1])
            self.str_label.size_hint_max_x = 0.01 * width_screen
            self.str_label.disabled = 1
            layout.add_widget(self.str_label)
            for stroka in range(kol_str+1):
                button = Button(text=str(stroka+1), on_press=self.table_create_perelist)
                button.size_hint_max_x = 0.05 * width_screen
                layout.add_widget(button)
            layout.padding = 10
            layout.size_hint_max_y = 0.1 * height_screen



            #layout.add_widget(button)


            # layout.add_widget(button_minus)
            # layout.add_widget(button_plus)

            self.main_tablica.add_widget(layout)


            self.mestodlyainfi.add_widget(self.main_tablica)

            self.proverka_nal_table = 1

    def autorizac(self):
      #  layout = FloatLayout(),
        self.autor = FloatLayout(size = (320, 300))  #BoxLayout(orientation = 'horizontal')
        self.vvod_login = TextInput(hint_text='Введите логин', size_hint=(0.5, 0.1), pos =(20, 370), font_size = 24)
        self.vvod_login.multiline = False
        self.vvod_pass = TextInput(hint_text='Введите пароль', size_hint=(0.5, 0.1), pos = (20, 320), font_size = 24)
        self.vvod_pass.foreground_color = [0,0,0,0]
        self.vvod_pass.allow_copy = 0
        self.vvod_pass.multiline = False
        self.enter_date = Button(text='Авторизоваться', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=24, pos = (20, 270))
        self.enter_date.bind(on_press = self.on_press_button)
        # self.enter_date.width = 0.5
        # self.enter_date.height = 0.5
        # self.vvod_pass.height = 0.5
        # self.vvod_login.height = 0.5
        self.enter_date.size_hint_x = 0.4
        self.enter_date.size_hint_y = 0.09
        # self.vvod_login.size_hint_x = 0.9
        # self.vvod_login.size_hint_y = 0.09
        # self.vvod_pass.size_hint_x = 0.9
        # self.vvod_pass.size_hint_y = 0.09
        self.autor.add_widget(self.enter_date)
        self.autor.add_widget(self.vvod_login)
        self.autor.add_widget(self.vvod_pass)
        exit_button = Button(text = 'Выйти из\nприложения',font_size = 24 ,size_hint = (0.2, 0.12), pos = (20, 20), background_color=[255 / 255, 204 / 255, 51 / 255, 1])
        exit_button.bind(on_press = self.on_press_button)
        self.autor.add_widget(exit_button)
        self.otkryto_predstavlenie = 0
        return self.autor

    def enter_the_bd(self, log, pas, database):
        try:
            # Подключение к существующей базе данных
            self.connection = psycopg2.connect(user=log,
                                          # пароль, который указали при установке PostgreSQL
                                          password=pas,
                                          host="127.0.0.1",
                                          port="5432",
                                          database=database)

            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
            # Распечатать сведения о PostgreSQL
            print("Информация о сервере PostgreSQL")
            print(self.connection.get_dsn_parameters(), "\n")
            # Выполнение SQL-запроса
            self.cursor.execute("SELECT version();")
            # Получить результат
            record = self.cursor.fetchone()
            print("Вы подключены к - ", record, "\n")
        #    cursor.execute("SELECT * from zadanie")
        #    record = cursor.fetchall()
        #    print("Результат", record)
            self.proverka_autor = 1
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        # finally:
        #    if connection:
        #        cursor.close()
        #        connection.close()
        #       print("Соединение с PostgreSQL закрыто")
            self.proverka_autor = 0

    def proverka_polz(self):

        try:
            logi = ''

            logi, rolename = self.parent_group()

            # self.cursor.execute('select current_user')
            # logi = self.cursor.fetchall()[0][0]
            # print(logi)
            # self.btn_join_an_bd.disabled = 1
            # self.btn_join_an_bd.opacity = 0
            if logi == 'postgres':
                self.start(1)
                print('postgres')

            if logi != 'postgres':
                # self.cursor.execute('''Select rolname from pg_roles where pg_has_role((select current_user), oid, 'member') and rolname not in (select current_user)''')
                # vyvod = self.cursor.fetchall()
                # print(vyvod)
                # rolename = vyvod[0][0]
                # #b =[j for i in vyvod for j in i][0]
                # print(rolename)



                if rolename == 'sotr_migr':
                    self.start(2)

                if rolename == 'sotr_pasp_st':
                    self.start(3)


                if rolename == 'admin_mfc':
                    self.start(4)

                else:
                    self.autorizac()

            logi = ''

        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def vybor_atr(self, instance):
        self.button_atr = instance.text
        print(self.button_atr)
        try:

            layout = BoxLayout(orientation='vertical')
            niz_layout = BoxLayout(orientation='horizontal')
            textik = Label(text='Введите строку или символ для поиска', font_size=15)
            knopka = Button(text='Ввести')
            vihod = Button(text='Отмена')
            self.vvod = TextInput(hint_text='Поле для ввода', size_hint=(1, 0.8))
            niz_layout.add_widget(knopka)
            niz_layout.add_widget(vihod)
            layout.add_widget(textik)
            layout.add_widget(self.vvod)
            layout.add_widget(niz_layout)
            popu = Popup(content=layout, auto_dismiss=False, title='Поиск по атрибутам',
                          size_hint=(None, None), size=(0.5 * height_screen, 0.45 * width_screen))
            knopka.bind(on_press=popu.dismiss)
            knopka.bind(on_press = self.poisk_po_atr)
            vihod.bind(on_press=popu.dismiss)
            popu.open()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def poisk_po_atr(self, instance):

        print(self.button_atr, self.vvod.text)
        command = 'select * from poisk_po_atr(' + "'" + self.button_atr + "'" + ', ' + "'" + self.vvod.text + "'" + ')'
        self.button_atr = ''
        self.vvod.text = ''
        print(command)
        try:
            self.cursor.execute(command)
            record = self.cursor.fetchall()
            # new_record = [[0] * len(record) for _ in range(len(record[0]))]
            #
            # for i in range(len(record)):
            #     for j in range(len(record[0])):
            #         new_record[j][i] = record[i][j]
            #self.table_create(new_record)
            self.table_create(record)
        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def enter_the_table(self, instance):
        print(instance.text)
        tablichka = ''
        tablica = instance.text
        if tablica == 'Дети иностранных граждан':
            tablichka = 'deti_nerus'
        if tablica == 'Дети российских граждан':
            tablichka = 'deti_rus'
        if tablica == 'Граждане РФ':
            tablichka = '"grazhdane_RF"'
        if tablica == 'Иностранные граждане':
            tablichka = 'nerus_grazhd'
        if tablica == 'Паспорта РФ':
            tablichka = 'pasporta'
        if tablica == 'Список подразделений':
            tablichka = 'podrazdelenie'
        if tablica == 'Список сотрудников миграционного отдела':
            tablichka = 'sotrudnik_migrazi'
        if tablica == 'Список сотрудников паспортного стола':
            tablichka = 'sotrudnik_pasp_stola'
        if tablica == 'Супруги иностранных граждан':
            tablichka = 'suprugi_nerus'
        if tablica == 'Супруги граждан РФ':
            tablichka = 'suprugi_rus'
        if tablica == 'Временные удостоверения личности':
            tablichka = 'wrem_udos_li4n'
        if tablica == 'Информация по выдаче документов':
            tablichka = 'wydacha_dokumenta'
        if tablica == 'Соответствие детей и граждан':
            tablichka = 'mnogo_deti_rus'
        if tablica == 'Соответствие детей и граждан ':
            tablichka = 'mnogo_deti_nerus'


        command = 'select * from ' + tablichka
        print(command)
        try:

            self.cursor.execute(command)
            record = self.cursor.fetchall()
            header = self.cursor.description
            print(self.cursor.description)
            self.supername_table = tablichka
            self.kakaya_now_tabl.text = 'Открыта таблица:\n' + self.perevodchik(self.supername_table)
            # new_record = [[0] * len(record) for _ in range(len(record[0]))]
            #
            # for i in range(len(record)):
            #     for j in range(len(record[0])):
            #         new_record[j][i] = record[i][j]
            # self.table_create(new_record)
            self.table_create(record, header)
            self.otkryto_predstavlenie = 0

        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=14)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            content.bind(on_press = self.autorollback)
            popup.open()

    def zaversh_zad(self,instance):

        try:
            print(self.vvod.text, instance.text)
            id_zav = self.vvod.text
            zapros = 'call done_zadanie(' + id_zav + ')'

            self.cursor.execute(zapros)

            content = Button(text='Хорошо', font_size=24)
            popup = Popup(content=content, auto_dismiss=False, title='Завершено',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


        except (Exception, Error) as error:
            print(error)
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def vsyat_zadanie(self, instance):

        prioritet = instance.text.lower()
        try:

            print(prioritet)

            zapros = 'call vsyat_zadanie(' + "'" + prioritet + "'" + ')'
            print(prioritet, zapros)
            self.cursor.execute(zapros)
            content = Button(text='Вы взяли задание', font_size=24)
            popup = Popup(content=content, auto_dismiss=False, title='Взять задание',
                          size_hint=(None, None), size=(0.5 * height_screen, 0.45 * width_screen))
            content.bind(on_press=popup.dismiss)
            popup.open()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()
            print('oshibla vsyat')
    def enter_the_bd_and_serv(self, instance):   #instance, log, pas, database, host, port):
        log = self.login.text
        self.login.text = ''
        pas = self.password.text
        self.password.text = ''
        database = self.database.text
        self.database.text = ''
        host = self.host.text
        self.host.text = ''
        port = self.port.text
        self.port.text = ''

        if database == '':
           database = 'pasport_stol'
        if host == '':
           host = '127.0.0.1'
        if port == '':
           port = '5432'

        print(log, pas, database, host, port)
        print(instance.text)
        try:
            # Подключение к существующей базе данных
            self.connection = psycopg2.connect(user=log,
                                          # пароль, который указали при установке PostgreSQL
                                          password=pas,
                                          host=host, #"127.0.0.1"
                                          port=port, #"5432"
                                          database=database) #lababd

            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
            # Распечатать сведения о PostgreSQL
            print("Информация о сервере PostgreSQL")
            print(self.connection.get_dsn_parameters(), "\n")
            # Выполнение SQL-запроса
            self.cursor.execute("SELECT version();")
            # Получить результат
            record = self.cursor.fetchone()
            print("Вы подключены к - ", record, "\n")
        #    cursor.execute("SELECT * from zadanie")
        #    record = cursor.fetchall()
        #    print("Результат", record)
            self.proverka_autor = 1
            self.proverka_polz()
        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def reg_new_polzovat(self, instance):
        print(instance.text)

        try:
            if instance.text != 'Повторить':
                self.dolgnost = instance.text
            niz_lalout = BoxLayout(orientation='vertical')
            lalout = BoxLayout(orientation='vertical')
            ok = Button(text='Продолжить регистрацию')
            spis_pasp = ('делопроизводитель', 'заместитель директора', 'директор отдела', 'паспортист','инспектор', 'менеджер', 'паспортист')
            spis_migr = ('заместитель директора','директор отдела', 'менеджер',  'паспортист',  'делопроизводитель',  'инспектор',  'паспортист')

            if self.dolgnost == 'Администратор':

                niz_lalout.add_widget(ok)

            otmena = Button(text='Отмена')
            #niz_lalout.add_widget(ok)

            lalout.add_widget(niz_lalout)
            popup = Popup(content=lalout, auto_dismiss=False, title='Регистрация нового пользователя',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.6 * height_screen))
            if self.dolgnost == 'Сотрудник паспортного стола':
                for dolg in spis_pasp:
                    knopka = Button(text=dolg, on_press = self.reg_new_polz)
                    knopka.bind(on_press =popup.dismiss)
                    niz_lalout.add_widget(knopka)
            if self.dolgnost == 'Сотрудник отдела по миграции':
                for dolg in spis_migr:
                    knopka = Button(text=dolg, on_press = self.reg_new_polz)
                    knopka.bind(on_press =popup.dismiss)
                    niz_lalout.add_widget(knopka)
            niz_lalout.add_widget(otmena)
            ok.bind(on_press=self.reg_new_polz)
            ok.bind(on_press=popup.dismiss)
            otmena.bind(on_press=popup.dismiss)
            popup.open()

        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def reg_new_polz(self, instance):
        print(instance.text)

        try:
            if instance.text != 'Повторить':
                self.professiya = instance.text
            if instance.text == 'Повторить':
                login = self.login.text
                fio = self.fio.text

            niz_lalout = BoxLayout(orientation='horizontal')
            lalout = BoxLayout(orientation='vertical')
            self.login = TextInput(hint_text='Логин', size_hint=(1, 0.8))
            self.login.multiline = False
            self.password1 = TextInput(hint_text='Пароль', size_hint=(1, 0.8))
            self.password1.multiline = False
            self.password1.foreground_color = [0,0,0,0]
            self.password1.allow_copy = 0

            self.password2 = TextInput(hint_text='Повторите пароль', size_hint=(1, 0.8))
            self.password2.multiline = False
            self.password2.foreground_color = [0, 0, 0, 0]
            self.password2.allow_copy = 0
            self.fio = TextInput(hint_text='ФИО', size_hint=(1, 0.8))
            self.fio.multiline = False
            ok = Button(text='Зарегистрировать')
            otmena = Button(text='Отмена')
            lalout.add_widget(self.login)
            lalout.add_widget(self.password1)
            lalout.add_widget(self.password2)
            lalout.add_widget(self.fio)
            niz_lalout.add_widget(ok)
            niz_lalout.add_widget(otmena)
            lalout.add_widget(niz_lalout)
            if instance.text == 'Повторить':
                self.login.text = login
                self.fio.text = fio
            popup = Popup(content=lalout, auto_dismiss=False, title='Регистрация нового пользователя',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.6 * height_screen))
            ok.bind(on_press=self.konec_registracii)
            ok.bind(on_press=popup.dismiss)
            otmena.bind(on_press=popup.dismiss)
            popup.open()

        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def konec_registracii(self, instance):

        try:

            if self.password1.text == self.password2.text:
                login = self.login.text
                self.login.text = ''
                password = self.password1.text
                self.password1.text = ''
                professiya = self.professiya
                self.professiya = ''
                dolgnost = self.dolgnost
                self.dolgnost = ''
                fio = self.fio.text
                self.fio.text = ''
                # print(instance.text)
                # print(login, password, professiya, dolgnost, fio)
                tabl_dolg = ''
                dolg = ''
                if dolgnost == 'Сотрудник паспортного стола':
                    dolg = 'sotr_pasp_st'
                    tabl_dolg = 'sotrudnik_pasp_stola'
                if dolgnost == 'Сотрудник отдела по миграции':
                    dolg = 'sotr_mig'
                    tabl_dolg = 'sotrudnik_migrazi'


                dolg_table = 'insert into ' + tabl_dolg + '(fio, professiya) values (' + "'" + fio + "'" + ',' + "'"+ professiya + "'" + ')'

                if dolgnost == 'Администратор':
                    dolg = 'admin_mfc'
                    dolg_table = ''

                zapros =  'create user ' + login + ' with password ' + "'" + password + "'" + '; grant ' + dolg +' to ' + login + ';' + dolg_table

                print(zapros)


                self.cursor.execute(zapros)

                ok = Button(text='Успешно')
                popup = Popup(content=ok, auto_dismiss=False, title='Регистрация нового пользователя',
                              size_hint=(None, None), size=(0.8 * width_screen, 0.6 * height_screen))
                ok.bind(on_press=popup.dismiss)
                popup.open()

            else:
                layout = BoxLayout(orientation = 'vertical')
                niz_layout = BoxLayout(orientation = 'horizontal')
                label = Label(text = 'Пароли не совпадают', font_size = 24)
                ok = Button(text='Повторить')
                otmena = Button(text = 'Отменить')
                niz_layout.add_widget(ok)
                niz_layout.add_widget(otmena)
                niz_layout.size_hint_max_y = 0.09 * height_screen
                layout.add_widget(label)
                layout.add_widget(niz_layout)
                popup = Popup(content=layout, auto_dismiss=False, title='Регистрация нового пользователя',
                              size_hint=(None, None), size=(0.8 * width_screen, 0.6 * height_screen))
                ok.bind(on_press=self.reg_new_polz)
                ok.bind(on_press=popup.dismiss)
                otmena.bind(on_press = popup.dismiss)
                popup.open()

        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def vybrat_ispolnitelya(self, instance):

        try:
            self.vybor_zad = instance.text
            print(self.vybor_zad)

            zapros = 'select id_rab, fio, professiya ' \
                     'from rabotniki '


            print(zapros)
            self.cursor.execute(zapros)
            record = self.cursor.fetchall()
            layout = BoxLayout(orientation='vertical')
            # niz_layout = BoxLayout(orientation = 'horizontal')
            print(record)

            popup = Popup(content=layout, auto_dismiss=False, title='Смена исполнителя задания',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.65 * height_screen))

            for stroka in record:
                nadpis = BoxLayout(orientation='horizontal')
                strocha = ' ФИО: ' + str(stroka[1]) + '\n' + " Должность: " + str(stroka[2])
                print(strocha)
                # 'ID = ' + str(stroka[0]) +
                levaya = Button(text=str(stroka[0]))
                levaya.size_hint_max_x = 0.1 * width_screen
                pravaya = Label(text=strocha, font_size=13)
                nadpis.add_widget(levaya)
                nadpis.add_widget(pravaya)
                levaya.bind(on_press=popup.dismiss)
                levaya.bind(on_press=self.pomenyat_ispolnitelya)
                layout.add_widget(nadpis)

            zaversh = Button(text='Отменить')
            layout.add_widget(zaversh)
            # layout.add_widget(niz_layout)
            print('oshib')

            zaversh.bind(on_press=popup.dismiss)
            popup.open()

        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def pomenyat_ispolnitelya(self, instance):

        try:
            id_isp = instance.text
            id_zad = self.vybor_zad
            self.vybor_zad = ''
            print(id_isp, id_zad)

            zapros = 'call set_isp_zadanie(' + id_zad + ', ' + id_isp + ')'

            print(zapros)
            self.cursor.execute(zapros)
            button = Button(text = 'Исполнитель успешно\nизменён')
            popup = Popup(content=button, auto_dismiss=False, title='Смена исполнителя задания',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.65 * height_screen))
            button.bind(on_press=popup.dismiss)
            popup.open()



        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def create_zadanie(self, instance):

        try:
            nazv_zad = self.nazv_zad.text
            prioritet_zad = self.prioritet_zad.text
            text_zad = self.text_zad.text
            srok_zad = self.srok_zad.text
            id_clienta = self.id_clienta.text

            self.nazv_zad.text = ''
            self.prioritet_zad.text = ''
            self.text_zad.text = ''
            self.srok_zad.text = ''
            self.id_clienta.text = ''

            print(nazv_zad, prioritet_zad, text_zad, srok_zad, id_clienta)

            zapros = 'call create_zadanie(' + "'" + nazv_zad + "', " + "'" + prioritet_zad + "', " + "'" + text_zad + "', " + "'" + srok_zad + "'," + id_clienta + ')'

            print(zapros)
            self.cursor.execute(zapros)



            button = Button(text='Задание успешно\nсоздано', font_size = 24)
            popup = Popup(content=button, auto_dismiss=False, title='Создание задания',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.65 * height_screen))
            button.bind(on_press=popup.dismiss)
            popup.open()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def start(self, role_num):

        self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_UNCOMMITTED)
        try:
            self.layout.remove_widget(self.currenter_table)
        except (Exception, Error) as error:
            print(error)
        self.otkryto_predstavlenie = 0
        self.currenter_table = FloatLayout(size = (320, 300))

        self.levyistolb = BoxLayout(orientation = 'vertical', size_hint=(0.1, 1)  , pos =(0.01 * width_screen, 1))
        self.praviystolb = BoxLayout(orientation = 'vertical', size_hint=(0.1, 1)  , pos =(0.88 * width_screen, 1))
        self.mestodlyainfi = BoxLayout(orientation = 'vertical', size_hint=(0.8, 1)  , pos =(0.11 * width_screen, 1))

        if role_num == 1:
            for i in range(8):
                if i == 0:
                    self.btn_exit = Button(text='Выйти из\nприложения',
                                           background_color=[255 / 255, 104 / 255, 51 / 255, 1], font_size=12)
                    self.btn_exit.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_exit)

                if i == 1:
                    self.btn_enter_c = Button(text='Ввести команду\nSQL',
                                              background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_enter_c.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_enter_c)
                if i == 2:
                    self.btn_join_an_bd = Button(text='Подключение\nк другой\nбазе данных',
                                                 background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_join_an_bd.bind(on_press=self.on_press_button)
                    # self.btn = Label(text='', font_size=12)
                    self.praviystolb.add_widget(self.btn_join_an_bd)
                if i == 4:
                    self.btn_uzn = Button(text='Узнать имя\nпользователя', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_uzn.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_uzn)
                if i == 5:
                    self.btn_otm = Button(text='Отменить\nоперации', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_otm.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_otm)
                if i == 6:
                    self.btn_podt = Button(text='Подтвердить\nоперации', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_podt.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_podt)
                if i == 7:
                    self.btn_close_soed = Button(text='Закрыть\nсоединение', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_close_soed.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_close_soed)


            self.supername_table = 'wydacha_dokumenta'

            #zapros = 'select * from '+'"grazhdane_RF"'
            zapros ='Select * from ' + self.supername_table
            #print(zapros)
            self.cursor.execute(zapros)
            record = self.cursor.fetchall()
            header = self.cursor.description
            #print(record, header)
            self.table_create(record, header)

            for i in range(8):
                if i == 0:
                    self.deti_rod_predst = Button(text='Картотека \nграждан',
                                          background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.deti_rod_predst.bind(on_press=self.on_press_button)
                    self.deti_rod_predst.bind(on_press = self.vybor_cartoteki)
                    self.levyistolb.add_widget(self.deti_rod_predst)
                if i == 1:
                    self.full_delete = Button(text='Удаление \nгражданина \nиз базы',
                                          background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.full_delete.bind(on_press=self.on_press_button)
                    self.levyistolb.add_widget(self.full_delete)
                if i == 2:
                    self.srch_atr = Button(text='Поиск по \nатрибутам',
                                          background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.srch_atr.bind(on_press=self.on_press_button)
                    self.srch_atr.bind(on_press=self.vybor_tabl_dlya_srch)
                    self.levyistolb.add_widget(self.srch_atr)
                if i == 3:
                    self.btn_reg = Button(text='Регистрация\nнового\nпользователя',
                                          background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_reg.bind(on_press=self.on_press_button)
                    self.levyistolb.add_widget(self.btn_reg)
                if i == 4:
                    self.btn_soed = Button(text='Зайти под другим\nпользователем', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_soed.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_soed)

                if i ==6:
                    self.btn_open = Button(text='Открыть\nтаблицу', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    #self.btn = Label(text='', font_size=12)
                    self.btn_open.bind(on_press=self.otrkytie_tabl)
                    self.levyistolb.add_widget(self.btn_open)
                if i == 5:
                    self.btn_chng = Button(text='Взаимодействие с\nтаблицей', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    #self.btn = Label(text='', font_size=12)
                    self.btn_chng.bind(on_press=self.on_press_button)
                    self.levyistolb.add_widget(self.btn_chng)
                if i == 7:
                    self.kakaya_now_tabl = Button(text='', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12, disabled = 1)
                    #self.btn = Label(text='', font_size=12)
                    self.kakaya_now_tabl.text = 'Открыта таблица:\n' + self.perevodchik(self.supername_table)
                    self.levyistolb.add_widget(self.kakaya_now_tabl)

        if role_num == 2:  # sotr mig
            for i in range(8):
                if i == 0:
                    self.btn_exit = Button(text='Выйти из\nприложения',
                                           background_color=[255 / 255, 104 / 255, 51 / 255, 1], font_size=12)
                    self.btn_exit.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_exit)

                # if i == 1:
                #     self.btn_enter_c = Button(text='Ввести команду\nSQL',
                #                               background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                #     self.btn_enter_c.bind(on_press=self.on_press_button)
                #     self.praviystolb.add_widget(self.btn_enter_c)
                # if i == 2:
                #     self.btn_join_an_bd = Button(text='Подключение\nк другой\nбазе данных',
                #                                  background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                #     self.btn_join_an_bd.bind(on_press=self.on_press_button)
                #     # self.btn = Label(text='', font_size=12)
                #     self.praviystolb.add_widget(self.btn_join_an_bd)
                if i == 4:
                    self.btn_uzn = Button(text='Узнать имя\nпользователя', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_uzn.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_uzn)
                if i == 5:
                    self.btn_otm = Button(text='Отменить\nоперации', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_otm.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_otm)
                if i == 6:
                    self.btn_podt = Button(text='Подтвердить\nоперации', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_podt.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_podt)
                if i == 7:
                    self.btn_close_soed = Button(text='Закрыть\nсоединение', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_close_soed.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_close_soed)


            self.supername_table = 'nerus_grazhd'

            #zapros = 'select * from '+'"grazhdane_RF"'
            zapros ='Select * from ' + self.supername_table
            #print(zapros)
            self.cursor.execute(zapros)
            record = self.cursor.fetchall()
            header = self.cursor.description
            #print(record, header)
            self.table_create(record, header)

            for i in range(8):
                if i == 0:
                    self.deti_rod_predst = Button(text='Картотека \nграждан',
                                                  background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.deti_rod_predst.bind(on_press=self.on_press_button)
                    self.deti_rod_predst.bind(on_press=self.cartoteka_nerus)
                    self.levyistolb.add_widget(self.deti_rod_predst)

                if i == 1:
                    self.full_delete = Button(text='Удаление \nгражданина \nиз базы',
                                              background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.full_delete.bind(on_press=self.on_press_button)
                    self.levyistolb.add_widget(self.full_delete)
                if i == 2:
                    self.srch_atr = Button(text='Поиск по \nатрибутам',
                                           background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.srch_atr.bind(on_press=self.on_press_button)
                    self.levyistolb.add_widget(self.srch_atr)
                # if i == 3:
                #     self.btn_reg = Button(text='Регистрация\nнового\nпользователя',
                #                           background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                #     self.btn_reg.bind(on_press=self.on_press_button)
                #     self.levyistolb.add_widget(self.btn_reg)
                if i == 4:
                    self.btn_soed = Button(text='Зайти под другим\nпользователем', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_soed.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_soed)

                if i ==6:
                    self.btn_open = Button(text='Открыть\nтаблицу', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    #self.btn = Label(text='', font_size=12)
                    self.btn_open.bind(on_press=self.otrkytie_tabl)
                    self.levyistolb.add_widget(self.btn_open)
                if i == 5:
                    self.btn_chng = Button(text='Взаимодействие с\nтаблицей', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    #self.btn = Label(text='', font_size=12)
                    self.btn_chng.bind(on_press=self.on_press_button)
                    self.levyistolb.add_widget(self.btn_chng)
                if i == 7:
                    self.kakaya_now_tabl = Button(text='', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12, disabled = 1)
                    #self.btn = Label(text='', font_size=12)
                    self.kakaya_now_tabl.text = 'Открыта таблица:\n' + self.perevodchik(self.supername_table)
                    self.levyistolb.add_widget(self.kakaya_now_tabl)

        if role_num == 3:   #sotr pasp
            for i in range(8):
                if i == 0:
                    self.btn_exit = Button(text='Выйти из\nприложения',
                                           background_color=[255 / 255, 104 / 255, 51 / 255, 1], font_size=12)
                    self.btn_exit.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_exit)

                # if i == 1:
                #     self.btn_enter_c = Button(text='Ввести команду\nSQL',
                #                               background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                #     self.btn_enter_c.bind(on_press=self.on_press_button)
                #     self.praviystolb.add_widget(self.btn_enter_c)
                # if i == 2:
                #     self.btn_join_an_bd = Button(text='Подключение\nк другой\nбазе данных',
                #                                  background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                #     self.btn_join_an_bd.bind(on_press=self.on_press_button)
                #     # self.btn = Label(text='', font_size=12)
                #     self.praviystolb.add_widget(self.btn_join_an_bd)
                if i == 4:
                    self.btn_uzn = Button(text='Узнать имя\nпользователя', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_uzn.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_uzn)
                if i == 5:
                    self.btn_otm = Button(text='Отменить\nоперации', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_otm.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_otm)
                if i == 6:
                    self.btn_podt = Button(text='Подтвердить\nоперации', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_podt.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_podt)
                if i == 7:
                    self.btn_close_soed = Button(text='Закрыть\nсоединение', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_close_soed.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_close_soed)


            self.supername_table = '"grazhdane_RF"'

            #zapros = 'select * from '+'"grazhdane_RF"'
            zapros ='Select * from ' + self.supername_table
            #print(zapros)
            self.cursor.execute(zapros)
            record = self.cursor.fetchall()
            header = self.cursor.description
            #print(record, header)
            self.table_create(record, header)

            for i in range(8):
                if i == 0:
                    self.deti_rod_predst = Button(text='Картотека \nграждан',
                                                  background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.deti_rod_predst.bind(on_press=self.on_press_button)
                    self.deti_rod_predst.bind(on_press=self.cartoteka_rus)
                    self.levyistolb.add_widget(self.deti_rod_predst)
                if i == 1:
                    self.full_delete = Button(text='Удаление \nгражданина \nиз базы',
                                              background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.full_delete.bind(on_press=self.on_press_button)
                    self.levyistolb.add_widget(self.full_delete)
                if i == 2:
                    self.srch_atr = Button(text='Поиск по \nатрибутам',
                                           background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.srch_atr.bind(on_press=self.on_press_button)
                    self.levyistolb.add_widget(self.srch_atr)
                # if i == 3:
                #     self.btn_reg = Button(text='Регистрация\nнового\nпользователя',
                #                           background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                #     self.btn_reg.bind(on_press=self.on_press_button)
                #     self.levyistolb.add_widget(self.btn_reg)
                if i == 4:
                    self.btn_soed = Button(text='Зайти под другим\nпользователем', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_soed.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_soed)

                if i ==6:
                    self.btn_open = Button(text='Открыть\nтаблицу', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    #self.btn = Label(text='', font_size=12)
                    self.btn_open.bind(on_press=self.otrkytie_tabl)
                    self.levyistolb.add_widget(self.btn_open)
                if i == 5:
                    self.btn_chng = Button(text='Взаимодействие с\nтаблицей', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    #self.btn = Label(text='', font_size=12)
                    self.btn_chng.bind(on_press=self.on_press_button)
                    self.levyistolb.add_widget(self.btn_chng)
                if i == 7:
                    self.kakaya_now_tabl = Button(text='', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12, disabled = 1)
                    #self.btn = Label(text='', font_size=12)
                    self.kakaya_now_tabl.text = 'Открыта таблица:\n' + self.perevodchik(self.supername_table)
                    self.levyistolb.add_widget(self.kakaya_now_tabl)

        if role_num == 4:
            for i in range(8):
                if i == 0:
                    self.btn_exit = Button(text='Выйти из\nприложения',
                                           background_color=[255 / 255, 104 / 255, 51 / 255, 1], font_size=12)
                    self.btn_exit.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_exit)

                if i == 1:
                    self.btn_enter_c = Button(text='Ввести команду\nSQL',
                                              background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_enter_c.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_enter_c)
                # if i == 2:
                #     self.btn_join_an_bd = Button(text='Подключение\nк другой\nбазе данных',
                #                                  background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                #     self.btn_join_an_bd.bind(on_press=self.on_press_button)
                #     # self.btn = Label(text='', font_size=12)
                #     self.praviystolb.add_widget(self.btn_join_an_bd)
                if i == 4:
                    self.btn_uzn = Button(text='Узнать имя\nпользователя', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_uzn.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_uzn)
                if i == 5:
                    self.btn_otm = Button(text='Отменить\nоперации', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_otm.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_otm)
                if i == 6:
                    self.btn_podt = Button(text='Подтвердить\nоперации', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_podt.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_podt)
                if i == 7:
                    self.btn_close_soed = Button(text='Закрыть\nсоединение', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_close_soed.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_close_soed)


            self.supername_table = 'wydacha_dokumenta'

            #zapros = 'select * from '+'"grazhdane_RF"'
            zapros ='Select * from ' + self.supername_table
            #print(zapros)
            self.cursor.execute(zapros)
            record = self.cursor.fetchall()
            header = self.cursor.description
            #print(record, header)
            self.table_create(record, header)

            for i in range(8):
                if i == 0:
                    self.deti_rod_predst = Button(text='Картотека \nграждан',
                                                  background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.deti_rod_predst.bind(on_press=self.on_press_button)
                    self.deti_rod_predst.bind(on_press = self.vybor_cartoteki)
                    self.levyistolb.add_widget(self.deti_rod_predst)
                if i == 1:
                    self.full_delete = Button(text='Удаление \nгражданина \nиз базы ',
                                              background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.full_delete.bind(on_press=self.on_press_button)
                    self.full_delete.bind(on_press=self.delete_vybor)
                    self.levyistolb.add_widget(self.full_delete)
                if i == 2:
                    self.srch_atr = Button(text='Поиск по \nатрибутам ',
                                           background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.srch_atr.bind(on_press=self.on_press_button)
                    self.srch_atr.bind(on_press=self.vybor_tabl_dlya_srch)
                    self.levyistolb.add_widget(self.srch_atr)
                if i == 3:
                    self.btn_reg = Button(text='Регистрация\nнового\nпользователя',
                                          background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_reg.bind(on_press=self.on_press_button)
                    self.levyistolb.add_widget(self.btn_reg)
                if i == 4:
                    self.btn_soed = Button(text='Зайти под другим\nпользователем', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    self.btn_soed.bind(on_press=self.on_press_button)
                    self.praviystolb.add_widget(self.btn_soed)

                if i == 6:
                    self.btn_open = Button(text='Открыть\nтаблицу', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    #self.btn = Label(text='', font_size=12)
                    self.btn_open.bind(on_press=self.otrkytie_tabl)
                    self.levyistolb.add_widget(self.btn_open)
                if i == 5:
                    self.btn_chng = Button(text='Взаимодействие с\nтаблицей', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12)
                    #self.btn = Label(text='', font_size=12)
                    self.btn_chng.bind(on_press=self.on_press_button)
                    self.levyistolb.add_widget(self.btn_chng)
                if i == 7:
                    self.kakaya_now_tabl = Button(text='', background_color=[255 / 255, 204 / 255, 51 / 255, 1], font_size=12, disabled = 1)
                    #self.btn = Label(text='', font_size=12)
                    self.kakaya_now_tabl.text = 'Открыта таблица:\n' + self.perevodchik(self.supername_table)
                    self.levyistolb.add_widget(self.kakaya_now_tabl)



        self.currenter_table.add_widget(self.levyistolb)
        self.currenter_table.add_widget(self.praviystolb)
        self.currenter_table.add_widget(self.mestodlyainfi)

        self.layout.add_widget(self.currenter_table)


    def perevodchik(self, name_stolb):
        if name_stolb == 'id_pasp':
            name_stolb = 'Номер паспорта'
        if name_stolb == 'id_rebenok_nerus':
            name_stolb = 'ID'
        if name_stolb == 'fio_reb_nerus':
            name_stolb = 'ФИО'
        if name_stolb == 'data_rozhd_reb_nerus':
            name_stolb = 'Дата рождения'
        if name_stolb == 'id_rebenka':
            name_stolb = 'ID ребёнка'
        if name_stolb == 'fio_rebenka':
            name_stolb = 'ФИО'
        if name_stolb == 'data_rozhd_reb':
            name_stolb = 'Дата рождения'
        if name_stolb == 'id_grazhd':
            name_stolb = 'ID гражданина'
        if name_stolb == 'fio':
            name_stolb = 'ФИО'
        if name_stolb == 'address':
            name_stolb = 'Место \nрегистрации'
        if name_stolb == 'number_tel':
            name_stolb = 'Номер телефона'
        if name_stolb == 'date_rozhd':
            name_stolb = 'Дата \nрождения'
        if name_stolb == 'pol':
            name_stolb = 'Пол'
        if name_stolb == 'pasport_supruga':
            name_stolb = 'Паспортные \nданные супруга'
        if name_stolb == 'fam_status':
            name_stolb = 'Семейное \nположение'
        if name_stolb == 'id_rebenka':
            name_stolb = 'ID ребенка'
        if name_stolb == 'id_nerus':
            name_stolb = 'ID'
        if name_stolb == 'fio':
            name_stolb = 'ФИО'
        if name_stolb == 'address_prozhiv':
            name_stolb = 'Адрес \nпроживания'
        if name_stolb == 'number_tel_nerus':
            name_stolb = 'Номер \nтелефона'
        if name_stolb == 'data_rozhd_nerus':
            name_stolb = 'Дата рождения'
        if name_stolb == 'pol_nerus':
            name_stolb = 'Пол'
        if name_stolb == 'grazhdanstvo':
            name_stolb = 'Гражданство'
        if name_stolb == 'passport_sup_nerus':
            name_stolb = 'Паспортные \nданные супруга'
        if name_stolb == 'id_reb_nerus':
            name_stolb = 'ID ребенка'
        if name_stolb == 'id_pasp':
            name_stolb = 'ID паспорта'
        if name_stolb == 'seriya':
            name_stolb = 'Серия паспорта'
        if name_stolb == 'nomer':
            name_stolb = 'Номер паспорта'
        if name_stolb == 'data_wydachi':
            name_stolb = 'Дата выдачи'
        if name_stolb == 'id_grazhd':
            name_stolb = 'ID гражданина'
        if name_stolb == 'id_podraz':
            name_stolb = 'ID \nподразделения'
        if name_stolb == 'name':
            name_stolb = 'Название'
        if name_stolb == 'address':
            name_stolb = 'Адрес'
        if name_stolb == 'fio_direktora':
            name_stolb = 'ФИО директора'
        if name_stolb == 'tab_nomer_migr':
            name_stolb = 'Табельный номер'
        if name_stolb == 'fio_sot_mig':
            name_stolb = 'ФИО'
        if name_stolb == 'professiya':
            name_stolb = 'Профессия'
        if name_stolb == 'tabel_nomer_sotr_stol':
            name_stolb = 'Табельный номер'
        if name_stolb == 'fio':
            name_stolb = 'ФИО'
        if name_stolb == 'professiya':
            name_stolb = 'Профессия'
        if name_stolb == 'fio_sup_nerus':
            name_stolb = 'ФИО'
        if name_stolb == 'id_sup_nerus':
            name_stolb = 'Номер \nосновного документа'
        if name_stolb == 'date_create_brak':
            name_stolb = 'Дата \nрегистрации брака'
        if name_stolb == 'date_rozhd_sup_nerus':
            name_stolb = 'Дата \nрождения супруга'
        if name_stolb == 'id_supruga':
            name_stolb = 'Номер \nосновного документа'
        if name_stolb == 'fio_sup':
            name_stolb = 'ФИО'
        if name_stolb == 'familiya_do_zamuzh':
            name_stolb = 'Фамилия до замужества'
        if name_stolb == 'data_rozhdeniya_sup':
            name_stolb = 'Дата рождения супруга'
        if name_stolb == 'data_registr_braka':
            name_stolb = 'Дата регистрации брака'
        if name_stolb == 'id_dokumenta':
            name_stolb = 'ID документа'
        if name_stolb == 'data_wydachi_dok':
            name_stolb = 'Дата выдачи'
        if name_stolb == 'mesto_wydachi_dok':
            name_stolb = 'Место выдачи'
        if name_stolb == 'id_nerus_gr':
            name_stolb = 'ID гражданина'
        if name_stolb == 'id_wyd':
            name_stolb = 'ID выдачи'
        if name_stolb == 'id_pasporta':
            name_stolb = 'ID паспорта'
        if name_stolb == 'osnowanie_wydacha':
            name_stolb = 'Основание выдачи'
        if name_stolb == 'data_wydachi':
            name_stolb = 'Дата выдачи'
        if name_stolb == 'kod_sotrudnika_rus':
            name_stolb = 'Табельный номер \nсотрудника \nпаспортного стола'
        if name_stolb == 'id_doka':
            name_stolb = 'ID временного \nудостоверения \nличности'
        if name_stolb == 'kod_sotr_migr':
            name_stolb = 'Табельный номер \nсотрудника \nмиграции'
        if name_stolb == 'kod_podrazdeleniya':
            name_stolb = 'Код \nподразделения'
        if name_stolb == 'grazhd_d_n':
            name_stolb = 'Гражданство'
        if name_stolb == 'imya_rf':
            name_stolb = 'Имя'
        if name_stolb == 'imya_nerus':
            name_stolb = 'Имя'
        if name_stolb == 'fam_nerus':
            name_stolb = 'Фамилия'
        if name_stolb == 'ot4_nerus':
            name_stolb = 'Отчество'
        if name_stolb == 'unik_id':
            name_stolb = 'ID родного \nдокумента'
        if name_stolb == 'kod_podr_pasp':
            name_stolb = 'Код подразделения \nпаспорта'
        if name_stolb == 'famil_rf':
            name_stolb = 'Фамилия'
        if name_stolb == 'ot4_rf':
            name_stolb = 'Отчество'
        if name_stolb == 'id_zapis22':
            name_stolb = 'Номер записи'
        if name_stolb == 'id_rod_ner':
            name_stolb = 'ID родителя'
        if name_stolb == 'id_deti_ner':
            name_stolb = 'ID ребёнка'
        if name_stolb == 'id_zapisi1':
            name_stolb = 'Номер записи'
        if name_stolb == 'id_rod_rus':
            name_stolb = 'ID родителя'
        if name_stolb == 'id_deti_rus':
            name_stolb = 'ID ребёнка'
        if name_stolb == 'id_reb_rus':
            name_stolb = 'ID ребёнка'


        if name_stolb == 'deti_nerus':
            name_stolb ='Дети \nиностранных \nграждан'
        if name_stolb == 'deti_rus':
            name_stolb = 'Дети \nроссийских \nграждан'
        if name_stolb == '"grazhdane_RF"':
            name_stolb = 'Граждане РФ'
        if name_stolb == 'nerus_grazhd':
            name_stolb = 'Иностранные \nграждане'
        if name_stolb == 'pasporta':
            name_stolb = 'Паспорта РФ'
        if name_stolb == 'podrazdelenie':
            name_stolb = 'Список \nподразделений'
        if name_stolb == 'sotrudnik_migrazi':
            name_stolb = 'Список \nсотрудников \nмиграционного \nотдела'
        if name_stolb == 'sotrudnik_pasp_stola':
            name_stolb = 'Список \nсотрудников \nпаспортного стола'
        if name_stolb == 'suprugi_nerus':
            name_stolb = 'Супруги \nиностранных \nграждан'
        if name_stolb == 'suprugi_rus':
            name_stolb = 'Супруги \nграждан РФ'
        if name_stolb == 'wrem_udos_li4n':
            name_stolb = 'Временные \nудостоверения \nличности'
        if name_stolb == 'wydacha_dokumenta':
            name_stolb = 'Информация \nпо выдаче \nдокументов'
        if name_stolb == 'mnogo_deti_rus':
            name_stolb = 'Соответствие \nдетей и граждан'
        if name_stolb == 'mnogo_deti_nerus':
            name_stolb = 'Соответствие \nдетей и граждан '


        if name_stolb == 'None':
            #print(name_stolb)
            name_stolb = 'Отсутствует'

        return name_stolb



    def table_create_perelist(self, instance):
        if self.proverka_nal_table == 1:
            self.mestodlyainfi.remove_widget(self.main_tablica)
        self.main_tablica = BoxLayout(orientation='vertical')
        table = self.supertable
        header =self.superheader
        # print(instance.text)
        # print(header, len(header))
        oglav = BoxLayout(orientation = 'horizontal')
        for i in header:
            textus = self.perevodchik(i[0])
            stolb = Label(text=textus, font_size=13, color= [1, 1, 1, 1])   #[153 / 255, 153 / 255, 153 / 255, 1])
            CustomGraphics.SetBG(stolb, bg_color=[84 / 255, 47 / 255, 58 / 255, 1])
            stolb.outline_color = [1, 1, 1, 1]
            oglav.add_widget(stolb)
            oglav.padding = 1
            oglav.size_hint_min_y = 0.1 * height_screen
        self.main_tablica.add_widget(oglav)
        count = 0
        count_str = 0
        lene = len(table)
        kol_str = lene // 8
        # print(lene)
        # print(kol_str)
        num_nugn_str = int(instance.text) - 1
        nugn_kon_str = 8 * num_nugn_str
        count = 0
        if kol_str > -1:
            for row in table[nugn_kon_str:]:
                if count == 8:
                    break
                tablica = BoxLayout()
                for label in row:
                    if type(label) is str and len(label.strip()) > 15:
                        # new_label = label
                        new_label = self.perenos_stroki(label.strip())
                        # a = (new_label[:(len(new_label) // 2 // 2)])
                        # b = (new_label[(len(new_label) // 2 // 2):])
                        # # print(a)
                        # # print(b)
                        # new_label = (a + '\n' + b)
                        # print(' '.join(map(str, new_label)))
                    else:
                        if type(label) is str:
                            new_label = label.strip()
                        else:
                            new_label = label
                    # print(new_label)
                    # print(new_label)
                    new_label = self.perevodchik(str(new_label))
                    textik = Label(text=str(new_label), font_size=13, color=[1, 1, 1, 1])
                    CustomGraphics.SetBG(textik, bg_color=[84 / 255, 47 / 255, 58 / 255, 0.75])

                    tablica.add_widget(textik)
                tablica.padding = (1, 1)

                self.main_tablica.add_widget(tablica)
                count += 1



            layout = BoxLayout(orientation='horizontal')
            self.str_label = Button(text = instance.text, background_color=[255 / 255, 204 / 255, 51 / 255, 1])
            layout.add_widget(self.str_label)
            self.str_label.size_hint_max_x = 0.01 * width_screen
            self.str_label.disabled = 1
            for stroka in range(kol_str+1):
                button = Button(text=str(stroka+1), on_press=self.table_create_perelist)
                button.size_hint_max_x = 0.05 * width_screen
                layout.add_widget(button)
            layout.padding = 10
            layout.size_hint_max_y = 0.1 * height_screen



            #layout.add_widget(button)


            # layout.add_widget(button_minus)
            # layout.add_widget(button_plus)

            self.main_tablica.add_widget(layout)


            self.mestodlyainfi.add_widget(self.main_tablica)

            self.proverka_nal_table = 1

    def perenos_stroki(self, stroka):
        #print(stroka, len(stroka))
        if len(stroka) > 27:
            new_label = '...'

        else:
            label = stroka.split(sep = ' ')
            new_label = label[0]
            for i in label[1:]:
                new_label = str(new_label) + '\n' + str(i)
        return new_label

    def otrkytie_tabl(self, instance):
        #print('otm')
        #content = Button(text='Хорошо')
        #popup = Popup(content=content, auto_dismiss=False, title='Не надо',
        #              size_hint=(None, None), size=(0.5 * height_screen, 0.25 * width_screen))
        #content.bind(on_press=popup.dismiss)
        #popup.open()
        #
        #
        # print(self.proverka_nal_table)
        # print('GOPA')
        # #cursor.execute(self.txt.text)
        # if self.proverka_nal_table == 0:
        #     self.cursor.execute('Select * from zadanie')
        #     record = self.cursor.fetchall()
        #     new_record = [[0]*len(record) for _ in range(len(record[0]))]
        #
        #     for i in range(len(record)):
        #         for j in range(len(record[0])):
        #             new_record[j][i] = record[i][j]
        #     self.table_create(new_record)
        # else:
        #     content = Button(text='Понятно!')
        #     popup = Popup(content=content, auto_dismiss=False, title='Закройте предыдущую таблицу',
        #                    size_hint=(None, None), size=(0.25 * height_screen, 0.25 * width_screen))
        #
        #     # bind the on_press event of the button to the dismiss function
        #     content.bind(on_press=popup.dismiss)
        #
        #     # open the popup
        #     popup.open()

        try:
            print('otm')
            if self.connection:
                self.connection.commit()
        except (Exception, Error) as error:
            print(error)

        try:

            logi, rolename = self.parent_group()


            layout = BoxLayout(orientation='vertical')
            niz_layout = BoxLayout(orientation = 'horizontal')
            levo_layout = BoxLayout(orientation = 'vertical')
            pravo_layout = BoxLayout(orientation = 'vertical')
            nadpis = Label(text='Какую таблицу нужно открыть?', font_size=24, size_hint_max_y = 0.1 * height_screen)
            content = Button(text='Отмена', font_size=24, size_hint_max_y = 0.1 * height_screen)
            deti_nerus = Button(text = 'Дети иностранных граждан', on_press=self.enter_the_table)
            levo_layout.add_widget(deti_nerus)
            deti_rus = Button(text = 'Дети российских граждан', on_press=self.enter_the_table)
            levo_layout.add_widget(deti_rus)
            grazhdane_RF = Button(text = 'Граждане РФ', on_press=self.enter_the_table)
            pravo_layout.add_widget(grazhdane_RF)
            nerus_grazhd = Button(text = 'Иностранные граждане', on_press=self.enter_the_table)
            pravo_layout.add_widget(nerus_grazhd)
            pasporta = Button(text = 'Паспорта РФ', on_press=self.enter_the_table)
            pravo_layout.add_widget(pasporta)
            podrazdelenie = Button(text = 'Список подразделений', on_press=self.enter_the_table)
            levo_layout.add_widget(podrazdelenie)
            sotr_mig = Button(text = 'Список сотрудников миграционного отдела', on_press=self.enter_the_table)
            pravo_layout.add_widget(sotr_mig)
            sotr_pasp = Button(text = 'Список сотрудников паспортного стола', on_press=self.enter_the_table)
            pravo_layout.add_widget(sotr_pasp)
            suprugi_nerus = Button(text = 'Супруги иностранных граждан', on_press=self.enter_the_table)
            levo_layout.add_widget(suprugi_nerus)
            suprugi_rus = Button(text = 'Супруги граждан РФ', on_press=self.enter_the_table)
            levo_layout.add_widget(suprugi_rus)
            wrem_udos = Button(text = 'Временные удостоверения личности', on_press=self.enter_the_table)
            levo_layout.add_widget(wrem_udos)
            wydacha_dokumenta = Button(text = 'Информация по выдаче документов', on_press=self.enter_the_table)
            levo_layout.add_widget(wydacha_dokumenta)
            mnogo_deti_nerus = Button(text = 'Соответствие детей и граждан ', on_press=self.enter_the_table)
            levo_layout.add_widget(mnogo_deti_nerus)
            mnogo_deti_rus = Button(text = 'Соответствие детей и граждан', on_press=self.enter_the_table)
            levo_layout.add_widget(mnogo_deti_rus)

            if rolename == 'sotr_migr':
                levo_layout.remove_widget(deti_rus)
                pravo_layout.remove_widget(grazhdane_RF)
                pravo_layout.remove_widget(pasporta)
                pravo_layout.remove_widget(sotr_pasp)
                levo_layout.remove_widget(suprugi_rus)
                levo_layout.remove_widget(mnogo_deti_rus)
            if rolename == 'sotr_pasp_st':
                levo_layout.remove_widget(deti_nerus)
                pravo_layout.remove_widget(nerus_grazhd)
                pravo_layout.remove_widget(sotr_mig)
                levo_layout.remove_widget(suprugi_nerus)
                levo_layout.remove_widget(wrem_udos)
                levo_layout.remove_widget(mnogo_deti_nerus)

            niz_layout.add_widget(levo_layout)
            niz_layout.add_widget(pravo_layout)
            layout.add_widget(nadpis)
            layout.add_widget(niz_layout)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Просмотр таблицы',
                          size_hint=(None, None), size=(0.7 * width_screen, 0.9 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            deti_nerus.bind(on_press=popup.dismiss)
            deti_rus.bind(on_press=popup.dismiss)
            grazhdane_RF.bind(on_press=popup.dismiss)
            nerus_grazhd.bind(on_press=popup.dismiss)
            pasporta.bind(on_press=popup.dismiss)
            podrazdelenie.bind(on_press=popup.dismiss)
            sotr_mig.bind(on_press=popup.dismiss)
            sotr_pasp.bind(on_press=popup.dismiss)
            suprugi_rus.bind(on_press=popup.dismiss)
            suprugi_nerus.bind(on_press=popup.dismiss)
            wrem_udos.bind(on_press=popup.dismiss)
            wydacha_dokumenta.bind(on_press=popup.dismiss)
            mnogo_deti_nerus.bind(on_press=popup.dismiss)
            mnogo_deti_rus.bind(on_press=popup.dismiss)
            popup.open()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def zap_deistv(self,instance):
        deistv = instance.text
        print(deistv)

        if deistv == 'Добавить новую запись':
            print('dobav')


        try:
            layout = BoxLayout(orientation='vertical')
            niz_layout = BoxLayout(orientation = 'horizontal')
            nadpis = Label(text='Выберите номер нужной записи\n(Самый левый столбик)', font_size=14)
            content = Button(text='Отмена', font_size=14)
            layout.add_widget(nadpis)

            popup = Popup(content=layout, auto_dismiss=False, title='Взаимодействие с таблицей',
                          size_hint=(None, None), size=(0.6 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)

            for zap in self.supertable:
                #print(zap[0])
                btn = Button(text = str(zap[0]), font_size = 14, on_press = popup.dismiss)
                if deistv == 'Посмотреть отдельную запись':
                    btn.bind(on_press = self.zap_prosm)
                if deistv == 'Изменить отдельную запись':
                    btn.bind(on_press = self.zap_izm)
                if deistv == 'Удалить отдельную запись':
                    btn.bind(on_press = self.zap_delete)
                niz_layout.add_widget(btn)
            # print(self.superheader, self.supertable, self.supername_table)
            #
            # for slovo in self.superheader:
            #     #print(slovo)
            #     knoka = Button(text = slovo[0])
            #     #zadanie.bind(on_press=self.enter_the_table)
            #     knoka.bind(on_press=popup.dismiss)
            #     niz_layout.add_widget(knoka)

            layout.add_widget(niz_layout)
            layout.add_widget(content)


            popup.open()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def zap_prosm(self, instance):
        print(instance.text)
        try:
            layout = BoxLayout(orientation='vertical')
            niz_layout = BoxLayout(orientation = 'horizontal')
            niz_layout.size_hint_min_y = 0.8 * height_screen
            nadpis = Label(text='Запись номер: ' + instance.text, font_size=18)
            content = Button(text='Отмена', font_size=18)
            layout.add_widget(nadpis)

            popup = Popup(content=layout, auto_dismiss=False, title='Взаимодействие с таблицей (посмотреть запись)',
                          size_hint=(None, None), size=(0.6 * width_screen, 0.95 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)

            olg_layout = BoxLayout(orientation = 'vertical')
            zapis_layout = BoxLayout(orientation = 'vertical')

            for i in self.superheader:
                textus = self.perevodchik(i[0])
                stolb_layout = BoxLayout(orientation = 'horizontal')
                stolb = Label(text=textus, font_size=16, color= [1, 1, 1, 1])   #[153 / 255, 153 / 255, 153 / 255, 1])
                CustomGraphics.SetBG(stolb, bg_color=[84 / 255, 47 / 255, 58 / 255, 1])
                stolb.outline_color = [1, 1, 1, 1]
                stolb_layout.add_widget(stolb)
                stolb_layout.padding = 2
                olg_layout.add_widget(stolb_layout)
                #olg_layout.size_hint_min_y = 0.1 * height_screen

            for zap in self.supertable:
                print(zap)
                if str(zap[0]) == instance.text:
                    for i in zap:
                        print(i)
                        if type(i) == str or str(i) == 'None':
                            textus = self.perevodchik(i)
                        else:
                            textus = i
                        textus = self.perevodchik(str(textus).strip())
                        stolb_layout = BoxLayout(orientation = 'horizontal')
                        stolb = Label(text=str(textus), font_size=16, color= [1, 1, 1, 1])   #[153 / 255, 153 / 255, 153 / 255, 1])
                        CustomGraphics.SetBG(stolb, bg_color=[84 / 255, 47 / 255, 58 / 255, 0.75])
                        stolb.outline_color = [1, 1, 1, 1]
                        stolb_layout.add_widget(stolb)
                        stolb_layout.padding = 2
                        zapis_layout.add_widget(stolb_layout)
                        #olg_layout.size_hint_min_y = 0.1 * height_screen
                    break
            # print(self.superheader, self.supertable, self.supername_table)
            #
            # for slovo in self.superheader:
            #     #print(slovo)
            #     knoka = Button(text = slovo[0])
            #     #zadanie.bind(on_press=self.enter_the_table)
            #     knoka.bind(on_press=popup.dismiss)
            #     niz_layout.add_widget(knoka)
            niz_layout.add_widget(olg_layout)
            niz_layout.add_widget(zapis_layout)
            layout.add_widget(niz_layout)
            layout.add_widget(content)


            popup.open()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def zap_izm(self,instance):
        try:
            self.supernadpis_dlya_izm = instance.text
            layout = BoxLayout(orientation='vertical')
            niz_layout = BoxLayout(orientation = 'horizontal')
            niz_layout.size_hint_min_y = 0.8 * height_screen
            nadpis = Label(text='Запись номер: ' + instance.text, font_size=18)
            #change = Button(text='Изменить', font_size=18)
            content = Button(text='Отмена', font_size=18)
            layout.add_widget(nadpis)

            popup = Popup(content=layout, auto_dismiss=False, title='Взаимодействие с таблицей (изменить запись)',
                          size_hint=(None, None), size=(0.6 * width_screen, 0.95 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            #change.bind(on_press=popup.dismiss)
            #change.bind(on_press = self.zap_izm_konec)
            olg_layout = BoxLayout(orientation = 'vertical')
            zapis_layout = BoxLayout(orientation = 'vertical')

            for i in self.superheader:
                textus = self.perevodchik(i[0])
                stolb_layout = BoxLayout(orientation = 'horizontal')
                stolb = Label(text=textus, font_size=16, color= [1, 1, 1, 1])   #[153 / 255, 153 / 255, 153 / 255, 1])
                CustomGraphics.SetBG(stolb, bg_color=[84 / 255, 47 / 255, 58 / 255, 1])
                stolb.outline_color = [1, 1, 1, 1]
                stolb_layout.add_widget(stolb)
                stolb_layout.padding = 2
                olg_layout.add_widget(stolb_layout)
                #olg_layout.size_hint_min_y = 0.1 * height_screen


            for zap in self.supertable:
                #print(zap)
                if str(zap[0]) == instance.text:
                    self.mesto_button = []
                    count = 0
                    for i in zap:

                        # if type(i) == str or str(i) == 'None':
                        #     textus = self.perevodchik(i)
                        # else:
                        #     textus = i
                        textus = i
                        #textus = self.perevodchik(str(textus).strip())
                        textus = str(textus).strip()
                        stolb_layout = BoxLayout(orientation = 'horizontal')
                        stolb = Button(text=str(textus), font_size=16, size_hint=(1, 1), on_press = popup.dismiss)   #[153 / 255, 153 / 255, 153 / 255, 1])
                        stolb.disabled = 1
                        knopka = Button(text=str(count), font_size=0, size_hint=(1, 1), on_press = popup.dismiss)
                        knopka.bind(on_press = self.zap_izm_nachalo)
                        if count == 0:
                            self.id_dlya_izm = textus
                            knopka.disabled = 1
                        knopka.size_hint_max_x = 0.01 * width_screen
                        knopka.background_color = [184 / 255, 47 / 255, 58 / 255, 1]
                        stolb.bind(on_press = self.zap_izm_nachalo)
                        #dobav = (count, stolb.text)
                        self.mesto_button.append(count)
                        #print(self.superheader[count][1])
                        #self.vvod_pass = TextInput(hint_text='Введите пароль', size_hint=(0.5, 0.1), pos = (20, 320), font_size = 24)
                        stolb_layout.add_widget(stolb)
                        stolb_layout.add_widget(knopka)
                        stolb_layout.padding = 2
                        zapis_layout.add_widget(stolb_layout)
                        #olg_layout.size_hint_min_y = 0.1 * height_screen
                        count += 1
                    break
            # print(self.superheader, self.supertable, self.supername_table)
            #
            # for slovo in self.superheader:
            #     #print(slovo)
            #     knoka = Button(text = slovo[0])
            #     #zadanie.bind(on_press=self.enter_the_table)
            #     knoka.bind(on_press=popup.dismiss)
            #     niz_layout.add_widget(knoka)
            niz_layout.add_widget(olg_layout)
            niz_layout.add_widget(zapis_layout)
            layout.add_widget(niz_layout)

            knopki_layout = BoxLayout(orientation = 'horizontal')
            #knopki_layout.add_widget(change)
            knopki_layout.add_widget(content)
            layout.add_widget(knopki_layout)


            popup.open()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def zap_izm_nachalo(self, instance):

        try:
            #print(instance.text)
            layout = BoxLayout(orientation='vertical')
            niz_layout = BoxLayout(orientation = 'horizontal')
            niz_layout.size_hint_min_y = 0.8 * height_screen
            nadpis = Label(text='Запись номер: ' + instance.text, font_size=18)
            change = Button(text='Изменить', font_size=18)
            content = Button(text='Отмена', font_size=18)
            layout.add_widget(nadpis)

            popup = Popup(content=layout, auto_dismiss=False, title='Взаимодействие с таблицей (изменить запись)',
                          size_hint=(None, None), size=(0.6 * width_screen, 0.95 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            change.bind(on_press=popup.dismiss)
            change.bind(on_press = self.zap_izm_konec)
            olg_layout = BoxLayout(orientation = 'vertical')
            zapis_layout = BoxLayout(orientation = 'vertical')

            for i in self.superheader:
                textus = self.perevodchik(i[0])
                stolb_layout = BoxLayout(orientation = 'horizontal')
                stolb = Label(text=textus, font_size=16, color= [1, 1, 1, 1])   #[153 / 255, 153 / 255, 153 / 255, 1])
                CustomGraphics.SetBG(stolb, bg_color=[84 / 255, 47 / 255, 58 / 255, 1])
                stolb.outline_color = [1, 1, 1, 1]
                stolb_layout.add_widget(stolb)
                stolb_layout.padding = 2
                olg_layout.add_widget(stolb_layout)
                #olg_layout.size_hint_min_y = 0.1 * height_screen


            for zap in self.supertable:
                #print(zap)
                if str(zap[0]) == self.supernadpis_dlya_izm:
                    self.values = []
                    count = 0
                    for i in zap:

                        # if type(i) == str or str(i) == 'None':
                        #     textus = self.perevodchik(i)
                        # else:
                        #     textus = i
                        textus = i
                        #textus = self.perevodchik(str(textus).strip())
                        textus = str(textus).strip()
                        stolb_layout = BoxLayout(orientation = 'horizontal')
                        if instance.text == str(count):
                            stolb = TextInput(hint_text=str(textus), font_size=16, size_hint=(1, 1))   #[153 / 255, 153 / 255, 153 / 255, 1])
                            #print(self.superheader[count][1])
                            type_perem =self.superheader[count][1]
                            if type_perem == 23 or type_perem == 20:
                                stolb.input_filter = 'int'
                            if type_perem == 1082:
                                stolb.input_type = 'datetime'
                            self.perenos_input_v_update = (count, stolb)
                        else:
                            stolb = Button(text=str(textus), font_size=16, size_hint=(1, 1), on_press = popup.dismiss)   #[153 / 255, 153 / 255, 153 / 255, 1])
                            stolb.disabled = 1
                        self.values.append(stolb)
                        #self.vvod_pass = TextInput(hint_text='Введите пароль', size_hint=(0.5, 0.1), pos = (20, 320), font_size = 24)
                        stolb_layout.add_widget(stolb)
                        stolb_layout.padding = 2
                        zapis_layout.add_widget(stolb_layout)
                        #olg_layout.size_hint_min_y = 0.1 * height_screen
                        count += 1
                    break
            # print(self.superheader, self.supertable, self.supername_table)
            #
            # for slovo in self.superheader:
            #     #print(slovo)
            #     knoka = Button(text = slovo[0])
            #     #zadanie.bind(on_press=self.enter_the_table)
            #     knoka.bind(on_press=popup.dismiss)
            #     niz_layout.add_widget(knoka)
            niz_layout.add_widget(olg_layout)
            niz_layout.add_widget(zapis_layout)
            layout.add_widget(niz_layout)

            knopki_layout = BoxLayout(orientation = 'horizontal')
            knopki_layout.add_widget(change)
            knopki_layout.add_widget(content)
            layout.add_widget(knopki_layout)


            popup.open()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def zap_izm_konec(self, instance):
        try:

            nomer_count = self.perenos_input_v_update[0]
            stolbec_perenosa = self.superheader[nomer_count][0]
            text_perenosa = self.perenos_input_v_update[1].text
            id_perenosa = self.id_dlya_izm
            kriteryi_perenosa = self.superheader[0][0]
            name_table_perenosa = self.supername_table
            self.perenos_input_v_update = ''
            print(stolbec_perenosa, text_perenosa, id_perenosa, kriteryi_perenosa, name_table_perenosa)



            type_perem =self.superheader[nomer_count][1]
            print(type_perem, text_perenosa.isdigit())
            #type_perem != 23 or type_perem != 20
            if not(text_perenosa.isdigit()):
                text_perenosa = '"' + text_perenosa + '"'


            zapros = 'update ' + name_table_perenosa + ' set ' + stolbec_perenosa + '=' + text_perenosa + ' where ' + kriteryi_perenosa + ' = '  + id_perenosa


            print(zapros)
            self.cursor.execute(zapros)
            self.connection.commit()
            self.proverka_polz()
        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def zap_delete(self, instance):

        try:
            print(self.supername_table, self.superheader[0][0], instance.text)
            zapros = 'delete from ' + self.supername_table + ' where ' + self.superheader[0][0] + ' = ' + instance.text
            print(zapros)
            self.cursor.execute(zapros)


            layout = BoxLayout(orientation='vertical')
            nadpis = Label(text='Запись успешно удалена', font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0.7 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()
            self.connection.commit()
            self.proverka_polz()

        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка удаления записи'
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0.7 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def zap_add(self, instance):
        try:
            layout = BoxLayout(orientation='vertical')
            niz_layout = BoxLayout(orientation = 'horizontal')
            niz_layout.size_hint_min_y = 0.8 * height_screen
            nadpis = Label(text='Запись номер: ' + instance.text, font_size=18)
            change = Button(text='Изменить', font_size=18)
            content = Button(text='Отмена', font_size=18)
            layout.add_widget(nadpis)

            popup = Popup(content=layout, auto_dismiss=False, title='Взаимодействие с таблицей (добавить запись)',
                          size_hint=(None, None), size=(0.6 * width_screen, 0.95 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            change.bind(on_press=popup.dismiss)
            change.bind(on_press = self.zap_izm_konec)
            olg_layout = BoxLayout(orientation = 'vertical')
            zapis_layout = BoxLayout(orientation = 'vertical')

            for i in self.superheader:
                textus = self.perevodchik(i[0])
                stolb_layout = BoxLayout(orientation = 'horizontal')
                stolb = Label(text=textus, font_size=16, color= [1, 1, 1, 1])   #[153 / 255, 153 / 255, 153 / 255, 1])
                CustomGraphics.SetBG(stolb, bg_color=[84 / 255, 47 / 255, 58 / 255, 1])
                stolb.outline_color = [1, 1, 1, 1]
                stolb_layout.add_widget(stolb)
                stolb_layout.padding = 2
                olg_layout.add_widget(stolb_layout)
                #olg_layout.size_hint_min_y = 0.1 * height_screen


            for zap in self.supertable:
                #print(zap)
                if 1:
                    self.values = []
                    count = 0
                    for i in zap:

                        # if type(i) == str or str(i) == 'None':
                        #     textus = self.perevodchik(i)
                        # else:
                        #     textus = i
                        textus = i
                        #textus = self.perevodchik(str(textus).strip())
                        textus = str(textus).strip()
                        stolb_layout = BoxLayout(orientation = 'horizontal')
                        stolb = TextInput(hint_text='Ввод сюда', font_size=16, size_hint=(1, 1))   #[153 / 255, 153 / 255, 153 / 255, 1])
                        #print(self.superheader[count][1])
                        type_perem =self.superheader[count][1]
                        if type_perem == 23 or type_perem == 20:
                            stolb.input_filter = 'int'
                        if type_perem == 1082:
                            stolb.input_type = 'datetime'
                        self.values.append(stolb)
                        #self.vvod_pass = TextInput(hint_text='Введите пароль', size_hint=(0.5, 0.1), pos = (20, 320), font_size = 24)
                        stolb_layout.add_widget(stolb)
                        stolb_layout.padding = 2
                        zapis_layout.add_widget(stolb_layout)
                        #olg_layout.size_hint_min_y = 0.1 * height_screen
                        count += 1
                    break
            # print(self.superheader, self.supertable, self.supername_table)
            #
            # for slovo in self.superheader:
            #     #print(slovo)
            #     knoka = Button(text = slovo[0])
            #     #zadanie.bind(on_press=self.enter_the_table)
            #     knoka.bind(on_press=popup.dismiss)
            #     niz_layout.add_widget(knoka)
            niz_layout.add_widget(olg_layout)
            niz_layout.add_widget(zapis_layout)
            layout.add_widget(niz_layout)

            knopki_layout = BoxLayout(orientation = 'horizontal')
            knopki_layout.add_widget(change)
            knopki_layout.add_widget(content)
            layout.add_widget(knopki_layout)


            popup.open()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def zap_add_konec(self, instance):
        try:
            super_perem = self.superheader[1:]
            count = 0
            values = []
            for i in self.values[1:]:
                type_perem =super_perem[count][1]
                if i.text == '':
                    values.append(i.hint_text)

                else:
                    if type_perem == 23 or type_perem == 20:
                        values.append(i.text)
                        #print(type_perem, i.text, i.hint_text)
                    else:
                        values.append(i.text)
                count += 1
            header = []
            type_stolb = []
            count = 0
            for a in self.superheader[1:]:
                heada = a[0]
                type_st = a[1]
                type_perem = self.superheader[count][1]
                #print(heada, type_st, type_perem)
                header.append(a[0])
                type_stolb.append(a[1])
                type_perem =self.superheader[count][1]
                #print(type_perem)
                if type_perem == 23 or type_perem == 20:
                    pass
                if type_perem == 1082:
                    pass
                else:
                    pass
                count += 1
            zapros = 'insert into ' + self.supername_table + '('
            # print(header)
            # print(type_stolb)
            # print(values)
            for perebor in header:
                zapros = zapros + perebor + ','
            zapros = zapros[:-1] + ') VALUES ('
            for perebor in values:
                zapros = zapros + "'" + perebor + "',"
            zapros = zapros[:-1] + ')'
            print(zapros)
            self.cursor.execute(zapros)
            self.connection.commit()
            self.proverka_polz()
        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def zap_add___a(self,instance):
        try:
            layout = BoxLayout(orientation='vertical')
            niz_layout = BoxLayout(orientation = 'horizontal')
            niz_layout.size_hint_min_y = 0.8 * height_screen
            nadpis = Label(text='Запись номер: ' + instance.text, font_size=18)
            change = Button(text='Изменить', font_size=18)
            content = Button(text='Отмена', font_size=18)
            layout.add_widget(nadpis)

            popup = Popup(content=layout, auto_dismiss=False, title='Взаимодействие с таблицей (изменить запись)',
                          size_hint=(None, None), size=(0.6 * width_screen, 0.95 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            change.bind(on_press=popup.dismiss)
            change.bind(on_press = self.zap_izm_konec)
            olg_layout = BoxLayout(orientation = 'vertical')
            zapis_layout = BoxLayout(orientation = 'vertical')

            for i in self.superheader:
                textus = self.perevodchik(i[0])
                stolb_layout = BoxLayout(orientation = 'horizontal')
                stolb = Label(text=textus, font_size=16, color= [1, 1, 1, 1])   #[153 / 255, 153 / 255, 153 / 255, 1])
                CustomGraphics.SetBG(stolb, bg_color=[84 / 255, 47 / 255, 58 / 255, 1])
                stolb.outline_color = [1, 1, 1, 1]
                stolb_layout.add_widget(stolb)
                stolb_layout.padding = 2
                olg_layout.add_widget(stolb_layout)
                #olg_layout.size_hint_min_y = 0.1 * height_screen


            for zap in self.supertable:
                #print(zap)
                if str(zap[0]) == instance.text:
                    self.values = []
                    count = 0
                    for i in zap:

                        # if type(i) == str or str(i) == 'None':
                        #     textus = self.perevodchik(i)
                        # else:
                        #     textus = i
                        textus = i
                        #textus = self.perevodchik(str(textus).strip())
                        textus = str(textus).strip()
                        stolb_layout = BoxLayout(orientation = 'horizontal')
                        stolb = TextInput(hint_text=str(textus), font_size=16, size_hint=(1, 1))   #[153 / 255, 153 / 255, 153 / 255, 1])
                        #print(self.superheader[count][1])
                        type_perem =self.superheader[count][1]
                        if type_perem == 23 or type_perem == 20:
                            stolb.input_filter = 'int'
                        if type_perem == 1082:
                            stolb.input_type = 'datetime'
                        self.values.append(stolb)
                        #self.vvod_pass = TextInput(hint_text='Введите пароль', size_hint=(0.5, 0.1), pos = (20, 320), font_size = 24)
                        stolb_layout.add_widget(stolb)
                        stolb_layout.padding = 2
                        zapis_layout.add_widget(stolb_layout)
                        #olg_layout.size_hint_min_y = 0.1 * height_screen
                        count += 1
                    break
            # print(self.superheader, self.supertable, self.supername_table)
            #
            # for slovo in self.superheader:
            #     #print(slovo)
            #     knoka = Button(text = slovo[0])
            #     #zadanie.bind(on_press=self.enter_the_table)
            #     knoka.bind(on_press=popup.dismiss)
            #     niz_layout.add_widget(knoka)
            niz_layout.add_widget(olg_layout)
            niz_layout.add_widget(zapis_layout)
            layout.add_widget(niz_layout)

            knopki_layout = BoxLayout(orientation = 'horizontal')
            knopki_layout.add_widget(change)
            knopki_layout.add_widget(content)
            layout.add_widget(knopki_layout)


            popup.open()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def zap_add_konec___a(self, instance):
        try:
            super_perem = self.superheader[1:]
            count = 0
            values = []
            for i in self.values[1:]:
                type_perem =super_perem[count][1]
                if i.text == '':
                    values.append(i.hint_text)

                else:
                    if type_perem == 23 or type_perem == 20:
                        values.append(i.text)
                        #print(type_perem, i.text, i.hint_text)
                    else:
                        values.append(i.text)
                count += 1
            header = []
            type_stolb = []
            count = 0
            for a in self.superheader[1:]:
                heada = a[0]
                type_st = a[1]
                type_perem = self.superheader[count][1]
                #print(heada, type_st, type_perem)
                header.append(a[0])
                type_stolb.append(a[1])
                type_perem =self.superheader[count][1]
                #print(type_perem)
                if type_perem == 23 or type_perem == 20:
                    pass
                if type_perem == 1082:
                    pass
                else:
                    pass
                count += 1
            zapros = 'insert into ' + self.supername_table + '('
            # print(header)
            # print(type_stolb)
            # print(values)
            for perebor in header:
                zapros = zapros + perebor + ','
            zapros = zapros[:-1] + ') VALUES ('
            for perebor in values:
                zapros = zapros + "'" + perebor + "',"
            zapros = zapros[:-1] + ')'
            print(zapros)
            self.cursor.execute(zapros)
        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0.8 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def parent_group(self):
        logi = ''
        self.cursor.execute('select current_user')
        logi = self.cursor.fetchall()[0][0]
        #print(logi)
        self.cursor.execute('''Select rolname from pg_roles where pg_has_role((select current_user), oid, 'member') and rolname not in (select current_user)''')
        vyvod = self.cursor.fetchall()
        #print(vyvod)
        rolename = vyvod[1][0]
        #b =[j for i in vyvod for j in i][0]
        #print(rolename)
        return logi,rolename

    def autorollback(self, instance):

        try:
            print('otm')
            if self.connection:
                self.connection.rollback()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def print_texty(self, instance):


        values = []
        for i in self.values[1:]:
            if i.text == '':
                values.append('None')
            else:
                values.append(i.text)
        header = []
        for a in self.superheader[1:]:
            header.append(a[0])
        zapros = 'insert into ' + self.supername_table + '('
        print(header)
        print(values)
        for perebor in header:
            zapros = zapros + perebor + ','
        zapros = zapros + ') VALUES ('
        for perebor in values:
            zapros = zapros + "'" + perebor + "', "
        print(zapros)
    def vybor_cartoteki(self, instance):
        try:
            text = Label(text='Выберите нужный набор информации', font_size=24)
            lalout = BoxLayout(orientation='vertical')
            rus = Button(text='Семьи граждан России', on_press = self.cartoteka_rus)
            nerus = Button(text = 'Семьи иностранцев', on_press = self.cartoteka_nerus)
            otmena = Button(text='Отмена')
            lalout.add_widget(rus)
            lalout.add_widget(nerus)
            lalout.add_widget(otmena)
            popup = Popup(content=lalout, auto_dismiss=False, title='Открытие представлений',
                          size_hint=(None, None), size=(0.6 * width_screen, 0.6 * height_screen))
            rus.bind(on_press=popup.dismiss)
            nerus.bind(on_press=popup.dismiss)
            otmena.bind(on_press=popup.dismiss)
            popup.open()

        except (Exception, Error) as error:
            layout = BoxLayout(orientation = 'vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text = textik, font_size = 24)
            content = Button(text = 'Хорошо',font_size = 24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0, 6 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def cartoteka_rus(self,instance):
        try:

            # cartoteka = '
            # popa =  + cartoteka
            # print(popa)
            self.cursor.execute('Select * from all_rus_gr')
            print('proverka')
            record = self.cursor.fetchall()
            header = self.cursor.description
            self.kakaya_now_tabl.text = 'Открыта таблица: \nСемьи'
            self.otkryto_predstavlenie = 1
            # new_record = [[0]*len(record) for _ in range(len(record[0]))]
            #
            # for i in range(len(record)):
            #     for j in range(len(record[0])):
            #         new_record[j][i] = record[i][j]
            self.table_create(record, header)

                # content = Button(text='Понятно!')
                # popup = Popup(content=content, auto_dismiss=False, title='Закройте предыдущую таблицу',
                #               size_hint=(None, None), size=(0.25 * height_screen, 0.25 * width_screen))
                #
                # # bind the on_press event of the button to the dismiss function
                # content.bind(on_press=popup.dismiss)
                #
                # # open the popup
                # popup.open()
        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()


    def cartoteka_nerus(self,instance):
        try:

            # cartoteka = '
            # popa =  + cartoteka
            # print(popa)
            self.cursor.execute('Select * from all_nerus_gr')
            print('proverka')
            record = self.cursor.fetchall()
            header = self.cursor.description
            self.kakaya_now_tabl.text = 'Открыта таблица: \nСемьи'
            self.otkryto_predstavlenie = 1
            # new_record = [[0]*len(record) for _ in range(len(record[0]))]
            #
            # for i in range(len(record)):
            #     for j in range(len(record[0])):
            #         new_record[j][i] = record[i][j]
            self.table_create(record, header)

            # content = Button(text='Понятно!')
            # popup = Popup(content=content, auto_dismiss=False, title='Закройте предыдущую таблицу',
            #               size_hint=(None, None), size=(0.25 * height_screen, 0.25 * width_screen))
            #
            # # bind the on_press event of the button to the dismiss function
            # content.bind(on_press=popup.dismiss)
            #
            # # open the popup
            # popup.open()
        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def delete_all_inf_rus(self, instance):

        try:
            number = instance.text
            zapros = 'call full_delete_rus(' + number + ')'

            print(zapros)

            try:

                self.connection.commit()

                self.cursor.execute('call full_delete_rus(%s)', (number))

                layout = BoxLayout(orientation='vertical')
                nadpis = Label(text='Записи успешно удалены', font_size=24)
                content = Button(text='Хорошо', font_size=24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Удаление из бд',
                              size_hint=(None, None), size=(0.7 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()
                self.connection.commit()
                self.proverka_polz()
            except (Exception, Error) as error:
                self.connection.rollback()
                print(error)

                layout = BoxLayout(orientation='vertical')
                nadpis = Label(text='Записи не удалены', font_size=24)
                content = Button(text='Хорошо', font_size=24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Удаление из бд',
                              size_hint=(None, None), size=(0.7 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()





        except (Exception, Error) as error:
            layout = BoxLayout(orientation = 'vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text = textik, font_size = 24)
            content = Button(text = 'Хорошо',font_size = 24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0, 6 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def delete_all_inf_nerus(self, instance):

        try:
            number = instance.text
            zapros = 'call full_delete_nerus(' + number + ')'

            print(zapros)

            try:

                self.connection.commit()

                self.cursor.execute('call full_delete_nerus(%s)', (number))

                layout = BoxLayout(orientation='vertical')
                nadpis = Label(text='Записи успешно удалены', font_size=24)
                content = Button(text='Хорошо', font_size=24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Удаление из бд',
                              size_hint=(None, None), size=(0.7 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()
                self.connection.commit()
                self.proverka_polz()
            except (Exception, Error) as error:
                self.connection.rollback()
                print(error)

                layout = BoxLayout(orientation='vertical')
                nadpis = Label(text='Записи не удалены', font_size=24)
                content = Button(text='Хорошо', font_size=24)
                layout.add_widget(nadpis)
                layout.add_widget(content)
                popup = Popup(content=layout, auto_dismiss=False, title='Удаление из бд',
                              size_hint=(None, None), size=(0.7 * width_screen, 0.35 * height_screen))
                # bind the on_press event of the button to the dismiss function
                content.bind(on_press=popup.dismiss)
                popup.open()





        except (Exception, Error) as error:
            layout = BoxLayout(orientation = 'vertical')
            textik = 'Ошибка'
            nadpis = Label(text = textik, font_size = 24)
            content = Button(text = 'Хорошо',font_size = 24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0, 6 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def delete_vybor(self,instance):
        try:
            text = Label(text='Выберите нужный отдел для удаления из базы', font_size=24)
            lalout = BoxLayout(orientation='vertical')
            rus = Button(text='Граждане России', on_press = self.delete_vybor_kon)
            nerus = Button(text = 'Иностранцы', on_press = self.delete_vybor_kon)
            otmena = Button(text='Отмена')
            lalout.add_widget(text)
            lalout.add_widget(rus)
            lalout.add_widget(nerus)
            lalout.add_widget(otmena)
            popup = Popup(content=lalout, auto_dismiss=False, title='Удаление из базы',
                          size_hint=(None, None), size=(0.6 * width_screen, 0.6 * height_screen))
            rus.bind(on_press=popup.dismiss)
            nerus.bind(on_press=popup.dismiss)
            otmena.bind(on_press=popup.dismiss)
            popup.open()

        except (Exception, Error) as error:
            layout = BoxLayout(orientation = 'vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text = textik, font_size = 24)
            content = Button(text = 'Хорошо',font_size = 24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0, 6 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def delete_vybor_kon(self,instance):
        try:



            #print(instance.text)
            layout = BoxLayout(orientation='vertical')
            niz_layout = BoxLayout(orientation = 'horizontal')
            content = Button(text='Отмена', font_size=18)
            content.size_hint_max_y = 0.03 * height_screen
            popup = Popup(content=layout, auto_dismiss=False, title='Удалить гражданина из базы',
                          size_hint=(None, None), size=(0.5 * width_screen, 0.5 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)

            if instance.text == 'Граждане России':
                self.supername_table = '"grazhdane_RF"'
                #zapros = 'select * from '+'"grazhdane_RF"'
                zapros ='Select * from ' + self.supername_table
                #print(zapros)
                self.cursor.execute(zapros)
                record = self.cursor.fetchall()
                header = self.cursor.description
                #print(record, header)
                self.table_create(record, header)
            if instance.text == 'Иностранцы':
                self.supername_table = 'nerus_grazhd'
                #zapros = 'select * from '+'"grazhdane_RF"'
                zapros ='Select * from ' + self.supername_table
                #print(zapros)
                self.cursor.execute(zapros)
                record = self.cursor.fetchall()
                header = self.cursor.description
                #print(record, header)
                self.table_create(record, header)

            for zap in self.supertable:
                #print(zap[0])
                btn = Button(text = str(zap[0]), font_size = 14, on_press = popup.dismiss)
                btn.size_hint_min_x = 0.01 * width_screen
                if instance.text == 'Граждане России':
                    btn.bind(on_press=self.delete_all_inf_rus)
                if instance.text == 'Иностранцы':
                    btn.bind(on_press = self.delete_all_inf_nerus)

                niz_layout.add_widget(btn)


            olg_layout = BoxLayout(orientation = 'vertical')
            zapis_layout = BoxLayout(orientation = 'vertical')
            niz_layout.add_widget(olg_layout)
            niz_layout.add_widget(zapis_layout)
            layout.add_widget(niz_layout)

            knopki_layout = BoxLayout(orientation = 'horizontal')
            knopki_layout.add_widget(content)
            layout.add_widget(knopki_layout)


            popup.open()

        except (Exception, Error) as error:
            layout = BoxLayout(orientation = 'vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text = textik, font_size = 24)
            content = Button(text = 'Хорошо',font_size = 24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0, 6 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def poisk_po_atr_rus(self,instance):
        try:

            # cartoteka = '
            # popa =  + cartoteka
            # print(popa)

            self.cursor.execute('Select * from poisk_po_fio_rf(%s, %s, %s)', (self.familia.text, self.imya.text, self.otchestvo.text) )
            #print('proverka')
            record = self.cursor.fetchall()
            header = self.cursor.description
            self.kakaya_now_tabl.text = 'Открыта таблица: \nПоиск человека'
            self.otkryto_predstavlenie = 1
            # new_record = [[0]*len(record) for _ in range(len(record[0]))]
            #
            # for i in range(len(record)):
            #     for j in range(len(record[0])):
            #         new_record[j][i] = record[i][j]



            self.table_create(record, header)

            # content = Button(text='Понятно!')
            # popup = Popup(content=content, auto_dismiss=False, title='Закройте предыдущую таблицу',
            #               size_hint=(None, None), size=(0.25 * height_screen, 0.25 * width_screen))
            #
            # # bind the on_press event of the button to the dismiss function
            # content.bind(on_press=popup.dismiss)
            #
            # # open the popup
            # popup.open()
        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def poisk_po_atr_nerus(self,instance):
        try:

            # cartoteka = '
            # popa =  + cartoteka
            # print(popa)

            self.cursor.execute('Select * from poisk_po_fio_ner(%s, %s, %s)', (self.familia.text, self.imya.text, self.otchestvo.text) )
            #print('proverka')
            record = self.cursor.fetchall()
            header = self.cursor.description
            self.kakaya_now_tabl.text = 'Открыта таблица: \nПоиск человека'
            self.otkryto_predstavlenie = 1
            # new_record = [[0]*len(record) for _ in range(len(record[0]))]
            #
            # for i in range(len(record)):
            #     for j in range(len(record[0])):
            #         new_record[j][i] = record[i][j]



            self.table_create(record, header)

            # content = Button(text='Понятно!')
            # popup = Popup(content=content, auto_dismiss=False, title='Закройте предыдущую таблицу',
            #               size_hint=(None, None), size=(0.25 * height_screen, 0.25 * width_screen))
            #
            # # bind the on_press event of the button to the dismiss function
            # content.bind(on_press=popup.dismiss)
            #
            # # open the popup
            # popup.open()
        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def vybor_tabl_dlya_srch(self, instance):
        try:
            text = Label(text='Выберите нужный отдел для поиска', font_size=24)
            lalout = BoxLayout(orientation='vertical')
            rus = Button(text='Граждане России', on_press = self.vybor_tabl_dlya_srch_kon)
            nerus = Button(text = 'Иностранцы', on_press = self.vybor_tabl_dlya_srch_kon)
            otmena = Button(text='Отмена')
            lalout.add_widget(text)
            lalout.add_widget(rus)
            lalout.add_widget(nerus)
            lalout.add_widget(otmena)
            popup = Popup(content=lalout, auto_dismiss=False, title='Поиск по ФИО',
                          size_hint=(None, None), size=(0.6 * width_screen, 0.6 * height_screen))
            rus.bind(on_press=popup.dismiss)
            nerus.bind(on_press=popup.dismiss)
            otmena.bind(on_press=popup.dismiss)
            popup.open()

        except (Exception, Error) as error:
            layout = BoxLayout(orientation = 'vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text = textik, font_size = 24)
            content = Button(text = 'Хорошо',font_size = 24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(0, 6 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()

    def vybor_tabl_dlya_srch_kon(self, instance):
        try:

            sovsem_niz = BoxLayout(orientation = 'horizontal')
            sovsem_niz.size_hint_max_y = 0.04 * height_screen
            layout = BoxLayout(orientation = 'vertical')
            niz_layout = BoxLayout(orientation = 'vertical')
            self.imya = TextInput(hint_text='Введите имя', size_hint=(1, 0.8))
            self.imya.multiline = False
            self.familia = TextInput(hint_text='Введите фамилию', size_hint=(1, 0.8))
            self.familia.multiline = False
            self.otchestvo = TextInput(hint_text='Введите отчество', size_hint=(1, 0.8))
            self.otchestvo.multiline = False
            vihod = Button(text='Отмена')
            podtverdit = Button(text='Найти')
            if instance.text == 'Граждане России':
                podtverdit.bind(on_press = self.poisk_po_atr_rus)
            if instance.text == 'Иностранцы':
                podtverdit.bind(on_press = self.poisk_po_atr_nerus)

            sovsem_niz.add_widget(podtverdit)
            sovsem_niz.add_widget(vihod)
            niz_layout.add_widget(self.imya)
            niz_layout.add_widget(self.familia)
            niz_layout.add_widget(self.otchestvo)
            layout.add_widget(niz_layout)

            layout.add_widget(sovsem_niz)
            popup = Popup(content= layout, auto_dismiss=False, title='Поиск по атрибутам',
                          size_hint=(None, None), size=( 0.45 * width_screen, 0.3 * height_screen))
            vihod.bind(on_press=popup.dismiss)
            podtverdit.bind(on_press = popup.dismiss)
            popup.open()


        except (Exception, Error) as error:
            layout = BoxLayout(orientation='vertical')
            textik = 'Ошибка: ' + str(error)
            nadpis = Label(text=textik, font_size=24)
            content = Button(text='Хорошо', font_size=24)
            layout.add_widget(nadpis)
            layout.add_widget(content)
            popup = Popup(content=layout, auto_dismiss=False, title='Ошибка',
                          size_hint=(None, None), size=(1.25 * width_screen, 0.35 * height_screen))
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()
# Запуск проекта
if __name__ == "__main__":
    MainApp().run()
    #TestApp().run()