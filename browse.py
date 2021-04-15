#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Gayatri Venugopal
"""

import os

import xml.etree.ElementTree as ET

def iterate(keys, node):
    #print(node.tag.title(), ": ", node.attrib.get("name", node.text))
    #print(node.tag.title(),node.text)
    #print(node.tag)
    if node.tag in ["title", "fixed-case", "abstract"]:
        for key in keys:
            if node.text is not None and key in node.text.split():
                print(node.tag, node.text)
    for child in node:
        iterate(keys, child)
    return
    
def parse(file, keys):
    tree = ET.parse(file)
    root = tree.getroot()
    
    #get year
    #year = root.attrib.get("id").split(".")[0]
    #print(year)
    
    iterate(keys, root)
    
def search_by_keyword(location, keys): 
    for file in sorted(os.listdir(location)):
        parse(path + file, keywords)
        
path = "/opt/Research/Bibliometric Analysis/acl-anthology/data/xml/"
keywords = ["lexical simplification", "complex word identification", 
            "lexical complexity prediction", "lexical complexity", "complex word",
            "text simplification"]

search_by_keyword(path, keywords)