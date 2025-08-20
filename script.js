// Inline dataset (all 10 talking points)
const data = [
  {
    "talking_point_id": "immutable-binary",
    "claim": "“Biological sex is a simple, immutable XX/XY binary; transgender identity denies scientific reality.”",
    "category": "Biology/Medicine & Endocrinology",
    "debunk": {
      "summary": "Sex is multi-dimensional (chromosomes, gonads, hormones, anatomy). Intersex variations and medical consensus show biology is not a strict binary and sex is distinct from gender identity.",
      "evidence_badge": "High",
      "key_facts": [
        "Sex traits span multiple axes; XX/XY are common, not universal.",
        "Intersex variations exist and are part of normal human diversity.",
        "Gender identity is distinct from sex traits and is a core aspect of personhood."
      ],
      "sources": [
        {"type":"consensus","title":"WHO: Gender definitions","url":"https://www.who.int/health-topics/gender"},
        {"type":"consensus","title":"NASEM: Measuring Sex & Gender Identity","url":"https://www.ncbi.nlm.nih.gov/books/NBK581050/"},
        {"type":"expert-consensus","title":"Endocrine Society statement","url":"https://reports.mountsinai.org/article/endo2023-_9_transgender"}
      ],
      "limitations": ["Terminology and prevalence estimates for intersex traits vary across studies."]
    }
  },
  {
    "talking_point_id": "bathroom-predator",
    "claim": "“Trans-inclusive bathrooms endanger women; predators will exploit access.”",
    "category": "Bathrooms/Safety/Crime",
    "debunk": {
      "summary": "Large-scale analyses show no increase in assaults or privacy violations with inclusive policies; trans people face elevated harassment and health harms when access is restricted.",
      "evidence_badge": "High",
      "key_facts": [
        "No empirical link between inclusive policies and increased restroom crime.",
        "Trans people report high rates of harassment and avoidance of facilities.",
        "Avoidance leads to medical issues (e.g., UTIs, dehydration)."
      ],
      "sources": [
        {"type":"peer_reviewed","title":"Williams Institute: Crime data","url":"https://williamsinstitute.law.ucla.edu/"},
        {"type":"report","title":"GLAAD Fact Sheet on Restrooms","url":"https://glaad.org/fact-sheet-misleading-narratives-about-transgender-people-and-restrooms-locker-rooms-and-other-single-sex-spaces/"},
        {"type":"survey","title":"U.S. Transgender Survey (2015)","url":"https://transequality.org/issues/us-trans-survey"}
      ],
      "limitations": ["Some datasets are observational; continued monitoring is advised."]
    }
  },
  {
    "talking_point_id": "sports-advantage",
    "claim": "“Trans women have an insurmountable athletic advantage; women’s sports are threatened.”",
    "category": "Sports/Fairness",
    "debunk": {
      "summary": "Gender-affirming hormone therapy reduces performance metrics; dominance in sports is not observed. Best practice is sport-specific evidence-based policies, not blanket bans.",
      "evidence_badge": "High",
      "key_facts": [
        "After ~2 years of GAHT, strength differences largely diminish.",
        "Trans athletes are extremely rare and show no pattern of dominance.",
        "IOC framework advises no presumption of advantage."
      ],
      "sources": [
        {"type":"systematic_review","title":"Sports Medicine Review (2017)","url":"https://link.springer.com/journal/40279"},
        {"type":"peer_reviewed","title":"BJSM Study on Fitness in Trans Service Members","url":"https://bjsm.bmj.com/"},
        {"type":"policy","title":"IOC 2021 Framework","url":"https://olympics.com/ioc"}
      ],
      "limitations": ["More longitudinal sport-specific data is needed."]
    }
  },
  {
    "talking_point_id": "groomer-libel",
    "claim": "“Affirming or educating about gender identity is ‘grooming’ of children.”",
    "category": "Religion/Morality/Culture",
    "debunk": {
      "summary": "This is a defamatory moral panic; no evidence links LGBTQ+ visibility to abuse. ‘Groomer’ is recognized as a slur that incites harassment.",
      "evidence_badge": "High",
      "key_facts": [
        "No evidence LGBTQ+ inclusion is linked to grooming.",
        "Use of this slur correlates with harassment and threats.",
        "Youth mental health is harmed by this stigma."
      ],
      "sources": [
        {"type":"report","title":"Institute for Strategic Dialogue Report","url":"https://www.isdglobal.org/"},
        {"type":"policy","title":"Platform policy bans on ‘groomer’ slur","url":"https://transparency.fb.com/"},
        {"type":"education","title":"GLAAD Safety Myths","url":"https://glaad.org/"}
      ],
      "limitations": ["Evidence mainly from monitoring reports, not RCTs."]
    }
  },
  {
    "talking_point_id": "social-contagion-rogd",
    "claim": "“A surge of trans youth is ‘rapid onset’ due to social contagion (ROGD).”",
    "category": "Social Contagion/ROGD",
    "debunk": {
      "summary": "ROGD is not recognized; the original study was methodologically flawed. Increased visibility and acceptance better explain disclosure.",
      "evidence_badge": "High",
      "key_facts": [
        "ROGD is absent from DSM-5 and ICD-11.",
        "The original study surveyed only parents from anti-trans forums.",
        "Greater visibility drives safe disclosure."
      ],
      "sources": [
        {"type":"consensus","title":"WPATH SOC-8 FAQs","url":"https://wpath.org/publications/soc8/"},
        {"type":"peer_reviewed","title":"Critiques of ROGD paper","url":"https://link.springer.com/"},
        {"type":"consensus","title":"CAAPS coalition statement","url":"https://www.psychologicalscience.org/"}
      ],
      "limitations": ["Surveys subject to recall bias."]
    }
  },
  {
    "talking_point_id": "gender-ideology-conspiracy",
    "claim": "“Gender ideology is being pushed to capture institutions and indoctrinate children.”",
    "category": "Free Speech/Institutions",
    "debunk": {
      "summary": "Medical and human-rights standards are based on evidence, not conspiracy. Multiple independent bodies affirm gender distinctions.",
      "evidence_badge": "Medium",
      "key_facts": [
        "Consensus comes from independent bodies across disciplines.",
        "Standards like WPATH SOC-8 are evidence-based, peer-reviewed."
      ],
      "sources": [
        {"type":"consensus","title":"WHO Gender Definitions","url":"https://www.who.int/health-topics/gender"},
        {"type":"consensus","title":"NASEM Report on Sex/Gender Measures","url":"https://www.ncbi.nlm.nih.gov/books/NBK581050/"},
        {"type":"standards","title":"WPATH SOC-8","url":"https://wpath.org/publications/soc8/"}
      ],
      "limitations": ["Public often confuses academic terms with activism."]
    }
  },
  {
    "talking_point_id": "conflict-of-rights",
    "claim": "“Trans rights conflict with women’s and children’s rights.”",
    "category": "Rights/Law/Policy",
    "debunk": {
      "summary": "Civil rights frameworks protect everyone. Inclusive policies uphold safety and dignity without increasing violence.",
      "evidence_badge": "Medium",
      "key_facts": [
        "No evidence inclusive policies increase risk to women/children.",
        "Rights frameworks balance competing needs neutrally."
      ],
      "sources": [
        {"type":"law","title":"EEOC Guidance on Sex Discrimination","url":"https://www.eeoc.gov/youth/sex-discrimination"},
        {"type":"peer_reviewed","title":"Williams Institute Policy Analyses","url":"https://williamsinstitute.law.ucla.edu/"},
        {"type":"report","title":"GLAAD Restroom Safety Fact Sheet","url":"https://glaad.org/fact-sheet-misleading-narratives-about-transgender-people-and-restrooms-locker-rooms-and-other-single-sex-spaces/"}
      ],
      "limitations": ["Implementation quality varies."]
    }
  },
  {
    "talking_point_id": "detransition-and-regret",
    "claim": "“Most people regret transition; detransition proves care is harmful.”",
    "category": "Youth Care/Detransition",
    "debunk": {
      "summary": "Published regret rates are very low; detransition often results from stigma or barriers, not rejection of identity.",
      "evidence_badge": "High",
      "key_facts": [
        "Regret rates are lower than many elective surgeries.",
        "Detransition reasons include social/family pressure, not identity change.",
        "Assessment and follow-up are standard of care."
      ],
      "sources": [
        {"type":"peer_reviewed","title":"Cohort Studies on Transition Outcomes","url":"https://pubmed.ncbi.nlm.nih.gov/"},
        {"type":"standards","title":"WPATH SOC-8","url":"https://wpath.org/publications/soc8/"},
        {"type":"consensus","title":"Endocrine Society Guidelines","url":"https://www.endocrine.org/clinical-practice-guidelines"}
      ],
      "limitations": ["More long-term follow-up data needed."]
    }
  },
  {
    "talking_point_id": "child-abuse-framing",
    "claim": "“Youth gender-affirming care is child abuse.”",
    "category": "Education/Schools/Curriculum",
    "debunk": {
      "summary": "Major medical associations recognize youth care as evidence-based and often life-saving. Puberty blockers are reversible; surgeries on minors are rare.",
      "evidence_badge": "High",
      "key_facts": [
        "Puberty blockers are reversible and allow time for decisions.",
        "Care access lowers suicide risk and distress.",
        "Multidisciplinary assessment precedes interventions."
      ],
      "sources": [
        {"type":"standards","title":"WPATH SOC-8 (Youth Care)","url":"https://wpath.org/publications/soc8/"},
        {"type":"consensus","title":"AAP/AMA Statements","url":"https://www.aap.org/"},
        {"type":"clinical","title":"Johns Hopkins Adolescent Guide","url":"https://www.hopkinsmedicine.org/-/media/center-for-transgender-health/documents/adolescentvisitguide41224.pdf"}
      ],
      "limitations": ["RCTs not feasible; evidence is observational/longitudinal."]
    }
  },
  {
    "talking_point_id": "delusion-compelled-speech",
    "claim": "“Being trans is a delusion; pronoun use is compelled speech.”",
    "category": "Free Speech/Institutions",
    "debunk": {
      "summary": "Trans identity is not classified as a disorder in ICD-11/DSM-5. Correct pronoun use is correlated with improved well-being; laws balance speech with anti-harassment.",
      "evidence_badge": "High",
      "key_facts": [
        "ICD-11 and DSM-5 do not classify being trans as a disorder.",
        "Affirming pronouns/names improve mental health outcomes.",
        "Workplace/school policies limit harassment, not free expression."
      ],
      "sources": [
        {"type":"consensus","title":"WHO ICD-11 Classification","url":"https://icd.who.int/"},
        {"type":"consensus","title":"APA DSM-5 Gender Dysphoria","url":"https://www.psychiatry.org/"},
        {"type":"law","title":"EEOC Harassment Guidance","url":"https://www.eeoc.gov/"}
      ],
      "limitations": ["Legal standards vary by country."]
    }
  }
];

