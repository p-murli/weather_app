from tkinter import *
from ttkthemes import ThemedTk
from configparser import ConfigParser
import requests
from tkinter import messagebox


class WeatherApplication(Frame):

	def __init__(self, master):
		super().__init__(master)

		self.master = master

		master.title("Weather app")
		master.geometry("700x400")

		photo = PhotoImage(file='random_logo.png')
		master.iconphoto(False, photo)

		self.create_widgets()

		self.url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

		self.config_file = 'config.ini'
		self.config = ConfigParser()
		self.config.read(self.config_file)

		self.api_key = self.config['api_key']['key']

	def on_click_entry(self, event):

		if(self.city_entry.get()=='Enter Location'):
			self.city_entry.delete(0,END)
			self.city_entry.insert(0, '')
			self.city_entry.config(fg='black')

	def on_focus_out(self, event):

		if(self.city_entry.get() == ''):
			self.city_entry.insert(0, 'Enter Location')
			self.city_entry['fg'] = 'gray'
	
	def create_widgets(self):


		self.entry_frame = Frame(self.master)
		self.entry_frame.pack(pady=10)

		self.city_text = StringVar()

		self.city_entry = Entry(self.entry_frame, textvariable=self.city_text, width=30)
		self.city_entry.insert(0, 'Enter Location')
		self.city_entry.config(fg ='gray')
		self.city_entry.bind('<FocusIn>', self.on_click_entry)
		self.city_entry.bind('<FocusOut>', self.on_focus_out)
		self.city_entry.pack(pady=5)

		self.search_button = Button(self.entry_frame, text='Search Weather', command=self.search_weather, width=15)
		self.search_button.pack(pady=5)

		self.master.bind("<Return>", self.search_weather)


		self.weather_frame = Frame(self.master)
		self.weather_frame.pack(pady=5)

		self.location_label = Label(self.weather_frame, text="", font=('bold', 18))
		self.location_label.pack(pady=5,padx=5)

		self.weather_image = Label(self.weather_frame, image="")
		self.weather_image.pack(pady=5)

		self.temparature_label = Label(self.weather_frame, text="", font=('bold', 14))
		self.temparature_label.pack(pady=5)

		self.weather_label = Label(self.weather_frame, text="", font=('bold', 14))
		self.weather_label.pack(pady=5)


	def get_weather(self, city):

		result = requests.get(self.url.format(self.city, self.api_key))

		if(result):

			json = result.json()

			city = json['name']
			country = json['sys']['country']
			temp_celsius = json['main']['temp'] - 273.15
			temp_fahrenheit = (json['main']['temp'] - 273.15)*9/5 + 32
			ico = json['weather'][0]['icon']
			weather = json['weather'][0]['main']

			self.final = (city, country, temp_celsius, temp_fahrenheit, ico, weather)

			return self.final
		else:
			return None




	def search_weather(self, event=None):



		self.city = self.city_text.get()

		self.city_entry.delete(0,END)

		result = self.get_weather(self.city)

		if result:
			self.location_label['text'] = '{}, {}'.format(result[0], result[1])
			self.image = PhotoImage(file='weather_icons/{}@2x.png'.format(result[4]))
			self.weather_image.image = self.image
			self.weather_image.config(image=self.weather_image.image)
			self.temparature_label['text'] = '{:.2f} Celsius, {:.2f} Fahrenheit'.format(result[2], result[3])
			self.weather_label['text'] = '{}'.format(result[5])
		else:
			messagebox.showerror('Error', 'Cannot find city {}'.format(self.city))


window = ThemedTk('ark')
app = WeatherApplication(master=window)
app.mainloop()
