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
    """
    Iterate through the elements and store the details in the instance of Paper.
    """
    if node is None:
        return
    if len(node.findall("paper")) == 0:
        #iterate through child nodes to search for the paper element
         for child in node:
             iterate(keys, child, year, month, country, publisher, source, out_path)
    else:
        for paper in node.findall("paper"):
            if paper.find("title") is not None and paper.find("title").find("fixed-case") is not None:
                #recreate the title by extracting values from title and fixed-case
                xmlstr = (ET.tostring(paper.find("title"), encoding='utf8', method='xml')).decode("utf-8")
                xmlstr = xmlstr.replace("<fixed-case>", "")
                xmlstr = xmlstr.replace("</fixed-case>", "")
                title = xmlstr[xmlstr.find("<title>")+7:xmlstr.find("</title>")]
            else:
                title = paper.find("title").text
            #search for each keyword
            for key in keys:
                     if title is not None and title.find(key) != -1 or (paper.find("abstract") is not None and paper.find("abstract").text is not None and (paper.find("abstract").text).find(key) != -1):
                         #if keyword is found, store the paper details
                         if paper.findall("author") is not None:
                             auth_list = []
                             for child in paper.findall("author"):
                                 auth_list.append(child.find("first").text + " " + child.find("last").text)
                         paper_object =  Paper()
                         paper_object.save(year, month, title, auth_list, country, source, publisher)
                         paper_object.write(out_path)
                         #once the paper details have been saved for a key, continue to the next paper
                         break
    
def parse(file, keys, out_path):
    """
    Extract the details of the journal/conference/workshop.
    Args:
        file (str): path to the data file
        keys (list): list of keywords to be used as filter
        out_path (str): path to the file in which the details should be stored
    """
    tree = ET.parse(file)
    root = tree.getroot()
    year = publisher = month = country = None
    source = "journal"
    conf_identifiers = ["findings of the association for computational linguistics", 
                        "coling", "proceedings", "conference", "meeting", 
                        "conférence", "workshop"]
    
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
        for identifier in conf_identifiers:
            if source.find(identifier) != -1:
                source = "conference/workshop"
    iterate(keys, root, year, month, country, publisher, source, out_path)

def search_by_keyword(location, keys, out_path):
    """
    Search for the keywords in each file in the data directory and store the details.
    Args:
        location (str): path to the data directory
        keys (list): list of keywords to be used as filter
        out_path (str): path to the file in which the details should be stored
    """
    for file in sorted(os.listdir(location)):
        parse(path + file, keywords, out_path)
        
path = "acl-anthology/data/xml/"
out_path = "acl-anthology/out.csv"
keywords = ["lexical simplification", "complex word identification", 
            "lexical complexity prediction", "lexical complexity", "complex word",
            "text simplification"]

search_by_keyword(path, keywords, out_path)