import random


data = {
    "Nutrition": {
        "Nutrition": 1.0008370000000204,
        "Shelter": 0.905474999999998,
        "Agriculture": 0.9341449999999994,
        "Cross": 0.7454839999999971,
        "Protection": 0.9209870000000043,
        "WASH": 0.8539259999999956,
        "Livelihood": 0.43460999999999966,
        "NFI": 0.5333959999999964,
        "Logistic": 0.4687599999999992,
        "Health": 0.9242680000000012,
        "Food": 0.886449000000001,
        "Education": 0.6365589999999974
    },
    "Shelter": {
        "Nutrition": 0.905474999999998,
        "Shelter": 0.9994730000000077,
        "Agriculture": 0.9490029999999998,
        "Cross": 0.7724389999999901,
        "Protection": 0.9402180000000032,
        "WASH": 0.8699570000000011,
        "Livelihood": 0.4414299999999979,
        "NFI": 0.5428880000000016,
        "Logistic": 0.4812079999999972,
        "Health": 0.9379960000000018,
        "Food": 0.8981600000000024,
        "Education": 0.5673729999999955
    },
    "Agriculture": {
        "Nutrition": 0.9341449999999994,
        "Shelter": 0.9490029999999998,
        "Agriculture": 0.999431999999987,
        "Cross": 0.7916569999999952,
        "Protection": 0.982831000000002,
        "WASH": 0.895221,
        "Livelihood": 0.4426100000000016,
        "NFI": 0.5462449999999931,
        "Logistic": 0.48740799999999884,
        "Health": 0.987227000000001,
        "Food": 0.932070000000001,
        "Education": 0.5811430000000034
    },
    "Cross": {
        "Nutrition": 0.7454839999999971,
        "Shelter": 0.7724389999999901,
        "Agriculture": 0.7916569999999952,
        "Cross": 1.0003329999999693,
        "Protection": 0.8175969999999949,
        "WASH": 0.7438340000000009,
        "Livelihood": 0.6248020000000034,
        "NFI": 0.6566220000000005,
        "Logistic": 0.6398550000000033,
        "Health": 0.7698199999999953,
        "Food": 0.7892150000000004,
        "Education": 0.5292650000000015
    },
    "Protection": {
        "Nutrition": 0.9209870000000043,
        "Shelter": 0.9402180000000032,
        "Agriculture": 0.982831000000002,
        "Cross": 0.8175969999999949,
        "Protection": 0.9996800000000094,
        "WASH": 0.8922899999999998,
        "Livelihood": 0.4966969999999986,
        "NFI": 0.5876319999999972,
        "Logistic": 0.5497519999999985,
        "Health": 0.9774880000000019,
        "Food": 0.9333610000000016,
        "Education": 0.5699859999999977
    },
    "WASH": {
        "Nutrition": 0.8539259999999956,
        "Shelter": 0.8699570000000011,
        "Agriculture": 0.895221,
        "Cross": 0.7438340000000009,
        "Protection": 0.8922899999999998,
        "WASH": 1.0010679999999794,
        "Livelihood": 0.4532909999999989,
        "NFI": 0.5620329999999968,
        "Logistic": 0.47405200000000136,
        "Health": 0.8703369999999973,
        "Food": 0.8544560000000013,
        "Education": 0.5983339999999877
    },
    "Livelihood": {
        "Nutrition": 0.43460999999999966,
        "Shelter": 0.4414299999999979,
        "Agriculture": 0.4426100000000016,
        "Cross": 0.6248020000000034,
        "Protection": 0.4966969999999986,
        "WASH": 0.4532909999999989,
        "Livelihood": 1.0001949999999944,
        "NFI": 0.6084770000000009,
        "Logistic": 0.6244570000000017,
        "Health": 0.4114660000000014,
        "Food": 0.49295500000000037,
        "Education": 0.3886990000000008
    },
    "NFI": {
        "Nutrition": 0.5333959999999964,
        "Shelter": 0.5428880000000016,
        "Agriculture": 0.5462449999999931,
        "Cross": 0.6566220000000005,
        "Protection": 0.5876319999999972,
        "WASH": 0.5620329999999968,
        "Livelihood": 0.6084770000000009,
        "NFI": 1.0003600000000197,
        "Logistic": 0.5582769999999991,
        "Health": 0.514612,
        "Food": 0.5655640000000023,
        "Education": 0.4399610000000052
    },
    "Logistic": {
        "Nutrition": 0.4687599999999992,
        "Shelter": 0.4812079999999972,
        "Agriculture": 0.48740799999999884,
        "Cross": 0.6398550000000033,
        "Protection": 0.5497519999999985,
        "WASH": 0.47405200000000136,
        "Livelihood": 0.6244570000000017,
        "NFI": 0.5582769999999991,
        "Logistic": 0.999866999999993,
        "Health": 0.4583250000000021,
        "Food": 0.5263940000000014,
        "Education": 0.3781250000000019
    },
    "Health": {
        "Nutrition": 0.9242680000000012,
        "Shelter": 0.9379960000000018,
        "Agriculture": 0.987227000000001,
        "Cross": 0.7698199999999953,
        "Protection": 0.9774880000000019,
        "WASH": 0.8703369999999973,
        "Livelihood": 0.4114660000000014,
        "NFI": 0.514612,
        "Logistic": 0.4583250000000021,
        "Health": 0.999719000000006,
        "Food": 0.9218659999999965,
        "Education": 0.5325559999999939
    },
    "Food": {
        "Nutrition": 0.886449000000001,
        "Shelter": 0.8981600000000024,
        "Agriculture": 0.932070000000001,
        "Cross": 0.7892150000000004,
        "Protection": 0.9333610000000016,
        "WASH": 0.8544560000000013,
        "Livelihood": 0.49295500000000037,
        "NFI": 0.5655640000000023,
        "Logistic": 0.5263940000000014,
        "Health": 0.9218659999999965,
        "Food": 1.0004870000000337,
        "Education": 0.5624359999999918
    },
    "Education": {
        "Nutrition": 0.6365589999999974,
        "Shelter": 0.5673729999999955,
        "Agriculture": 0.5811430000000034,
        "Cross": 0.5292650000000015,
        "Protection": 0.5699859999999977,
        "WASH": 0.5983339999999877,
        "Livelihood": 0.3886990000000008,
        "NFI": 0.4399610000000052,
        "Logistic": 0.3781250000000019,
        "Health": 0.5325559999999939,
        "Food": 0.5624359999999918,
        "Education": 1.0002829999999854
    }
}

