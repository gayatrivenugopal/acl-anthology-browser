#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 21:34:58 2021

@author: g3
"""

import os.path

class Paper:
    def __init__(self):
        self.id = id(self)
        
    def save(self, year, month, title, auth_list, country, source, publisher):
        self.year = year if year is not None else ""
        self.month = month if month is not None else ""
        self.title = title if title is not None else ""
        self.auth_list = auth_list if len(auth_list) is not None else []
        self.country = country if country is not None else ""
        self.source = source if source is not None else ""
        self.publisher = publisher if publisher is not None else ""
        
    def write(self, out_path):
        if not os.path.exists(out_path):
            with open(out_path, "w", encoding = "utf-8") as file:
                file.write("year\tmonth\ttitle\tauthors\tcountry\tsource\tpublisher\n")
        with open(out_path, "a", encoding = "utf-8") as file: 
            file.write(self.year + "\t" + self.month + "\t" + self.title + "\t" + 
                       ",".join(self.auth_list) + "\t" + 
                       self.country + "\t" + self.source + "\t" + self.publisher + "\n")