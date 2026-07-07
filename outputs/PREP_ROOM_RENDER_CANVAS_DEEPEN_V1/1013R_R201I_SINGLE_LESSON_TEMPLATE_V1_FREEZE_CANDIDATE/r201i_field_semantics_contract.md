# R201I Field Semantics Contract

R201I freezes the v1 candidate meaning of `single_lesson_template` fields. It does not freeze final teaching quality.

| Field | Semantics | Teacher-main rule |
| --- | --- | --- |
| `lesson_header` | lesson identity, unit, grade, code, readonly status | May render title metadata; must not imply formal apply. |
| `basis` | source-grounded lesson basis and confirmation gaps | May include uploaded source and graph projection; generic filler is not a quality target. |
| `student_analysis` | observable learner starting point and likely classroom difficulty | Must be source/projection based and teacher-reviewable. |
| `objectives` | observable learning outcomes | Must not invent curriculum depth beyond current chain. |
| `key_difficult_points` | teacher-confirmable emphasis and difficulty | Gap text is allowed when upload lacks explicit data. |
| `preparation` | materials, screens, tools, safety or prep needs | Gap text is allowed; renderer must not infer tools. |
| `process_episodes` | ordered classroom execution episodes | Each episode must preserve title, teacher action, student action, support and evidence separation. |
| `assessment_or_homework` | observable evidence, homework, learning-sheet or evaluation cues | Engineering terms are forbidden; source gaps cannot become conclusions. |
| `reflection_or_notes` | before-class note or after-class placeholder | Before-class preview may explicitly defer reflection until after teaching. |

All teacher-main fields keep source ownership metadata separate from teacher-facing labels.
