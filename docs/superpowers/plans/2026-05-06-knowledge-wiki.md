# Knowledge Wiki Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write 4 wiki pages in `knowledge/wiki/` and update `knowledge/index.md` to give a human and Claude Code a queryable knowledge base scoped to the Greenlight Associate Data Analyst (Marketing Science) role.

**Architecture:** Pure markdown content files. No code, no tests. Each page follows a shared format convention: `> Source: filename.md` for claims drawn from raw files, `> Background:` for content not in raw sources, bold on first use of any term a hiring manager might ask to define. Tasks are independent — write and commit each page separately.

**Tech Stack:** Markdown, git

**Spec:** `docs/superpowers/specs/2026-05-06-knowledge-wiki-design.md`

---

## File Map

| Action | Path | Responsibility |
|---|---|---|
| Create | `knowledge/wiki/overview.md` | What family fintech is and where Greenlight sits |
| Create | `knowledge/wiki/key-players.md` | Greenlight + competitors, market structure |
| Create | `knowledge/wiki/market-trends.md` | Growth drivers, Gen Z behavior, regulatory context |
| Create | `knowledge/wiki/marketing-analytics.md` | CAC, LTV, attribution, CRM — role vocabulary |
| Modify | `knowledge/index.md` | Replace weather-project content with role-scoped index |

---

## Task 1: Write `overview.md`

**Files:**
- Create: `knowledge/wiki/overview.md`

- [ ] **Step 1: Write the file**

Create `knowledge/wiki/overview.md` with this exact content:

```markdown
# Overview: Family Fintech and Greenlight

## What is fintech?

**Financial technology (fintech)** encompasses software and algorithms that deliver financial services to businesses and consumers. Initially focused on backend systems for banks and institutions, fintech has expanded to consumer-facing products spanning retail banking, payments, investment management, and insurance. Today, nearly half of American households use mobile banking, and 50% use mobile payment apps such as PayPal or Venmo.

> Source: `investopedia_fintech_2026-04-27.md`

## Why family banking exists as a category

Traditional banks abandoned younger consumers after the **Dodd-Frank Act** (2010) restricted credit card marketing on college campuses, eliminating their primary revenue model for student relationships. Only 28% of Gen Z and millennials trust banks to be fair and honest. Meanwhile, 75% of major bank IT budgets go toward maintaining legacy systems rather than building new products — leaving incumbents structurally unable to compete with faster-moving entrants.

**Infrastructure commoditization** removed the remaining barrier: API-first providers (Plaid for bank data aggregation, Synapse for core banking, Comply Advantage for AML compliance) made it possible to launch a banking product without building financial infrastructure from scratch. This created the opening for vertically-focused fintechs serving audiences traditional banks ignored.

> Source: `02-a16z-every-company-will-be-fintech.md`, `03-a16z-fintech-gen-z-millennials.md`

## What Greenlight is

Greenlight Financial Technology is a **family banking app** serving 6M+ parents and children. The product gives parents tools to automate allowance, manage chores, set flexible spend controls, and invest on behalf of their children. Kids and teens use a Greenlight debit card and app to earn, save, spend wisely, and invest. The mission: help parents raise financially smart kids.

> Background: sourced from job posting — not covered in raw knowledge base files.

## How Greenlight makes money

Greenlight earns revenue through two streams: a **subscription fee** (tiered monthly plans) and **interchange revenue** on debit card spend. Subscription provides predictable recurring revenue (ARR); interchange scales with how actively families use their cards.

> Background: not covered in raw sources.

## Why this matters for the Marketing Science role

A subscription + interchange model means the Marketing Science team optimizes for two things simultaneously: initial conversion (acquiring the family) and long-term retention (keeping them subscribed and spending). The connecting metric is **CAC payback period** — how many months of combined subscription + interchange gross margin it takes to recover the cost of acquiring a new family. Every KPI the team tracks connects back to this.

> Background: not covered in raw sources.
```

- [ ] **Step 2: Verify against spec**

Check that the file contains:
- 5 H2 sections matching the spec exactly
- At least 2 `> Source:` citations referencing real filenames in `knowledge/raw/`
- At least 3 `> Background:` labels
- Bold on first use of: fintech, Dodd-Frank Act, infrastructure commoditization, family banking app, subscription fee, interchange revenue, CAC payback period

- [ ] **Step 3: Commit**

