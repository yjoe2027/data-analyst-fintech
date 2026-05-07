# Knowledge Base Wiki Design

**Date:** 2026-05-06  
**Scope:** `knowledge/wiki/` — 4 pages + updated `knowledge/index.md`  
**Role context:** Greenlight Financial Technology — Associate Data Analyst (Marketing Science)  
**Primary use:** Interview prep (human) + Claude Code queries (programmatic) — both equally

---

## Goal

Build a queryable wiki from the 4 raw sources in `knowledge/raw/` that arms the user to:
1. Speak fluently about Greenlight's market, competitors, and growth dynamics in an interview
2. Answer analytics-vocabulary questions (CAC, LTV, attribution, CRM) specific to the Marketing Science role
3. Give Claude Code a citable knowledge base scoped to this role

---

## Format Conventions (applied on every page)

- `> Source: filename.md` blockquote after any claim drawn from a raw file
- `> Background:` blockquote for content not covered by raw sources (clearly labeled)
- **Bold** on first use of any term a hiring manager might ask to define
- H2 section names phrased as questions or plain descriptive labels — query-friendly
- Short, factual prose preferred over long paragraphs

These conventions let a human skim for talking points and let Claude Code retrieve precise, citable answers.

---

## Files

```
knowledge/wiki/
├── overview.md            # What family fintech is and where Greenlight sits
├── key-players.md         # Greenlight + competitors, market structure
├── market-trends.md       # Growth drivers, Gen Z behavior, regulation
└── marketing-analytics.md # CAC, LTV, attribution, CRM — role-specific vocabulary
knowledge/index.md         # Updated to point at all 4 wiki pages + raw sources
```

---

## Page 1: `overview.md`

**Purpose:** Ground-level context on what family fintech is and where Greenlight fits. Covers "tell me about this industry" interview territory.

### H2 sections

**What is fintech?**  
One-paragraph definition. Covers the shift from backend institutional tech to consumer-facing products across banking, payments, investing, and insurance.  
Source: `investopedia_fintech_2026-04-27.md`

**Why family banking exists as a category**  
Traditional banks abandoned younger consumers after the Dodd-Frank Act restricted campus credit card marketing (2010). Only 28% of Gen Z/millennials trust banks to be fair and honest. Infrastructure commoditization (Plaid for data, Synapse for core banking) dropped the cost to launch a neobank dramatically. This created the opening for family-focused fintechs.  
Sources: `02-a16z-every-company-will-be-fintech.md`, `03-a16z-fintech-gen-z-millennials.md`

**What Greenlight is**  
Family banking app serving 6M+ parents and kids. Features: automated allowance, chore management, parental spend controls, investing for kids. Mission: raise financially smart kids.  
Background (job posting is not a raw source file — label as `> Background:`)

**How Greenlight makes money**  
Subscription fee (tiered monthly plans) + interchange revenue on debit card spend. Subscription provides predictable ARR; interchange scales with card usage.  
Background

**Why this matters for the Marketing Science role**  
A subscription + interchange model means the team optimizes for both initial conversion (paid marketing) and long-term retention (CRM). CAC payback period is the connecting metric — how many months of subscription + interchange revenue it takes to recover what was spent acquiring a family.  
Background

---

## Page 2: `key-players.md`

**Purpose:** Competitive landscape and market structure. Covers "who are Greenlight's competitors?" and "why doesn't one player win everything?"

### H2 sections

**The vertical segmentation thesis**  
Consumer fintech will not consolidate into one winner. The internet lets neobanks "aggregate a customer segment with shared needs" across geography, enabling many $10B–$100B companies each owning a distinct vertical: age cohort, ethnicity, credit history, etc.  
Source: `01-a16z-rise-of-many-consumer-fintech.md`

**Greenlight's vertical: families with children**  
Audience: parents ages 25–45 with school-age kids. Differentiation: financial literacy tooling (earn/save/spend/invest framework for kids) + parental control layer. These features are purpose-built for the family segment and not replicable by general neobanks without undermining their own UX.  
Background + Source: `03-a16z-fintech-gen-z-millennials.md`

