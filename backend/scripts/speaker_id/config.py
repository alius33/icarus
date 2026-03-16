"""Stakeholder roster, aliases, speech patterns, and domain configuration."""

from __future__ import annotations

# Canonical name → list of aliases (case-insensitive matching)
STAKEHOLDER_ALIASES: dict[str, list[str]] = {
    # Tier 1 — Decision Makers
    "Diya Sawhny": ["Diya", "diya"],
    "Andy Frappe": ["Andy", "andy"],
    "Ari Lahavi": ["Ari", "ari"],
    "Colin Holmes": ["Colin", "colin"],

    # Tier 2 — Core Product & Delivery
    "Ben Brookes": ["Ben B", "BenB", "ben b", "Ben Brooks", "Ben Brookes"],
    "Richard Dosoo": ["Richard", "Rich", "richard", "rich"],
    "Azmain Hossain": ["Azmain", "azmain"],
    "Natalia Plant": ["Natalia", "Nat", "natalia", "nat"],
    "Ben Van Houten": ["BenVH", "Ben VH", "Ben Van Houten", "benVH", "ben vh"],

    # Tier 2 — CSM Leadership
    "Josh Ellingson": ["Josh", "Josh E", "josh"],
    "George Dyke": ["George", "George D", "george"],
    "Stacy Dixtra": ["Stacy", "stacy"],

    # Tier 3 — Technical & Development
    "Martin Davies": ["Martin", "martin"],
    "Chris M": ["Chris", "chris"],
    "Rhett": ["Rhett", "rhett"],
    "Nikhil Koli": ["Nikhil", "nikhil", "Nikhil Koli"],
    "Bala": ["Bala", "bala"],
    "Prashant": ["Prashant", "prashant"],

    # Tier 3 — Sales Recon & Adjacent
    "Jamie": ["Jamie", "jamie"],
    "Cara": ["Cara", "cara"],
    "Kevin Pern": ["Kevin", "kevin"],

    # Tier 4 — Product & Architecture
    "Cihan": ["Cihan", "cihan"],
    "Lonny": ["Lonny", "Lonnie", "lonny", "lonnie"],
    "Courtney": ["Courtney", "courtney"],
    "Peter Kimes": ["Peter", "P Kimes", "peter", "Peter Kimes"],
    "Liz Couchman": ["Liz", "liz"],
    "Kathryn Palkovics": ["Kathryn", "kathryn", "Catherine", "catherine", "Kathryn Palkovics"],

    # Tier 4 — PM & Governance
    "Diana Kazakova-Ivanova": ["Diana", "diana", "Diana Kazakova-Ivanova"],
    "Divya": ["Divya", "divya"],
    "Adrian Thomas": ["Adrian", "adrian"],
    "Brandon Smith": ["Brandon", "brandon"],
    "Nicole": ["Nicole", "nicole"],
    "Tina Palumbo": ["Tina", "tina"],
    "Charlotte": ["Charlotte", "charlotte"],

    # Tier 4 — Business & CSM Field
    "Steve Gentilli": ["Steve", "steve"],
    "Vlad": ["Vlad", "vlad"],
    "Philip Garner": ["Philip", "Phil", "philip", "phil"],
    "Rhonda": ["Rhonda", "rhonda"],
    "Naveen": ["Naveen", "naveen"],
    "Miles": ["Miles", "miles"],
    "Chanel": ["Chanel", "chanel"],
    "Rachel Gillespie": ["Rachel", "rachel"],
    "Dan Flemington": ["Dan", "dan", "Dan Flemington"],
    "Amanda Fleming": ["Amanda", "amanda"],

    # Banking & Life
    "Idris": ["Idris", "idris"],
    "Conrad": ["Conrad", "conrad"],
    "Bernard": ["Bernard", "bernard"],
    "Alexandra": ["Alexandra", "alexandra", "Alex"],
    "Julia Valencia": ["Julia", "julia"],

    # Other
    "Pietro": ["Pietro", "pietro"],
    "Stephanie": ["Stephanie", "stephanie"],
}