```bash
git add knowledge/wiki/overview.md
git commit -m "docs: add knowledge wiki overview page"
```

---

## Task 2: Write `key-players.md`

**Files:**
- Create: `knowledge/wiki/key-players.md`

- [ ] **Step 1: Write the file**

Create `knowledge/wiki/key-players.md` with this exact content:

```markdown
# Key Players and Market Structure

## The vertical segmentation thesis

Consumer fintech will not consolidate into one dominant winner. The internet enables neobanks to "aggregate a customer segment with shared needs" across geographic boundaries — something impossible for local banks. This dynamic supports many **$10B–$100B companies** each owning a distinct vertical audience, defined by age cohort, ethnicity, religion, credit history, or life stage.

The four core banking functions — savings, spending, investing, lending — provide the product axis; the vertical audience provides the differentiation axis. Most successful consumer fintechs innovate deeply on one function for one audience.

> Source: `01-a16z-rise-of-many-consumer-fintech.md`

## Greenlight's vertical: families with children

Greenlight targets parents aged roughly 25–45 with school-age children. Its differentiation is the combination of a **financial literacy framework** (kids earn, save, spend wisely, and invest) with a **parental control layer** (spend controls, approval flows, real-time notifications). These features are purpose-built for the family segment and would undermine the UX of a general-purpose neobank if added on. Greenlight and Step are explicitly cited as platforms targeting early financial habit formation for younger users.

> Background (competitive positioning) + Source: `03-a16z-fintech-gen-z-millennials.md`

## Direct competitors

- **Step** — teen-focused, credit-building angle via a secured card, minimal parental controls
- **Copper** — teen debit + financial education content, school partnership as an acquisition channel
- **FamZoo** — prepaid family card, older product, less consumer-facing polish, no investing features
- **Current (teen card)** — family banking as a feature of a broader neobank, not family-first positioning

> Background: not covered in raw sources.

## Why multiple players co-exist

Chime, Current, Cash App, and Earnin appear to compete directly in the "subprime neobank" category but succeed by targeting different demographic sub-segments within that broad label. Apparent competitors are often serving meaningfully different people with different primary needs. This co-existence pattern applies directly to family fintech: Greenlight (financial literacy for younger children), Step (credit-building for teens), and Copper (education-focused) each own a distinct audience moment.

> Source: `01-a16z-rise-of-many-consumer-fintech.md`

## Non-fintech entrants as a long-term risk

Apple, Shopify, and Uber already derive significant revenue from embedded financial services — Apple Card, Shopify Balance, Uber Money. A platform with a large existing family user base (a major education provider, entertainment platform, or gaming company) could embed family banking features and acquire families at near-zero marginal CAC. Not an immediate competitive threat, but a structural risk to vertical specialists that depend on paid acquisition.

> Source: `02-a16z-every-company-will-be-fintech.md`
```

- [ ] **Step 2: Verify against spec**

Check that the file contains:
- 5 H2 sections matching the spec
- `> Source:` citations for: `01-a16z-rise-of-many-consumer-fintech.md`, `03-a16z-fintech-gen-z-millennials.md`, `02-a16z-every-company-will-be-fintech.md`
- The four direct competitors listed: Step, Copper, FamZoo, Current
- Bold on first use of: $10B–$100B companies, financial literacy framework, parental control layer

- [ ] **Step 3: Commit**

```bash
git add knowledge/wiki/key-players.md
git commit -m "docs: add knowledge wiki key-players page"
```

---

## Task 3: Write `market-trends.md`

**Files:**
- Create: `knowledge/wiki/market-trends.md`

- [ ] **Step 1: Write the file**

Create `knowledge/wiki/market-trends.md` with this exact content:

