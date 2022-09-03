def CalcRiskRating(likelihood, impact):

    ThisRiskRating = ""
    
    risk_ratings = {
        "VERY_LOW_VERY_LOW": "VERY_LOW",
        "VERY_LOW_LOW": "VERY_LOW",
        "VERY_LOW_MODERATE": "VERY_LOW",
        "VERY_LOW_HIGH": "LOW",
        "VERY_LOW_VERY_HIGH": "LOW",
        "LOW_VERY_LOW": "VERY_LOW",
        "LOW_LOW": "LOW",
        "LOW_MODERATE": "LOW",
        "LOW_HIGH": "LOW",
        "LOW_VERY_HIGH": "MODERATE",
        "MODERATE_VERY_LOW": "VERY_LOW",
        "MODERATE_LOW": "LOW",
        "MODERATE_MODERATE": "MODERATE",
        "MODERATE_HIGH": "MODERATE",
        "MODERATE_VERY_HIGH": "HIGH",
        "HIGH_VERY_LOW": "VERY_LOW",
        "HIGH_LOW": "LOW",
        "HIGH_MODERATE": "MODERATE",
        "HIGH_HIGH": "HIGH",
        "HIGH_VERY_HIGH": "VERY_HIGH",
        "VERY_HIGH_VERY_LOW": "VERY_LOW",
        "VERY_HIGH_LOW": "LOW",
        "VERY_HIGH_MODERATE": "MODERATE",
        "VERY_HIGH_HIGH": "HIGH",
        "VERY_HIGH_VERY_HIGH": "VERY_HIGH"
        }

    input_likelihood_impact = str(likelihood) + "_" + str(impact)

    for key, value in risk_ratings.items():
        if input_likelihood_impact == key:
            ThisRiskRating = value

    return(ThisRiskRating)
