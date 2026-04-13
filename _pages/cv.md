---
layout: archive
title: "CV/Statements"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

<p><a href="{{ base_path }}/files/CV.pdf" class="btn">Download CV (PDF)</a></p>

## Interests

{{ site.data.cv.interests }}

## Education

<ul>
{% for item in site.data.cv.education %}
  <li>
    <strong>{{ item.degree }}</strong>, {{ item.institution }} ({{ item.years }}).
    {% if item.details %}<br><em>{{ item.details }}</em>{% endif %}
  </li>
{% endfor %}
</ul>

## Publications and Preprints

<ol reversed>
{% for post in site.publications reversed %}
  <li>
    {{ post.citation }}
    {% if post.paperurl %} <a href="{{ post.paperurl }}">[PDF]</a>{% endif %}
  </li>
{% endfor %}
</ol>

## Talks and Posters

<ol reversed>
{% for item in site.data.cv.talks %}
  <li>
    "{{ item.title }}", <em>{{ item.venue }}</em>, {{ item.location }}, {{ item.date }}.
  </li>
{% endfor %}
</ol>

## Awards

<ul>
{% for item in site.data.cv.awards %}
  <li><strong>{{ item.name }}</strong>, {{ item.org }} ({{ item.years }}).</li>
{% endfor %}
</ul>

## Teaching Experience

<ul>
{% for post in site.teaching reversed %}
  <li>{{ post.type }}, {{ post.title }} ({{ post.date | date: "%Y" }} {{ post.semester }}, {{ post.venue }}).</li>
{% endfor %}
</ul>

## Organization

<h3>Seminars</h3>
<ul>
{% for item in site.data.cv.organization %}
  <li>
    {{ item.role }},
    {% if item.url %}<a href="{{ item.url }}">{{ item.what }}</a>{% else %}{{ item.what }}{% endif %},
    {{ item.org }} ({{ item.years }}).
  </li>
{% endfor %}
</ul>

<h3>Professional</h3>
<ul>
{% for item in site.data.cv.professional %}
  <li>
    {{ item.role }},
    {% if item.url %}<a href="{{ item.url }}">{{ item.org }}</a>{% else %}{{ item.org }}{% endif %}
    ({{ item.years }}).
  </li>
{% endfor %}
</ul>