**Direct competitors**  
- **Step** — teen-focused, credit-building angle, no parental controls  
- **Copper** — teen debit + financial education, school partnership channel  
- **FamZoo** — prepaid family card, older product, less consumer-facing polish  
- **Current (teen card)** — feature of a broader neobank, not family-first  
Background

**Why multiple players co-exist**  
Chime, Current, Cash App, and Earnin appear to compete in "subprime" but actually target different demographic sub-segments within that label. Apparent competitors are often serving different people.  
Source: `01-a16z-rise-of-many-consumer-fintech.md`

**Non-fintech entrants as a long-term risk**  
Apple, Shopify, and Uber already derive meaningful revenue from financial services. A platform with large family user bases (Disney+, Nintendo) could embed family banking features. Not an immediate threat but a structural risk to vertical specialists.  
Source: `02-a16z-every-company-will-be-fintech.md`

---

## Page 3: `market-trends.md`

**Purpose:** Forces shaping the consumer fintech market. Covers "what trends are you seeing in fintech?" and regulatory awareness.

### H2 sections

**Trust deficit in traditional banking**  
28% of millennials and Gen Z trust banks to be fair and honest. 75% of major bank IT budgets go to maintaining legacy systems rather than new products. This structural constraint is the primary reason neobanks can compete — incumbents can't move fast enough.  
Source: `02-a16z-every-company-will-be-fintech.md`

**Infrastructure-as-a-service enabling new entrants**  
A composable stack of API-first providers (Plaid for bank data, Synapse for core banking, Comply Advantage for AML, Sentilink for fraud) means any company can launch a banking product without building financial infrastructure from scratch. Greenlight is a beneficiary of this layer.  
Source: `02-a16z-every-company-will-be-fintech.md`

**Gen Z financial behavior**  
Gen Z witnessed parental financial struggles in 2008 and 2020. Defining traits: debt aversion, digital-native expectations (mobile-first, no friction), demand for radical transparency about how companies make money, and preference for products where business incentives align with customer interests. Greenlight and Step are explicitly named as platforms targeting early financial habit formation.  
Source: `03-a16z-fintech-gen-z-millennials.md`

