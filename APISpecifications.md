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
 - deeper(mandatory for deeper): to let api know that this is from DEEPER so that It will have entries in database(or we can populate our db for every api hits)
 - group_id(optional): this is for the purpose where different users are assigned with different projects
 - text(mandatory): text to be classified
 - doc_id(optional): send this to fetch classification details of already submitted lead(text). No need to send **text** field in this case. But
#### Sample Requests
 - curl -X POST -H 'Content-Type: application/x-www-form-urlencoded' http://deepl.togglecorp.com/api/v2/classify/ -d 'deeper=1&doc_id=18'
 - curl -X POST -H 'Content-Type: application/x-www-form-urlencoded' http://deepl.togglecorp.com/api/v2/classify/ -d 'deeper=1&text=deep inside'
#### Response: 
<pre>
{
  "group_id": null,
  "id": 18,
  "classification_confidence": 0.45,
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
      "classification_confidence": 0.45,
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
      "classification_confidence": 0.45,
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
</pre>
## [POST] /api/v{n}/recommendation/
#### Purpose: to recommend the correct class for a text
#### Content-Type: application/x-www-form-urlencoded
#### Params:
 - text: the text for which recommendation is being generated(can be whole lead or sentence)
 - classification_label: classified label by the classifier vn
 - useful: string value of 'true' or 'false' indicating the classification was useful or not
#### Sample Requests
 - curl -X POST -H 'Content-Type: application/x-www-form-urlencoded' http://deepl.togglecorp.com/api/v2/recommendation/ -d 'text=deep is awesome&classification_label=Health&useful=true'
 
## [GET] /api/subtopics/correlation/
#### Purpose: to get correlation among subtopics
#### Content-Type: application/x-www-form-urlencoded
#### Params: None


## [GET] /api/ner/
#### Purpose to get Named Entities from given text
#### Content-type: application/json
#### Params:
- text: The text from which named entities are to be extracted
#### Sample Request Body
<pre>
    {"text": "This is a text from which named entities are to be extracted"}
</pre>
#### Sample Response Body
<pre>
"locations": [
    {
      "info": {
        "place_id": "ChIJBylOcadSVjAREStiHOQOe7o",
        "cached": true,
        "geometry": {
          "bounds": {
            "southwest": {
              "lat": 9.4518,
              "lng": 92.171808
            },
            "northeast": {
              "lat": 28.5478351,
              "lng": 101.1702717
            }
          },
          "location": {
            "lat": 21.916221,
            "lng": 95.955974
          },
          "location_type": "APPROXIMATE",
          "viewport": {
            "southwest": {
              "lat": 9.4518,
              "lng": 92.171808
            },
            "northeast": {
              "lat": 28.5478351,
              "lng": 101.1702717
            }
          }
        },
        "formatted_address": "Myanmar (Burma)",
        "address_components": [
          {
            "short_name": "MM",
            "long_name": "Myanmar (Burma)",
            "types": [
              "country",
              "political"
            ]
          }
        ],
        "types": [
          "country",
          "political"
        ]
      },
      "name": "BURMA"
    },
    ]
}
</pre>


