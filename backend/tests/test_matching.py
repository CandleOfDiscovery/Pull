from app.services.matching import analyze_match


def test_match_analysis_is_explainable() -> None:
    match = analyze_match(["Python", "Docker"], ["Machine Learning Engineer"], ["Python", "PyTorch", "Docker"], "Machine Learning Engineer", "Paris, France", "Paris")
    assert match.matched_skills == ["Docker", "Python"]
    assert match.missing_skills == ["PyTorch"]
    assert match.overall_score > 0
