def chair_decision(policy_result):

    if policy_result.risk_score == 0:
        return "ACCEPT"

    elif policy_result.risk_score <= 3:
        return "MINOR REVISION"

    elif policy_result.risk_score <= 7:
        return "MAJOR REVISION"

    else:
        return "REJECT"