```markdown
# Market Trends in Consumer Fintech

## Trust deficit in traditional banking

Only 28% of millennials and Gen Z trust their banks to be fair and honest. Legacy institutions allocate 75% of their IT budgets to maintaining existing systems rather than building new products. This creates a durable structural advantage for neobanks: incumbents cannot reallocate fast enough to compete on product velocity or customer-centric design.

> Source: `02-a16z-every-company-will-be-fintech.md`

## Infrastructure-as-a-service enabling new entrants

A composable stack of API-first financial infrastructure providers has dramatically lowered the cost and time to launch a consumer banking product:

- **Plaid** — consolidates thousands of bank data integrations into a single API
- **Synapse** — account management and payment processing as a service
- **Comply Advantage** — automated AML (anti-money laundering) monitoring
- **Sentilink** — synthetic identity fraud detection

Any company — fintech or otherwise — can now offer banking features by assembling this stack rather than building financial infrastructure from scratch. Greenlight is a direct beneficiary of this layer.

> Source: `02-a16z-every-company-will-be-fintech.md`

## Gen Z financial behavior

Gen Z entered adulthood having witnessed two major financial crises (2008 and 2020) affecting their parents. Their financial behavior differs from millennials in meaningful ways:

- **Debt aversion** — skeptical of credit products; prefer debit and earned income
- **Digital-native expectations** — mobile-first, frictionless onboarding, no tolerance for legacy UX
- **Radical transparency** — require companies to demonstrate that business incentives align with customer interests; skeptical of "free" products with hidden revenue models
- **Early habit formation** — open to financial products that build long-term behaviors (saving, investing) rather than just facilitating transactions

Greenlight and Step are explicitly named as platforms capturing this early-habit-formation opportunity.

> Source: `03-a16z-fintech-gen-z-millennials.md`

## Regulatory environment

The U.S. Treasury (2022) called for enhanced oversight of nonbank consumer financial activities, with particular focus on **data privacy** and **regulatory arbitrage** (fintechs operating outside traditional bank regulatory frameworks). Financial services remain heavily regulated, and compliance is a structural cost that limits product iteration speed.

Family banking carries additional regulatory constraints not covered by the raw sources:

- **COPPA (Children's Online Privacy Protection Act)** — governs data collection for users under 13. Affects how Greenlight can collect data from, market to, and communicate with its youngest users.
- **State money transmission licenses** — required to move money across state lines; requirements vary by state and add compliance overhead.

> Source: `investopedia_fintech_2026-04-27.md` (general regulation) + Background (COPPA, state licensing)

## Gaps in this knowledge base

This wiki was built from sources dated 2020–2021 (a16z essays) and a 2026-scraped Investopedia overview. Notable absences:

- No Greenlight-specific press releases, blog posts, or product announcements
- No market data from 2023–2026 (family fintech growth, churn benchmarks, funding rounds)
- No CAC or LTV benchmarks for family fintech or consumer subscription apps
- No coverage of banking-as-a-service partner failures (e.g., Synapse filed for bankruptcy in 2024, affecting neobanks relying on its infrastructure)
- No analysis of post-iOS 14 ATT impact on mobile attribution for consumer fintech
- No competitive teardowns of Step, Copper, or FamZoo at a product or business model level

These gaps define the next scraping priorities for `knowledge/raw/`.
```

- [ ] **Step 2: Verify against spec**

Check that the file contains:
- 5 H2 sections including "Gaps in this knowledge base"
- `> Source:` citations for all three a16z files and Investopedia
- The 4 infrastructure providers named: Plaid, Synapse, Comply Advantage, Sentilink
- COPPA mentioned and explained
- At least 5 bullet points in the Gaps section

- [ ] **Step 3: Commit**

```bash
git add knowledge/wiki/market-trends.md
git commit -m "docs: add knowledge wiki market-trends page"
```

---

## Task 4: Write `marketing-analytics.md`

**Files:**
- Create: `knowledge/wiki/marketing-analytics.md`

- [ ] **Step 1: Write the file**

Create `knowledge/wiki/marketing-analytics.md` with this exact content:

~~~~markdown
# Marketing Analytics: Role Vocabulary

> Background: all content on this page is background knowledge — not drawn from raw source files. It defines the analytics vocabulary used daily in the Greenlight Marketing Science role.

## Core acquisition metrics

**CAC (Customer Acquisition Cost)** — total marketing and sales spend in a period divided by new customers acquired in that period. For Greenlight, the unit of acquisition is a *family* (one subscription account), not an individual user. A family that adds three children counts as one customer acquired.

**ROAS (Return on Ad Spend)** — revenue attributed to a paid channel divided by the cost of that channel's advertising. Tracked channel-by-channel: Meta ROAS, Google ROAS, CTV ROAS. The Greenlight Marketing Science team tracks this across Meta, Google, CTV, affiliates, and OOH.

**Payback period** — the number of months until cumulative gross margin from a cohort of acquired customers equals the CAC paid to acquire them. More meaningful than CAC alone for subscription businesses because it incorporates churn. A $60 CAC with $5/month gross margin at 5% monthly churn has a very different health profile than $60 CAC with $10/month gross margin at 2% churn.

