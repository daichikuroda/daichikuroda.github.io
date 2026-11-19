---
layout: topic
title: Hierarchical clustering
permalink: /research/hierarchical-clustering/
lede: >-
  What should a hierarchical clustering method guarantee, and which methods actually meet those guarantees?
description: Daichi Kuroda's research on the foundations of hierarchical clustering.
topic: hierarchical-clustering # papers in _data/research.json with this topic are listed at the bottom
icon: dendrogram
math: true

# This page is hidden from the live site until you change the line below to `published: true`.
# Preview it locally with:  bundle exec jekyll serve --unpublished
published: false
---

{% comment %}
HOW TO WRITE THIS PAGE (this comment is not shown on the site)

• Write in Markdown. Every "## Heading" appears in the "On this page" menu.
• Paragraphs followed by {: .todo} are writing prompts (yellow boxes in the preview).
Replace each with your own text and delete the {: .todo} line.
As a safety net, any prompt you forget is hidden on the live site.
• Math (MathJax): wrap TeX in double dollars. Inline: $$d(x, y)$$.
Display: put $$ ... $$ on its own lines, with a blank line before and after.
• Boxes: write a blockquote that starts with **Definition**, **Theorem** or _Remark_,
then add {: .definition}, {: .theorem} or {: .remark} on the next line (see below).
• Figures: put the image in assets/img/research/ and use
{% raw %}{% include research-figure.liquid src="/assets/img/research/file.png" alt="..." caption="**Figure 2.** ..." %}{% endraw %}
• Link to a paper on the list at the bottom with its key, e.g. [NeurIPS 2026 paper](#dreveton2026hierarchical).
{% endcomment %}

Open with two or three sentences for a curious non-specialist: what is hierarchical clustering, and why does it matter? One concrete example helps, such as a taxonomy of species, topics in a document collection, or cell types in single-cell data.
{: .todo}

## Why hierarchies?

Explain that data often have structure at several scales at once, and that a hierarchy (a tree, or dendrogram) records all of these scales together. Mention the classical linkage algorithms (single, average, complete, Ward) and their limitation: they always return a binary tree, even when the data have no hierarchical structure at all.
{: .todo}

{% include research-figure.liquid src="/assets/img/research/hierarchy-example.svg" alt="Points forming two clusters, A with two sub-clusters and B with three, and the corresponding tree in which B's three sub-clusters merge at the same level." caption="**Figure 1.** (a) Points with nested cluster structure. (b) The corresponding hierarchy. Cluster A splits into two sub-clusters, while the three sub-clusters of B merge at the same height, so the tree is not binary." %}

Keep, edit, or replace the example figure above (assets/img/research/hierarchy-example.svg).
{: .todo}

## What should a clustering method satisfy?

Introduce the axiomatic viewpoint. Kleinberg (2002) showed that no flat clustering method can satisfy richness, consistency, and scale invariance at the same time. State the three properties informally, one sentence each, and say why each is a natural requirement.
{: .todo}

> **Definition** (Ultrametric). A dissimilarity $$u$$ on a finite set $$X$$ is an _ultrametric_ if, for all $$x, y, z \in X$$,
>
> $$
> u(x, z) \le \max\{u(x, y),\, u(y, z)\}.
> $$
>
> Ultrametrics on $$X$$ correspond one-to-one to dendrograms (hierarchies with merge heights) on $$X$$.
{: .definition}

Present your result in plain words: the hierarchical versions of the three axioms _can_ hold together. Explain what "admissible" methods are and give one or two examples, such as methods based on well-separated clusters or a non-binary variant of single linkage. You can state the main theorem informally in a box: start a blockquote with **Theorem** (informal) and add {: .theorem} below it, like the definition above.
{: .todo}

Describe the structure shared by all admissible methods: they partially order one another, there is no single best method, but any finite set of them shares a common backbone of well-separated clusters. A small figure could help here.
{: .todo}

## Beyond binary trees and ultrametrics

Summarize the [NeurIPS 2026 paper](#dreveton2026hierarchical): valid hierarchies, the finest valid hierarchy, and the two-step method that runs a linkage algorithm and then prunes the tree. Say which linkages work (single, complete, average) and which do not (Ward), and what this means for practitioners.
{: .todo}

## Hierarchies in networks

Connect the clustering work to [hierarchical community detection](#dreveton2026bottomup): nested communities in graphs, the hierarchical stochastic block model, and when bottom-up algorithms beat top-down ones.
{: .todo}

## Open questions

List two to four questions you find exciting. This section helps prospective collaborators and students see where the work is going.
{: .todo}

## Code

Link to code and notebooks, for example [bottom_up_HCD on GitHub](https://github.com/daichikuroda/bottom_up_HCD), plus any package or demo for the clustering papers.
{: .todo}