**Regulatory environment**  
U.S. Treasury (2022) called for enhanced oversight of nonbank consumer financial activities, focusing on data privacy and regulatory arbitrage. Family banking carries additional constraints not in the raw sources — particularly COPPA (Children's Online Privacy Protection Act), which governs data collection for users under 13 and shapes how Greenlight can market to and communicate with its youngest users.  
Source: `investopedia_fintech_2026-04-27.md` (general regulation) + Background (COPPA specifics)

**Gaps in this knowledge base**  
This wiki was built from sources dated 2020–2021 (a16z) and a 2026-scraped Investopedia overview. Notable absences: no Greenlight-specific press or product data, no 2023–2026 market data, no CAC/LTV benchmarks for family fintech, no analysis of banking-as-a-service partner failures (e.g., Synapse 2024 bankruptcy) or post-iOS 14 attribution degradation.

---

## Page 4: `marketing-analytics.md`

**Purpose:** Analytics vocabulary specific to the Marketing Science role. Entirely background-labeled — no raw source covers this. Directly arms interview answers to "walk me through how you'd measure X."

### H2 sections

> Background: all content in this page is background knowledge not drawn from raw sources.

**Core acquisition metrics**  
- **CAC (Customer Acquisition Cost):** total marketing + sales spend ÷ new customers acquired in a period. For Greenlight, "customer" = a family (one subscription), not an individual user.  
- **ROAS (Return on Ad Spend):** revenue attributed to ads ÷ ad spend. Used channel-by-channel (Meta ROAS vs. Google ROAS). Greenlight's team tracks this across Meta, Google, CTV, affiliates, and OOH.  
- **Payback period:** months until cumulative gross margin from a cohort equals its CAC. More meaningful than CAC alone for subscription businesses because it accounts for churn. A 12-month payback with 24-month average LTV is healthy; a 18-month payback with 20-month LTV is not.

**Retention and lifetime value**  
- **LTV (Lifetime Value):** for a subscription product: `ARPU × gross margin % ÷ monthly churn rate`. For Greenlight, ARPU includes both subscription fee and interchange.  
- **LTV:CAC ratio:** the north-star health metric for a consumer subscription business. Rule of thumb: 3:1 is the minimum healthy ratio; below 1:1 means the business loses money on every customer.  
- **Cohort LTV curves:** plot cumulative revenue per customer by months-since-acquisition. Early cohorts show rapid early monetization from subscription; curves flatten as churn removes lower-engaged users. Comparing cohort shapes across acquisition channels reveals channel quality.

**Attribution models**  
- **Last-touch:** 100% of credit to the final touchpoint before conversion. Simple but over-credits retargeting.  
- **First-touch:** 100% credit to the first touchpoint. Over-credits top-of-funnel awareness channels.  
- **Linear / time-decay:** distribute credit across all touchpoints. Better for multi-channel journeys.  
- **Data-driven (algorithmic):** model-based credit allocation using conversion probability. Google and Meta offer native versions; accuracy degraded post-iOS 14 ATT (2021) which broke cross-app tracking on iPhone.  
- **Greenlight context:** a family banking app likely has a long consideration cycle (parents research before signing up). First-touch or data-driven models are more appropriate than last-touch; the team likely uses MMM (media mix modeling) for upper-funnel channels like CTV and OOH where pixel tracking doesn't apply.

**CRM and lifecycle analytics**  
- **Lifecycle stages:** Acquisition → Onboarding (first card activated) → Activation (first allowance set) → Engagement (regular app usage) → Retention → Win-back (lapsed users)  
- **Channels at Greenlight:** email, push notification, in-app message. Each stage uses different channels at different frequencies.  
- **CRM metrics:** open rate, click rate, conversion rate per campaign; unsubscribe rate as a health signal; segment-level engagement scores.  
- **Audience segmentation:** divide users by behavioral signals (days since last login, number of kids on account, features used) rather than demographics alone. Segments drive targeting for both paid re-engagement and CRM campaigns.

**How to connect your project to this vocabulary**  
Your project measures trading volume and fundamentals for fintech stocks — a different domain, but the analytical muscles transfer:  
- Your fact table (instrument × day) is analogous to a CRM event table (user × action × timestamp)  
- Sector-level volume aggregation is analogous to cohort-level LTV aggregation  
- Anomaly detection on volume spikes maps to flagging engagement drop-offs in CRM reporting  
In an interview: "I haven't run a CAC model in production, but I've built the dimensional model and aggregation layer that such a model would sit on top of — and I understand the business logic well enough to define the metrics correctly before writing the SQL."

---

## `knowledge/index.md` Update

Replace existing weather-project content. New structure:

```markdown
# Knowledge Base Index

**Domain:** Fintech — Greenlight Associate Data Analyst role prep  
**Sources:** 4 raw files (a16z essays + Investopedia)  
**Last updated:** See git history

## Wiki Pages

| Page | Summary |
|---|---|
| wiki/overview.md | What family fintech is and where Greenlight sits |
| wiki/key-players.md | Greenlight + competitors, market structure |
| wiki/market-trends.md | Growth drivers, Gen Z behavior, regulatory context |
| wiki/marketing-analytics.md | CAC, LTV, attribution, CRM — role vocabulary |

## Raw Sources

| File | Source | Topic |
|---|---|---|
| raw/investopedia_fintech_2026-04-27.md | Investopedia | Fintech definition and ecosystem overview |
| raw/01-a16z-rise-of-many-consumer-fintech.md | a16z (2021) | Consumer fintech market structure |
| raw/02-a16z-every-company-will-be-fintech.md | a16z (2020) | Infrastructure thesis, non-bank entrants |
| raw/03-a16z-fintech-gen-z-millennials.md | a16z (2020) | Gen Z/millennial banking behavior |
```

---

## Out of Scope

- Greenlight press releases or product blog posts (not yet scraped)
- 2023–2026 market data
- CAC/LTV benchmark data for family fintech
- COPPA deep-dive
- Competitive teardowns of Step, Copper, FamZoo

These are documented as gaps in `market-trends.md` so future scraping targets are explicit.
