# Glossary

## The Programme
- **Icarus** — Internal codename for this analysis project
- **CS Gen AI Programme** — The formal name; six workstreams under Richard Dosoo
- **CLARA** — The IRP adoption tracker app. Built by Ben Brooks over Christmas 2025, now the programme's flagship deliverable
- **Build in Five** — Workstream 6; framework for building demo apps on IRP's Risk Data Lake using Cursor in customer conversations. Led by Martin Davies.

## Organisation
- **Moody's Analytics** — Parent company
- **RMS** — Risk Management Solutions; acquired by Moody's. The insurance division's origin
- **IRP** — Intelligent Risk Platform; the core product CSMs support
- **OUs** — Operating Units (insurance, banking, KYC, asset management, life)

## Systems & Tools
- **Salesforce** — CRM. CSMs use it. Data quality is poor. API access blocked for Gainsight.
- **Gainsight** — Customer success platform. Natalia Plant's team owns it. API access pending security review. March 2026 earliest.
- **Sales Recon** — Enterprise platform led by Jamie. CS workflow is meant to migrate here by end of FY26. "Intelligence Anywhere" = Salesforce data surfaced into Copilot.
- **Copilot Studio** — Microsoft tool. Kevin Pern built CS Agent prototype here.
- **Cursor** — AI coding tool. The team uses it for app development. Token budget issues ($10K→$20K corporate, Opus 4.6 3x more expensive).
- **Claude Code** — Anthropic's coding agent. Access secured via AWS Bedrock ~Feb 9.
- **MCP** — Model Context Protocol. Product team (Cihan, Lonny) building MCP server for IRP Navigator.
- **User Voice** — Feedback/feature request system. Peter Kimes wants it integrated into CLARA.
- **Power BI** — Microsoft BI tool. Andy Frappe wants centralised migration dashboard here.
- **Midas** — Life team's usage platform. May be in scope for data pipeline.
- **Risk Link** — Legacy product being migrated away from. Migration = switching off Risk Link.

## Infrastructure
- **AWS** — Where CLARA is deployed (after Azure was blocked)
- **AWS RDS** — Database (SQL Server)
- **AWS Bedrock** — AI model hosting. Claude access route.
- **ALB** — Application Load Balancer (AWS). Caused routing issues.
- **CDK vs CloudFormation** — Infrastructure-as-code debate. CDK currently used, some want simpler CloudFormation.
- **Alembic** — Database migration tool (Python). Source of deployment sync issues.
- **CICD** — Continuous Integration/Continuous Deployment pipeline. BenVH manages.

## Key Concepts
- **Golden Source** — The O&M spreadsheet that was the single source of truth before CLARA
- **Adoption vs Migration** — Migration = moving off Risk Link. Adoption = actually using IRP features.
- **Migration-critical workflows** — Workflows that must work before a customer can migrate
- **RAG status** — Red/Amber/Green status indicators
- **Portfolio Review** — Weekly meeting where Natalia reviews priority accounts using CLARA
- **Scorecard** — Executive reporting mechanism. 30-31 migration target for 2026.
- **Adoption Charter** — Customer-level plan for adoption. Being folded into CLARA (Workstream 4).
- **Solution Blueprint** — Technical architecture document per customer implementation
- **Exceedance event** — Risk modelling concept. Now targeting May (shifted from March 21). Build in Five demo target.
- **Friday** — Internal project management app built by Azmain, like Monday.com. Named after the 1940 film "His Girl Friday". Replaces WS4 (Adoption Charter). Syncs bidirectionally with CLARA for IRP projects.
- **Phantom Agent** — BenVH's patented CICD orchestration concept for AI agent governance. Proposed as infrastructure layer for CLARA and App Factory.
- **App Factory** — Platform for deploying internal productivity apps on AWS. Managed by BenVH. Four apps in pipeline besides CLARA.
- **Cat Accelerate** — Existing platform with tech debt (manual Step Function deployment, no backup, no traceability). Subject of CDK vs CloudFormation debate.

