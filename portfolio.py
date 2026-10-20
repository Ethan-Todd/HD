import math
import sys


# Editable inputs
SLEEVES = {
    "Treasury bills": {"expected_return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"expected_return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"expected_return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"expected_return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00,
        "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05,
        "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10,
        "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80,
        "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05,
        "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00,
        "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00,
        "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25,
        "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


def validate_inputs(sleeves, correlations):
    names = list(sleeves)
    if set(correlations) != set(names):
        raise ValueError("correlation table rows must match the sleeve names")

    for name in names:
        if set(correlations[name]) != set(names):
            raise ValueError(f"correlation table columns for {name} must match the sleeve names")
        if sleeves[name]["volatility"] <= 0.0:
            raise ValueError(f"volatility for {name} must be greater than zero")

    for row_name in names:
        for column_name in names:
            correlation = correlations[row_name][column_name]
            if correlation < -1.0 or correlation > 1.0:
                raise ValueError(
                    f"correlation for {row_name} and {column_name} must be between -1 and 1"
                )
            reverse = correlations[column_name][row_name]
            if not math.isclose(correlation, reverse, abs_tol=1e-12):
                raise ValueError(
                    f"correlation table is not symmetric for {row_name} and {column_name}"
                )


def build_covariance_matrix(sleeves, correlations):
    names = list(sleeves)
    return {
        row_name: {
            column_name: (
                correlations[row_name][column_name]
                * sleeves[row_name]["volatility"]
                * sleeves[column_name]["volatility"]
            )
            for column_name in names
        }
        for row_name in names
    }


def benchmark_weights(sleeves):
    return {
        name: (
            0.40
            if name == "Investment-grade bond fund"
            else 0.60
            if name == "Global equity index fund"
            else 0.0
        )
        for name in sleeves
    }


def equal_weights(sleeves):
    weight = 1.0 / len(sleeves)
    return {name: weight for name in sleeves}


def inverse_volatility_weights(sleeves):
    inverse_volatilities = {
        name: 1.0 / values["volatility"] for name, values in sleeves.items()
    }
    total = sum(inverse_volatilities.values())
    return {name: value / total for name, value in inverse_volatilities.items()}


def portfolio_expected_return(weights, sleeves):
    return sum(weights[name] * sleeves[name]["expected_return"] for name in sleeves)


def portfolio_volatility(weights, covariance_matrix):
    variance = sum(
        weights[row_name]
        * weights[column_name]
        * covariance_matrix[row_name][column_name]
        for row_name in weights
        for column_name in weights
    )
    return math.sqrt(max(0.0, variance))


def reserve_eligible_weight(weights, reserve_eligible):
    return sum(weights[name] for name in reserve_eligible)


def meets_objective(expected_return, objective_return):
    return expected_return >= objective_return


def build_portfolios(sleeves):
    return {
        "Benchmark": benchmark_weights(sleeves),
        "Equal weight": equal_weights(sleeves),
        "Inverse volatility": inverse_volatility_weights(sleeves),
    }


def print_portfolio(
    name, weights, sleeves, covariance_matrix, objective_return, reserve_eligible
):
    expected_return = portfolio_expected_return(weights, sleeves)
    volatility = portfolio_volatility(weights, covariance_matrix)
    reserve_weight = reserve_eligible_weight(weights, reserve_eligible)

    print(f"\n{name}")
    for sleeve_name, weight in weights.items():
        print(f"  {sleeve_name}: {weight:.1%}")
    print(f"  Expected return: {expected_return:.2%}")
    print(f"  Volatility: {volatility:.2%}")
    print(f"  Reserve-eligible weight: {reserve_weight:.2%}")
    print(
        "  Meets objective: "
        + ("yes" if meets_objective(expected_return, objective_return) else "no")
    )


def main():
    try:
        validate_inputs(SLEEVES, CORRELATIONS)
        covariance_matrix = build_covariance_matrix(SLEEVES, CORRELATIONS)
        portfolios = build_portfolios(SLEEVES)
        print(f"Objective return: {OBJECTIVE_RETURN:.2%}")
        for name, weights in portfolios.items():
            print_portfolio(
                name,
                weights,
                SLEEVES,
                covariance_matrix,
                OBJECTIVE_RETURN,
                RESERVE_ELIGIBLE,
            )
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
