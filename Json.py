import copy
import json


class JsonParser:
	def __init__(self, json_dict_or_string=None):
		if json_dict_or_string is None:
			self.__json_dict = None
		elif isinstance(json_dict_or_string, str):
			self.__json_dict = json.loads(json_dict_or_string)
		elif isinstance(json_dict_or_string, (dict, list)):
			self.__json_dict = json_dict_or_string
		else:
			raise TypeError("Expecting a str or dict or list")

	def get(self, path):
		is_found = True
		current_value = copy.deepcopy(self.__json_dict)

		keys_list = path.split(".")
		for key in keys_list:
			if key.startswith("["):
				if isinstance(current_value, list):
					try:
						index = int(key[1:-1])
					except ValueError:
						raise ValueError("Expecting an integer between '[' and ']'")
					current_value = current_value[index]
				else:
					is_found = False
					break
			else:
				if isinstance(current_value, dict):
					if key in current_value:
						current_value = current_value[key]
					else:
						is_found = False
						break
				else:
					is_found = False
					break

		return (is_found, current_value) if is_found else (is_found, None)

	def set(self, path, value):
		current_value = self.__json_dict
		keys_list = path.split(".")

		# initializing the json object
		if len(keys_list) > 0:
			key = keys_list[0]
			if current_value is None:
				if key.startswith("["):
					self.__json_dict = []
				else:
					self.__json_dict = {}
				current_value = self.__json_dict

		# creating or iterating the json object
		for i in range(len(keys_list)-1):
			present_key = keys_list[i]
			next_key = keys_list[i+1]

			if present_key.startswith("["):
				index = -1 if present_key[1:-1] == "" else int(present_key[1:-1])
				try:
					temp_value = current_value[index]
					if next_key.startswith("["):
						if not isinstance(temp_value, list):
							current_value[index] = []
					else:
						if not isinstance(temp_value, dict):
							current_value[index] = {}
					current_value = current_value[index]
				except IndexError:
					current_value.append([] if next_key.startswith("[") else {})
					current_value = current_value[-1]
			else:
				if present_key in current_value:
					temp_value = current_value[present_key]
					if next_key.startswith("["):
						if not isinstance(temp_value, list):
							current_value[present_key] = []
					else:
						if not isinstance(temp_value, dict):
							current_value[present_key] = {}
				else:
					current_value[present_key] = [] if next_key.startswith("[") else {}
				current_value = current_value[present_key]

		# setting the value to the json path
		key = keys_list[-1]
		if key.startswith("["):
			index = -1 if key[1:-1] == "" else int(key[1:-1])
			try:
				current_value[index] = value
			except IndexError:
				current_value.append(value)
		else:
			current_value[key] = value

	def get_json_dict(self):
		return self.__json_dict

	def __str__(self):
		return json.dumps(self.__json_dict)


if __name__ == "__main__":
	jp = JsonParser()
	jp.set("name.first_name", "Partha")
	jp.set("name.middle_name", "Pratim")
	jp.set("name.last_name", "Manna")
	jp.set("greeting", "Hello everyone")
	print(jp)
	print(json.dumps(jp.get_json_dict(), indent="\t"))
