import rasterio
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

print("Done with help https://github.com/KoTuK777/GeoLabs/")

file_path = '../dataPic.tif'
with rasterio.open(file_path) as src:
  bbox = src.bounds

@app.route('/get_image_bbox')
@cross_origin()
def get_image_bbox():
  return jsonify({
      'lat_max': bbox.top,
      'lat_min': bbox.bottom,
      'lon_max': bbox.right,
      'lon_min': bbox.left
  })

@app.route('/get_moisture_value/lng=<float:lng>/lat=<float:lat>', methods=['GET'])
@cross_origin()
def get_moisture_value(lng, lat):
    try:
        dataset = rasterio.open(r'../dataPic.tif')
        try:
            index = dataset.index(lng, lat)
            array = dataset.read(1)
            moisture = array[index]
            dataset.close()
            return jsonify({'moisture': int(moisture)})
        except ValueError:
            return jsonify({'moisture': 'no data'})
    except FileNotFoundError:
        return jsonify({'error': 'File not found'})


if __name__ == '__main__':
  app.run(debug=True)