keywords_data = {'edges': [{'source': 'rohingya', 'target': 'crisis', 'value': 11},
  {'source': 'rohingya', 'target': 'esk', 'value': 13},
  {'source': 'rohingya', 'target': 'bangladesh', 'value': 1},
  {'source': 'rohingya', 'target': 'called', 'value': 7},
  {'source': 'rohingya', 'target': 'government', 'value': 5},
  {'source': 'said', 'target': 'leave', 'value': 1},
  {'source': 'said', 'target': 'bamboo', 'value': 1},
  {'source': 'said', 'target': 'myanmar', 'value': 13},
  {'source': 'people', 'target': 'shelter', 'value': 1},
  {'source': 'people', 'target': 'flee', 'value': 13},
  {'source': 'people', 'target': 'usk', 'value': 11},
  {'source': 'people', 'target': 'plan', 'value': 7},
  {'source': 'people', 'target': 'week', 'value': 1},
  {'source': 'border', 'target': 'shelter', 'value': 13},
  {'source': 'border', 'target': 'leave', 'value': 11},
  {'source': 'border', 'target': 'health', 'value': 11},
  {'source': 'border', 'target': 'week', 'value': 7},
  {'source': 'esk', 'target': 'shelter', 'value': 5},
  {'source': 'esk', 'target': 'persecution', 'value': 1},
  {'source': 'esk', 'target': 'message', 'value': 1},
  {'source': 'esk', 'target': 'government', 'value': 11},
  {'source': 'shelter', 'target': 'bamboo', 'value': 11},
  {'source': 'shelter', 'target': 'country', 'value': 7},
  {'source': 'shelter', 'target': 'plan', 'value': 1},
  {'source': 'shelter', 'target': 'live', 'value': 11},
  {'source': 'shelter', 'target': 'week', 'value': 13},
  {'source': 'leave', 'target': 'flee', 'value': 1},
  {'source': 'leave', 'target': 'bamboo', 'value': 11},
  {'source': 'leave', 'target': 'right', 'value': 1},
  {'source': 'leave', 'target': 'committee', 'value': 5},
  {'source': 'leave', 'target': 'week', 'value': 1},
  {'source': 'flee', 'target': 'right', 'value': 7},
  {'source': 'flee', 'target': 'plan', 'value': 7},
  {'source': 'flee', 'target': 'message', 'value': 13},
  {'source': 'flee', 'target': 'called', 'value': 13},
  {'source': 'flee', 'target': 'government', 'value': 1},
  {'source': 'country', 'target': 'usk', 'value': 1},
  {'source': 'country', 'target': 'persecution', 'value': 5},
  {'source': 'country', 'target': 'health', 'value': 5},
  {'source': 'country', 'target': 'criticism', 'value': 5},
  {'source': 'country', 'target': 'week', 'value': 13},
  {'source': 'right', 'target': 'barbed', 'value': 5},
  {'source': 'right', 'target': 'health', 'value': 13},
  {'source': 'right', 'target': 'criticism', 'value': 7},
  {'source': 'right', 'target': 'government', 'value': 7},
  {'source': 'plan', 'target': 'message', 'value': 1},
  {'source': 'plan', 'target': 'rohingyas', 'value': 7},
  {'source': 'plan', 'target': 'committee', 'value': 11},
  {'source': 'plan', 'target': 'process', 'value': 1},
  {'source': 'persecution', 'target': 'called', 'value': 7},
  {'source': 'persecution', 'target': 'barbed', 'value': 1},
  {'source': 'persecution', 'target': 'government', 'value': 13},
  {'source': 'myanmar', 'target': 'message', 'value': 13},
  {'source': 'message', 'target': 'called', 'value': 1},
  {'source': 'message', 'target': 'committee', 'value': 13},
  {'source': 'message', 'target': 'criticism', 'value': 11},
  {'source': 'called', 'target': 'committee', 'value': 11},
  {'source': 'called', 'target': 'live', 'value': 1},
  {'source': 'called', 'target': 'week', 'value': 13},
  {'source': 'rohingyas', 'target': 'committee', 'value': 7},
  {'source': 'rohingyas', 'target': 'refugee', 'value': 13},
  {'source': 'rohingyas', 'target': 'government', 'value': 7},
  {'source': 'committee', 'target': 'live', 'value': 5},
  {'source': 'live', 'target': 'week', 'value': 11}],
 'nodes': [{'group': 9, 'id': 'rohingya'},
  {'group': 11, 'id': 'pressure'},
  {'group': 2, 'id': 'crisis'},
  {'group': 6, 'id': 'said'},
  {'group': 0, 'id': 'people'},
  {'group': 10, 'id': 'border'},
  {'group': 11, 'id': 'esk'},
  {'group': 4, 'id': 'shelter'},
  {'group': 0, 'id': 'leave'},
  {'group': 9, 'id': 'flee'},
  {'group': 4, 'id': 'bamboo'},
  {'group': 8, 'id': 'country'},
  {'group': 5, 'id': 'usk'},
  {'group': 3, 'id': 'right'},
  {'group': 2, 'id': 'bangladesh'},
  {'group': 3, 'id': 'plan'},
  {'group': 3, 'id': 'persecution'},
  {'group': 11, 'id': 'myanmar'},
  {'group': 4, 'id': 'message'},
  {'group': 2, 'id': 'called'},
  {'group': 6, 'id': 'barbed'},
  {'group': 1, 'id': 'rohingyas'},
  {'group': 4, 'id': 'committee'},
  {'group': 7, 'id': 'refugee'},
  {'group': 11, 'id': 'process'},
  {'group': 10, 'id': 'live'},
  {'group': 1, 'id': 'health'},
  {'group': 8, 'id': 'criticism'},
  {'group': 10, 'id': 'week'},
  {'group': 3, 'id': 'government'}]
}

