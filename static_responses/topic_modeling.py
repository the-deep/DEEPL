import random

from topic_modeling.keywords_extraction import get_key_ngrams


data = {
  "Topic 0": {
    "keywords": [
      [
        "shelter",
        0.028301557465689207
      ],
      [
        "bamboo",
        0.028281110426793585
      ],
      [
        "esk",
        0.013130481753307112
      ],
      [
        "sector",
        0.010102894661625315
      ]
    ],
    "subtopics": {
      "Topic 0": {
        "keywords": [
          [
            "myanmar",
            0.038078355150122895
          ],
          [
            "rohingya",
            0.023012047710942053
          ],
          [
            "bangladesh",
            0.021757046391928773
          ],
          [
            "said",
            0.012964286223227851
          ]
        ],
        "subtopics": {
          "Topic 0": {
            "keywords": [
              [
                "rohingyas",
                0.016417569378282114
              ],
              [
                "bangladesh",
                0.012615218758114291
              ],
              [
                "rakhine",
                0.008839428701601655
              ],
              [
                "feel",
                0.008838835011852854
              ]
            ],
            "subtopics": {
              "Topic 0": {
                "keywords": [
                  [
                    "rohingya",
                    0.02233496044780371
                  ],
                  [
                    "myanmar",
                    0.02233219840536828
                  ],
                  [
                    "bangladesh",
                    0.017658126268498945
                  ],
                  [
                    "said",
                    0.012982073367171082
                  ]
                ],
                "subtopics": {
                  "Topic 0": {
                    "keywords": [
                      [
                        "myanmar",
                        0.035486451822063475
                      ],
                      [
                        "bangladesh",
                        0.02302842956097408
                      ],
                      [
                        "rohingya",
                        0.021899358860177586
                      ],
                      [
                        "refugee",
                        0.011704326221565297
                      ]
                    ],
                    "subtopics": {}
                  },
                  "Topic 1": {
                    "keywords": [
                      [
                        "shelter",
                        0.020751188549015226
                      ],
                      [
                        "bamboo",
                        0.02074003306893707
                      ],
                      [
                        "consultation",
                        0.01185143699276954
                      ],
                      [
                        "children",
                        0.011851434503695048
                      ]
                    ],
                    "subtopics": {}
                  },
                  "Topic 2": {
                    "keywords": [
                      [
                        "bazar",
                        0.0018733999932968022
                      ],
                      [
                        "cox",
                        0.0018733948481803706
                      ],
                      [
                        "host",
                        0.0018733880303648152
                      ],
                      [
                        "humanitarian",
                        0.0018733722628922645
                      ]
                    ],
                    "subtopics": {}
                  }
                }
              },
              "Topic 1": {
                "keywords": [
                  [
                    "myanmar",
                    0.02700499345530682
                  ],
                  [
                    "shelter",
                    0.015432719193853035
                  ],
                  [
                    "committee",
                    0.015427221915407373
                  ],
                  [
                    "bamboo",
                    0.015427199276847372
                  ]
                ],
                "subtopics": {}
              },
              "Topic 2": {
                "keywords": [
                  [
                    "rohingyas",
                    0.016414758215326314
                  ],
                  [
                    "bangladesh",
                    0.01261671121434878
                  ],
                  [
                    "rakhine",
                    0.008841713634820014
                  ],
                  [
                    "feel",
                    0.008838662081498559
                  ]
                ],
                "subtopics": {}
              }
            }
          },
          "Topic 1": {
            "keywords": [
              [
                "myanmar",
                0.03806856808173397
              ],
              [
                "rohingya",
                0.023012446185700704
              ],
              [
                "bangladesh",
                0.021751534231030382
              ],
              [
                "land",
                0.012964878103485285
              ]
            ],
            "subtopics": {}
          },
          "Topic 2": {
            "keywords": [
              [
                "shelter",
                0.020751652618668497
              ],
              [
                "bamboo",
                0.020740671382531037
              ],
              [
                "children",
                0.011851740052682662
              ],
              [
                "consultation",
                0.011851737659981912
              ]
            ],
            "subtopics": {}
          }
        }
      },
      "Topic 1": {
        "keywords": [
          [
            "children",
            0.01789604351887204
          ],
          [
            "consultation",
            0.017896038820866912
          ],
          [
            "child",
            0.014540525362428646
          ],
          [
            "experience",
            0.011185001181704674
          ]
        ],
        "subtopics": {}
      },
      "Topic 2": {
        "keywords": [
          [
            "shelter",
            0.024850115989366893
          ],
          [
            "bamboo",
            0.022439663563302372
          ],
          [
            "esk",
            0.010418378358666248
          ],
          [
            "rohingyas",
            0.010413992501983587
          ]
        ],
        "subtopics": {}
      }
    }
  },
  "Topic 1": {
    "keywords": [
      [
        "myanmar",
        0.03548682849635618
      ],
      [
        "bangladesh",
        0.02302865675894976
      ],
      [
        "rohingya",
        0.021901280394066944
      ],
      [
        "refugee",
        0.011705197279097622
      ]
    ],
    "subtopics": {}
  },
  "Topic 2": {
    "keywords": [
      [
        "children",
        0.017895507180749008
      ],
      [
        "consultation",
        0.01789550709329989
      ],
      [
        "child",
        0.014540085391904281
      ],
      [
        "experience",
        0.011184663204325524
      ]
    ],
    "subtopics": {}
  }
}


