from bs4 import BeautifulSoup
import pymongo, urllib2
from datetime import datetime
from pymongo import MongoClient

_vesseltypes = {}
client = MongoClient("mongodb://ais:hofhofBRGET32723vw5!@localhost:27017/ais")
db = client.ais

for vtype in db.vesseltype.find():
	_vesseltypes[vtype["name"]] = vtype["_id"]

# get or assign a vesseltype
def get_vesseltype(name):
	if _vesseltypes.has_key(name):
		return _vesseltypes[name]
	else:
		highest_num = db.vesseltype.find_one({}, sort = [("_id", pymongo.DESCENDING)])
		if highest_num:
			new_index = int(highest_num["_id"]) + 1
			db.vesseltype.insert({
				"_id": new_index,
				"name": name
			})

			_vesseltypes[name] = new_index

			return new_index

# read all vessels
def get_vessels(page):
	print "**** PAGE " + str(page) + " ****"
	url = "http://www.marinetraffic.com/en/ais/index/ships/all/per_page:50/page:" + str(page) + "/speed_between:1,50"
	headers = {"User-Agent": "Mozilla/5.0"}
	req = urllib2.Request(url, None, headers)
	site = urllib2.urlopen(req)
	soup = BeautifulSoup(site.read())

	# get ship links
	for link in soup.find_all('a'):
		if "ais/details/ships" in link.get("href"):
			l = link.get("href").split("/")
			vessel = {}
			for ll in l:
				if ":" in ll:
					lll = ll.split(":")
					if lll[1].isdigit():
						vessel[lll[0]] = int(lll[1])
					else:
						vessel[lll[0]] = lll[1].replace("%20", " ")
			
			# prepare _id
			vessel["_id"] = vessel["shipid"]
			vessel["lastcrawled"] = datetime.utcnow()
			vessel.pop("shipid", None)

			# get vessel type
			for img in link.parent.parent.find_all("img"):
				if "vessel_types" in img.get("src"):
					vessel["type"] = get_vesseltype(img.get("alt"))

			try:
				db.vessel.insert(vessel)
				print vessel
			except pymongo.errors.DuplicateKeyError:
				print "duplicate... "

	# has next?
	n = soup.find("span", {"class": "next"})
	if n:
		if not "disabled" in n["class"]:
			db.status.update({"_id": "vessel_page"}, {"$set": {"value": page}}, upsert = True)
			page += 1
			get_vessels(page)
		else:
			page = 1
			db.status.update({"_id": "vessel_page"}, {"$set": {"value": 0}}, upsert = True)

start = 1

# try to start where the last run interupted
vessel_page = db.status.find_one({"_id": "vessel_page"})
if vessel_page:
	start = vessel_page["value"] + 1

# crawl vessels
get_vessels(start)