# Known gender for pronoun-based narrowing
SPEAKER_GENDER: dict[str, str] = {
    "Richard Dosoo": "M", "Ben Brookes": "M", "Ben Van Houten": "M",
    "Azmain Hossain": "M", "Martin Davies": "M", "Josh Ellingson": "M",
    "George Dyke": "M", "Steve Gentilli": "M", "Peter Kimes": "M",
    "Chris M": "M", "Rhett": "M", "Dan Flemington": "M", "Bernard": "M",
    "Philip Garner": "M", "Idris": "M", "Nikhil Koli": "M", "Kevin Pern": "M",
    "Vlad": "M", "Naveen": "M", "Miles": "M", "Bala": "M", "Cihan": "M",
    "Jamie": "M", "Conrad": "M", "Andy Frappe": "M", "Ari Lahavi": "M",
    "Colin Holmes": "M", "Adrian Thomas": "M", "Brandon Smith": "M",
    "Prashant": "M", "Pietro": "M",
    "Natalia Plant": "F", "Diya Sawhny": "F", "Diana Kazakova-Ivanova": "F",
    "Stacy Dixtra": "F", "Courtney": "F", "Liz Couchman": "F",
    "Rachel Gillespie": "F", "Alexandra": "F", "Kathryn Palkovics": "F",
    "Nicole": "F", "Rhonda": "F", "Tina Palumbo": "F",
    "Amanda Fleming": "F", "Charlotte": "F", "Chanel": "F",
    "Cara": "F", "Julia Valencia": "F", "Stephanie": "F", "Divya": "F",
}

# Build reverse lookup: alias → canonical name
_ALIAS_TO_CANONICAL: dict[str, str] = {}
for canonical, aliases in STAKEHOLDER_ALIASES.items():
    _ALIAS_TO_CANONICAL[canonical.lower()] = canonical
    for alias in aliases:
        _ALIAS_TO_CANONICAL[alias.lower()] = canonical


def resolve_name(name: str) -> str | None:
    """Resolve a name or alias to canonical form. Returns None if not found."""
    return _ALIAS_TO_CANONICAL.get(name.lower().strip())


# Title patterns → candidate names
# Each pattern is tried against the cleaned title (underscores → spaces)
TITLE_NAME_PATTERNS: list[tuple[str, str]] = [
    # Specific multi-word names first (order matters!)
    (r"(?i)\bBen\s*VH\b|BenVH\b|Ben\s+Van\s+Houten\b", "Ben Van Houten"),
    (r"(?i)\bBen\s*B\b|Ben\s+Brookes?\b", "Ben Brookes"),
    (r"(?i)\bJosh\s*E\b|Josh\s+Ellingson\b", "Josh Ellingson"),
    (r"(?i)\bGeorge\s*D\b|George\s+Dyke\b", "George Dyke"),
    (r"(?i)\bP\s*Kimes\b|Peter\s+Kimes\b", "Peter Kimes"),
    (r"(?i)\bDan\s+Flemington\b", "Dan Flemington"),
    (r"(?i)\bSteve\s+Gentilli\b", "Steve Gentilli"),
    (r"(?i)\bRachel\s+Gillespie\b", "Rachel Gillespie"),
    (r"(?i)\bLiz\s+Couchman\b", "Liz Couchman"),
    (r"(?i)\bStacy\s+Dixtra\b", "Stacy Dixtra"),
    (r"(?i)\bJulia\s+Valencia\b", "Julia Valencia"),
    # Single names (matched after multi-word to avoid partial matches)
    (r"(?i)\bRichard\b", "Richard Dosoo"),
    (r"(?i)\bRich\b", "Richard Dosoo"),
    (r"(?i)\bDiya\b", "Diya Sawhny"),
    (r"(?i)\bNatalia\b|\bNat\b", "Natalia Plant"),
    (r"(?i)\bMartin\b", "Martin Davies"),
    (r"(?i)\bJosh\b", "Josh Ellingson"),
    (r"(?i)\bGeorge\b", "George Dyke"),
    (r"(?i)\bStacy\b", "Stacy Dixtra"),
    (r"(?i)\bDiana\b", "Diana Kazakova-Ivanova"),
    (r"(?i)\bCourtney\b", "Courtney"),
    (r"(?i)\bSteve\b", "Steve Gentilli"),
    (r"(?i)\bLiz\b", "Liz Couchman"),
    (r"(?i)\bPeter\b", "Peter Kimes"),
    (r"(?i)\bRhett\b", "Rhett"),
    (r"(?i)\bJamie\b", "Jamie"),
    (r"(?i)\bCihan\b", "Cihan"),
    (r"(?i)\bLonny\b|\bLonnie\b", "Lonny"),
    (r"(?i)\bDan\b", "Dan Flemington"),
    (r"(?i)\bChris\b", "Chris M"),
    (r"(?i)\bIdris\b", "Idris"),
    (r"(?i)\bBernard\b", "Bernard"),
    (r"(?i)\bAlexandra\b", "Alexandra"),
    (r"(?i)\bKathryn\b|(?i)\bCatherine\b", "Kathryn Palkovics"),
    (r"(?i)\bVlad\b", "Vlad"),
    (r"(?i)\bNikhil\b", "Nikhil Koli"),
    (r"(?i)\bAmanda\b", "Amanda Fleming"),
    (r"(?i)\bKevin\b", "Kevin Pern"),
]

