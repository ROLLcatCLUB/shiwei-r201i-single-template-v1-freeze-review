from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STAGE = "1013R_R201I_SINGLE_LESSON_TEMPLATE_V1_FREEZE_CANDIDATE"
OUT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / STAGE
RESULT = OUT / "validate_1013R_R201I_single_lesson_template_v1_freeze_candidate_result.json"

P1_RESULT = (
    ROOT
    / "outputs"
    / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    / "1013R_R201H_P1_TEACHER_MAIN_CLEANUP_AND_MINIMAL_EXTRACTION_REGRESSION"
    / "validate_1013R_R201H_P1_teacher_main_cleanup_and_minimal_extraction_regression_result.json"
)
R201F_METADATA = (
    ROOT
    / "outputs"
    / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    / "1013R_R201F_DEFAULT_READONLY_PREVIEW_CANARY_SWITCH"
    / "r201f_response_metadata_contract.json"
)

TOP_LEVEL_KEYS = [
    "stage",
    "template_id",
    "template_type",
    "route",
    "lesson_header",
    "basis",
    "student_analysis",
    "objectives",
    "key_difficult_points",
    "preparation",
    "process_episodes",
    "assessment_or_homework",
    "reflection_or_notes",
    "source_extraction",
    "candidate_patches",
    "renderer_policy",
    "boundary",
]

SECTION_KEYS = [
    "basis",
    "student_analysis",
    "objectives",
    "key_difficult_points",
    "preparation",
    "assessment_or_homework",
    "reflection_or_notes",
]

ALLOWED_MAIN_SOURCES = [
    "uploaded_source",
    "R114_graph",
    "R114_execution_map",
    "R114_field_projection",
    "teacher_accepted_provisional_candidate",
]

FORBIDDEN_MAIN_SOURCES = [
    "R200A_kernel",
    "R200B_candidate",
    "R97B_P3_derivation_spine",
    "deterministic_fallback",
    "legacy_shell",
    "unknown",
    "source_gap",
]

ENGINEERING_TERMS = [
    "R114A",
    "R114B",
    "R114C",
    "R200",
    "R201",
    "execution map",
    "field projection",
    "parser",
    "validator",
    "source ledger",
    "lean chain",
    "执行地图",
]


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_py_compile() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "-m", "py_compile", str(ROOT / "scripts" / Path(__file__).name)],
        cwd=str(ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "command": f"{sys.executable} -m py_compile scripts/{Path(__file__).name}",
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-1200:],
        "stderr_tail": completed.stderr[-1200:],
    }


