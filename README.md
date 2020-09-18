
# Markdown to Roam #

[Roam Research](https://roamresearch.com) isn't too god at importing markdown code. For one, it doesn't read actual markdown. `__bold text__` is recognized as italic while `_italic text_` is not recognized at all. It also looses all structure of the document.

But there is a way of importing files into Roam that keeps their structure: Using json files. Here, I'm working on a script that will convert Markdown in [John Grubers original syntax](https://daringfireball.net/projects/markdown/) to Markdown as Roam understands it, keeping the original structure of the document.