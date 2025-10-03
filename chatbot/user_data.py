# DUMMY_USER_DATA = {
#     "name": "Sarah Johnson",
#     "gender": "Female",
#     "birth_country": "United States",
#     "cultural_background": [
#         "American",
#         "first-generation college student",
#         "rural upbringing",
#         "STEM-focused",
#         "environmental advocate",
#     ],
#     "academic": {
#         "gpa": "3.95",
#         "school_type": "Public High School",
#         "test_scores": {"SAT": "1450", "ACT": "32"},
#     },
#     "activities": [
#         {
#             "position": "President",
#             "category": "Academic",
#             "description": "Led environmental science club, organized community clean-up events, coordinated with local government on sustainability initiatives",
#         },
#         {
#             "position": "Team Captain",
#             "category": "Athletics",
#             "description": "Varsity soccer team captain, led team to state championship, organized team community service projects",
#         },
#         {
#             "position": "Volunteer",
#             "category": "Community Service",
#             "description": "Tutored underprivileged students in math and science, developed curriculum for after-school program",
#         },
#         {
#             "position": "Research Assistant",
#             "category": "Research",
#             "description": "Assisted professor in environmental impact study, analyzed data on renewable energy adoption in rural communities",
#         },
#     ],
#     "future_plans": [
#         "Study environmental engineering",
#         "Work on renewable energy solutions",
#         "Masters degree",
#         "Start a non-profit focused on rural sustainability",
#     ],
# }


DUMMY_USER_DATA = {
    "student_profile": {
        "name": "Ali Khan",
        "sex": "Male",
        "gender": "Male",
        "birth_country": "Pakistan",
        "cultural_background": ["South Asian", "first-generation college student"],
        "languages": [{"English": ["Speak", "Read", "Write"]}, {"Urdu": ["Speak", "Read", "Write", "Spoken at Home"]}],
        "socioeconomic_indicators": [],
        "geographic_context": {
            "birth_place": "Lahore, Pakistan",
            "citizenship_status": "Citizen of non-U.S. country",
            "citizenship": "Pakistan",
            "current_address": "House #12, Garden Town, Lahore, Pakistan",
        },
    },
    "academic_profile": {
        "schools": [
            {
                "name": "City Grammar School, Lahore",
                "type": "Private High School",
                "grades_attended": "9-12",
                "gpa_weighting": "Unweighted",
                "gpa_scale": "4.0",
                "gpa": 3.9,
                "rank_weighting": "Unweighted",
                "rank": "5/200",
                "recent_courses_taken": [
                    {"subject": "Mathematics", "type": "A-Level", "leaving_exam": "Predicted A*", "grade": "12"},
                    {"subject": "Physics", "type": "A-Level", "leaving_exam": "Predicted A", "grade": "12"},
                ],
            }
        ],
        "graduation_date": "06/2025",
        "gap_year": None,
        "Honors": [
            {
                "Title": "Best Science Student Award",
                "type": "School",
                "grade": [11, 12],
                "keywords": ["Academic Excellence", "STEM"],
            }
        ],
        "future_plans": ["Engineer", "Researcher"],
    },
    "activity_profile": {
        "activities": [
            {
                "category": "Science/Math",
                "grades": "11, 12",
                "timing": "Year",
                "hours": "10 hr/wk, 40 wk/yr",
                "position": "Team Member",
                "organization": "National Science Olympiad",
                "description": "Represented school in national-level science competitions.",
                "keywords": ["science olympiad", "STEM"],
            },
            {
                "category": "Community Service",
                "grades": "10, 11, 12",
                "timing": "Year",
                "hours": "4 hr/wk, 40 wk/yr",
                "position": "Volunteer",
                "organization": "Clean City Campaign",
                "description": "Worked on waste management and awareness campaigns.",
                "keywords": ["community", "environment", "volunteering"],
            },
        ],
        "time_commitment": {"total_annual_hours": 560, "average_weekly_hours": 12, "activity_count": 2},
    },
    "personal_statement": {
        "essay_prompt": "Share an essay on any topic.",
        "personal_statement": "I grew up in a small city where opportunities were limited. Through science fairs and community projects, I discovered my passion for problem-solving...",
        "essay_analysis": {
            "themes": ["STEM passion", "community impact"],
            "challenges_overcome": ["resource limitations"],
            "unique_cultural_and_other_elements": ["small-town background"],
            "growth_narrative": "From limited resources to national recognition.",
            "why_this_worked": "Shows resilience and intellectual curiosity.",
        },
    },
    "university_specific_questions": {
        "college_name": "Harvard University",
        "entry_term": "Fall 2025",
        "decision_plan": "Regular Decision",
        "ACT/SAT_scores": {"SAT": "1450", "ACT": "32"},
        "top_academic_majors_interest": ["1. Computer Science", "2. Physics", "3. Environmental Science"],
    },
}

# DUMMY_USER_DATA = {
#     "student_profile": {
#         "name": "Ali Hamza Meer",
#         "sex": "Male",
#         "gender": "Male",
#         "birth_country": "Pakistan",
#         "cultural_background": [
#             "South Asian",
#             "Punjabi",
#             "Kashmiri migrant family",
#             "rural agrarian background",
#             "first-generation formally educated",
#             "caste-based discrimination survivor",
#             "children of laborers in feudal system",
#             "resilient village student in a feudal social order",
#             "intergenerational mobility through education and science"
#         ],
#         "languages": [],
#         "socioeconomic_indicators": [
#             "Fee Waiver Requested",
#             "father is a farmer/teacher",
#             "mother is a government-employed physician/farmer",
#             "from a feudal and caste-discriminated minority (Kashmiri migrants)",
#             "lives in a rural village in Sialkot, Punjab, Pakistan",
#             "no access to specialized biology/biotech/environmental science at high school",
#             "pursued Coursera and EdX courses independently to overcome academic limitations"
#         ],
#         "geographic_context": {
#             "birth_place": "Sialkot, Punjab, Pakistan",
#             "citizenship_status": "Citizen of non-U.S. country",
#             "citizenship": "Pakistan",
#             "current_address": "Dhillam Blagan, Mohalla Shaheen, St1, House 3, Sialkot, PUNJAB, 51070, PAK"        }
#     },
#     "academic_profile": {
#         "schools": [
#             {
#                 "name": "Cadet College Hasan Abdal, District Attock, Punjab, PAK",
#                 "type": "Boarding",
#                 "grades_attended": "9, 10, 11, 12",

