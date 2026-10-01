from dataclasses import dataclass


@dataclass(frozen=True)
class MatchAnalysis:
    overall_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    score_breakdown: dict[str, int]


def analyze_match(candidate_skills: list[str], candidate_roles: list[str], job_skills: list[str], job_title: str, job_location: str | None, preferred_location: str | None) -> MatchAnalysis:
    """Deterministic similarity, not a prediction of hiring success."""
    candidate = {skill.casefold(): skill for skill in candidate_skills}
    required = {skill.casefold(): skill for skill in job_skills}
    matched = sorted(candidate[key] for key in candidate.keys() & required.keys())
    missing = sorted(value for key, value in required.items() if key not in candidate)
    skills_score = round(100 * len(matched) / max(len(required), 1))
    title_score = 100 if any(role.casefold() in job_title.casefold() or job_title.casefold() in role.casefold() for role in candidate_roles) else 35
    location_score = 100 if not preferred_location or (job_location and preferred_location.casefold() in job_location.casefold()) else 50
    overall = round(skills_score * 0.65 + title_score * 0.2 + location_score * 0.15)
    return MatchAnalysis(overall, matched, missing, {"skills": skills_score, "title": title_score, "location": location_score})