## People — Quick Reference

### Core Team
| Name | Role | Key trait |
|------|------|-----------|
| **Azmain** | Programme manager, CLARA developer | Stretched thin, learning Git on the job |
| **Richard Dosoo** | Programme/operational owner | Technical bridge, manages stakeholders up/across/down |
| **Ben Brooks** | Product visionary, built CLARA v1 | Pushes speed, "just do it" mentality |
| **Natalia (Plant)** | CS lead, Azmain's manager | Process-focused, runs Portfolio Reviews |
| **BenVH (Van Houten)** | Platform/infra engineer | AWS, CICD, security. Single point of failure. |
| **Martin Davies** | Developer (12-week assignment) | Building Build in Five |
| **Chris** | Developer | CLARA bug fixes, security audit findings |
| **Diana** | Advisory PM, now Azmain's manager | Supportive of Friday, presenting vision to Ben/Charlotte |
| **Prashant** | Developer (planned) | To be allocated to help with Friday |

### Leadership / Decision Makers
| Name | Role | Key trait |
|------|------|-----------|
| **Diya Sawhny** | Executive sponsor | Impatient with detail, wants elevator pitches |
| **Andy Frappe** | President, Moody's Analytics | One level below board. Saw CLARA demo Feb 20. |
| **Colin Holmes** | Senior leadership | AI steerco, training governance |
| **Josh Ellingson** | CSM leadership | Gatekeeper for CSM adoption, cautious |
| **George Dyke** | CSM leadership (different team) | Pragmatic, organised workshops, building account planner |
| **Stacy (Dixtra)** | Data/reporting backbone | 300-slide decks, cautious but supportive |

### Technical / Adjacent
| Name | Role |
|------|------|
| **Nikhil** | New tech consulting lead (replaced Alex) |
| **Bala** | New, from banking/edfx |
| **Rhett** | Consulting/tech, learning to push code |
| **Kevin Pern** | CS Agent prototype (Copilot Studio) |
| **Cihan** | Product team, MCP server |
| **Lonny** | Product team, MCP server |

### Stakeholders / External
| Name | Role |
|------|------|
| **Jamie** | Sales Recon lead |
| **Divya** | AI programme governance, licences, budgets |
| **Ari Lahavi** | Head of Applied AI |
| **Bernard** | Life team, sceptical about Q1 delivery |
| **Conrad** | Banking CS |
| **Idris** | Banking equivalent to Richard |
| **Cara** | Jamie's team, ran Sales Recon pilot |
| **Courtney** | Specialist team, HD models analysis |
| **Peter Kimes** | User Voice integration requirements |
| **Pietro** | Learning specialist (training) |
| **Stephanie** | Training KPIs and measurement |
| **Liz (Couchman)** | Solution architecture, tracker feedback |
| **Steve Gentilli** | Adoption charter process owner |
| **Diana** | Advisory PM, ILS team help |
| **Philip (Garner)** | CSM, used as test subject for RBAC |
| **Alexandra** | Partner tracking requirements |
| **Nicole** | Infrastructure, Cat Accelerate tech debt |
| **Adrian Thomas** | Security/infra (Azure blocker) |
| **Brandon Smith** | Cyber architecture team |
| **Charlotte** | Cultural resistance to rapid iteration |
| **Catherine** | Data alignment, complex account mapping |
| **Amanda Fleming** | Asset management / KYC team |
| **Dan Flemington** | Sales, building own tools |
| **Julia Valencia** | Salesforce data access contact |
| **Catherine** | Data alignment + Gainsight governance ally |
| **Tina Palumbo** | Gainsight team |
| **Vlad** | PM, data input process |
| **Miles** | CSM, workshop guinea pig |
| **Naveen** | CSM, Arkansas, onboarded 1:1 |
| **Rhonda** | CSM, gave first live account update (Aeon) |
| **Chanel** | CSM, had issues flagged in Feb |
