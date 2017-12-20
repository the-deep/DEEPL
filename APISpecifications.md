## [GET] /api/versions
#### Purpose: To get the available classifier versions
#### Params: None
#### Response:
<pre>
{
  "versions": [
    {
      "version": "1",
      "accuracy": 60.0
    },
    {
      "version": "2",
      "accuracy": 70.0
    }
  ]
}
</pre>


## [POST] /api/v{n}/classify/
#### Purpose: classification of (lead) text.
#### Content-Type: application/x-www-form-urlencoded
#### Params:
 - group_id(optional): this is for the purpose where different users are assigned with different projects
 - text(mandatory): text to be classified
 - doc_id(optional): send this to fetch classification details of already submitted lead(text). No need to send **text** field in this case.
#### Response: 
<pre>
{
  "group_id": null,
  "id": 18,
  "classification": [
    [
      "WASH",
      0.28137738948930135
    ],
    [
      "Logistic",
      0.2720483295850061
    ],
    [
      "Health",
      0.13988154392055305
    ],
    [
      "Protection",
      0.131329692235918
    ]
  ],
  "excerpts_classification": [
    {
      "start_pos": 0,
      "end_pos": 95,
      "classification": [
        [
          "WASH",
          0.28137738948930135
        ],
        [
          "Logistic",
          0.2720483295850061
        ],
        [
          "Health",
          0.13988154392055305
        ]
    },
    {
      "start_pos": 96,
      "end_pos": 265,
      "classification": [
        [
          "Nutrition",
          0.437922567103639
        ],
        [
          "Cross",
          0.22420366185035998
        ],
        [
          "Protection",
          0.06951939510798563
        ],
        [
          "Health",
          0.056812508106154465
        ]
      ]
    }
  ]
}