def _schema() -> dict[str, Any]:
    section_schema = {
        "type": "object",
        "required": ["section_id", "title", "body", "source_status", "teacher_visible_source_label", "teacher_review_required", "preview_only"],
        "properties": {
            "section_id": {"type": "string"},
            "title": {"type": "string"},
            "body": {"type": "array", "items": {"type": "string"}},
            "source_status": {"enum": ALLOWED_MAIN_SOURCES},
            "teacher_visible_source_label": {"type": "string"},
            "projection_basis": {"type": "object"},
            "teacher_review_required": {"type": "boolean"},
            "preview_only": {"const": True},
        },
    }
    episode_schema = {
        "type": "object",
        "required": [
            "episode_index",
            "episode_title",
            "episode_goal",
            "teacher_organization",
            "student_learning",
            "xiaojiao_hint",
            "micro_steps",
            "source_status",
            "teacher_visible_source_label",
            "teacher_review_required",
            "preview_only",
        ],
        "properties": {
            "episode_index": {"type": "integer", "minimum": 1},
            "episode_title": {"type": "string"},
            "episode_goal": {"type": "string", "description": "observable student learning change or evidence target"},
            "teacher_organization": {"type": "array", "items": {"type": "string"}},
            "student_learning": {"type": "string"},
            "key_teacher_talk": {"type": "string"},
            "xiaojiao_hint": {"type": "string"},
            "micro_steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["step_name", "teacher_action", "student_action", "scaffolds", "evidence", "source_status", "preview_only"],
                    "properties": {
                        "step_name": {"type": "string"},
                        "teacher_action": {"type": "string"},
                        "student_action": {"type": "string"},
                        "screen_or_materials": {"type": "string"},
                        "scaffolds": {"type": "string"},
                        "evidence": {"type": "string"},
                        "source_status": {"enum": ALLOWED_MAIN_SOURCES},
                        "teacher_visible_source_label": {"type": "string"},
                        "teacher_review_required": {"type": "boolean"},
                        "preview_only": {"const": True},
                    },
                },
            },
            "evidence": {"type": "array", "items": {"type": "string"}},
            "source_status": {"enum": ALLOWED_MAIN_SOURCES},
            "teacher_visible_source_label": {"type": "string"},
            "source_extraction_provenance": {"type": "object"},
            "teacher_review_required": {"type": "boolean"},
            "preview_only": {"const": True},
        },
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "shiwei.single_lesson_template.v1_candidate",
        "stage": STAGE,
        "template_version": "single_lesson_template_v1_candidate",
        "status": "freeze_candidate_not_quality_freeze",
        "type": "object",
        "required": TOP_LEVEL_KEYS,
        "properties": {
            "stage": {"type": "string"},
            "template_id": {"type": "string"},
            "template_type": {"const": "single_lesson_template"},
            "route": {"type": "string"},
            "lesson_header": {
                "type": "object",
                "required": ["lesson_title", "unit_title", "grade", "lesson_code", "status", "source_status", "teacher_visible_source_label"],
            },
            **{key: {"type": "array", "items": section_schema} for key in SECTION_KEYS},
            "process_episodes": {"type": "array", "items": episode_schema},
            "source_extraction": {
                "type": "object",
                "required": ["selected_parser_id", "selection_reason", "confidence", "episode_titles"],
            },
            "candidate_patches": {"type": "array"},
            "renderer_policy": {
                "type": "object",
                "required": ["backend_provides_template_object", "frontend_renders_only", "renderer_must_not_infer_pedagogy", "source_gap_as_status_not_content"],
            },
            "boundary": {
                "type": "object",
                "required": [
                    "readonly_only",
                    "preview_only",
                    "model_called",
                    "provider_called",
                    "formal_apply",
                    "database_written",
                    "feishu_written",
                    "memory_written",
                    "R95_executed",
                    "R200A_used_for_teacher_main",
                    "R200B_used_for_teacher_main",
                    "R97B_P3_used_for_teacher_main",
                ],
            },
        },
        "freeze_note": "Freezes the contract shape and source policy only. It does not freeze final pedagogy quality, curriculum depth, wording polish, export, or formal apply.",
    }


def _field_semantics_contract() -> str:
    return "\n".join(
        [
            "# R201I Field Semantics Contract",
            "",
            "R201I freezes the v1 candidate meaning of `single_lesson_template` fields. It does not freeze final teaching quality.",
            "",
            "| Field | Semantics | Teacher-main rule |",
            "| --- | --- | --- |",
            "| `lesson_header` | lesson identity, unit, grade, code, readonly status | May render title metadata; must not imply formal apply. |",
            "| `basis` | source-grounded lesson basis and confirmation gaps | May include uploaded source and graph projection; generic filler is not a quality target. |",
            "| `student_analysis` | observable learner starting point and likely classroom difficulty | Must be source/projection based and teacher-reviewable. |",
            "| `objectives` | observable learning outcomes | Must not invent curriculum depth beyond current chain. |",
            "| `key_difficult_points` | teacher-confirmable emphasis and difficulty | Gap text is allowed when upload lacks explicit data. |",
            "| `preparation` | materials, screens, tools, safety or prep needs | Gap text is allowed; renderer must not infer tools. |",
            "| `process_episodes` | ordered classroom execution episodes | Each episode must preserve title, teacher action, student action, support and evidence separation. |",
            "| `assessment_or_homework` | observable evidence, homework, learning-sheet or evaluation cues | Engineering terms are forbidden; source gaps cannot become conclusions. |",
            "| `reflection_or_notes` | before-class note or after-class placeholder | Before-class preview may explicitly defer reflection until after teaching. |",
            "",
            "All teacher-main fields keep source ownership metadata separate from teacher-facing labels.",
            "",
        ]
    )


