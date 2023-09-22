from itertools import product
from threading import Thread
from pynput.keyboard import Listener, KeyCode
from time import sleep
from playsound import playsound
from random import shuffle

class Program:
	active = False
	running = True
	code_index = 0

	def __init__(self, code_list, total_digits):
		self.code_list = code_list
		total_codes = len(code_list)

		for i, code in enumerate(code_list):
			code = "\n " + code if i == 0 else code
			print(code + "\n" if i % 4 == 3 else code, end=" ")
	
		print(f"\n\nTotal of {total_codes} codes to check" if total_digits <= 2 else f"\nTotal of {total_codes} codes to check")
		print("Press '#' to call out the next code")

		main_thread = Thread(target=self.__main)
		main_thread.start()

		with Listener(on_press=self.__on_press) as listener:
			listener.join()

	def __main(self):
		while self.running:
			if self.active:
				for x in self.code_list[self.code_index]:
					playsound(f"sound\\{x}.mp3")
				
				self.code_index += 1
				self.running = self.code_index < len(self.code_list)
			
			self.active = False
			sleep(0.1)

	def __on_press(self, key):
		if key == KeyCode.from_char('#'):
			self.active = True
			if not self.running:
				playsound("sound\\finished.mp3", False)
				return False

if __name__ == "__main__":
	while True:
		digits = list(input("Enter digits: "))
		
		if any(x not in "0123456789" for x in digits):
			print("Enter only digits")
		elif (total_digits := len(digits)) == 0:
			print("You need to enter some digits")
		elif total_digits > 4:
			print("A maximum of 4 digits can be entered")
		else:
			break

	total_digits = len(set(digits))
	code_list = ["".join(p) for p in product(set(digits), repeat=4) if len(set(p)) == total_digits]
	shuffle(code_list)

	Program(code_list, total_digits)
	input("Finished calling out codes. Press 'Enter' to exit")