def keywords_correlation(*args, **kwargs):
    from topic_modeling.keywords_extraction import get_key_ngrams
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
    # generate static data
    groups  = [x for x in range(12)]
    grams = get_key_ngrams(doc, max_grams=1)['1grams']
    grams = grams[:30]
    data = {}
    data['nodes'] = [
        {'id': x[0], 'group': random.choice(groups)}
        for x in grams
    ]
    # now create edges
    data['edges'] = []
    for i, x in enumerate(grams):
        if random.random() < 0.3:
            continue
        for j in range(i+1, len(grams)):
            value = random.randrange(0, 15)
            # just don't create edges for everything
            if value % 2 != 0 and value % 3 != 0:
                data['edges'].append(
                    {'source': x[0], 'target': grams[j][0], 'value': value}
                )
    return data

def subtopic_correlation(*args, **kwargs):
    subtopics =  [
        "Nutrition", "Shelter", "Agriculture", "Cross", "Protection",
        "WASH", "Livelihood", "NFI", "Logistic", "Health", "Food", "Education",
    ]
    data = {x: {} for x in subtopics}
    for i, k in enumerate(subtopics):
        for j, l in enumerate(subtopics):
            val = random.random()
            if j < i:
                data[k][l] = data[l][k]
            elif j > i:
                data[k][l] = val
            else:
                data[k][l] = 1.0
    return data


def static_data(*args, **kwargs):
    if kwargs['entity'] == 'subtopics':
        if kwargs.get('filter'):
            return subtopic_correlation()
        else:
            return data  # TODO: think of something
    elif kwargs['entity'] == 'keywords':
        if kwargs.get('filter'):
            print('FILTER')
            return keywords_correlation()
        return keywords_data
    else:
        return {}
