# Shiwei R201I Single Lesson Template V1 Freeze Candidate Review

This review package is for GPT/external audit of:

```text
1013R_R201I_SINGLE_LESSON_TEMPLATE_V1_FREEZE_CANDIDATE
```

## Decision

```text
R201I = PASS_AS_TEMPLATE_CONTRACT_FREEZE_CANDIDATE
Freeze target = single_lesson_template v1 candidate structure and source rules
Not a teaching quality freeze
Not a route switch
```

## What R201I Freezes

- `single_lesson_template` top-level structure.
- Field semantics for `lesson_header`, front matter, process episodes, assessment and reflection.
- Episode semantics for `episode_goal`, `teacher_organization`, `student_learning`, `scaffolds` and `evidence`.
- Teacher-main allowed and forbidden source ownership.
- `source_gap` and provisional candidate display policy.
- Teacher-facing source labels.
- Engineering terminology leakage guard.
- Minimal extraction regression guard from R201H-P1.
- R201F canary metadata contract.

## What R201I Does Not Freeze

- Final teaching design quality.
- Curriculum-standard depth.
- Art pedagogy method library.
- Provider-backed generation quality.
- Xiaojiao real edit/writeback.
- R95 export.
- Formal apply / save / full default route switch.

## Key PASS Checks

```text
schema_parseable = true
teacher_main_allowed_source_policy_explicit = true
teacher_main_forbidden_source_policy_explicit = true
source_gap_not_teacher_content = true
provisional_requires_teacher_confirmation = true
engineering_guard_kept = true
minimal_line_fish_regression_kept = true
R201F_canary_metadata_contract_kept = true
not_quality_freeze = true
no formal apply / no write / no R95 / no model-provider call
```

## Main Review Files

- `outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013R_R201I_SINGLE_LESSON_TEMPLATE_V1_FREEZE_CANDIDATE/validate_1013R_R201I_single_lesson_template_v1_freeze_candidate_result.json`
- `outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013R_R201I_SINGLE_LESSON_TEMPLATE_V1_FREEZE_CANDIDATE/r201i_single_lesson_template_v1_schema.json`
- `outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013R_R201I_SINGLE_LESSON_TEMPLATE_V1_FREEZE_CANDIDATE/r201i_teacher_main_source_policy.json`
- `outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013R_R201I_SINGLE_LESSON_TEMPLATE_V1_FREEZE_CANDIDATE/r201i_freeze_scope_and_non_scope.md`
- `outputs/PREP_ROOM_RENDER_CANVAS_DEEPEN_V1/1013R_R201I_SINGLE_LESSON_TEMPLATE_V1_FREEZE_CANDIDATE/r201i_regression_guard_matrix.json`

## Code Anchors

- `scripts/validate_1013r_r201i_single_lesson_template_v1_freeze_candidate.py`
- `backend/xiaobei_ai/prep_room_lean_readonly_chain_1013R_R201C.py`
- `backend/xiaobei_ai/prep_room_import_understanding_v2_graph_1013R_R114A.py`

## Boundary

This package is a review-only contract freeze candidate. It does not change formal apply, save, export, curriculum library, Xiaojiao writeback, provider/model calls or R97B UI rendering.
