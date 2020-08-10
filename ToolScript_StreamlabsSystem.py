#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import time
import re

import random
random = random.WichmannHill()

#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "ToolScript"
Website = "https://www.twitch.tv/sirphilthyowl"
Creator = "An Owl"
Version = "1.0.1"
Description = "Purchasable tool for viewers too spend on commands."
#---------------------------------------
# Versions
#---------------------------------------


#1.0.1 Added commands for adding tools.
#1.0.0 Script made

#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
ReadList = os.path.join(os.path.dirname(__file__), "ReadMe.txt")
UserFile = os.path.join(os.path.dirname(__file__), "lib/UserFile.json")
ToolsFile = os.path.join(os.path.dirname(__file__), "lib/ToolsFile.json")

#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8')
        else: #set variables if no custom settings file is found
            self.only_live = only_live
            self.tool_name = tool_name
            self.store_command = store_command
            self.store_message = store_message
            self.buy_command = buy_command
            self.buy_message = buy_message
            self.cant_buy_message = cant_buy_message
            self.status_command = status_command
            self.status_message = status_message
            self.no_status_message = no_status_message
            self.exempt = exempt
            self.format_store = format_store
            self.tool_used_message = tool_used_message
            self.tool_broke = tool_broke

            self.AlterTool_command = AlterTool_command
            self.AddTool_message_succes = AddTool_message_succes
            self.AddTool_message_fail = AddTool_message_fail
            self.RemoveTool_message_succes = RemoveTool_message_succes
            self.RemoveTool_message_fail = RemoveTool_message_fail

    # Reload settings on save through UI
    def ReloadSettings(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        try:
            """Save settings to files (json and js)"""
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
                json.dump(self.__dict__, f, encoding='utf-8', ensure_ascii=False)
            with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        T.SaveTools()
        if not P == None and not len(P.Dict) == 0:
            P.SaveSettings()
        return

class Tool:
    def __init__(self):
        if ToolsFile and os.path.isfile(ToolsFile):
            try:
                with codecs.open(ToolsFile, encoding='utf-8-sig', mode='r') as f:
                    self.tools = json.load(f, encoding='utf-8')
            except:
                self.tools = {}

    def SaveTools(self):
        with codecs.open(ToolsFile, encoding='utf-8-sig', mode='w+') as f:
            json.dump(self.tools, f, encoding='utf-8', ensure_ascii=False)

    @property
    def tools_string(self):
        """Property for turning all tools into a string to be displayed"""
        if len(self.tools) == 0:
            second_message = "sadly there are no tools in the shop."
            return second_message
        second_message = ""
        for key, value in self.tools.items():
            tmp = MySet.format_store
            tmp = tmp.replace("$type", key)
            tmp = tmp.replace("$durability", value["Durability"])
            tmp = tmp.replace("$price", str(value["Cost"]))
            second_message = second_message + tmp + " "
        return second_message

    def add_tool(self, regex):
        """Method for adding tools"""
        self.tools[regex.group(1)] = {}
        self.tools[regex.group(1)]["Type"] = regex.group(1)
        self.tools[regex.group(1)]["Durability"] = regex.group(2)
        self.tools[regex.group(1)]["Cost"] = regex.group(3)

    def remove_tool(self, tool):
        """Method for removing tools"""
        for key, value in self.tools.items():
            if key == tool:
                self.tools.pop(key, None)
                return True
        return False

    def check_tool(self, word):
        for key, value in self.tools.items():
            if key.lower() == word.lower():
                return key
        return None


class Users:
    def __init__(self):
        if UserFile and os.path.isfile(UserFile):
            with codecs.open(UserFile, encoding='utf-8-sig', mode='r+') as f:
                self.Dict = json.load(f, encoding='utf-8')
        else:
            self.Dict = {}

    def SaveSettings(self):
        with codecs.open(UserFile, encoding='utf-8-sig', mode='w+') as f:
            json.dump(self.Dict, f, encoding='utf-8', ensure_ascii=False)

    def ReloadSettings(self):
        with codecs.open(UserFile, encoding='utf-8-sig', mode='r') as f:
            self.Dict = json.load(f, encoding='utf-8')


    def Add(self, name, tool):
        Durability = T.tools[tool]["Durability"]
        Durability = "{}/{}".format(Durability, Durability)
        self.Dict[name] = {"Tool": T.tools[tool]["Type"], "Durability": Durability}

    def Replacer(self, data, string):
        Message = string
        if "$user" in string:
            Message = Message.replace("$user", data.UserName)
        if "$tooltype" in string:
            Message = Message.replace("$tooltype", self.Dict[data.User]["Tool"])
        if "$durability" in string:
            Message = Message.replace("$durability", self.Dict[data.User]["Durability"])
        if "$currencyname" in string:
            Message = Message.replace("$currencyname", Parent.GetCurrencyName())
        if "$price" in string:
            Message = Message.replace("$price", str(T.tools[self.Dict[data.User]["Tool"]]["Cost"]))
        if "$nametools" in string:
            Message = Message.replace("$nametools", MySet.tool_name)
        if "$buycommand" in string:
            Message = Message.replace("$buycommand", MySet.buy_command)
        if "$addtool" in string:
            Message = Message.replace("$addtool", MySet.AlterTool_command)
        if "$addformat" in string:
            Message = Message.replace("$addformat", "+name[durability,uses]")
        if "$tools" in Message:
            Message = Message.replace("$tools", T.tools_string)
        return Message

#---------------------------------------
# Settings functions
#---------------------------------------
def ReloadSettings(jsondata):
    """Reload settings on Save"""
    # Reload saved settings
    MySet.ReloadSettings(jsondata)
    P.ReloadSettings()
    # End of ReloadSettings

def SaveSettings(self, settingsFile):
    """Save settings to files (json and js)"""
    with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
        json.dump(self.__dict__, f, encoding='utf-8')
    with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
        f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
    T.SaveTools()
    if not P == None and not len(P.Dict) == 0:
        P.SaveSettings()
    return

#---------------------------------------
# System functions
#---------------------------------------

def Unload():
    T.SaveTools()
    P.SaveSettings()

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    global P
    global T
    P = None
    MySet = Settings(settingsFile)
    T = Tool()
    # Load in saved settings
    MySet.SaveSettings(settingsFile)
    P = Users()

    # End of Init

def Execute(data):
    if (MySet.only_live and Parent.IsLive()) or (not MySet.only_live and not Parent.IsLive()):

        #adding tool command.
        if data.GetParam(0) == MySet.AlterTool_command and Parent.HasPermission(data.User, "Editor", ""):
            regex = re.search(r'\+(.*)\[(\d+)\,(\d+)\]', data.Message)
            if regex:
                T.add_tool(regex)
                Parent.SendStreamMessage(P.Replacer(data, MySet.AddTool_message_succes))
                return
            regex = re.search(r'\-(.*)', data.Message)
            if regex:
                Parent.SendStreamMessage(P.Replacer(data, MySet.RemoveTool_message_succes) if T.remove_tool(regex.group(1)) else P.Replacer(data, MySet.RemoveTool_message_fail))
                return
            else:
                Parent.SendStreamMessage(P.Replacer(data, MySet.Altertool_message_fail))

        #Showing Store command
        elif data.GetParam(0) == MySet.store_command:
            Parent.SendStreamMessage(P.Replacer(data, MySet.store_message))
            return

        #Showing tool command
        elif data.GetParam(0) == MySet.status_command:
            Parent.SendStreamMessage(P.Replacer(data, MySet.status_message) if data.User in P.Dict else P.Replacer(data, MySet.no_status_message))
            return

        #Buy command
        elif data.GetParam(0) == MySet.buy_command:
            if data.GetParam(1):
                Tool = T.check_tool(data.GetParam(1))
                if not Tool == None and Parent.RemovePoints(data.User, data.UserName, int(T.tools[Tool]["Cost"])):
                    P.Add(data.User, Tool)
                    Parent.SendStreamMessage(P.Replacer(data, MySet.buy_message))
                    return
                else:
                    Parent.SendStreamMessage(P.Replacer(data, MySet.cant_buy_message))
                    return
            Parent.SendStreamMessage(P.Replacer(data, MySet.buy_incorrect))

#---------------------------------------
# [Required] functions for emoteDic handling
#---------------------------------------

def Tick():
    pass

#---------------------------------------
# Parsefunction
#---------------------------------------

def Parse(parseString, userid, username, targetid, targetname, message):
    if "$tool" in parseString:
        if username == Parent.GetChannelName() and MySet.exempt:
            placeholder = ""
        else:
            if userid in P.Dict:
                Durability = P.Dict[userid]["Durability"]
                Durability = Durability.split("/")
                tmp = int(Durability[0]) - 1
                Parent.SendStreamMessage(parseReplacer(userid, MySet.tool_used_message))
                if tmp == 0:
                    Parent.SendStreamMessage(parseReplacer(userid, MySet.tool_broke))
                    P.Dict.pop(userid, None)
                else:
                    P.Dict[userid]["Durability"] = str(tmp) + "/" + Durability[1]
            else:
                Parent.SendStreamMessage(parseReplacer(userid, MySet.no_status_message))
                return
        regex = re.search(r'\$tool\((.*)\)', parseString)
        parseString = regex.group(1).replace("~", "$")
    return parseString

def parseReplacer(name, string):
    """stupid function because #Parse has no "data" object and
    I can't run it through my class Replacer method that needs data object REE"""
    Message = string
    userName = Parent.GetDisplayName(name)
    if "$user" in string:
        Message = Message.replace("$user", userName)
    if "$tooltype" in string:
        Message = Message.replace("$tooltype", P.Dict[name]["Tool"])
    if "$nametools" in string:
        Message = Message.replace("$nametools", MySet.tool_name)
    if "$buycommand" in string:
        Message = Message.replace("$buycommand", MySet.buy_command)
    return Message
#---------------------------------------
# UI functions
#---------------------------------------
def openreadme():
    os.startfile(ReadList)

def opentool():
    os.startfile(ToolsFile)
