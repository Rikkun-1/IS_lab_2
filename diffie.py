from   random import randint

from sympy import isprime
from sympy.ntheory.residue_ntheory import primitive_root
from sympy.ntheory.generate import randprime

from simplecrypt import encrypt, decrypt, DecryptionException

class Agent:

	def __init__(self, name):
		self.name  			  = name
		self.P				  = None
		self.G				  = None
		self.__private_number = None

	def generate_PG(self):
		P = randprime(10**26, 10**27)

		while not (((P - 1) % 2 == 0) and isprime((P - 1) // 2)):
			P = randprime(10**26, 10**27)

		G = primitive_root(P)

		self.P = P
		self.G = G

		return P, G

	def generate_private_number(self):
		self.__private_number = randint(10**26, 10**27)

		print(f"Private key {self.name}: \t{self.__private_number}") 

	def get_reminder(self):
		return pow(self.G, self.__private_number, self.P)

	def encrypt(self, message, reminder):
		secret_key = pow(reminder, self.__private_number, self.P)
		print(f"Secret key {self.name} is: \t{secret_key}")
		return encrypt(str(secret_key), message)

	def decrypt(self, cipher, reminder):
		secret_key = pow(reminder, self.__private_number, self.P)
		print(f"Secret key {self.name} is: \t{secret_key}")

		try:
			return decrypt(str(secret_key), cipher).decode()
		except DecryptionException:
			return "Wrong password"

message = input("Enter message: ")

Bob   = Agent("Bob")
Alice = Agent("Alice")

Alice.P, Alice.G = Bob.generate_PG()

Bob.generate_private_number()
Alice.generate_private_number()

Alice_reminder = Alice.get_reminder()
Bob_reminder   = Bob.get_reminder()

print(f"\nReminder Alice: \t{Alice_reminder}")
print(f"Reminder Bob  : \t{Bob_reminder}\n")

encripted = Alice.encrypt(message, Bob_reminder)
decripted = Bob.decrypt(encripted, Alice_reminder)

print(f"\nMessage: \n{message}\n")
print(f"Encripted message: \n{encripted.hex()}\n")
print(f"Decripted message: \n{decripted}\n")





