class cam_properties:
    def __init__(self):
        self.allowed_values = {"takemode":[], "focalvalue":[],"isospeedvalue":[],"expcomp":[],"shutspeedvalue":[],\
            "drivemode":[], "wbvalue":[],"artfilter":[],"colortone":[],"exposemovie":[],"colorphase":[]}
        self.current_value = {"takemode":'', "focalvalue":'',"isospeedvalue":'',"expcomp":'',"shutspeedvalue":'',\
            "drivemode":'', "wbvalue":'',"artfilter":'',"colortone":'',"exposemovie":'',"colorphase":''}
        self.allowed_live_view_res = {"low":"0320x0240","mid":"0640x0480","high":"1280x0960"}
        self.current_live_view_res = ""

    def set_allowed_values(self,key,values):
        self.allowed_values[key] = values
    def set_current_value(self,key,value):
        self.current_value[key] = value

    def set_live_view_res(self,key):
        self.current_live_view_res = self.allowed_live_view_res[key]
    def get_live_view_res(self):
        for key in self.allowed_live_view_res:
            if self.allowed_live_view_res[key] == self.current_live_view_res:
                return self.current_live_view_res,key
    def get_allowed_live_view_res(self):
        return self.allowed_live_view_res

    def get_allowed_values(self,key):
        return self.allowed_values[key]

    def get_all_allowed_values(self):
        return self.allowed_values

    def get_current_value(self,key):
        return self.current_value[key]

    def change_allowed_values_range(self,key,min_value,max_value):
        n = len(self.allowed_values[key])
        av = self.allowed_values[key]
        self.allowed_values[key] = [av[i]  for i in range(n) \
            if (float(av[i]) > float(min_value) and  float(av[i]) < float(max_value) )]
        self.allowed_values[key] = [str(min_value),*self.allowed_values[key],str(max_value)]
