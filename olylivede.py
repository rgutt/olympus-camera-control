from cam_properties import cam_properties
import time

def hexstring_to_floatstring(s):
#    s = ''.join([c for c in s])
    s_int = int(s,16) / 10
    s_string = str(s_int)
    return s_string

def hexstring_to_int(s):
#    s = ''.join([c for c in s])
    s_int = int(s,16)
    return s_int

def hexstring_to_intstring(s):
#    s = ''.join([c for c in s])
    s_int = int(s,16)
    return str(s_int)


class PacketType(object):
    __slots__ = ('first', 'middle', 'end')
    def __init__(self,packet_type_tag):
        self.first = False
        self.middle = False
        self.end = False
        if ( str(packet_type_tag[0:2]) == "90" ) and ( str(packet_type_tag[2:4]) == "60" ) : self.first = True
        elif ( str(packet_type_tag[0:2]) == "80" ) and ( str(packet_type_tag[2:4]) == "60" ) : self.middle = True
        elif ( str(packet_type_tag[0:2]) == "80" ) and ( str(packet_type_tag[2:4]) == "e0" ) : self.end = True

    @property
    def packet_type(self):
        if self.first : return  "first"
        elif self.middle : return  "middle"
        elif self.end : return  "end"
        else : return "None"

    @packet_type.setter
    def packet_type(self,rhs):
        if rhs == "first" : self.first = True
        elif rhs == "middle" : self.middle = True
        elif rhs == "end" : self.end = True
        else : raise ValueError("packet type not defined")


    def __eq__(self, rhs):
        if rhs == "first" : return self.first
        elif rhs == "middle" : return self.middle
        elif rhs == "end" : return self.end
        else : return False


#start
class RecvData:
    def __init__(self,bin_data):
        self.pos = "None"
        self.packet_type_tag = []
        self.frame_number_tag =  []
        self.frame_id_tag = []
        self.stream_id_tag = []
#        self.data = bin_data.hex()
        self.bin_data = bin_data
        self.subframe = b''
        self.startID = 12
        self.endID = len(self.bin_data)
        self.cameraCurrenValues= {"shutspeedvalue":[0,0,0], "focalvalue":[0,0,0],"isospeedvalue":[0],"expcomp":[0] }  #current focallength, min focallength, maxfocallength
        self.init_frame_tags()

    def init_frame_tags(self):
        self.packet_type_tag = self.bin_data[0:2].hex()
        self.frame_number_tag = self.bin_data[2:4].hex()
        self.frame_id_tag = self.bin_data[4:8].hex()
        self.stream_id_tag = self.bin_data[8:12].hex()


        self.pos = PacketType(self.packet_type_tag)


        if self.pos == "first":
            if (self.bin_data[224:226].hex() == 'ffd8'):  #224,225
                self.startID = 224
                self.extract_camera_settings(self.bin_data[12:self.startID].hex())

        elif self.pos == "end":
            if (self.bin_data[len(self.bin_data)-2:len(self.bin_data)].hex() == 'ffd9'):
                self.endID = len(self.bin_data)

        self.subframe = self.bin_data[self.startID:self.endID]

    def extract_camera_settings(self,camera_settings_raw):
#        print(camera_settings_raw)
#        time.sleep(10)
        self.cameraCurrenValues["focalvalue"] = [hexstring_to_floatstring(camera_settings_raw[214:216]),hexstring_to_floatstring(camera_settings_raw[206:208]),hexstring_to_int(camera_settings_raw[198:200])//10]
#        print(hexstring_to_int((camera_settings_raw[176:180])))
        if hexstring_to_int((camera_settings_raw[176:180])) > 1:                                                           #89 is 01 = 1 if the shutterspeed is < 1
            self.cameraCurrenValues["shutspeedvalue"][0] = str(hexstring_to_int(camera_settings_raw[176:180]) / hexstring_to_int((camera_settings_raw[182:184])))  + '"'
#            if self.cameraCurrenValues["shutspeedvalue"][0]
        else:
            self.cameraCurrenValues["shutspeedvalue"][0] = hexstring_to_intstring(camera_settings_raw[180:184])
        self.cameraCurrenValues["shutspeedvalue"][1] = hexstring_to_intstring(camera_settings_raw[172:176])
        self.cameraCurrenValues["shutspeedvalue"][2] = hexstring_to_intstring(camera_settings_raw[160:164]) + '"'
        if self.cameraCurrenValues["shutspeedvalue"][0] == '65531':
            self.cameraCurrenValues["shutspeedvalue"][0] = "livecomp"
        elif self.cameraCurrenValues["shutspeedvalue"][0] == '65533':
            self.cameraCurrenValues["shutspeedvalue"][0] = "livetime"
        elif self.cameraCurrenValues["shutspeedvalue"][0] == '65534':
            self.cameraCurrenValues["shutspeedvalue"][0] = "livebulb"

#        print()
        if hexstring_to_intstring(camera_settings_raw[260:264]) == "65534":
            self.cameraCurrenValues["isospeedvalue"][0] = "Low"
        else:
            self.cameraCurrenValues["isospeedvalue"][0] = hexstring_to_intstring(camera_settings_raw[260:264])
        if hexstring_to_int((camera_settings_raw[244:246])) > 0:
            self.cameraCurrenValues["expcomp"][0] = "-" + str((256 - hexstring_to_int(camera_settings_raw[246:248]))/10.)
        else:
            self.cameraCurrenValues["expcomp"][0] = "+" + hexstring_to_floatstring(camera_settings_raw[246:248])


#        print(self.cameraCurrenValues)


class Frame:
    def __init__(self, bin_data):
        self.frame = b''
        self.frame_end = False
        self.frame_start = False
        self.frame_id_tag = []
        self.n_subframes = 0
        self.prev_subframe_number_tag = []

        self.cameraCurrenValues= { }

        self.add_subframe(bin_data)


    def add_subframe(self,bin_data):
        recvdata = RecvData(bin_data)
        if recvdata.pos == "first":
            if self.frame_start == False:
                self.frame_start = True
                self.frame_id_tag = recvdata.frame_id_tag
                self.prev_subframe_number_tag = recvdata.frame_number_tag

                self.cameraCurrenValues = recvdata.cameraCurrenValues
            else:
#                print("first")
                return True

        if self.frame_id_tag == recvdata.frame_id_tag and self.frame_start == True:
            self.frame = self.frame + recvdata.subframe
#            self.frame[-1:-1] = recvdata.subframe
#            for item in recvdata.subframe:
#                self.frame.append(item)
            self.n_subframes = self.n_subframes + 1
            self.prev_subframe_number_tag = recvdata.frame_number_tag
            if recvdata.pos == "end":
                self.frame_end = True
            return False
        else:
#            print("second")
            return True

    def has_finished(self):
        return self.frame_end
    def has_started(self):
        return self.frame_start


class LiveViewDecoder(Frame):
    def __init__(self):
        pass