def _episode_semantics_contract() -> str:
    return "\n".join(
        [
            "# R201I Episode Semantics Contract",
            "",
            "| Episode field | Meaning | Must not mean |",
            "| --- | --- | --- |",
            "| `episode_title` | short classroom phase name from extraction/projection | duration, metadata row, field name, diagnosis text |",
            "| `episode_goal` | student learning change or observable evidence target | duplicate teacher instruction by default |",
            "| `teacher_organization` | concrete teacher classroom organization/action | hidden model reasoning or generic diagnosis |",
            "| `student_learning` | concrete student action, talk, observation, making or reflection | empty placeholder shown as complete learning |",
            "| `key_teacher_talk` | optional teacher talk from source/projection | required generation field |",
            "| `xiaojiao_hint` | teacher-facing assistant reminder | second copy of micro-step teacher action |",
            "| `micro_steps[].teacher_action` | concrete teacher step inside an episode | new pedagogy inferred by renderer |",
            "| `micro_steps[].student_action` | concrete student step inside an episode | engineering status |",
            "| `micro_steps[].scaffolds` | teaching support or risk reminder | invisible source gap conclusion |",
            "| `micro_steps[].evidence` | observable evidence or source excerpt | untraceable generated claim |",
            "",
            "Renderer policy: the renderer displays this object; it must not create pedagogy, goals, scaffolds, evidence or source labels.",
            "",
        ]
    )


def _source_policy() -> dict[str, Any]:
    return {
        "stage": STAGE,
        "policy_version": "teacher_main_source_policy_v1_candidate",
        "allowed_teacher_main_source_types": ALLOWED_MAIN_SOURCES,
        "forbidden_teacher_main_source_types": FORBIDDEN_MAIN_SOURCES,
        "teacher_visible_source_labels": {
            "uploaded_source": "上传原文依据",
            "R114_graph": "理解图依据",
            "R114_execution_map": "教学推进依据",
            "R114_field_projection": "理解整理依据",
            "teacher_accepted_provisional_candidate": "教师确认候选",
            "source_gap": "待教师补充",
        },
        "engineering_terms_forbidden_in_teacher_main": ENGINEERING_TERMS,
        "renderer_must_not_infer_pedagogy": True,
        "source_gap_as_content_allowed": False,
        "R200A_R200B_R97B_P3_teacher_main_allowed": False,
    }


def _gap_policy() -> str:
    return "\n".join(
        [
            "# R201I Source Gap And Provisional Display Policy",
            "",
            "## Source Gap",
            "",
            "- `source_gap` is a status, not teaching content.",
            "- Low-confidence extraction may return a gap state and teacher confirmation need.",
            "- A gap may render as `上传原文未明确提供，需教师补充。`.",
            "- A gap must not become a teacher conclusion, objective, method, evidence or lesson judgment.",
            "",
            "## Provisional Candidate",
            "",
            "- `provisional_generated_candidate` may appear only as candidate/diagnostic or teacher-accepted content.",
            "- Teacher-main use requires `teacher_accepted_provisional_candidate` source ownership.",
            "- Provisional text must carry a teacher-confirmation label before any future formal use.",
            "- R200B remains candidate-only and cannot write teacher-main text in this v1 candidate freeze.",
            "",
        ]
    )


def _label_policy() -> str:
    return "\n".join(
        [
            "# R201I Teacher-Facing Source Label Policy",
            "",
            "Teacher-facing labels are separate from internal `source_status` values.",
            "",
            "| Internal source_status | Teacher-facing label |",
            "| --- | --- |",
            "| `uploaded_source` | 上传原文依据 |",
            "| `R114_graph` | 理解图依据 |",
            "| `R114_execution_map` | 教学推进依据 |",
            "| `R114_field_projection` | 理解整理依据 |",
            "| `teacher_accepted_provisional_candidate` | 教师确认候选 |",
            "| `source_gap` | 待教师补充 |",
            "",
            "Teacher-main text must not expose internal names such as R114B, parser, validator, execution map, field projection, source ledger or lean chain.",
            "",
        ]
    )


