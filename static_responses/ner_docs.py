data = {
  "locations": [
    {
      "name": "Karachi",
      "info": {
        "address_components": [
          {
            "short_name": "Karachi",
            "types": [
              "locality",
              "political"
            ],
            "long_name": "Karachi"
          },
          {
            "short_name": "Karachi City",
            "types": [
              "administrative_area_level_2",
              "political"
            ],
            "long_name": "Karachi City"
          },
          {
            "short_name": "Sindh",
            "types": [
              "administrative_area_level_1",
              "political"
            ],
            "long_name": "Sindh"
          },
          {
            "short_name": "PK",
            "types": [
              "country",
              "political"
            ],
            "long_name": "Pakistan"
          }
        ],
        "types": [
          "locality",
          "political"
        ],
        "place_id": "ChIJv0sdZQY-sz4RIwxaVUQv-Zw",
        "formatted_address": "Karachi, Karachi City, Sindh, Pakistan",
        "geometry": {
          "bounds": {
            "northeast": {
              "lat": 25.6398011,
              "lng": 67.65694169999999
            },
            "southwest": {
              "lat": 24.7466037,
              "lng": 66.6539822
            }
          },
          "location_type": "APPROXIMATE",
          "location": {
            "lat": 24.8607343,
            "lng": 67.0011364
          },
          "viewport": {
            "northeast": {
              "lat": 25.6398011,
              "lng": 67.65694169999999
            },
            "southwest": {
              "lat": 24.7466037,
              "lng": 66.6539822
            }
          }
        }
      }
    },
    {
      "name": "Pakistan",
      "info": {
        "cached": True,
        "formatted_address": "Pakistan",
        "address_components": [
          {
            "short_name": "PK",
            "types": [
              "country",
              "political"
            ],
            "long_name": "Pakistan"
          }
        ],
        "place_id": "ChIJH3X9-NJS2zgRXJIU5veht0Y",
        "types": [
          "country",
          "political"
        ],
        "geometry": {
          "bounds": {
            "northeast": {
              "lat": 37.084107,
              "lng": 77.8316195
            },
            "southwest": {
              "lat": 23.6344999,
              "lng": 60.8729721
            }
          },
          "location_type": "APPROXIMATE",
          "location": {
            "lat": 30.375321,
            "lng": 69.34511599999999
          },
          "viewport": {
            "northeast": {
              "lat": 37.084107,
              "lng": 77.8316195
            },
            "southwest": {
              "lat": 23.6344999,
              "lng": 60.8729721
            }
          }
        }
      }
    },
    {
      "name": "Indus River",
      "info": {
        "address_components": [
          {
            "short_name": "Indus River",
            "types": [
              "establishment",
              "natural_feature"
            ],
            "long_name": "Indus River"
          }
        ],
        "types": [
          "establishment",
          "natural_feature"
        ],
        "place_id": "ChIJGVGmt5Z5JjkRBQQMhNWG93c",
        "formatted_address": "Indus River",
        "geometry": {
          "bounds": {
            "northeast": {
              "lat": 35.8912897,
              "lng": 79.560344
            },
            "southwest": {
              "lat": 23.9177466,
              "lng": 67.36821619999999
            }
          },
          "location_type": "APPROXIMATE",
          "location": {
            "lat": 29.9045182,
            "lng": 73.4642801
          },
          "viewport": {
            "northeast": {
              "lat": 35.8912897,
              "lng": 79.560344
            },
            "southwest": {
              "lat": 23.9177466,
              "lng": 67.36821619999999
            }
          }
        }
      }
    },
    {
      "name": "South Punjab",
      "info": {
        "address_components": [
          {
            "short_name": "Punjab",
            "types": [
              "administrative_area_level_1",
              "political"
            ],
            "long_name": "Punjab"
          },
          {
            "short_name": "PK",
            "types": [
              "country",
              "political"
            ],
            "long_name": "Pakistan"
          }
        ],
        "types": [
          "administrative_area_level_1",
          "political"
        ],
        "place_id": "ChIJy5pBdImU3zgRoOxO0hgwnjo",
        "formatted_address": "Punjab, Pakistan",
        "geometry": {
          "bounds": {
            "northeast": {
              "lat": 34.0434647,
              "lng": 75.38186639999999
            },
            "southwest": {
              "lat": 27.7051105,
              "lng": 69.3288726
            }
          },
          "location_type": "APPROXIMATE",
          "location": {
            "lat": 31.1704063,
            "lng": 72.7097161
          },
          "viewport": {
            "northeast": {
              "lat": 34.0434647,
              "lng": 75.38186639999999
            },
            "southwest": {
              "lat": 27.7051105,
              "lng": 69.3288726
            }
          }
        }
      }
    },
    {
      "name": "Turkey.",
      "info": {
        "address_components": [
          {
            "short_name": "TR",
            "types": [
              "country",
              "political"
            ],
            "long_name": "Turkey"
          }
        ],
        "types": [
          "country",
          "political"
        ],
        "place_id": "ChIJcSZPllwVsBQRKl9iKtTb2UA",
        "formatted_address": "Turkey",
        "geometry": {
          "bounds": {
            "northeast": {
              "lat": 42.3666999,
              "lng": 44.8178449
            },
            "southwest": {
              "lat": 35.808592,
              "lng": 25.5377
            }
          },
          "location_type": "APPROXIMATE",
          "location": {
            "lat": 38.963745,
            "lng": 35.243322
          },
          "viewport": {
            "northeast": {
              "lat": 42.3666999,
              "lng": 44.8178449
            },
            "southwest": {
              "lat": 35.808592,
              "lng": 25.5377
            }
          }
        }
      }
    }
  ]
}


def static_data(*args, **kwargs):
    return data
