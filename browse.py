#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Gayatri Venugopal
"""

#TODO: extract and pass year, month, country, source, publisher
import os

import xml.etree.ElementTree as ET

from paper import Paper

def iterate(keys, node, year, month, country, publisher, source, out_path):
    if node is None:
        return
    if len(node.findall("paper")) == 0:
         for child in node:
             iterate(keys, child, year, month, country, publisher, source, out_path)
    else:
        for paper in node.findall("paper"):
            if paper.find("title") is not None and paper.find("title").find("fixed-case") is not None:
                xmlstr = (ET.tostring(paper.find("title"), encoding='utf8', method='xml')).decode("utf-8")
                xmlstr = xmlstr.replace("<fixed-case>", "")
                xmlstr = xmlstr.replace("</fixed-case>", "")
                title = xmlstr[xmlstr.find("<title>")+7:xmlstr.find("</title>")]
            else:
                title = paper.find("title").text
            for key in keys:
                     if title is not None and title.find(key) != -1 or (paper.find("abstract") is not None and paper.find("abstract").text is not None and (paper.find("abstract").text).find(key) != -1):
                         #pass
                         #TODO: store paper element, store paper details in a file
                         if paper.findall("author") is not None:
                             auth_list = []
                             for child in paper.findall("author"):
                                 auth_list.append(child.find("first").text + " " + child.find("last").text)
                         paper_object =  Paper()
                         paper_object.save(year, month, title, auth_list, country, source, publisher)
                         paper_object.write(out_path)
                         break
    return
    
def parse(file, keys, out_path):
    tree = ET.parse(file)
    root = tree.getroot()
    
    year = publisher = month = country = source = None
    
    year = root.find(".//year")
    if year is not None and year.text is not None:
        year = year.text.strip()
    publisher = root.find(".//publisher")
    if publisher is not None and publisher.text is not None:
        publisher = publisher.text.strip()
    month = root.find(".//month")
    if month is not None and month.text is not None:
        month = month.text.strip().split()[0]
    country = root.find(".//address")
    if country is not None and country.text is not None:
        country = country.text.strip().split()[-1]
    source = root.find(".//booktitle")
    if source is not None and source.text is not None:
        source = source.text.strip().lower()
        if source.find("findings of the association for computational linguistics") == -1 and source.find("coling") == -1 and source.find("proceedings") == -1 and source.find("conference") == -1 and source.find("meeting") == -1 and source.find("conférence") == -1 and source.find("workshop") == -1:
            source = "journal"
        else:
            source = "conference/workshop"
    iterate(keys, root, year, month, country, publisher, source, out_path)

def search_by_keyword(location, keys, out_path): 
    for file in sorted(os.listdir(location)):
        parse(path + file, keywords, out_path)
        
path = "../acl-anthology/data/xml/"
out_path = "../acl-anthology/out.csv"
keywords = ["lexical simplification", "complex word identification", 
            "lexical complexity prediction", "lexical complexity", "complex word",
            "text simplification"]

search_by_keyword(path, keywords, out_path)