#                 "recent_courses_taken": [
#                     {
#                         "subject": "Biology - (Cambridge AICE AS A-Level)",
#                         "type": "GCE-Advanced Level Examinations (GCE-A Levels)",
#                         "leaving_exam": "Predicted A*",
#                         "grade": "12"
#                     },
#                     {
#                         "subject": "Chemistry - (Cambridge AICE AS A-Level)",
#                         "type": "GCE-Advanced Level Examinations (GCE-A Levels)",
#                         "leaving_exam": "Predicted A*",
#                         "grade": "12"
#                     },
#                     {
#                         "subject": "Physics - (Cambridge AICE AS A-Level)",
#                         "type": "GCE-Advanced Level Examinations (GCE-A Levels)",
#                         "leaving_exam": "Predicted A*",
#                         "grade": "12"
#                     },
#                     {
#                         "subject": "Mathematics - (Cambridge AICE AS A-Level)",
#                         "type": "GCE-Advanced Level Examinations (GCE-A Levels)",
#                         "leaving_exam": "Predicted A",
#                         "grade": "12"
#                     }
#                 ]
#             }
#         ],
#         "graduation_date": "07/2025",
#         # "Honors": [
#         #     {
#         #         "Title": "Selected as a Top RISE $500,000 Scholarship Finalist from 40,000+ Students",
#         #         "type": "International",
#         #         "grade": [ 12 ],
#         #         "keywords": [ "global finalist", "RISE scholarship", "STEM recognition", "research potential" ]
#         #     },
#         #     {
#         #         "Title": "1st Place Grand Winner Microbiology, National Science and Engineering Fair",
#         #         "type": "National",
#         #         "grade": [ 11, 12 ],
#         #         "keywords": [ "microbiology", "research", "national champion", "DNA barcoding" ]
#         #     },
#         #     {
#         #         "Title": "Gold Medalist, All Pakistan National Athletics Championship",
#         #         "type": "National",
#         #         "grade": [ 11 ],
#         #         "keywords": [ "athletics", "national medal", "track and field", "disc throw" ]
#         #     },
#         #     {
#         #         "Title": "Best Delegate Award at Yale MUN, Yale University",
#         #         "type": "International",
#         #         "grade": [ 12 ],
#         #         "keywords": [ "debate", "MUN", "international award", "public speaking" ]
#         #     },
#         #     {
#         #         "Title": "Most Outstanding Exhibit Award, The Yale Science & Engineering Association, INC",
#         #         "type": "International",
#         #         "grade": [ 12 ],
#         #         "keywords": [ "science fair", "innovation", "engineering", "research exhibition" ]
#         #     }
#         # ],
#         "future_plans": [ "Policymaker", "Government Leadership", "Doctorate" ],
#         "standardized_tests": [
#             {
#                 "exam_name": "SAT",
#                 "results": [
#                     { "section": "Evidence-based Reading and Writing", "score": "690" },
#                     { "section": "Math", "score": "780" }
#                 ]
#             }
#         ]
#     },
#     # "activity_profile": {
#     #     "activities": [
#     #         {
#     #             "category": "Science/Math",
#     #             "grades": "11",
#     #             "timing": "School, Break",
#     #             "hours": "10 hr/wk, 20 wk/yr",
#     #             "position": "Lead Student Researcher (Microbiology), 1st Author, Grand Winner",
#     #             "organization": "Punjab Agriculture Research Center, National Science & Engineering Fair (NSEF)",
#     #             "description": "Developed DNA barcoding markers for Diaphorina citri via ITS2, identifying 4 genetic haplotypes in 50 specimens for HLB management. NSEF 1st Place GW",
#     #             "keywords": [
#     #                 "research-leadership",
#     #                 "biotech innovation",
#     #                 "national-award",
#     #                 "intellectual-vitality",
#     #                 "disease-management",
#     #                 "scientific-publishing"
#     #             ]
#     #         },
#     #         {
#     #             "category": "Research",
#     #             "grades": "11, 12",
#     #             "timing": "Year",
#     #             "hours": "10 hr/wk, 25 wk/yr",
#     #             "position": "Student Research Assistant & Remote Lab Intern",
#     #             "organization": "Biotechnology, Rise Scholarship Finalist, Dr. Iram Liaqat, GCU Lahore, GAO Lab China",
#     #             "description": "Researched CRISPR/Cas9 applications to combat HLB, focusing on gene editing, susceptibility, resistance & delivery; analyzed lab’s past papers/projects",
#     #             "keywords": [
#     #                 "CRISPR-research",
#     #                 "global-research-collaboration",
#     #                 "STEM-international",
#     #                 "intellectual-curiosity",
#     #                 "bioengineering",
#     #                 "Rise-Scholar"
#     #             ]
#     #         },
#     #         {
#     #             "category": "Research",
#     #             "grades": "10",
#     #             "timing": "School, Break",
#     #             "hours": "10 hr/wk, 12 wk/yr",
#     #             "position": "Student Research Intern",
#     #             "organization": "Govt. College University, International Conference on Agriculture, Environment and Biotechnology",
#     #             "description": "Analyzed soil microbiome for nitrogen fixation; assisted with qPCR, DNA/RNA extraction, & plasmid design; 5th author research paper; pub in int'l Conf",
#     #             "keywords": [
#     #                 "soil-microbiome",
#     #                 "lab-techniques",
#     #                 "international-publication",
#     #                 "environmental-science",
#     #                 "emerging-scientist",
#     #                 "PCR-DNA-labwork"
#     #             ]
#     #         },
#     #         {
#     #             "category": "Environmental",
#     #             "grades": "10, 11, 12",
#     #             "timing": "School",
#     #             "hours": "5 hr/wk, 10 wk/yr",
#     #             "position": "Founder and Project Head",
#     #             "organization": "TerraWrap, Biodegradable Packaging Sheets",
#     #             "description": "Prototyped & developed 10K+ sheets from agricultural waste (corn husks); scaled with local producers; cut 5K+ plastic items/yr; deployed in 3 schools",
#     #             "keywords": [
#     #                 "environmental-entrepreneurship",
#     #                 "biodegradable-materials",
#     #                 "climate-action",
#     #                 "STEM-sustainability",
#     #                 "founder-initiative",
#     #                 "agricultural-waste-solution"
#     #             ]
#     #         },
#     #         {
#     #             "category": "Social Justice",
#     #             "grades": "10, 11, 12",
#     #             "timing": "Break",
#     #             "hours": "10 hr/wk, 12 wk/yr",
#     #             "position": "Founder, Activist",
#     #             "organization": "Horizon Shift towards Education, Umeed ka Safar (A journey of Hope)",
#     #             "description": "Visited families & advocated for children education; documented stories; Raised $3K; Connected service employees to families, sent 30+ kids to school",
#     #             "keywords": [
#     #                 "rural-education-access",
#     #                 "activism",
#     #                 "minority-rights",
#     #                 "fundraising-impact",
#     #                 "grassroots-advocacy",
#     #                 "first-gen-support"
#     #             ]
#     #         },
#     #         {
#     #             "category": "Debate/Speech",
#     #             "grades": "10, 11, 12",
#     #             "timing": "Year",
#     #             "hours": "6 hr/wk, 20 wk/yr",
#     #             "position": "Int’l & State MUN Champion, MUN/Debating Coach",
#     #             "organization": "Yale University, Cadet College Hasanabdal",
#     #             "description": "Led 7+ MUN wins, inspired 30+ introverts, & formed delegations of different caste, learning how hierarchies and power asymmetries affect decisions",
#     #             "keywords": [
#     #                 "public-speaking",
#     #                 "debate-coach",
#     #                 "model-united-nations",
#     #                 "caste-awareness",
#     #                 "team-building",
#     #                 "Yale-MUN"
#     #             ]
#     #         },
#     #         {
#     #             "category": "Athletics: Club",
#     #             "grades": "9, 10, 11, 12",
#     #             "timing": "Year",
#     #             "hours": "6 hr/wk, 42 wk/yr",
#     #             "position": "Athletics Team Captain, National Team Member",
#     #             "organization": "Cadet College Hasanabdal, Athletics Federation of Pakistan (AFP)",
#     #             "description": "Trained with Pak team at int'l camp; 150.2 ft discus throw; TFA for 2 yrs; connected 30+ hidden talent from village to coaches, providing opportunity.",
#     #             "keywords": [
#     #                 "athletics-captain",
#     #                 "national-sports",
#     #                 "sports-equity",
#     #                 "rural-talent-mentor",
#     #                 "disciplined-leadership",
#     #                 "international-training"
#     #             ]
#     #         },
#     #         {
#     #             "category": "Student Govt./Politics",
#     #             "grades": "11, 12",
#     #             "timing": "School",
#     #             "hours": "36 hr/wk, 35 wk/yr",
#     #             "position": "Commander, President Student Council",
#     #             "organization": "Cadet College Hasanabdal",
#     #             "description": "Led 100+ juniors; formed diverse groups of 5 from varied backgrounds for social welfare projects, encouraging respect for each other's perspectives.",
#     #             "keywords": [
#     #                 "student-leadership",
#     #                 "intercultural-respect",
#     #                 "inclusive-governance",
#     #                 "cadet-command",
#     #                 "peer-mentorship",
#     #                 "student-council-president"
#     #             ]
#     #         },
#     #         {
#     #             "category": "Social Justice",
#     #             "grades": "10, 11, 12",
#     #             "timing": "Break",
#     #             "hours": "10 hr/wk, 12 wk/yr",
#     #             "position": "Founder & Project Head, Sustainable Livelihood & Equality Advocate",
#     #             "organization": "Roshan Rasta Initiative— Women’s Vocational Farm",
#     #             "description": "Advocate for female farmers; provided them with vocational skills; promoted skill based earning, raised $3K for sewing machines; promote self-reliance",
#     #             "keywords": [
#     #                 "female-empowerment",
#     #                 "vocational-education",
#     #                 "economic-equity",
#     #                 "gender-justice",
#     #                 "entrepreneurial-advocacy",
#     #                 "founder-initiative"
#     #             ]
#     #         },
#     #         {
#     #             "category": "Other Club/Activity",
#     #             "grades": "11, 12",
#     #             "timing": "School",
#     #             "hours": "3 hr/wk, 30 wk/yr",
#     #             "position": "Founder",
#     #             "organization": "“Is it a Cake” Club, Cross-Cultural Club",
#     #             "description": "Organize cake parties for students to promote social integration b/w diverse ethnicities, helped forge 50+ cross-ethnic friendships. Weekly Tradition",
#     #             "keywords": [
#     #                 "community-bridge-building",
#     #                 "boarding-school-tradition",
#     #                 "humor-and-hospitality",
#     #                 "cross-cultural-integration",
#     #                 "inclusion-through-food",
#     #                 "school-unity"
#     #             ]
#     #         }
#     #     ],
#     #     "activity_profile_meta_tags": {
#     #         "leadership_roles": [
#     #             "research-lead-author",
#     #             "founder-multiple-initiatives",
#     #             "student-council-president",
#     #             "athletics-team-captain",
#     #             "debate-coach",
#     #             "project-head",
#     #             "commander",
#     #             "intercultural-club-founder"
#     #         ],
#     #         "community_impact": [
#     #             "children-education-access",
#     #             "female-farmer-vocational-training",
#     #             "plastic-reduction-sustainability",
#     #             "village-talent-scouting",
#     #             "minority-education-advocacy",
#     #             "caste-diverse-delegations",
#     #             "cross-ethnic-integration"
#     #         ],
#     #         "unique_ideas": [
#     #             "biodegradable-corn-husk-sheets",
#     #             "cake-day-tradition-for-diversity",
#     #             "DNA-barcoding-of-citrus-pests",
#     #             "CRISPR-collaboration-China",
#     #             "student-groups-by-background",
#     #             "microbiome-nitrogen-study"
#     #         ],
#     #         "academic_excellence": [
#     #             "NSEF-national-grand-winner",
#     #             "CRISPR-internship",
#     #             "soil-genomics-paper",
#     #             "Rise-finalist-scholar",
#     #             "international-conference-publication",
#     #             "science-research-innovation"
#     #         ]
#     #     },
#     #     "time_commitment": { "total_annual_hours": 1860, "average_weekly_hours": 35.8, "activity_count": 10 }
#     # },
#     "personal_statement": {
#         "essay_prompt": "Share an essay on any topic of your choice. It can be one you've already written, one that",
#         "personal_statement": "“Zakhm toh mitti mein bhi lagte hain” (even soil can bear wounds) The first time I saw disease, it was in the soil of a field we could never call our own. We are Kashmiri migrants — tillers but never owners, laborers bound to feudal lords tethered to ideals of entrenched discrimination. The disdain of the upper caste landowners (chowdhuries) spread through the community like gossypium wilt. Whispers of “yeh Kashmiri log” (these Kashmiris) seep into the cracks of our lives and education is denied to us – as though literacy is a luxury reserved for the soil’s owners, not its servants. Abba, however, refused to let the blight of this ostracism seep into my destiny. So, while my hands harvested another man’s crop by day, my nights were spent poring over stolen glimpses of school books, their ink a promise that I might one day heal more than fields. In the fields, pathogens attack weakened roots. When I finally entered school, it was not without whispers of protest from the same community that had relegated us to the periphery. “Yeh log padh kar kya karenge?” (What will these people accomplish through education?) But I learned: to read, write and observe. In the yellowing citrus orchards surrounding our village, I noticed a sickness spreading through the trees: Huanglongbing (HLB), a bacterial disease that devastates citrus yields. The pathogen responsible, Candidatus Liberibacter asiaticus, moves stealthily through the veins of the tree. It was here that the metaphor crystallized: if we can decode the DNA of this pathogen, if we can trace its mutations and map its spread, then perhaps we can do the same for the diseases that corroded human systems — inequality, ostracism, prejudice. Abba’s sacrifices — moving to a city rent house so I can hold a pen instead of a plow — propelled me into research. At the Punjab Agriculture Research Center, I developed molecular markers for DNA barcoding Diaphorina citri, the vector of the HLB pathogen. My work centered on amplifying mitochondrial cytochrome oxidase I (COI) and ribosomal ITS2 regions through PCR, a process that mirrors my own experience of amplification: taking the whispers of my Kashmiri identity and making them resonate. Gel electrophoresis confirms product specificity and as I sequence the DNA and identify four genetic clusters among 50 individuals, I think of the ways our own social structures divide us into haplotypes: by caste, ethnicity, religion. Diseases like HLB cannot be eradicated overnight, nor can centuries of systemic inequality. But what they share is a common antidote: targeted intervention. The DNA barcoding technique I developed provides a high-resolution tool for tracking Diaphorina citri variants, enabling region-    specific pest management strategies. Similarly, I realized that understanding the variations within my own community — its histories, its traumas, its strengths—was key to devising solutions. Returning to the village that had once denied me the right to education, I founded a program to teach scientific literacy to young children in my ethnic tribe, many of whom are still barred from attending school. I designed workshops that integrated concepts from my research into hands-on activities, such as mapping phylogenetic trees with colored yarn or simulating PCR with beads and strings. These sessions emulate agency — giving my kin the tools to decode the systems that sought to limit them. When the same chowdhuries ,who had once sneered at my father’s dream for me, attended a community seminar where I presented my findings, their skepticism gave way to curiosity, then respect — an admission that the barriers they had erected are not insurmountable. As I continue my work, I carry with me the lessons of the field: we are all connected by invisible threads — haplotypes in a shared human genome. And so, I persist, ensuring that neither disease nor prejudice will define the harvest of the future. Mitti kabhi haar nahi maanti (the soil never gives up). Nor will I",
#         "essay_analysis": {
#             "themes": [
#                 "scientific curiosity",
#                 "social justice through science",
#                 "marginalized identity and empowerment",
#                 "education as liberation",
#                 "metaphor and meaning-making",
#                 "resilience and intergenerational sacrifice"
#             ],
#             "challenges_overcome": [
#                 "ethnic discrimination as a Kashmiri migrant",
#                 "caste-based educational denial",
#                 "poverty and manual labor as a child",
#                 "limited educational access in rural Pakistan",
#                 "overcoming skepticism from dominant caste elites"
#             ],
#             "unique_cultural_and_other_elements": [
#                 "Kashmiri migrant identity",
#                 "caste dynamics in Pakistani rural systems",
#                 "integration of scientific metaphor with lived experience",
#                 "multilingualism and Urdu phrases used for narrative power",
#                 "DNA barcoding of agricultural pathogens as symbolic tool",
#                 "community reinvestment via rural science education"
#             ],
#             "growth_narrative": [
#                 "from field laborer to published researcher",
#                 "from social exclusion to public recognition",
#                 "from micro-level biological intervention to macro-level social impact",
#                 "emergence of intellectual agency from adversity",
#                 "giving voice to silenced communities through science"
#             ],
#             "why_this_worked": [
#                 "This essay exemplifies narrative coherence and vulnerability — the applicant’s lived experience as a Kashmiri migrant seamlessly ties into his scientific research. Like *The Gatekeepers*, it shows how the best essays make the personal political and intellectual.",
#                 "The metaphor of pathogen and prejudice is both elegant and innovative — aligning with Ethan Sawyer’s 'College Essay Essentials' principle of narrative originality and transformation.",
#                 "It reveals intellectual vitality (per Stanford’s key value) through his sophisticated understanding of both lab and social systems. PCR becomes symbolic of self-amplification, and gel electrophoresis of identity clarity.",
#                 "The conclusion offers redemption and impact — a full-circle return that mirrors elite storytelling arcs seen in *50 Successful Ivy League Essays*. He not only endures but creates structural change.",
#                 "Its language blends lyrical and technical fluency, demonstrating both emotional intelligence and scientific rigor — a perfect storm of 'spike' and 'fit'."
#             ]
#         }
#     },
#     "education_progression": {
#         "education_progression_type": "no change",
#         "explanation": "No change in progression",
#         "school_change_reasoning": ""
#     },
#     "university_specific_questions": {
#         "college_name": "Princeton University",
#         "entry_term": "Fall 2025",
#         "decision_plan": "Regular Decision",
#         "top_academic_majors_interest": [
#             "1. Molecular Biology",
#             "2. Ecology and Evolutionary Biology",
#             "Minor: Environmental Studies",
#             "Minor: Technology and Society"
#         ]
#     },
#     "university_supplemental_questions": {
#         "short_essay_1": {
#             "prompt": "As a research institution that also prides itself on its liberal arts curriculum, Princeton allows students to explore areas across the humanities and the arts, the natural sciences, and the social sciences. What academic areas most pique your curiosity (Please respond in 250 words or fewer)",
#             "response": "What captivates me most is its freedom to mix curiosity with innovation (let’s be honest, a dash of trial and error). From chicken farming to experimenting with biology, my journey has been unconventional, to say the least. Take my “barnyard biology” setup, where I used my chickens as test subjects (don’t worry, no feathers were harmed) to experiment with thermal batteries and organic growth patterns. The results? Happy chickens and a whole lot of eggs, which I regularly donate to orphanages—community science at its finest. I’m intrigued by Princeton’s approach to encouraging interdisciplinary connections—because where else could an scientist-in-training with a love for chicken farming also dive into classes on public policy and environmental ethics? I see myself exploring biology, agriculture, and even entrepreneurship through the College’s open curriculum. Princeton’s Environmental Studies Program, with its interdisciplinary approach, offers the perfect platform to connect my work in sustainable farming with academic research. Additionally,who knows, the learnings from Keller Center for Innovation and Entrepreneurship may some day help me take my home-grown research and turn it into a start-up that revolutionizes sustainable farming. Or at the very least, I’ll leave with a deeper understanding of how science and society intertwine (while keeping my chickens happy). Princeton’s mix of academic rigor and flexibility will help me continue asking weird but important questions: How do we feed the world sustainably? And can chickens be the key to it all?",
#             "essay_analysis": {
#                 "themes": [
#                     "interdisciplinary exploration",
#                     "sustainable agriculture",
#                     "curiosity-driven learning",
#                     "biotechnology and environment",
#                     "science and entrepreneurship",
#                     "community service through science"
#                 ],
#                 "challenges_overcome": [
#                     "resource constraints in rural experimentation",
#                     "lack of institutional lab infrastructure",
#                     "bridging informal experiments with formal academic learning"
#                 ],
#                 "unique_cultural_and_other_elements": [
#                     "chicken farming as a rural innovation model",
#                     "barnyard biology as science access tool",
#                     "integration of grassroots sustainability with elite academic opportunities",
#                     "humor and humility as a narrative tone"
#                 ],
#                 "growth_narrative": [
#                     "self-directed learning",
#                     "evolution from informal tinkering to institutional research ambitions",
#                     "vision to connect local challenges with global sustainability"
#                 ],
#                 "why_this_worked": "This essay succeeds by demonstrating intellectual vitality in an unconventional form—using humor, humility, and ingenuity to position the applicant as a thinker who blends rural realities with scientific inquiry. Drawing from '50 Successful Ivy League Essays' and Ethan Sawyer’s 'College Essay Essentials', it exemplifies the 'quirky with purpose' model of standout supplemental writing. The student doesn't merely name-drop Princeton programs—they show *how* and *why* those programs matter to their lived experience. From a Gatekeepers standpoint, it blends community-rooted experimentation with global ambition—ideal for Princeton’s model of service-oriented scholarship."
#             }
#         },
#         "short_essay_2": {
#             "prompt": "Your Voice Princeton values community and encourages students, faculty, staff and leadership to engage in respectful conversations that can expand their perspectives and challenge their ideas and beliefs. As a prospective member of this community, reflect on how your lived experiences will impact the conversations you will have in the classroom, the dining hall or other campus spaces. What lessons have you learned in life thus far? What will your classmates learn from you? In short, how has your lived experience shaped you? (500 words or fewer)",
#             "response": "The soil of Sialkot clung to my father’s hands, cracked and calloused from a lifetime of labor, and settled in my mother’s silence—a silence heavier than words, teaching me that love is sacrifice, and strength is quiet endurance. I was born into this soil, its whispers shaping my world: “Don’t dream too big.” “Know your place.” My parents—bound to the earth—poured their lives into survival, a defiance in itself. Yet even as a child, I felt the soil beneath my feet trembling, as if begging me to rise, to break free, to be more than the dust I stood on. When I left Sialkot for Hasanabdal, I thought I’d escaped those whispers, but they clung to me like shadows. In the halls of that boarding school, they took new shapes, new voices: “Kashmiri scientist? Go free Kashmir. Their laughter cut deeper, the walls amplifying their doubt. My dreams felt fragile, trembling under the weight of their scorn. But somewhere deep within me, a quiet defiance stirred—refusing to let the laughter shatter what little hope I carried. In those moments, I turned to what I knew: bridging. I founded Cake Club, a place where prisoners like me could share laughter tearing down barriers we never knew we’d built. However, my heart was still in Sialkot. Every time I returned home,I saw my mother, her hands blistered from work no one acknowledged. She was my first lesson in resilience, but also my first heartbreak. I created Roshan Raasta, for women like Amma, to give them hope to reclaim their voices. Together, we turned barren fields into places of life and dignity. For the first time, I saw my mother smile—not the fleeting smile of endurance, but the unguarded joy of pride. In Sialkot’s fields, citrus greening stole more than crops—it stole my father’s dreams and broke countless hearts. I chased CRISPR-Cas9 research to fight back, and now, by collaborating with Professors at GAO Lab, China, I am pursuing my mission of creating disease-resistant crops—so no dream has to die in the soil again. At Princeton, I will bring these stories—the soil-stained lessons of Sialkot and the sharp edges of Hasanabdal. I will bring the silence of my mother and the defiance of a boy who dared to dream. My classmates will learn that strength is born in the quietest struggles, that community is built one connection at a time, and that even the hardest soil can bloom. This is who I am: the child of soil, the builder of bridges, the dreamer of impossible dreams. And this is the truth I will carry into every conversation: that from pain grows purpose, and from purpose grows change.",
#             "essay_analysis": {
#                 "themes": [
#                     "intergenerational resilience",
#                     "scientific purpose rooted in community struggle",
#                     "reimagining masculinity through service",
#                     "bridging cultural divides",
#                     "quiet leadership and identity formation",
#                     "community empowerment through education and agriculture"
#                 ],
#                 "challenges_overcome": [
#                     "ethnic stereotyping and social isolation as a Kashmiri in elite boarding school",
#                     "inherited socioeconomic hardship from rural agrarian background",
#                     "gendered emotional labor and silence modeled by his mother",
#                     "trauma of environmental degradation impacting family livelihood",
#                     "navigating elitism and cultural erasure while preserving identity"
#                 ],
#                 "unique_cultural_and_other_elements": [
#                     "use of soil as central cultural, emotional, and symbolic motif",
#                     "deep connection to Kashmiri agricultural labor traditions",
#                     "mother’s silence as metaphor for generational suppression and quiet power",
#                     "creation of 'Cake Club' as grassroots student diplomacy",
#                     "Roshan Raasta as gender-inclusive economic empowerment rooted in village values",
#                     "integration of village-based agricultural issues with CRISPR biotechnology research in China"
#                 ],
#                 "growth_narrative": [
#                     "evolved from internalized shame to public purpose",
#                     "transformed marginalization into fuel for innovation",
#                     "channeled personal grief into systemic solutions for food security",
#                     "leveraged cultural identity to form bridges across difference",
#                     "matured into a leader whose voice amplifies others rather than seeking the spotlight"
#                 ],
#                 "why_this_worked": "This essay masterfully balances the personal and the political, the poetic and the practical. From an admissions officer’s lens—especially within a 'Gatekeepers' or 'Who Gets In and Why' framework—it stands out for its rich, culturally embedded metaphors and multidimensional impact. The applicant doesn’t merely recount hardship; he repurposes it into innovation, blending environmental biotechnology with village revitalization. He doesn’t perform resilience; he reflects it through actions like founding Roshan Raasta and the Cake Club. The writing style itself evokes the narrative maturity of top-tier Ivy essays—mirroring the techniques outlined by Ethan Sawyer in 'College Essay Essentials': vulnerability, vivid imagery, earned wisdom, and specific transformation. The essay also signals what Princeton calls 'service through scholarship'—his lived experience is not baggage, but ballast. It anchors his sense of purpose and offers classmates a mirror to reflect on their own privilege, silence, and responsibility. His story becomes not just one of overcoming, but one of catalyzing community renewal. That’s Ivy League material."
#             }
#         },
#         "short_essay_3": {
#             "prompt": "Princeton has a longstanding commitment to understanding our responsibility to society through service and civic engagement. How does your own story intersect with these ideals? (250 words or fewer)",
#             "response": "Seven years before: I tore pages from textbooks—folded them into chips packets to sell on roadside carts. I was given a bat, a rare gift, and I sold it. The money? survival. A fleeting escape. I asked myself, “Kitabon ka kya faida, jab roti ka sawal ho?” (\"What good are books when bread is the question?\") I used the money donated for education for anything but education. Survival made dreams feel distant, unreachable! But then, CCH came. A chance. A doorway. I saw what could be. What I could be. What my friends could be! Now Books in hand, I walked the dusty paths of my village, my heart heavy with what could have been. Without CCH, I was one of them—children calloused hands, dreams crushed by survival. Generations chained to survival needed a shift—a mindset unshackled from hopelessness. I began “Umeed Ka Safar,” connecting families with public service employees. I sat with parents, pleading, “Bachay khet ke liye nahi, kal ke liye hain” (\"Children are for the future, not the fields\"). We raised $3k, sending 30+ children to schools, shifting parental mindset from survival to education. Because their dreams could have been mine. And I will fight for them to rise.",
#             "essay_analysis": {
#                 "themes": [
#                     "service as moral obligation",
#                     "education equity",
#                     "child advocacy",
#                     "intergenerational poverty",
#                     "civic leadership",
#                     "transformation through access"
#                 ],
#                 "challenges_overcome": [
#                     "extreme childhood poverty",
#                     "educational resource deprivation",
#                     "survival-based mindset in rural communities",
#                     "emotional burden of upward mobility",
#                     "cultural resistance to formal education"
#                 ],
#                 "unique_cultural_and_other_elements": [
#                     "rural Pakistani childhood labor",
#                     "code-switching between Urdu and English for cultural intimacy",
#                     "Umeed Ka Safar as grassroots civic movement",
#                     "leveraging student status to shift community perspectives",
#                     "symbolic use of textbooks and cricket bat as lost childhood"
#                 ],
#                 "growth_narrative": [
#                     "transformation from survivor to advocate",
#                     "shift from reactive survival to proactive service",
#                     "building agency in others through lived empathy",
#                     "turning past deprivation into present empowerment",
#                     "linking personal escape to collective liberation"
#                 ],
#                 "why_this_worked": "This essay is Princeton’s public service mission made manifest. It's brief, but every sentence punches with emotional weight and moral clarity. The applicant moves from a place of deep material scarcity—selling pages from donated textbooks—to organizing a village-wide movement advocating for children’s education. That’s not just service—it’s structural intervention, born of lived experience. From an admissions lens, it reflects the 'service-driven scholar' ideal: someone who acts not out of resume padding, but out of existential recognition. The linguistic duality (Urdu-English) adds cultural specificity and emotional realism, while the use of physical symbols (the bat, the books) anchors the narrative in visual storytelling, echoing models from '50 Successful Ivy League Essays'. It doesn’t romanticize poverty; it interrogates it and mobilizes against it. For an institution like Princeton, which values 'informed service', this essay is a declaration that the applicant won’t just benefit from Princeton—he’ll multiply its mission in the lives of others."
#             }
#         },
#         "short_essay_4": {
#             "prompt": "More About You Please respond to each question in 50 words or fewer. There are no right or wrong answers. Be yourself! What is a new skill you would like to learn in college?",
#             "response": "In college, I would love to learn Taekwondo—not just for the cool high kicks (though they’re a bonus) but because its movements feel like a metaphor for my life: stumbling, standing, and keep moving forward. Plus, who wouldn’t want to tackle life’s challenges with a black belt in resilience?",
#             "essay_analysis": {
#                 "themes": [ "discipline and self-mastery", "metaphor of physical action for emotional persistence" ],
#                 "challenges_overcome": [
#                     "emotional instability or hardship symbolized through 'stumbling'",
#                     "desire to translate past struggle into focused inner strength",
#                     "longing for control and confidence after earlier uncertainty"
#                 ],
#                 "unique_cultural_and_other_elements": [
#                     "use of Taekwondo as metaphorical framework",
#                     "black belt as both literal and symbolic aspiration",
#                     "cross-cultural reference to martial arts as life philosophy",
#                     "blend of humor with insight—a rare tonal balance in micro-essays"
#                 ],
#                 "growth_narrative": [
#                     "shifts from hardship to agency",
#                     "desire to transform pain into power",
#                     "self-reflective aspiration to grow beyond past circumstances",
#                     "seeks discipline not as defense but as development"
#                 ],
#                 "why_this_worked": "This 50-word response stands out by doing what great short essays must: it compresses metaphor, personality, and ambition into a space the size of a tweet. The tone is simultaneously light-hearted and deeply resonant. It nods toward a history of challenge (‘stumbling’) and reframes it through kinetic forward motion. The final punch—‘a black belt in resilience’—is not just clever wordplay; it’s a thesis on identity. It shows exactly what Princeton wants: a student who is self-aware, optimistic, growth-oriented, and emotionally agile. In the tradition of 'College Essay Essentials', it’s an example of the micro-essay as narrative haiku: short, symbolic, and unforgettable."
#             }
#         },
#         "short_essay_5": {
#             "prompt": "What brings you joy?",
#             "response": "Saying Fajr (dawn prayer) with my father. The thrill of a genetic breakthrough (cue my mad-scientist laugh). Watching my village friends walking by my side at school. Debating whether pineapple belongs on pizza, all while wrapping pizza in biodegradable wrappers. Truth: it has a price and I paid for it.",
#             "essay_analysis": {
#                 "themes": [
#                     "spiritual grounding",
#                     "scientific discovery",
#                     "community and belonging",
#                     "humor and authenticity",
#                     "moral courage and truth-telling"
#                 ],
#                 "challenges_overcome": [
#                     "identity tension between tradition and modernity",
#                     "vulnerability in speaking truth in unjust environments",
#                     "social cost of activism or dissent (truth: 'I paid for it')",
#                     "navigating cultural dualities with grace and integrity"
#                 ],
#                 "unique_cultural_and_other_elements": [
#                     "Fajr prayer as a moment of intergenerational spiritual intimacy",
#                     "genetics and biotechnology as sources of joy, not just academic interest",
#                     "reference to village friends reflects rural communal solidarity",
#                     "subtle environmentalism (biodegradable pizza wrap) as casual norm",
#                     "blending Islamic practice with cutting-edge science and Western humor"
#                 ],
#                 "growth_narrative": [
#                     "harmonizing faith, intellect, and humor",
#                     "evolving from conformity to conviction",
#                     "integration of childhood environment with global ambitions",
#                     "embracing contradiction while staying centered in values"
#                 ],
#                 "why_this_worked": "This micro-essay succeeds by blending joy with justice, tradition with curiosity, and humor with heaviness. Each line offers a layer: spiritual discipline, scientific thrill, communal uplift, light-heartedness, and moral reckoning. It reads like a mosaic of lived experience, echoing the narrative layering found in the best short answers from '50 Successful Ivy League Essays'. The final line—'Truth: it has a price and I paid for it'—introduces gravity without overexplaining. From an admissions perspective, this signals a student of integrity, resilience, and multidimensional joy. Princeton values 'service grounded in truth'—this is that value in poetic shorthand."
#             }
#         },
#         "short_essay_6": {
#             "prompt": "What song represents the soundtrack of your life at this moment?",
#             "response": "The song \"Papa Kehte Hain Bara Naam Kare Ga\"—Dad says I’ll make a big name—has always stuck with me, as it shared hope for the future—one filled with possibilities, challenges, and the drive to turn dreams into something meaningful, not just for myself, but for those I aim to serve.",
#             "essay_analysis": {
#                 "themes": [
#                     "hope and aspiration",
#                     "intergenerational dreams",
#                     "legacy and responsibility",
#                     "service to others",
#                     "self-belief through cultural expression"
#                 ],
#                 "challenges_overcome": [
#                     "pressure of expectations from family and community",
#                     "balancing personal ambition with collective responsibility",
#                     "growing up with limited means but boundless hope"
#                 ],
#                 "unique_cultural_and_other_elements": [
#                     "use of a classic Bollywood song as cultural metaphor",
#                     "Urdu/Hindi lyrics symbolize South Asian father-son dynamics",
#                     "expression of filial piety and duty as central motivator",
#                     "musical reference as vessel for inherited hope"
#                 ],
#                 "growth_narrative": [
#                     "transitioning from being the subject of someone else's dream to the agent of their fulfillment",
#                     "redefining success from personal achievement to community impact",
#                     "maturing from passive idealism to purposeful ambition"
#                 ],
#                 "why_this_worked": "This short essay works because it offers a deeply personal yet universally resonant metaphor. The choice of song, 'Papa Kehte Hain Bara Naam Kare Ga', immediately situates the reader within a culturally specific, emotionally rich narrative of intergenerational aspiration. Rather than centering himself solely, the student redirects the ambition implied in the song toward a communal purpose—a key value at Princeton. The lyric becomes more than a soundtrack; it becomes a thesis statement: that success is not just about personal acclaim, but shared uplift. In just a few lines, the student communicates identity, cultural depth, emotional resonance, and social mission—precisely what micro-essays should aim for."
#             }
#         },
#         "application_narrative": {
#             "connected_themes": [
#                 "scientific inquiry as social justice",
#                 "intergenerational sacrifice and mobility",
#                 "marginalized identity as intellectual lens",
#                 "education as defiance",
#                 "rural innovation and global ambition",
#                 "bridging caste, class, and access through leadership"
#             ],
#             "academic_to_extracurricular_connection": [
#                 {
#                     "subject": "Biology",
#                     "connection": "Biology is the narrative engine of the application — the applicant connects molecular biology research (DNA barcoding, microbiome studies, CRISPR editing) to rural disease management, and further to social systems like caste and prejudice. This academic strength fuels extracurriculars like TerraWrap and HLB pathogen research."
#                 },
#                 {
#                     "subject": "Chemistry",
#                     "connection": "Chemistry knowledge underpins his CRISPR work, genetic marker analysis, and biodegradability research. His TerraWrap biodegradable plastic initiative demonstrates how chemistry translates into climate-conscious innovation impacting rural sustainability."
#                 },
#                 {
#                     "subject": "Physics",
#                     "connection": "Physics is less directly present in content but supports the experimental rigor in his lab work, such as PCR, thermal battery experiments, and applied research methods in both home and institutional labs."
#                 },
#                 {
#                     "subject": "Mathematics",
#                     "connection": "Math provides the structural fluency needed for data analysis, gene mapping, statistical evaluation of genetic haplotypes, and scientific modeling, especially in molecular biology and bioinformatics contexts."
#                 }
#             ],
#             "success_factors": [
#                 "narrative coherence",
#                 "scientific originality",
#                 "community-rooted innovation",
#                 "exceptional leadership",
#                 "overcoming systemic barriers",
#                 "international research collaboration",
#                 "social transformation through STEM",
#                 "authentic voice and metaphorical sophistication",
#                 "alignment with institutional values of service and scholarship"
#             ],
#             "overall_analysis": "Ali Hamza Meer’s application succeeds because it weaves together intellectual intensity, social purpose, and cultural rootedness into a cohesive and transformative narrative. His 'spike' is clearly in biology and bioengineering, demonstrated through multiple high-impact research initiatives (e.g., CRISPR, DNA barcoding, microbiome analysis), many of which address urgent real-world problems in agriculture and public health. Yet unlike many science applicants, Ali transcends lab achievements by anchoring his work in a deep understanding of social injustice — caste oppression, rural exclusion, and educational inequity — and channeling his scientific skills toward dismantling those systems. \n\nFrom his personal statement’s symbolic use of pathogens and PCR as metaphors for prejudice and identity to his grassroots innovations like TerraWrap and 'Umeed Ka Safar', every component reinforces his central narrative: knowledge as liberation. His leadership is not performative — it’s restorative. He brings education to children and dignity to female farmers. He doesn’t just participate in global research, he repurposes it for marginalized communities.\n\nWhat makes this application elite-admissions-worthy is its *layered intentionality*: the essays are emotionally intelligent and thematically resonant; the activities show sustained impact and originality; the honors reflect national and international recognition; and the academic-extracurricular synergy is powerful. He models what Jeff Selingo calls a 'service-driven scholar,' and his authentic, unpolished courage — evidenced by quoting Urdu metaphors and building biodegradable plastics from corn husks — reveals a rare synthesis of humility, vision, and intellect. This is not just a compelling applicant. This is the future Princeton hopes to cultivate."
#         }
#     }
# }
