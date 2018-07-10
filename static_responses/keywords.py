data = {
  "nodes": [
    {
      "group": 5,
      "id": "pressure"
    },
    {
      "group": 2,
      "id": "crisis"
    },
    {
      "group": 0,
      "id": "said"
    },
    {
      "group": 0,
      "id": "people"
    },
    {
      "group": 4,
      "id": "border"
    },
    {
      "group": 5,
      "id": "esk"
    },
    {
      "group": 4,
      "id": "shelter"
    },
    {
      "group": 0,
      "id": "leave"
    },
    {
      "group": 3,
      "id": "flee"
    },
    {
      "group": 4,
      "id": "bamboo"
    },
    {
      "group": 2,
      "id": "country"
    },
    {
      "group": 5,
      "id": "usk"
    },
    {
      "group": 3,
      "id": "right"
    },
    {
      "group": 2,
      "id": "bangladesh"
    },
    {
      "group": 3,
      "id": "plan"
    },
    {
      "group": 3,
      "id": "persecution"
    },
    {
      "group": 5,
      "id": "myanmar"
    },
    {
      "group": 4,
      "id": "message"
    },
    {
      "group": 2,
      "id": "called"
    },
    {
      "group": 0,
      "id": "barbed"
    },
    {
      "group": 4,
      "id": "committee"
    },
    {
      "group": 1,
      "id": "refugee"
    },
    {
      "group": 5,
      "id": "process"
    },
    {
      "group": 4,
      "id": "live"
    },
    {
      "group": 1,
      "id": "health"
    },
    {
      "group": 2,
      "id": "criticism"
    },
    {
      "group": 4,
      "id": "week"
    },
    {
      "group": 3,
      "id": "government"
    }
  ],
  "links": [
    {
      "value": 1,
      "target": "leave",
      "source": "said"
    },
    {
      "value": 1,
      "target": "bamboo",
      "source": "said"
    },
    {
      "value": 13,
      "target": "myanmar",
      "source": "said"
    },
    {
      "value": 1,
      "target": "shelter",
      "source": "people"
    },
    {
      "value": 13,
      "target": "flee",
      "source": "people"
    },
    {
      "value": 11,
      "target": "usk",
      "source": "people"
    },
    {
      "value": 7,
      "target": "plan",
      "source": "people"
    },
    {
      "value": 1,
      "target": "week",
      "source": "people"
    },
    {
      "value": 13,
      "target": "shelter",
      "source": "border"
    },
    {
      "value": 11,
      "target": "leave",
      "source": "border"
    },
    {
      "value": 11,
      "target": "health",
      "source": "border"
    },
    {
      "value": 7,
      "target": "week",
      "source": "border"
    },
    {
      "value": 5,
      "target": "shelter",
      "source": "esk"
    },
    {
      "value": 1,
      "target": "persecution",
      "source": "esk"
    },
    {
      "value": 1,
      "target": "message",
      "source": "esk"
    },
    {
      "value": 11,
      "target": "government",
      "source": "esk"
    },
    {
      "value": 11,
      "target": "bamboo",
      "source": "shelter"
    },
    {
      "value": 7,
      "target": "country",
      "source": "shelter"
    },
    {
      "value": 1,
      "target": "plan",
      "source": "shelter"
    },
    {
      "value": 11,
      "target": "live",
      "source": "shelter"
    },
    {
      "value": 13,
      "target": "week",
      "source": "shelter"
    },
    {
      "value": 1,
      "target": "flee",
      "source": "leave"
    },
    {
      "value": 11,
      "target": "bamboo",
      "source": "leave"
    },
    {
      "value": 1,
      "target": "right",
      "source": "leave"
    },
    {
      "value": 5,
      "target": "committee",
      "source": "leave"
    },
    {
      "value": 1,
      "target": "week",
      "source": "leave"
    },
    {
      "value": 7,
      "target": "right",
      "source": "flee"
    },
    {
      "value": 7,
      "target": "plan",
      "source": "flee"
    },
    {
      "value": 13,
      "target": "message",
      "source": "flee"
    },
    {
      "value": 13,
      "target": "called",
      "source": "flee"
    },
    {
      "value": 1,
      "target": "government",
      "source": "flee"
    },
    {
      "value": 1,
      "target": "usk",
      "source": "country"
    },
    {
      "value": 5,
      "target": "persecution",
      "source": "country"
    },
    {
      "value": 5,
      "target": "health",
      "source": "country"
    },
    {
      "value": 5,
      "target": "criticism",
      "source": "country"
    },
    {
      "value": 13,
      "target": "week",
      "source": "country"
    },
    {
      "value": 5,
      "target": "barbed",
      "source": "right"
    },
    {
      "value": 13,
      "target": "health",
      "source": "right"
    }
  ]
}


def static_data(*args, **kwargs):
    return data
