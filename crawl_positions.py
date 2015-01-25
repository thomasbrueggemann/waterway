from bs4 import BeautifulSoup
import pymongo, urllib2, md5, json
from datetime import datetime
from pymongo import MongoClient

_vesseltypes = {}
client = MongoClient("mongodb://ais:hofhofBRGET32723vw5!@localhost:27017/ais")
db = client.ais

# serialize postion into m3 checksum
def pos_hash(position):
	raw = str(position["_id"]) + "_" +  str(position["time"]) + "_" + json.dumps(position["coord"]["coordinates"]) + "_" + str(position["course"]) + "_" + str(position["speed"])
	return md5.new(raw).hexdigest()

# crawl all positions of a ship
def get_positions(ship, page):

	print "**** PAGE " + str(page) + " ****"
	url = "http://www.marinetraffic.com/en/ais/index/positions/all/shipid:" + str(ship["_id"]) + "/mmsi:" + str(ship["mmsi"]) + "/shipname:" + ship["shipname"].replace(" ", "%20") + "/per_page:50/page:" + str(page)
	headers = {"User-Agent": "Mozilla/5.0"}
	req = urllib2.Request(url, None, headers)
	site = urllib2.urlopen(req)
	soup = BeautifulSoup(site.read())

	# find the main table with positions
	table = soup.find("table", {"class": "table"})
	if table:

		# get all rows
		for tr in table.find_all("tr"):

			# parse to columns of this row into an position object
			td = tr.find_all("td")
			if len(td) > 5:

				position = {}

				# time               
				conv = datetime.strptime(td[0].find("time").get("datetime"), "%Y-%m-%d %H:%M")
				position["time"] = conv

				# speed
				position["speed"] = float(td[2].getText().strip().replace(" kn", ""))

				if position["speed"] > 0.0:

					# latitude / longitude
					lat = round(float(td[3].getText().strip()), 4)
					lon = round(float(td[4].getText().strip()), 4)

					position["coord"] = { "type": "Point", "coordinates": [lon, lat] }
					position["course"] = int(td[5].getText().strip())
					position["shipid"] = ship["_id"]
					position["vesseltype"] = ship["type"]
					position["_id"] = pos_hash(position)

					try:
						db.position.insert(position)
						print position
					except pymongo.errors.DuplicateKeyError:
						print "duplicate... " 

	# has next?
	n = soup.find("span", {"class": "next"})
	if n:
		if not "disabled" in n["class"]:
			page += 1
			get_positions(ship, page)
		else:
			page = 1

# read all vessels form their last crawled time descending
vessels = db.vessel.find({}, sort=[("lastcrawled", pymongo.DESCENDING)])
for vessel in vessels:

	# crawl positions for vessel
	get_positions(vessel, 1)

	# update vessesls crawl time
	db.vessel.update({"_id": vessel["_id"]}, {"$set": {"lastcrawled": datetime.utcnow()}})