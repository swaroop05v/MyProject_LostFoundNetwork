# Community Lost & Found Matching Network

**Individual project, Software Engineering (PES University, Dept. of CSE)**
Problem Statement #59, Media, Events & Community

| | |
|---|---|
| Name | Swaroop Venkateshwar |
| SRN | PES1UG24CS923 |
| Course | Software Engineering |

## About the project

A lost-and-found community network. Finders post items they have found and Owners report items they have lost. The system extracts visual and text tags from each item, matches lost and found items by category, colour tags and location radius, notifies both parties, and requires the Owner to answer the Finder's private security questions before any contact details are revealed. A Community Admin moderates suspicious, fraudulent or duplicate posts.

**Actors:** Finder / Owner, Community Admin (external system: Notification Service)

**Requirements at a glance**

| ID | Summary |
|---|---|
| FR-001 | Match found items with active lost reports by category, colour tags and location radius |
| FR-002 | Finder creates a Found Item post (category, colour, description, photo, location) |
| FR-003 | Owner creates a Lost Item report (category, colour, description, search radius) |
| FR-004 | Notify Finder and Owner by push and email when a candidate match is found |
| FR-005 | Community Admin reviews, flags and removes suspicious posts |
| NFR-001 | Security questions must be answered before contact details are revealed |
| NFR-002 | Match results within 3 seconds at 100,000 active listings (95th percentile) |

## Repository contents

| Folder | What it contains |
|---|---|
| [1_RE](1_RE) | Requirements Engineering: functional and non-functional requirements, Requirements Traceability Matrix (RTM), 19 test cases, and the bug-report traceability table |
| [2_Architectural_Diagram](2_Architectural_Diagram) | Architecture diagram (three-tier, MERN) with the component table, key flows and proposed technology stack |
| [3_Screenshots_GitHub_and_Jira](3_Screenshots_GitHub_and_Jira) | GitHub repository creation screenshots, and Jira screenshots for the Scrum and Kanban projects |
| [4_SRS_and_Work_Breakdown](4_SRS_and_Work_Breakdown) | Software Requirements Specification (IEEE 830 format) and the Work Breakdown Structure with the sprint plan |
| 5_Copilot_Generated_Code | To be added |
| 6_Software_Testing_Practice | To be added |

## Jira projects

| Project | Key | Purpose |
|---|---|---|
| Scrum_BPS#59 | SBPS59 | Epic 1: Lost & Found Item Matching, 7 tasks (one per requirement), 7 user stories worth 47 story points, 2 sprints |
| Kanban_BPS#59 | | Kanban board with the same epic, tasks and stories |
| BugReport_BPS#59 | BBPS59 | 5 bugs, each traced to a requirement and a retest case in the RE document |

## How the documents connect

Each requirement in the RE document is traced forward to a use case, a Jira task and story, and one or more test cases. The SRS adds the detailed use-case flow, exception flows, interfaces and data model. The architecture document maps every component to the requirements it satisfies, and the work breakdown follows the Jira stories.
