from lxml import etree
import xml.etree.ElementTree as ET
import time
from requests_retry_session import requests_retry_session, requests
from cam_properties import cam_properties


save_files = True

class OMDNotThere(Exception):
    pass

class OMD:
    def __init__(self):
        self.ip = "192.168.0.10"
        self.cam_properties = cam_properties()
        self.cam_properties.set_live_view_res("mid")
        if self.islive():
            self.settings = self.get_all_settings()

    def reinit(self):
        if self.islive():
            self.settings = self.get_all_settings()

    def islive(self):
        try:
            requests_retry_session().get("http://" + self.ip + "/",timeout=1)
            return True
        except requests.RequestException as e:
            return False

    def make_url(self, cmd):
        return "http://%s/%s.cgi" % (self.ip, cmd)

    def remove_encoding(self, s):
        return s.replace('encoding="Shift-JIS"', "")

    def get_url(self, url, save=None, body = None, timeout = 1):
        try:
            if body == None:
                method = "get"
            else:
                method = "post"
            if save == None:
                save = save_files
#            if self.islive():
            headers = {
                'Host'        : '192.168.0.10',
                'Connection'  : 'Keep-Alive',
                'User-Agent'  : 'OI.Share v2',
                'Content-Type': 'text/xml',
            }


            page = etree.Element('set')
            page_element = etree.SubElement(page, 'value')
            page_element.text = '2'
            xml_data = etree.tostring(page, pretty_print=True, encoding=None).decode()

            response = requests_retry_session().get(url,headers=headers,data=body,timeout=timeout)
            txt = response.text
            return self.remove_encoding(txt)
        except requests.RequestException as e:
            raise OMDNotThere("Could not connect to the OM-D camera at 192.168.0.10. This is probably because you're not connected to the camera's wifi network.")


    def get_all_settings(self):
        self.switch_mode("rec")
        root = ET.fromstring(self.get_url("http://192.168.0.10/get_camprop.cgi?com=desc&propname=desclist"))
        settings = {}
        for child in root:
            if child.tag == "desc":
                propname  = child.find("propname").text  # property name
                attribute = child.find("attribute").text # get or getset
                value     = child.find("value").text     # the current value
                try:
                    enum      = child.find("enum").text      # the list of possible values
                    enum = enum.split(" ")
                except AttributeError:
                    enum = None
                if attribute == "getset":
                    self.cam_properties.set_allowed_values(propname,enum)
                    self.cam_properties.set_current_value(propname,value)
                settings[propname] = {
                    "attribute" : attribute,
                    "value"     : value,
                    "enum"      : enum,
                }
#        self.switch_mode("shutter")

        return settings

    def switch_mode(self, mode):
        if mode == "rec":
            self.get_url("http://192.168.0.10/switch_cammode.cgi?mode=rec&lvqty=%s" % self.cam_properties.get_live_view_res()[0])
        elif mode == "shutter":
            self.get_url("http://192.168.0.10/switch_cammode.cgi?mode=shutter")
        elif mode == "play":
            self.get_url("http://192.168.0.10/switch_cammode.cgi?mode=play")
        else:
            return "Couldn't find camera mode " + mode
#            raise Exception("Invalid camera mode")


    def change_live_stream_resolution(self,key):
        self.cam_properties.set_live_view_res(key)
        self.get_url("http://192.168.0.10/switch_cammode.cgi?mode=play")
        self.get_url("http://192.168.0.10/switch_cammode.cgi?mode=rec&lvqty=%s" % self.cam_properties.get_live_view_res()[0])

    def set_setting(self, settingname, value):
        try:
            self.cam_properties.get_allowed_values(settingname).index(value)
            self.get_url("http://192.168.0.10/set_camprop.cgi?com=set&propname=%s" % settingname , body = "<set><value>%s</value></set>" % value)
            return "%s set to %s" % (settingname, value)
        except ValueError:
            return "Couldn't find %svalue %s" % (settingname, value)


    def take_picture(self):
        shutspeedvalue = self.cam_properties.get_current_value("shutspeedvalue")
        waitTime = 0.5
        if shutspeedvalue[-1] == '"':
            waitTime = float(self.cam_properties.get_current_value("shutspeedvalue").strip('"'))
        elif shutspeedvalue[0] == 'l':
            waitTime = 60 + waitTime


        self.switch_mode("shutter")
        self.get_url("http://192.168.0.10/exec_shutter.cgi?com=1st2ndpush",timeout=waitTime)
        time.sleep(waitTime*2)
        self.get_url("http://192.168.0.10/exec_shutter.cgi?com=2nd1strelease")
        time.sleep(waitTime*2)
        self.switch_mode("rec")

    def get_caminfo(self):
        return self.get_url("http://192.168.0.10/get_caminfo.cgi")

    def get_commandlist(self):
        return self.get_url("http://192.168.0.10/get_commandlist.cgi")

    def get_imglist(self):
        # switch to play
        return self.get_url("http://192.168.0.10/get_imglist.cgi?DIR=%2FDCIM%2F100OLYMP")

    def get_img(self,imgname):
        return self.get_url("http://192.168.0.10/DCIM/100OLYMP/%s" % imgname)


    def start_liveview(self,UDP_PORT):
        self.get_url("http://192.168.0.10/exec_takemisc.cgi?com=startliveview&port=%s" % str(UDP_PORT))

    def stop_liveview(self):
        self.get_url("http://192.168.0.10/exec_takemisc.cgi?com=stopliveview")

    def assignafframe(self,x,y):
        if (self.cam_properties.get_live_view_res()[1] == "mid"):
            self.get_url("http://192.168.0.10/exec_takemotion.cgi?com=assignafframe&point=0%sx0%s" % (x,y))
        elif (self.cam_properties.get_live_view_res()[1] == "low"):
            self.get_url("http://192.168.0.10/exec_takemotion.cgi?com=assignafframe&point=0%sx0%s" % (x//2,y//2))
        elif (self.cam_properties.get_live_view_res()[1] == "high"):
            self.get_url("http://192.168.0.10/exec_takemotion.cgi?com=assignafframe&point=0%sx0%s" % (x*2,y*2))