## Retention and lifetime value

**LTV (Lifetime Value)** — for a subscription + interchange business:

```
LTV = ARPU × gross margin % ÷ monthly churn rate
```

**ARPU (Average Revenue Per User)** includes both the monthly subscription fee and interchange revenue from card spend. Higher card usage increases LTV without changing CAC — making engagement a direct revenue lever.

**LTV:CAC ratio** — the north-star health metric for a consumer subscription business. A ratio of 3:1 (LTV is three times CAC) is the commonly cited minimum healthy benchmark. Below 1:1 means the business destroys value on every customer acquired.

**Cohort LTV curves** — plot cumulative revenue per customer against months since acquisition, grouped by acquisition cohort. Early months show rapid subscription + interchange accumulation; curves flatten as churn removes lower-engaged customers. Comparing curve shapes across paid channels reveals which channels bring higher-quality (higher-LTV) customers even when their CAC looks similar.

## Attribution models

**Last-touch attribution** — 100% of conversion credit goes to the final touchpoint before signup. Simple to implement; systematically over-credits retargeting and brand search while under-crediting channels that created initial awareness.

**First-touch attribution** — 100% credit to the first touchpoint. Over-credits top-of-funnel awareness channels (CTV, OOH); ignores the role of mid- and lower-funnel in closing the conversion.

**Linear / time-decay attribution** — distribute credit across all tracked touchpoints, either equally (linear) or weighted toward more recent touchpoints (time-decay). Better for multi-channel customer journeys than single-touch models.

**Data-driven (algorithmic) attribution** — model-based credit allocation using observed conversion probabilities. Google Ads and Meta both offer native data-driven attribution. Accuracy degraded significantly after **iOS 14 ATT (App Tracking Transparency, 2021)**, which requires user opt-in for cross-app tracking on iPhone and broke the user-level measurement infrastructure that most mobile attribution depended on.

**Media Mix Modeling (MMM)** — statistical regression approach that infers channel contribution from aggregate spend and outcome data, without requiring user-level tracking. The standard approach for measuring upper-funnel channels (CTV, OOH, podcast) where pixel tracking does not apply. Greenlight's Marketing Science team almost certainly uses MMM or a hybrid approach for its non-digital channels.

## CRM and lifecycle analytics

**Lifecycle stages** for a family banking app:

1. **Acquisition** — paid or organic channel drives a parent to sign up
2. **Onboarding** — account created, first child profile added
3. **Activation** — first card issued, first transaction completed
4. **Engagement** — regular app usage (allowance set, chores tracked, spend reviewed)
5. **Retention** — active subscriber renewing month-over-month
6. **Win-back** — re-engagement of lapsed or churned subscribers

**CRM channels by stage:** Email and push notifications are the primary CRM channels. In-app messages handle onboarding and feature discovery. Each stage uses different frequency and content: onboarding sequences are time-triggered and instructional; retention campaigns are behavioral, triggered by declining app engagement.

**CRM metrics:** open rate, click-through rate (CTR), conversion rate per campaign; unsubscribe rate as a list health signal; **segment-level engagement score** (composite of logins, transactions, and feature usage).

**Audience segmentation** — effective CRM segments are built on behavioral signals, not demographics alone. Useful signals for Greenlight: days since last login, number of children on the account, which features are active (allowance vs. investing vs. chores), card spend frequency. These signals define who receives which campaign and at what cadence.

## Connecting this project to the role vocabulary

Your fintech equity analytics project operates in a different domain (market data vs. user behavior), but the analytical patterns transfer directly:

| Your project | Marketing Science equivalent |
|---|---|
| `fact_daily_prices` (instrument × day grain) | CRM event table (user × action × timestamp grain) |
| Sector-level volume aggregation | Cohort-level LTV aggregation |
| Volume anomaly detection | Engagement drop-off detection (churn risk signals) |
| `dim_instrument`, `dim_company`, `dim_sector` | `dim_user`, `dim_channel`, `dim_campaign` |

In an interview: *"I haven't run a CAC model in production, but I've built the dimensional model and aggregation pipeline that such a model would sit on top of. The grain decisions, the slowly-changing dimensions, the metric rollup logic — that's the same problem regardless of whether the subject is trading volume or customer acquisition."*
~~~~

- [ ] **Step 2: Verify against spec**

