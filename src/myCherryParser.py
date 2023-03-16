#!/usr/bin/env python3

from lxml import etree as ET
import os, sys
import json, base64


# Constants

COLOR = {
	"black" : "#000000",
	"red" : "#ff0000",
	"gray" : "#bfbfbf",
	"white" : "#ffffff"
}

ICON = {
	"redcherry" : 0,
	"green" : 1,
	"yellow" : 2,
	"red" : 3,
	"gray" : 4,
	"warning" : 10,
	"info" : 12,
	"question" : 13,
	"home" : 14,
}

class myCherryParser():
	"""
	A parser which transforms a JSON to a CherryTree
	"""

	uid = None
	input_file = None
	output_file = None

	def __init__(self, input_file, output_file):
		self.uid = 1
		self.input_file = input_file
		self.output_file = output_file

	def __repr__(self):
		return "<%s %s at %#x>" % (self.__class__.__name__, self.input_file, id(self))

	def parse_node_info(self, data):
		icon = None
		info = None
		bold = False
		node_name = ""
		color = None

		if 'icon' in data.keys():
			icon = ICON[data['icon']]

		if 'bold' in data.keys():
			bold = data['bold']

		if 'node_name' in data.keys():
			node_name = data['node_name']

		if 'color' in data.keys():
			color = COLOR[data['color']]

		return icon, bold, node_name, color

	def fill_node_with_content(self, element, data):
		# Array of contents
		for content in data:
			# Text
			if content['type'] == "text":
				style = content['style']
				text_field = ET.SubElement(element, "rich_text")
				text_field.text=content['string'] +"\n"

				if "bold" in style:
					text_field.attrib["weight"] = "heavy"
				if "italic" in style:
					text_field.attrib["style"] = "italic"
				if "underline" in style:
					text_field.attrib["underline"] = "single"
				if "h1" in style:
					text_field.attrib["scale"] = "h1"
				elif "h2" in style:
					text_field.attrib["scale"] = "h2"
				elif "h3" in style:
					text_field.attrib["scale"] = "h3"
				
			# Images
			elif content['type'] == "image":
				with open(content['path'], "rb") as img_file:
					my_image = base64.b64encode(img_file.read())
				ET.SubElement(element, "encoded_png", char_offset="99999999", justification="center", link="").text=my_image
				ET.SubElement(element, "rich_text", style="", weight="").text="\n\n"

			elif content['type'] == "image_b64":
				ET.SubElement(element, "encoded_png", char_offset="99999999", justification="center", link="").text=content['image']
				ET.SubElement(element, "rich_text", style="", weight="").text="\n\n"

			elif content['type'] == "table":
				table = ET.SubElement(element, "table", char_offset="99999999", justification="left", col_min="60", col_max="60", col_widths="0,0,0")
				sorted_content = content['cells'][1:] + content['cells'][0:1]
				for row in sorted_content:
					row_element = ET.SubElement(table, "row")
					for cell in row:
						ET.SubElement(row_element, "cell").text = cell
				ET.SubElement(element, "rich_text", style="", weight="").text="\n"

	def parse_subnodes(self, element, data):
			# Array of nodes
			for i in data:
				icon, bold, name, color = self.parse_node_info(i['info_node'])
				subelement = ET.SubElement(element, "node", custom_icon_id=str(icon), foreground=color, is_bold=str(bold), name=name,  prog_lang="custom-colors", readonly="False", tags="", unique_id=str(self.uid))

				self.uid = self.uid+1
				self.fill_node_with_content(subelement, i['content_node'])
				if len(i["sub_node"]):
					self.parse_subnodes(subelement, i["sub_node"])

	def parse(self):
		# Root
		root = ET.Element("cherrytree")

		# Parse JSON
		json_file = open(self.input_file)
		data = json.load(json_file)
		print(data)
		print("----")
		print(data['info_node'])

		# Initial Node
		# ----------
		icon, bold, name, color = self.parse_node_info(data['info_node'])
		node = ET.SubElement(root, "node", custom_icon_id=str(icon), foreground=color, is_bold=str(bold), name=name,  prog_lang="custom-colors", readonly="False", tags="", unique_id=str(self.uid))

		# Printing content
		self.fill_node_with_content(node, data['content_node'])
		self.parse_subnodes(node, data['sub_node'])

		# Save Tree
		tree = ET.ElementTree(root)
		tree.write(self.output_file)

if __name__ == "__main__":
	print("[+] Parsing: %s " % sys.argv[1])
	parser = myCherryParser(sys.argv[1], sys.argv[2])
	parser.parse()
	print("[+] Finished: %s " % sys.argv[2])
