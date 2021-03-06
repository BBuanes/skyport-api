import json

class SkyportReceiver:
	handler_handshake_successful = None
	handler_error = None
	handler_gamestate = None
	handler_gamestart = None
	handler_action = None
	handler_endturn = None

	def __init__(self):
		pass

	def parse_line(self, line):
		try:
			json_line = json.loads(line)
		except ValueError as e:
			print("Error decoding JSON packet: %s" % e)
		except AttributeError as e:
			print("Invalid message: %s" % e)
		else:
			self._parse_json_packet(json_line)

	def _parse_json_packet(self, json_packet):
		if "error" in json_packet:
			if self.handler_error != None:
				self.handler_error(json_packet["error"])
			return
		if json_packet["message"] == "connect":
			if self.handler_handshake_successful != None:
				self.handler_handshake_successful()
		elif json_packet["message"] == "gamestate":
			if json_packet["turn"] == 0:
				if self.handler_gamestart != None:
					self.handler_gamestart(json_packet["turn"],
                                           json_packet["map"],
                                           json_packet["players"])
			else:
				if self.handler_gamestate != None:
					self.handler_gamestate(json_packet["turn"],
                                           json_packet["map"],
                                           json_packet["players"])
		elif json_packet["message"] == "action":
			# def gotAction(self, actionType, who, restData):
			if self.handler_action != None:
				packet_type = json_packet["type"]
				who = json_packet["from"]
				del json_packet["type"]
				del json_packet["from"]
				self.handler_action(packet_type, who, json_packet)
		elif json_packet["message"] == "endturn":
			if self.handler_endturn != None:
				self.handler_endturn()
		else:
			print("unknown message type: '%s'" % json_packet["message"])

class SkyportTransmitter:
	handler_send = None
	def __init__(self, send_function):
		self.handler_send = send_function

    def send_message(self, message):
        self.handler_send(json.dumps(message))

	def send_loadout(self, primary_weapon, secondary_weapon):
		self.send_message({"message":"loadout",
                           "primary-weapon": primary_weapon,
                           "secondary-weapon": secondary_weapon})

	def send_handshake(self, name):
        self.send_message({"message":"connect",
                           "revision": 1,
                           "name": name})

	def send_move(self, whereto):
		self.send_message({"message":"action",
                           "type": "move",
                           "direction": whereto})

	def attack_laser(self, direction):
		self.send_message({"message":"action",
                           "type":"laser",
                           "direction":direction})

	def attack_mortar(self, j_coordinate, k_coordinate):
		coordinates = "%i,%i" % (j_coordinate, k_coordinate);
		self.send_message({"message":"action",
                           "type":"mortar",
                           "coordinates":coordinates})

	def attack_droid(self, sequence):
		self.send_message({"message":"action",
                           "type":"droid",
                           "sequence":sequence})

	def mine(self):
		self.send_message({"message":"action",
                           "type":"mine"})

	def upgrade(self, weapon):
		selfsend_message({"message":"action",
                          "type":"upgrade",
                          "weapon":weapon})