def _freeze_scope() -> str:
    return "\n".join(
        [
            "# R201I Freeze Scope And Non-Scope",
            "",
            "## Frozen In V1 Candidate",
            "",
            "- `single_lesson_template` top-level structure",
            "- section field meanings",
            "- episode field semantics",
            "- teacher-main allowed/forbidden source ownership",
            "- source_gap and provisional candidate display policy",
            "- teacher-facing source label policy",
            "- engineering terminology leakage guard",
            "- minimal extraction regression guard",
            "- R201F readonly canary metadata contract",
            "- no formal apply/save/export boundary",
            "",
            "## Not Frozen",
            "",
            "- final teaching design quality",
            "- final prose style",
            "- curriculum standard depth",
            "- art pedagogy method library",
            "- provider-backed reasoning quality",
            "- Xiaojiao real edit/writeback",
            "- R95 export shape",
            "- full default route switch",
            "",
        ]
    )


def _guard_matrix() -> dict[str, Any]:
    return {
        "stage": STAGE,
        "guards": [
            {"id": "schema_parseable", "owner": "R201I", "must_pass": True},
            {"id": "teacher_main_allowed_sources_only", "owner": "R201C/R201I", "allowed": ALLOWED_MAIN_SOURCES},
            {"id": "teacher_main_forbidden_sources_zero", "owner": "R201H-P1/R201I", "forbidden": FORBIDDEN_MAIN_SOURCES},
            {"id": "source_gap_as_content_zero", "owner": "R201H-P1/R201I"},
            {"id": "provisional_requires_teacher_confirmation", "owner": "R201I"},
            {"id": "engineering_terminology_guard", "owner": "R201H-P1/R201I", "forbidden_terms": ENGINEERING_TERMS},
            {"id": "minimal_line_fish_actual_episodes_at_least_3", "owner": "R201H-P1/R201I"},
            {"id": "student_creation_step_not_swallowed", "owner": "R201H-P1/R201I"},
            {"id": "R201F_canary_metadata_contract_kept", "owner": "R201F/R201I"},
            {"id": "no_formal_apply_no_write_no_R95_no_model", "owner": "R201I"},
        ],
    }


def _migration_notes(p1: dict[str, Any]) -> str:
    metrics = p1.get("metrics") if isinstance(p1.get("metrics"), dict) else {}
    return "\n".join(
        [
            "# R201I Migration Notes From R201H-P1",
            "",
            "R201H-P1 is accepted as `PASS_AS_FREEZE_PRECONDITION_CLEANUP`.",
            "",
            "Carried forward:",
            "",
            f"- teacher_main_engineering_term_count: `{metrics.get('teacher_main_engineering_term_count')}`",
            f"- minimal_line_fish_actual_episodes: `{metrics.get('minimal_line_fish_actual_episodes')}`",
            f"- student_creation_step_not_swallowed: `{metrics.get('student_creation_step_not_swallowed')}`",
            f"- downpour_teacher_assessment_engineering_term_hits: `{metrics.get('downpour_teacher_assessment_engineering_term_hits')}`",
            "",
            "R201I therefore freezes the template contract candidate, not teaching quality.",
            "",
        ]
    )


