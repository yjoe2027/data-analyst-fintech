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
