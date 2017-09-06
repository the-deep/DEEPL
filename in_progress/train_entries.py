import csv

from entries.models import Entry
from entries.models import Sector

#get lookups for sectors
SECT_LOOK = {i.id : i.name for i in Sector.objects.all()}


def extract_sects(raw):
    l = [i.entryinformation_set.all() for i in Entry.objects.all()]
    div = [sub for list in l for sub in list]
    sect_dict = {}

    for v in div:
		#there can be multiple sectors in an entry so we have to cycle through and get them
		#since we can have sub-pillars, we take the unique sector types

		# if we want dict of dicts
		# for uniq in list(set(SECT_LOOK[k['sector_id']] for k in v.informationattribute_set.values())):
		# 	if v.pk not in sect_dict:
		# 		sect_dict[v.pk] = {v.excerpt : [uniq]}
		# 	else:
		# 		sect_dict[v.pk][v.excerpt].append(uniq)

		for uniq_sect in list(set(SECT_LOOK[k['sector_id']] for k in v.informationattribute_set.values())):
			if uniq_sect not in sect_dict:
				sect_dict[uniq_sect] = [v.excerpt]
			else:
				sect_dict[uniq_sect].append(v.excerpt)

	return sect_dict


def train_nb(sect_dict):
    pass


def handle():
	#prep entries
    sect_dict = extract_sects()
    model = train_nb(sect_dict)