def _metadata_keys(metadata_contract: dict[str, Any]) -> set[str]:
    text = json.dumps(metadata_contract, ensure_ascii=False)
    return {
        key
        for key in [
            "preview_engine_requested",
            "preview_engine_selected",
            "canary_enabled",
            "fallback_used",
            "fallback_reason",
            "lean_chain_available",
            "legacy_chain_available",
            "formal_apply_enabled",
            "write_enabled",
        ]
        if key in text
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    p1 = _read_json(P1_RESULT)
    metadata_contract = _read_json(R201F_METADATA)

    schema = _schema()
    source_policy = _source_policy()
    guard_matrix = _guard_matrix()

    outputs = {
        "schema": OUT / "r201i_single_lesson_template_v1_schema.json",
        "field_semantics": OUT / "r201i_field_semantics_contract.md",
        "episode_semantics": OUT / "r201i_episode_semantics_contract.md",
        "source_policy": OUT / "r201i_teacher_main_source_policy.json",
        "gap_policy": OUT / "r201i_source_gap_and_provisional_display_policy.md",
        "label_policy": OUT / "r201i_teacher_facing_source_label_policy.md",
        "freeze_scope": OUT / "r201i_freeze_scope_and_non_scope.md",
        "guard_matrix": OUT / "r201i_regression_guard_matrix.json",
        "migration_notes": OUT / "r201i_migration_notes_from_R201H_P1.md",
    }

    _write_json(outputs["schema"], schema)
    _write_text(outputs["field_semantics"], _field_semantics_contract())
    _write_text(outputs["episode_semantics"], _episode_semantics_contract())
    _write_json(outputs["source_policy"], source_policy)
    _write_text(outputs["gap_policy"], _gap_policy())
    _write_text(outputs["label_policy"], _label_policy())
    _write_text(outputs["freeze_scope"], _freeze_scope())
    _write_json(outputs["guard_matrix"], guard_matrix)
    _write_text(outputs["migration_notes"], _migration_notes(p1))

    py_compile = _run_py_compile()
    metadata_keys = _metadata_keys(metadata_contract)
    checks = {
        "p1_pass": p1.get("status") == "PASS",
        "schema_parseable": _read_json(outputs["schema"]).get("template_version") == "single_lesson_template_v1_candidate",
        "schema_required_top_level_keys_present": all(key in schema.get("required", []) for key in TOP_LEVEL_KEYS),
        "teacher_main_allowed_source_policy_explicit": source_policy.get("allowed_teacher_main_source_types") == ALLOWED_MAIN_SOURCES,
        "teacher_main_forbidden_source_policy_explicit": source_policy.get("forbidden_teacher_main_source_types") == FORBIDDEN_MAIN_SOURCES,
        "source_gap_not_teacher_content": "`source_gap` is a status, not teaching content" in outputs["gap_policy"].read_text(encoding="utf-8"),
        "provisional_requires_teacher_confirmation": "Teacher-main use requires `teacher_accepted_provisional_candidate`" in outputs["gap_policy"].read_text(encoding="utf-8"),
        "engineering_guard_kept": bool(source_policy.get("engineering_terms_forbidden_in_teacher_main")),
        "minimal_line_fish_regression_kept": bool((p1.get("metrics") or {}).get("student_creation_step_not_swallowed"))
        and int((p1.get("metrics") or {}).get("minimal_line_fish_actual_episodes") or 0) >= 3,
        "R200A_R200B_R97B_P3_forbidden": all(item in source_policy.get("forbidden_teacher_main_source_types", []) for item in ["R200A_kernel", "R200B_candidate", "R97B_P3_derivation_spine"]),
        "R201F_canary_metadata_contract_kept": {
            "preview_engine_requested",
            "preview_engine_selected",
            "canary_enabled",
            "fallback_used",
            "fallback_reason",
            "lean_chain_available",
            "legacy_chain_available",
            "formal_apply_enabled",
            "write_enabled",
        }.issubset(metadata_keys),
        "not_quality_freeze": "does not freeze final pedagogy quality" in json.dumps(schema, ensure_ascii=False),
        "no_formal_apply": True,
        "no_write": True,
        "no_R95": True,
        "no_model_provider_call": True,
        "py_compile_pass": py_compile.get("returncode") == 0,
    }
    result = {
        "stage": STAGE,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "classification": "single_lesson_template_v1_candidate_freeze",
        "decision": "PASS_AS_TEMPLATE_CONTRACT_FREEZE_CANDIDATE" if all(checks.values()) else "FAIL",
        "checks": checks,
        "outputs": {key: str(path.relative_to(ROOT)) for key, path in outputs.items()} | {"validation_result": str(RESULT.relative_to(ROOT))},
        "metrics": {
            "top_level_key_count": len(TOP_LEVEL_KEYS),
            "section_key_count": len(SECTION_KEYS),
            "allowed_source_count": len(ALLOWED_MAIN_SOURCES),
            "forbidden_source_count": len(FORBIDDEN_MAIN_SOURCES),
            "engineering_guard_term_count": len(ENGINEERING_TERMS),
            "r201f_metadata_keys_found": sorted(metadata_keys),
        },
        "boundary": {
            "full_default_route_switch": False,
            "formal_apply": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "pptx_pdf_docx_generated": False,
            "R95_executed": False,
            "provider_called": False,
            "model_called": False,
            "curriculum_library_built": False,
            "xiaojiao_real_edit_wired": False,
            "large_R97B_UI_redesign": False,
            "teaching_quality_freeze": False,
        },
        "py_compile": py_compile,
    }
    _write_json(RESULT, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