doc = """
Hosts feel the pressure, refugees ever grateful x Six months have passed since the latest influx from Myanmar’s Rakhine state started, but there has been no real headway in ending the ongoing Rohingya crisis. Nearly 700,000 Rohingyas managed to save their lives fleeing into Bangladesh after a military crackdown began in Rakhine on August 25 last year, leaving behind all their belongings and property. On humanitarian ground, Bangladesh allowed the Rohingyas to stay at the refugee camps set up in Cox’s Bazar’s Ukhiya and Teknaf upazilas, where several hundreds of thousands of Rohingyas were already living for many years. Although the process of providing shelter feels like somewhat of a burden to the locals and the government as the days have progressed, Rohingyas are always expressing their gratefulness to the people of Bangladesh and Prime Minister Sheikh Hasina
Rohingya flee no man's land after Myanmar threat Rohingya flee no man's land after Myanmar threat By Afp Published: 05:26 EST, 28 February 2018 | Updated: 07:11 EST, 28 February 2018 Around 6,000 Rohingya have been living on a thin stretch of land between the two countries since fleeing Myanmar Hundreds of Rohingya living in no man's land have left their makeshift camp and crossed into Bangladesh after soldiers from Myanmar used loudhailers to threaten them, community leaders said Wednesday. Around 6,000 Rohingya have been living on a thin strip of land between the two countries since fleeing Myanmar in the wake of a brutal military crackdown on the Muslim minority in late August. They were among the first to flee Myanmar when the violence erupted last year and set up shelters in no man's land in the weeks before Bangladesh agreed to let the Rohingya into the country. In recent weeks they have come under pressure from Myanmar soldiers, who have stepped up patrols along the barbed-wire border fence just yards from the camp and broadcast messages using loudhailers ordering the Rohingya to leave. Community leader Dil Mohammad said the messages had spread panic through the camp. "We can't now sleep peacefully. Most of the Rohingya in the camps now want to flee and take shelter in Bangladesh," Mohammad said. "Around 150 families have already left the camp for Bangladesh as they were afraid they might be forcefully sent back to Rakhine," he told AFP, referring to the area of Myanmar where the Rohingya used to live. - Threatened with prosecution - One Border Guard Bangladesh official said the Myanmar soldiers were playing the announcement at least 10 to 15 times a day. In it they urge the Rohingya to leave, saying the land they are on is under Myanmar's jurisdiction and threatening them with prosecution if they remain. Last week Bangladesh and Myanmar officials visited the camp and urged the refugees to return to Rakhine. But community leaders have said they will not go back unless their demands for citizenship and security guarantees are met. Myanmar views the Rohingya as illegal immigrants from Bangladesh and has long denied them citizenship and basic rights. Nearly 700,000 have fled since the military backed by Buddhist mobs launched a brutal crackdown in the wake of attacks by Rohingya militants on police posts. Doctors without Borders has said 6,700 Rohingya were killed in the first month of the violence alone, in a campaign the United Nations has called ethnic cleansing. Most of the refugees are now living in camps in Bangladesh. The Bangladesh government has signed an agreement with Myanmar to repatriate them, but the refugees themselves say they do not want to return. Bangladesh was supposed to start the repatriation process last month but it has been delayed amid concerns over a lack of preparation. Myanmar forces have also erected a kilometres-long barbed-wire fence along the border in recent weeks and installed multiple outposts with armed guards and loudspeakers, the refugees said. "Unfortunately we have no presence in the so-called no man's land. We know that refugees continue to arrive in Bangladesh on a daily basis and we are assisting all new arrivals regardless of where they came from," said Vivian Tan, spokeswoman for the UN refugee agency. "UNHCR maintains that those who have fled human rights violations, persecution and violence have the right to seek asylum and must be guaranteed safety and protection." Share or comment on this article Sorry we are not currently accepting comments on this article.
Rohingya crisis: Myanmar ‘bars entry’ for UK govt body after criticism The Myanmar authorities have allegedly blocked entry for a fact-finding committee of the British government following criticism by the UK MPs over Myanmar’s role in the Rohingya crisis. The Commons International Development Committee was due to hold a series of meetings with Myanmar’s senior military and civilian leaders including the country’s de facto leader Aung San Suu Kyi and scrutinise the British aid projects in Myanmar, reports The Telegraph . The committee had produced a report in January this year condemning the persecution on Rohingyas in Myanmar, highlighting the evidence of sexual violence on the Muslim minority carried out by the country’s military during a crackdown in late August last year, forcing nearly 700,000 people to flee to Bangladesh. The Myanmar embassy has reportedly failed to provide visas for the members of the committee’s fact-finding body, a move which the committee accused as linked to their report on the Rohingya crisis. Expressing extreme disappointment, the Committee Chair and Labour MP Stephen Twigg said that it was hard to escape the conclusion that this was a direct consequence of the committee’s report on the Rohingyas, reports The Telegraph . The refusal to allow entry to the committee has also hampered its job of overseeing the projects in Myanmar funded by a £100 million Department for International Development (DFID) aid programme for 2018-19, Twigg also said. The UK MPs were due to visit the health and education projects in Myanmar’s Rakhine state and Magway region. Earlier in January, the committee expressed “grave concern” about the plans to repatriate the Rohingya refugees in Bangladesh, terming the crisis a “huge human tragedy” caused by Myanmar’s actions. The UK MPs had warned against any repatriation plan for the Rohingyas without guarantees of protection, and called for voluntary return of the refugees. The governments of Bangladesh and Myanmar had earlier drawn up an agreement to begin repatriation of the Rohingya refugees from late January. The repatriation process, however, has been postponed for logistical reasons, reports The Telegraph . The Rohingyas in the refugee camps in Bangladesh were reportedly traumatised by fears of forced return to Myanmar, with their community leaders demanding the Myanmar authorities first guarantee the Rohingyas of their long-denied citizenship and include them in the country’s list of recognised ethnic groups. On Wednesday, February 28, 2018, hundreds of Rohingyas living in the no man’s land between Bangladesh and Myanmar abruptly fled into Bangladesh, claiming that Myanmar soldiers had threatened them to leave. The incident took place after the Myanmar soldiers beefed up patrols along the barbed wire border fence, increasing pressure and causing panic among the around 6,000 people living on the thin strip of land between the two countries, reports The Telegraph .
The initial stage (called phase 1) of the Rohingya crises involved rapid, mass displacement of populations , during which shelter needs focused on access to adequate shelter for survival and dignity. Various humanitarian actors provided emergency shelter kits (ESK) for essential security and personal safety, protection from the climate and enhanced resistance to disease and ill health . ESK developed by the shelter sector included tarps , rope and bamboo. However, in the initial response, most agencies provided an acute version of these items , which excluded bamboo. In most cases , the refugee families procured some bamboo themselves , or foraged for sticks and timber in the surrounding forest to construct rudimentary makeshift shelters .
Given that shelters had already been constructed but were far below standards in terms of living conditions and structural integrity, rather than using bamboo in the emergency kits the sector developed and promoted the shelter upgrade kit (USK), or phase 2. This kit consists of tarps, bamboo, fixings, tools and
technical assistance with the aim of improving living conditions (with site improvements contributing to the effort) and shelter structural stability to better withstand climatic conditions. Because of the scale of the crisis and the urgency to respond before the monsoon season, the Shelter and NFI Sector decided in November to reorient whatever was already in the pipeline for ESK , toward the USK . The ESK had included four bamboo Borak and 55 Bamboo Mulli, whereas the USK includes four bamboo Borak and 60 bamboo Mulli per household.
Children’s experiences in Cox’s Bazar and the specific vulnerabilities they face are distinct from adults. To better understand children’s needs, their challenges and day-to-day experiences in the settlements and host communities, hearing from children themselves is critical. Therefore, SCI, Plan International and WVI undertook a children’s consultation with children from Rohingya refugee communities and host communities in Cox’s Bazar between the 2nd and 6th of December 2017. This exercise builds on experiences from after Typhoon Haiyan in the Philippines, the Earthquake in Nepal and the Ebola outbreak in Sierra Leone. What children have shared with the consultation teams about their needs, hopes and desires will be used to design and improve our interventions and will feed into the Humanitarian Response Plan (HRP).
The Children’s Consultation exercise collected a wealth of information however, due to time required for data encoding following the consultations there were significant limitations for detailed analysis. Therefore, main findings have been organised by sector allowing readers to easily navigate and influence their HRP contributions. It should be noted that this Children’s Consultation is not a sectoral needs assessment in itself but rather a collation of issues affecting children and their own perceptions of what is important to them based on what they believe to be their current reality.
"""


def get_levels(topics, keywords, depth, words):
    if depth == 0:
        return {}
    level = {}
    for x in range(topics):
        level['Topic {}'.format(x)] = {
            'keywords': [random.choice(words) for _ in range(keywords)],
            'subtopics': get_levels(topics, keywords, depth-1, words) \
                if random.random() > 0.7/(0.25*depth) else {}
        }
    return level


def get_random_data(topics=3, keywords=3, depth=5):
    # generate static data
    grams = get_key_ngrams(doc, max_grams=1)['1grams']
    grams = grams[:50]
    return get_levels(topics, keywords, depth, grams)


def static_data(*args, **kwargs):
    return get_random_data(4, 4, 5)