# "Ben" alone — requires context-dependent disambiguation
# Handled separately in heuristics.py with domain analysis
AMBIGUOUS_NAMES: dict[str, list[str]] = {
    "Ben": ["Ben Brookes", "Ben Van Houten"],
}

# Meeting type detection from title keywords
# Order matters: more specific patterns must come before generic ones
MEETING_TYPE_PATTERNS: list[tuple[str, str]] = [
    (r"(?i)chat\s+with|1-1|1:1|catchup|catch\s*up", "1_on_1"),
    (r"(?i)sales\s*recon", "sales_recon"),
    (r"(?i)build\s+in\s+(5|five)", "build_in_five"),
    (r"(?i)portfolio\s+review", "portfolio_review"),
    (r"(?i)hd\s+model|cat\s+model", "technical_specialist"),
    # "tracker/clara/adoption" before "standup" so "tracker standup" → clara
    (r"(?i)tracker|clara|adoption", "clara"),
    (r"(?i)standup|stand\s*up", "standup"),
    (r"(?i)workshop|session", "workshop"),
    (r"(?i)programme|program|alignment", "programme_review"),
    (r"(?i)deployment|aws|infrastructure|cicd", "infrastructure"),
    (r"(?i)executive|slt|leadership|steerco", "executive"),
    (r"(?i)demo|feedback", "demo"),
    (r"(?i)mcp|api|app\s+dev", "technical"),
    (r"(?i)blocker", "review"),
    (r"(?i)review|next\s+steps", "review"),
]

# Meeting type → typical attendees (used as prior in elimination)
MEETING_TYPE_ATTENDEES: dict[str, list[str]] = {
    "1_on_1": ["Azmain Hossain"],  # + person from title
    "standup": ["Azmain Hossain", "Richard Dosoo", "Ben Brookes", "Natalia Plant"],
    "workshop": ["Azmain Hossain", "George Dyke", "Josh Ellingson", "Ben Brookes"],
    "programme_review": ["Richard Dosoo", "Azmain Hossain", "Ben Brookes", "Natalia Plant", "Diana Kazakova-Ivanova"],
    "sales_recon": ["Richard Dosoo", "Jamie", "George Dyke", "Azmain Hossain"],
    "build_in_five": ["Martin Davies", "Richard Dosoo", "Azmain Hossain"],
    "portfolio_review": ["Natalia Plant", "Ben Brookes", "Azmain Hossain"],
    "infrastructure": ["Ben Van Houten", "Azmain Hossain", "Richard Dosoo"],
    "clara": ["Azmain Hossain", "Richard Dosoo", "Ben Brookes"],
    "executive": ["Richard Dosoo", "Diya Sawhny", "Azmain Hossain"],
    "technical_specialist": ["Richard Dosoo", "Courtney", "Azmain Hossain"],
    "demo": ["Azmain Hossain", "Richard Dosoo"],
    "technical": ["Azmain Hossain", "Richard Dosoo"],
    "review": ["Azmain Hossain", "Richard Dosoo"],
}

# Azmain records virtually every meeting
ALWAYS_PRESENT = "Azmain Hossain"

# Confidence threshold — below this, flag for manual review
CONFIDENCE_THRESHOLD = 0.7

# Filler word categories
FILLERS: dict[str, list[str]] = {
    "hesitation": ["um", "uh", "er", "hmm", "umm", "uhh"],
    "affirmative": ["yeah", "yes", "yep", "right", "okay", "ok", "sure", "yea"],
    "discourse": ["so", "well", "like", "basically", "actually", "obviously",
                  "honestly", "literally", "essentially", "I mean", "you know",
                  "you see", "I guess"],
    "hedge": ["I think", "maybe", "perhaps", "kind of", "sort of", "I suppose",
              "probably", "might", "I believe"],
    "assertive": ["definitely", "absolutely", "100%", "exactly", "certainly",
                  "totally", "clearly", "obviously"],
    "tag_questions": ["right?", "yeah?", "isn't it?", "don't you think?", "you know?"],
    "connective": ["and then", "but then", "so then", "and so"],
}

