# -*- coding: utf-8 -*-
###############################################################################
# mspFS von shadowrider
###############################################################################
from Plugins.Plugin import PluginDescriptor
from Components.PluginComponent import plugins
import os
from enigma import eTimer
import time
import datetime

if not os.path.exists("/etc/ConfFS/"):
    os.mkdir("/etc/ConfFS/")
from .anzeige import mspFS_anzeige
from .paint import mspFS_paint
version = "1.06"

session = None
del_on = 1
try:
    from Plugins.Extensions.LCD4linux.module import L4Lelement
    from .paint import mspFS_paint
    l4l = True
except:
    l4l = None


def timerstart():
    heute = datetime.date.today()
    if heute.year == 1970:
        SchichtTimer.startLongTimer(10)
    else:
        if 1 == 1:  # l4l:
            mspFS_paint()

            now = time.localtime()
            timestamp2 = time.mktime((now.tm_year, now.tm_mon, now.tm_mday, 0, 0, 0, 0, 0, 0)) + 86400
            diff = timestamp2 - time.mktime((now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, 0, 0, 0))
            #f=open("/tmp/diff","a")
            #f.write(str(diff)+"\n")
            #f.close()
            #morgen=datetime.timedelta(days=1)
            #neu=datetime.date.today()+morgen
            #dt = datetime.datetime(year=neu[0], month=neu[1], day=neu[2])
            #morgen=datetime.timedelta(days=1)
            #diff=now-(dt+morgen
            SchichtTimer.startLongTimer(int(diff))
        if del_on:
            run_autodel()


def run_autodel():
    try:
        from configparser import ConfigParser
        import datetime
        heute = datetime.date.today()
        configparser = ConfigParser()
        configparser.read("/etc/ConfFS/mspFS.conf")
        autodel = int(configparser.get("settings", "autodel"))
        sonders = eval(configparser.get("settings", "sonders"))
        if autodel == 1 and heute.month == 1:
            del_list = []
            jahr = heute.year
            for k in sonders:
                if str(k)[0:4] == str(jahr - 1):
                    del_list.append(k)
                if len(del_list):
                    for x in del_list:
                        del sonders[x]
            configparser2 = ConfigParser()
            configparser2.read("/etc/ConfFS/mspFS.conf")
            configparser2.set("settings", "sonders", str(sonders))
            fp = open("/etc/ConfFS/mspFS.conf", "w")
            configparser2.write(fp)
            fp.close()
        global del_on
        del_on = 0
    except:
        pass


def set_schicht():
    timerstart()

######################################################################################
######################################################################################


def main(session, **kwargs):
     session.open(mspFS_anzeige, version)


def autostart(reason, **kwargs):
     set_schicht()


def Plugins(path, **kwargs):
    global SchichtTimer
    SchichtTimer = eTimer()
    SchichtTimer.callback.append(set_schicht)
    list = []
    #if l4l:
    list.append(PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=autostart))
    list.append(PluginDescriptor(name="mspFS", description="mein Schichplan", where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], fnc=main))
    return list
