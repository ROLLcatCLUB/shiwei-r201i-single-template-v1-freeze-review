# R201I Episode Semantics Contract

| Episode field | Meaning | Must not mean |
| --- | --- | --- |
| `episode_title` | short classroom phase name from extraction/projection | duration, metadata row, field name, diagnosis text |
| `episode_goal` | student learning change or observable evidence target | duplicate teacher instruction by default |
| `teacher_organization` | concrete teacher classroom organization/action | hidden model reasoning or generic diagnosis |
| `student_learning` | concrete student action, talk, observation, making or reflection | empty placeholder shown as complete learning |
| `key_teacher_talk` | optional teacher talk from source/projection | required generation field |
| `xiaojiao_hint` | teacher-facing assistant reminder | second copy of micro-step teacher action |
| `micro_steps[].teacher_action` | concrete teacher step inside an episode | new pedagogy inferred by renderer |
| `micro_steps[].student_action` | concrete student step inside an episode | engineering status |
| `micro_steps[].scaffolds` | teaching support or risk reminder | invisible source gap conclusion |
| `micro_steps[].evidence` | observable evidence or source excerpt | untraceable generated claim |

Renderer policy: the renderer displays this object; it must not create pedagogy, goals, scaffolds, evidence or source labels.