# Technical vocabulary by domain
TECHNICAL_TERMS: dict[str, list[str]] = {
    "infrastructure": ["aws", "cicd", "cdk", "cloudformation", "alb", "ec2",
                       "docker", "kubernetes", "deployment", "pipeline", "lambda",
                       "s3", "vpc", "ecs", "fargate", "phantom agent"],
    "development": ["api", "endpoint", "database", "schema", "migration",
                    "cursor", "python", "typescript", "git", "branch", "pull request",
                    "commit", "backend", "frontend", "fastapi", "nextjs", "react"],
    "data": ["salesforce", "gainsight", "power bi", "excel", "csv", "etl",
             "data quality", "reporting", "dashboard", "analytics", "crm"],
    "product": ["adoption", "tracker", "roadmap", "sprint", "backlog",
                "user story", "feature", "requirement", "mvp", "demo"],
    "governance": ["governance", "scorecard", "steerco", "programme",
                   "workstream", "milestone", "charter", "kpi", "metric"],
}

# Known speech patterns per speaker (signature phrases and patterns)
SPEECH_PATTERNS: dict[str, dict] = {
    "Richard Dosoo": {
        "signature_words": [r"\bbro\b", r"\bright\?", r"\bbasically\b",
                            r"this is it", r"do you know what I mean",
                            r"rubber meets the road", r"long story short",
                            r"kool.?aid"],
        "role_phrases": [r"\bprogramme\b", r"\bgovernance\b", r"\bstakeholder\b"],
        "cultural_markers": [r"(?i)prayer", r"(?i)hadith", r"(?i)quran",
                             r"(?i)islamic", r"(?i)ramadan"],
    },
    "Azmain Hossain": {
        "signature_words": [r"\bobviously\b", r"100\s*%", r"\bliterally\b",
                            r"\bpersona\b", r"\bbloatware\b", r"\bfantastic\b"],
        "role_phrases": [r"\bcursor\b", r"\bpython\b", r"\bdatabase\b",
                         r"\bapi\b", r"\bendpoint\b", r"\bschema\b"],
        "personal_markers": [r"(?i)\badhd\b", r"(?i)\bwife\b",
                             r"(?i)my brain", r"(?i)drowning"],
    },
    "Ben Brookes": {
        "signature_words": [r"stealth preview", r"polish layer",
                            r"data visibility", r"kill.*csms.*kindness"],
        "role_phrases": [r"\badoption\b", r"\bcsm\b", r"\bdashboard\b",
                         r"\bmetrics\b", r"\bonboarding\b"],
    },
    "Kathryn Palkovics": {
        "role_phrases": [r"(?i)\bcoe\b", r"(?i)\benablement\b",
                         r"(?i)\bcouncil\b", r"(?i)\bgovernance\b"],
    },
    "Natalia Plant": {
        "signature_words": [r"\benablement\b", r"\bexecution\b",
                            r"if someone calls me operations"],
        "role_phrases": [r"\bscorecard\b", r"\bgovernance\b",
                         r"\bworkstream\b", r"\bportfolio\b"],
    },
    "Josh Ellingson": {
        "signature_words": [r"data quality", r"interpreted incorrectly",
                            r"I don't want.*seeing"],
        "role_phrases": [r"\bdata\b.*\bquality\b", r"\bcsm\b"],
    },
    "George Dyke": {
        "signature_words": [r"account planner", r"\bcursor\b"],
        "role_phrases": [r"\bflexibility\b", r"\bpragmatic\b"],
    },
    "Ben Van Houten": {
        "signature_words": [r"phantom agent", r"app factory"],
        "role_phrases": [r"\baws\b", r"\bdeployment\b", r"\bcicd\b",
                         r"\bcdk\b", r"\balb\b", r"\bpipeline\b"],
    },
    "Martin Davies": {
        "signature_words": [r"build in five", r"risk data lake"],
        "role_phrases": [r"\bdemo\b", r"\barchitecture\b", r"\bapollo\b"],
    },
    "Diya Sawhny": {
        "signature_words": [r"elevator pitch", r"continuation"],
        "utterance_style": "very_short",
    },
    "Steve Gentilli": {
        "signature_words": [r"adoption charter", r"data model"],
        "role_phrases": [r"\bworkflow\b", r"\bcharter\b"],
    },
    "Rachel Gillespie": {
        "signature_words": [r"(?i)UK.*team", r"(?i)implementation team",
                            r"(?i)broking"],
    },
    "Courtney": {
        "role_phrases": [r"(?i)hd model", r"(?i)cat model", r"(?i)dlm",
                         r"(?i)exceedance"],
    },
    "Peter Kimes": {
        "role_phrases": [r"(?i)user voice", r"(?i)feature request"],
    },
    "Idris": {
        "signature_words": [r"credit lens", r"360 hub"],
        "role_phrases": [r"(?i)banking", r"(?i)lending", r"(?i)cross.?ou"],
    },
    "Bernard": {
        "signature_words": [r"copilot", r"health dashboard"],
        "role_phrases": [r"(?i)life\s+team", r"(?i)salesforce\s+extract",
                         r"(?i)mixpanel"],
    },
    "Jamie": {
        "role_phrases": [r"(?i)sales\s*recon", r"(?i)intelligence anywhere"],
    },
}

