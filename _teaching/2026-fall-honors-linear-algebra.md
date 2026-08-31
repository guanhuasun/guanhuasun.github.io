---
title: "Honors Linear Algebra"
collection: teaching
type: "Instructor"
permalink: /teaching/honors-linear-algebra-fall-2026/
venue: "NYU"
date: 2026-09-02
semester: "Fall"
location: "New York, NY"
course_code: "MATH-UA 148-001"
credits: "4 points"
catalog_url: "https://math.nyu.edu/dynamic/courses/undergrad/math-ua-148/"
excerpt: "Honors Linear Algebra (MATH-UA 148-001) at NYU, Fall 2026."
has_materials: true
show_pagination: false
compact_layout: true
share: false
comments: false
---

{% capture syllabus_source %}
{% include course-sources/honors-linear-algebra/Syllabus_Fall_2026.md %}
{% endcapture %}
{% assign calendar_heading = "## Tentative course calendar" %}
{% assign syllabus_sections = syllabus_source | split: calendar_heading %}

<div class="course-page course-page--linked-syllabus">
  {{ syllabus_sections[0] | markdownify }}

  {% if syllabus_sections.size > 1 %}
    <h2 id="tentative-course-calendar">Tentative course calendar</h2>
    <div class="course-table-scroll">
      {{ syllabus_sections[1] | markdownify }}
    </div>
  {% endif %}
</div>