## [POST] /api/ner-docs/
#### Purpose: To get tagged named entities for list of doc_ids of docs which are already present in server
#### Content-Type: application/json
#### Params:
- doc_ids: the list of document ids
#### Sample Request Body
<pre>
{
    "doc_ids": [1,3,4,5]
}
</pre>
#### Sample Response Body
*Same as for /api/ner/*


## [POST] /api/keywords-extraction/
#### Purpose: To extract important keywords from given document
#### Params:
- document: to extract keywords from
- *max_grams*: max n-grams to extract from text, defaults to 3 if not provided
- *include_numbers*: (true|false) to include numeric values in result or not, defauls to false
#### Sample Request Body
<pre>
{
    "document": "This is a document whose keywords are for extraction",
    "max_grams": 2
}
</pre>
#### Sample Response Body
<pre>
{
    "1grams": ["one", "two", ...],
    "2grams": ["sample one", "sample two", "sample three", "sample four", ...],
}
</pre>


## [POST] /api/cluster/
#### Purpose: To initiate a clustering for given group_id
#### Params:
- group_id: cluster the docs belonging to the group_id
- num_clusters: number of clusters to cluster groups into
#### Sample Request Body
<pre>
{
    "group_id": 3,
    "num_clusters": 5
}
</pre>
#### Sample Response Body
Clustering is not real time. So, if clustering has begun or is still running, the response code will be 202
If complete, it will send 200 with following body:
<pre>
{
    "cluster_id": 1
}
</pre>


## [GET] /api/cluster/
#### Purpose: To get information about clusters formed from docs with certain group_id
#### Params:
- model_id:  cluster_id
#### Sample Request Body
<pre>
{
    "model_id": 1
}
</pre>
#### Sample Response Body
<pre>
{
    "score": "0.33",
    "doc_ids": [1,3,5,7],
    "group_id": 3,
    "relevant_terms": ["list", "of", "relevant", "terms", "for", "the", "cluster"]
}
</pre>


## [POST] /api/re-cluster/
#### Purpose: To invoke re clustering of documents in a group
#### Params:
- group_id: group_id of the documents
- num_clusters: number of clusters to recluster into
#### Sample Request Body
<pre>
{
    "group_id": 1,
    "num_clusters": 4
}
</pre>
#### Sample Response Body
<pre>
Clustering is not real time. So, if clustering has begun or is still running, the response code will be 202
If complete, it will send 200.
</pre>


## [GET] /api/cluster-data/
#### Purpose: To get cluster data
#### Params:
- group_id: Group id of the clusters to fetch data
#### Sampale Request Body
<pre>
{
    "group_id": 2
}
</pre>
#### Sample Response Body
<pre>
{
    "data": [
        {
            "value": "party",
            "cluster": 1,
            "score": 8
        },
        {
            "value": "incumbent",
            "cluster": 1,
            "score": 7
        },
        {
            "value": "summoned",
            "cluster": 2,
            "score": 10
        },
        {
            "value": "evidence",
            "cluster": 2,
            "score": 9
        },
        {
            "value": "mugabes",
            "cluster": 2,
            "score": 8
        },
        {
            "value": "official",
            "cluster": 2,
            "score": 7
        },
        {
            "value": "way",
            "cluster": 4,
            "score": 10
        },
        {
            "value": "chiredzi",
            "cluster": 4,
            "score": 9
        },
        {
            "value": "pave",
            "cluster": 4,
            "score": 8
        },
        {
            "value": "aid",
            "cluster": 6,
            "score": 9
        },
        {
            "value": "commission",
            "cluster": 6,
            "score": 8
        },
        {
            "value": "received",
            "cluster": 6,
            "score": 7
        }
    ]
}
</pre>


## [POST] /api/similardocs/
#### Purpose: To get similarity between docs
#### Params:
- group_id: group_id of docs to check the similarity
- *doc*: document for which similar docs are to be found
- *doc_id*: doc_id for which similar docs are to be found, either this or 'doc' should be present
#### Sample Request Body:
<pre>
{
    "doc_id": 1,
    "group_id": 1
}
</pre> or
{
    "doc": "This is a test doc",
    "group_id": 1
}
#### Sample Response Body:
Response will be list of doc_ids of similar docs 
<pre>
{
    "similar_docs": [1,2,3]
}
</pre>


## [PUT] /api/doc/
#### Purpose: to update a document(in fact, updating group_id of the doc)
#### Content-Type: application/json
#### Params:
- items: contains list of objects, each object containing:
    - doc_id: document id whose group_id is to be updated
    - group_id: updated group_id
#### Sample Request:
<pre>
{
    "items": [
        {"doc_id": 1, "group_id": "121"},
        {"doc_id": 2, "group_id": "122"},
    ]
}
</pre>