# Facilitator detection phrases
FACILITATOR_PHRASES: list[str] = [
    r"(?i)let's\s+(move on|go to|look at|start|wrap up|continue|begin)",
    r"(?i)any\s+(other\s+)?(?:thoughts|questions|comments|feedback)",
    r"(?i)shall we\s+(?:move on|continue|table|park|wrap)",
    r"(?i)next\s+(?:item|topic|point|agenda)",
    r"(?i)(?:great|okay|right),?\s+so\s+(?:moving|next|let's)",
    r"(?i)who\s+(?:wants|would like)\s+to\s+(?:go|start|share)",
    r"(?i)does anyone\s+(?:have|want)",
]

# Self-introduction patterns (for detecting speaker identity)
INTRO_PATTERNS: list[str] = [
    r"(?i)\bI'm\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})",
    r"(?i)\bmy name is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})",
    r"(?i)\bI am\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b",
    r"(?i)\bthis is\s+([A-Z][a-z]+)\s+(?:here|speaking)",
    r"(?i)\b([A-Z][a-z]+)\s+here\b",
    r"(?i)\bI'm\s+([A-Z][a-z]+),?\s+I\s+(?:work|lead|manage|run|head)",
]

# Greeting patterns (for detecting who is being greeted)
GREETING_PATTERNS: list[str] = [
    r"(?i)\b(?:hey|hi|hello|morning|afternoon|evening),?\s+([A-Z][a-z]+)",
    r"(?i)\bhere(?:'s| is)\s+([A-Z][a-z]+)",
    r"(?i)([A-Z][a-z]+)\s+(?:has|just)\s+joined",
    r"(?i)welcome,?\s+([A-Z][a-z]+)",
    r"(?i)(?:oh|ah),?\s+([A-Z][a-z]+)[,!.]",
    r"(?i)thanks?,?\s+([A-Z][a-z]+)",
]

# Direct address patterns (name at start of sentence directed at someone)
DIRECT_ADDRESS_PATTERNS: list[str] = [
    r"(?i)^([A-Z][a-z]+),?\s+(?:can you|could you|what do you|do you|would you|will you)",
    r"(?i)(?:so|and|but)\s+([A-Z][a-z]+),?\s+(?:what|how|can|could|do|would|tell)",
    r"(?i)^([A-Z][a-z]+),?\s+(?:I think|I was|I wanted|I need)",
    r"(?i)(?:over to you|what about you),?\s+([A-Z][a-z]+)",
]

# Signal correlation matrix (for Bayesian aggregation)
SIGNAL_CORRELATIONS: dict[tuple[str, str], float] = {
    ("title_parse", "elimination"): 0.7,
    ("title_parse", "azmain_recorder"): 0.5,
    ("greeting_exchange", "direct_address"): 0.5,
    ("self_introduction", "stylometric_match"): 0.1,
    ("self_introduction", "conversation_role"): 0.1,
    ("cross_reference", "named_mention"): 0.6,
    ("stylometric_match", "conversation_role"): 0.3,
}
