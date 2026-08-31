---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% include base_path %}

{% if site.author.googlescholar %}
<p class="pub-intro">See also my <a href="{{ site.author.googlescholar }}">Google Scholar profile</a>.</p>
{% endif %}

{% assign featured = site.publications | where: "featured", true | sort: "date" | reverse %}
{% if featured.size > 0 %}

<h2 class="pub-section__heading">Featured</h2>

<div class="pub-grid">
  {% for post in featured %}
    {% include publication-card.html %}
  {% endfor %}
</div>

{% endif %}

<h2 class="pub-section__heading">All publications</h2>

{% assign all_pubs = site.publications | sort: "date" | reverse %}
{% assign pubs_by_year = all_pubs | group_by_exp: "p", "p.date | date: '%Y'" %}

{% for year_group in pubs_by_year %}
<h3 class="pub-year__heading">{{ year_group.name }}</h3>
<ol class="pub-list">
  {% for post in year_group.items %}
  {% assign primary_url = post.paperurl | default: post.puburl %}
  <li class="pub-list__item">
    <div class="pub-list__title">
      {% if primary_url %}<a href="{{ primary_url }}">{{ post.title }}</a>{% else %}{{ post.title }}{% endif %}<span class="pub-list__links">{% if post.paperurl %}<a href="{{ post.paperurl }}">pdf</a>{% endif %}{% if post.arxiv %}<a href="{{ post.arxiv }}">arxiv</a>{% endif %}{% if post.doi %}<a href="{{ post.doi }}">doi</a>{% endif %}{% if post.puburl and post.puburl != post.paperurl %}<a href="{{ post.puburl }}">link</a>{% endif %}</span>
    </div>
    <div class="pub-list__cite">
      {{ post.citation | default: post.venue }}
    </div>
  </li>
  {% endfor %}
</ol>
{% endfor %}
