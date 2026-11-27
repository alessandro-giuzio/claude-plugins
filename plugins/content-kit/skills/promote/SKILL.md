---
name: promote
description: >
  Google Business Profile and LinkedIn posts for a published article. Usage:
  /promote <url>.
disable-model-invocation: true
argument-hint: "URL of the published post"
metadata:
  version: "0.1.1"
---

# Promote a published post

Load the `writing-voice` skill and the profile for the post's site.

## 1. Confirm the post

- Open the URL and confirm it loads and is the published version (not a draft or preview). If it doesn't load, stop and say so.
- Read it: the main problem it solves, the key takeaway, who it's for.

## 2. Write

**Google Business Profile post ("Novedad")**
- For non-technical owners: the problem → what it means for them → invitation to read.
- Max about 1,200 characters. No phone numbers, no hashtags, no exaggerated claims.
- Button: "Más información", with the exact URL. Suggest an image (the post's own image is fine).

**LinkedIn post A: promotes the article**
- First line is the hook (it's all that shows before "ver más").
- Short paragraphs, first person, slightly witty. The link. 3 to 5 hashtags. Max about 1,300 characters.

**LinkedIn post B: only if the user gives a news link**
- A standalone take on that news for small businesses, with the source link. No sales pitch; an optional soft close ("si te pasa esto, escríbeme").

## 3. Deliver

Give each post ready to paste, with its character count, for the user to publish. If the user wants a file, write `promo-<slug>.md` in the working directory.
