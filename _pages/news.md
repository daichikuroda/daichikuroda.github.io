---
layout: research
title: News
permalink: /news/
description: News and updates from Daichi Kuroda.
---

{%- include site-data.liquid -%}
<header class="page-intro">
  <p class="eyebrow">Updates</p>
  <h1>News</h1>
</header>
<section class="news-page" aria-label="All news, newest first">
  {% include news-list.liquid limit=1000 %}
</section>