Check that the file contains:
- Opening `> Background:` label for the whole page
- 5 H2 sections: Core acquisition metrics, Retention and lifetime value, Attribution models, CRM and lifecycle analytics, Connecting this project to the role vocabulary
- Definitions for: CAC, ROAS, payback period, LTV, ARPU, LTV:CAC ratio, cohort LTV curves, last-touch, first-touch, linear/time-decay, data-driven, MMM, lifecycle stages (6), CRM metrics, audience segmentation
- The comparison table at the bottom mapping project concepts to role concepts
- The interview framing quote in the final section

- [ ] **Step 3: Commit**

```bash
git add knowledge/wiki/marketing-analytics.md
git commit -m "docs: add knowledge wiki marketing-analytics page"
```

---

## Task 5: Update `knowledge/index.md`

**Files:**
- Modify: `knowledge/index.md` (replace all existing content)

- [ ] **Step 1: Replace the file contents**

Overwrite `knowledge/index.md` with this exact content:

```markdown
# Knowledge Base Index

**Domain:** Fintech — Greenlight Associate Data Analyst role prep  
**Role:** Associate Data Analyst, Marketing Science — Greenlight Financial Technology  
**Sources:** 4 raw files (3 a16z essays + Investopedia overview)  
**Last updated:** See git history

---

## Wiki Pages (`knowledge/wiki/`)

| Page | Summary |
|---|---|
| [overview.md](wiki/overview.md) | What family fintech is and where Greenlight sits |
| [key-players.md](wiki/key-players.md) | Greenlight + competitors, market structure |
| [market-trends.md](wiki/market-trends.md) | Growth drivers, Gen Z behavior, regulatory context |
| [marketing-analytics.md](wiki/marketing-analytics.md) | CAC, LTV, attribution, CRM — role vocabulary |

---

## Raw Sources (`knowledge/raw/`)

| File | Source | Topic |
|---|---|---|
| [investopedia_fintech_2026-04-27.md](raw/investopedia_fintech_2026-04-27.md) | Investopedia | Fintech definition and ecosystem overview |
| [01-a16z-rise-of-many-consumer-fintech.md](raw/01-a16z-rise-of-many-consumer-fintech.md) | a16z (2021) | Consumer fintech market structure, vertical segmentation |
| [02-a16z-every-company-will-be-fintech.md](raw/02-a16z-every-company-will-be-fintech.md) | a16z (2020) | Infrastructure thesis, trust deficit, non-bank entrants |
| [03-a16z-fintech-gen-z-millennials.md](raw/03-a16z-fintech-gen-z-millennials.md) | a16z (2020) | Gen Z and millennial banking behavior |

---

## Query Guide

Ask Claude Code questions like:

- *"What is Greenlight's business model?"*
- *"Who are Greenlight's direct competitors and how does the market structure work?"*
- *"What trends are shaping the consumer fintech market?"*
- *"Define CAC, LTV, and payback period for a subscription fintech."*
- *"How do attribution models work and which is appropriate for Greenlight?"*
- *"How does my analytics project connect to the vocabulary used at Greenlight?"*

Claude Code reads `knowledge/wiki/` first, then falls back to `knowledge/raw/`. See [CLAUDE.md](../CLAUDE.md) for full query conventions.
```

- [ ] **Step 2: Verify**

Confirm the file no longer contains "Weather" or "weather" anywhere:

```bash
grep -i "weather" knowledge/index.md
```

Expected: no output.

Confirm all 4 wiki pages are linked:

```bash
grep "wiki/" knowledge/index.md
```

Expected: 4 lines, one per wiki page.

- [ ] **Step 3: Commit**

```bash
git add knowledge/index.md
git commit -m "docs: update knowledge index for Greenlight role prep wiki"
```

---

## Task 6: Push and final check

- [ ] **Step 1: Verify all 4 wiki pages exist**

```bash
ls knowledge/wiki/
```

Expected output:
```
key-players.md
marketing-analytics.md
market-trends.md
overview.md
```

- [ ] **Step 2: Spot-check source citations are real**

```bash
grep "Source:" knowledge/wiki/overview.md knowledge/wiki/key-players.md knowledge/wiki/market-trends.md
```

Expected: every cited filename exists in `knowledge/raw/`. Cross-check:

```bash
ls knowledge/raw/
```

- [ ] **Step 3: Push to origin**

```bash
git push origin main
```

Expected: clean push. If rejected, run `git pull --rebase origin main` first, then push.