// Helpers
function badgeClass(level){
  return level==='High'?'badge--high':level==='Medium'?'badge--medium':'badge--moderate';
}
function renderCards(items){
  const container = document.getElementById('cards');
  container.innerHTML = '';
  items.forEach(item=>{
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <h3>${item.claim}</h3>
      <div class="card__meta">
        <span class="badge ${badgeClass(item.debunk.evidence_badge)}">${item.debunk.evidence_badge}</span>
        <span>${item.category}</span>
      </div>
      <p>${item.debunk.summary}</p>
      <strong>Key facts:</strong>
      <ul>${item.debunk.key_facts.map(f=>`<li>${f}</li>`).join('')}</ul>
      <strong>Sources:</strong>
      <ul class="sources">
        ${item.debunk.sources.map(s=>`<li><a href="${s.url}" target="_blank">${s.title}</a> <em>(${s.type})</em></li>`).join('')}
      </ul>
      ${item.debunk.limitations?.length ? `<strong>Limitations:</strong><ul>${item.debunk.limitations.map(l=>`<li>${l}</li>`).join('')}</ul>` : ''}
    `;
    container.appendChild(card);
  });
}
document.addEventListener("DOMContentLoaded", ()=>{
  renderCards(data);
  document.getElementById('last-updated').textContent =
    new Date().toISOString().slice(0,10);
});
