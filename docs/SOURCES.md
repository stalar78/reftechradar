# Sources

## 1. Source strategy

RefTechRadar is multi-source by design, but the MVP must not connect many sources at once.

For each source, assess acquisition in this priority order:

1. official/public API;
2. RSS/feed;
3. stable public endpoint;
4. search-engine discovery;
5. email alerts;
6. browser adapter;
7. scraping only when sustainable, permitted and justified.

Do not begin with aggressive scraping.

## 2. Candidate source backlog

Russian-language priority:

- HH.ru;
- Habr Career;
- GeekJob;
- Getmatch;
- Careerist;
- Finder;
- YoungJunior;
- company career pages;
- Telegram job channels;
- startup/AI communities;
- search engines.

Later international candidates:

- Wellfound;
- YC jobs;
- RemoteOK;
- other startup/AI boards.

International expansion is not an MVP priority.

## 3. Source qualification card

Before implementing an adapter, document:

- source name;
- acquisition method;
- authentication;
- stable external id availability;
- canonical URL quality;
- fields available;
- published timestamp semantics;
- pagination;
- rate limits;
- robots/ToS considerations;
- anti-bot behavior;
- update behavior;
- deletion/expiry behavior;
- expected implementation complexity;
- expected relevance to target profile.

## 4. First-source principle

The first real source should be chosen for:

- technical sustainability;
- enough vacancy volume;
- useful text detail;
- stable IDs/URLs;
- relevance to Russian IT hiring.

It does not have to be the "best" source by brand.

## 5. Second-source principle

The second source should maximize architectural learning.

Prefer a source that can expose overlapping vacancies so cross-source deduplication can be tested.

## 6. Collector contract

Collectors should only collect.

They should not:

- calculate opportunity score;
- apply candidate-specific filters;
- decide duplicates;
- mutate user decisions.

They return raw/source observations plus acquisition metadata.

## 7. Failure behavior

A source failure must be isolated.

One failed source should not invalidate the entire daily run.

Reports should expose partial-run status.

## 8. Source freshness

`published_at` is source evidence, not system novelty.

System novelty is based on persisted `first_seen_at`.
