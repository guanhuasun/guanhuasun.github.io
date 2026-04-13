---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% include base_path %}

{% if site.author.googlescholar %}
<p>See also my <a href="{{ site.author.googlescholar }}">Google Scholar profile</a>.</p>
{% endif %}

{% for t in site.data.publication_themes %}
  {% assign papers = site.publications | where: "theme", t.slug | sort: "date" | reverse %}
  {% if papers.size > 0 %}

<h2 class="pub-theme__heading">{{ t.name }}</h2>

{% if t.intro %}
<p class="pub-theme__intro">{{ t.intro }}</p>
{% endif %}

<div class="pub-grid">
  {% for post in papers %}
    {% include publication-card.html %}
  {% endfor %}
</div>

  {% endif %}
{% endfor %}
