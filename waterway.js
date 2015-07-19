var shp = require("shpjs");
var fs = require("fs");

// PREPARE SHAPE
var prepareShape = function(file, callback) {

	// read shapefile
	shp(file).then(function(geojson) {

		// write geojson to file
		fs.write(file.replace(".shp", ".json"), JSON.stringify(geojson), function(err) {

			// callback
        	return callback(err, geojson);
		});
    });
};

module.exports = {
	"prepareShape": prepareShape
}