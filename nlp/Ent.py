#new entry object

class Ent(object):
    def __init__(self):
        self.onedim = None
        self.twodim = None
        self.reliability = None
        self.severity = None
        self.demo_groups = None
        self.specific_needs = None
        self.affected_groups = None
        self.geo_locations = None
        self.information_date = None
        self.excerpt = None
        self.has_image = None
        self.lead_text = None
        self.lead_id = None
        self.event = None
    
    def add_onedim(self, info_att):
        pill_nm = info_att.subpillar.pillar.name
        subpill_nm = info_att.subpillar.name
        
        if not self.onedim:
            self.onedim = {}
        
        if pill_nm not in self.onedim:
            self.onedim[pill_nm] = [subpill_nm]
        else:
            self.onedim[pill_nm].append(subpill_nm)
    
    def add_twodim(self, info_att):
        if not self.twodim:
            self.twodim = []
            
        tddict = {'pillar' : None, 'subpillar' : None, 'sector' : None, 'subsectors' : None}
        
        tddict['sector'] = info_att.sector.name
        tddict['pillar'] = info_att.subpillar.pillar.name
        tddict['subpillar'] = info_att.subpillar.name
        if len(info_att.subsectors.all()) > 0:
            tddict['subsectors'] = [sub.name for sub in info_att.subsectors.all()]
        
        self.twodim.append(tddict)
