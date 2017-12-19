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
#### Params: group_id(optional), text(mandatory)
#### Response: 
<pre>
{
  "status": true,
  "doc_id": 4,
  "tags": [
    [
      "Health",
      0.18280685666458096
    ],
    [
      "WASH",
      0.12295736560336878
    ],
    [
      "Nutrition",
      0.10664479716673503
    ],
    ...
  ]
}
