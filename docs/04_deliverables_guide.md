# Deliverables guide: what to hand in for every lab

Every lab (except the guided streaming demo) has the same four deliverables, plus a filled test-case table. They go in a folder in your repo named `submissions/lab_NN/`.

```
submissions/lab_04/
  tests.md          <- the test-case table from the lab, with Result and Evidence filled in
  export/           <- your pipeline, notebook and SQL files, plus screenshots
  video.txt         <- the link to your Loom video (and anything needed to open it)
  reflection.md     <- answers to the reflection questions
  one_pager.md      <- your one-page explanation
```

Commit as you work. The history is part of the evidence.

## 1. Export (the blueprint)
This is the working thing, not a picture of it.
- Fabric items: use Git integration so notebooks and pipelines appear as files. If you cannot, export them by hand (notebook as `.ipynb`, pipeline as JSON) into `export/`.
- SQL: save every script you ran as a `.sql` file.
- App code: commit it and link the commits.
- Never commit `.env` or any secret.
- Screenshots support the export. They do not replace it.

## 2. Video (Loom, three minutes at most)
Say these four things in order, out loud, to the camera or over your screen:
1. **Why?** What was the business problem, and why did we build this?
2. **What went wrong?** At least one real problem you hit.
3. **How did you fix it?** Show the fix, not just the sentence.
4. **Run it.** Run it live and show the output.

Rules: no scripts read word for word, no editing out the problems, no waiting for long jobs (start them first and show the finished result).

## 3. Reflection sheet
Short answers in your own words, in `reflection.md`. Two or three sentences each is enough. We read for honesty and thinking, not for polish. Copy the template: `templates/reflection_template.md`.

## 4. One-pager
One page, no more, written for someone who was not in the room. Template: `templates/one_pager_template.md`. If your one-pager needs more than a page, you have not decided what matters yet.

## The test-case table
Each lab has a table of tests. Copy it to `tests.md` and fill in:
- **Result:** PASS, FAIL, BLOCKED or NOT RUN
- **Evidence:** screenshot, query output, or commit link

Honesty rule: a failed test with a good explanation scores better than a PASS you cannot show. Never write a result you did not observe.

## How labs are marked
| Part | Share |
|---|---|
| Test cases run, results honest, evidence present | 35% |
| Export works (someone else could rerun it) | 25% |
| Video covers all four points and shows it running | 15% |
| Reflection shows real thinking | 15% |
| One-pager is clear to a non-expert | 10% |

A lab counts as complete at 60 percent or more with all four deliverables present.
