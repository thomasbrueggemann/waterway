'use strict';

var waterway = require("../waterway");
var fs = require("fs");

describe("prepareShape", function () {

	it("should read at least one shape without error", function (done) {

		this.timeout(60000 * 60 * 24);

		waterway.prepareShape("../data/water_polygons.shp", function(err, geojson) {

			err.should.equal(null);
			geojson.length.should.not.equal(0);

			fs.exists("../data/water_polygons.json", function(exists) {
				exists.should.equal(true);
				return done();
			});
		});
	});
});