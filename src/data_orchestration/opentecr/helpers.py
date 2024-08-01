def transform_compound_name(name: str) -> str:
    """Transform the compound name."""
    # Remove the phase suffix.
    result = (
        name
        .strip()
        .removesuffix("(g)")  # gas phase
        .removesuffix("(aq)")  # aqueous phase
        .removesuffix("(l)")  # liquid phase
        .removesuffix("(1)")  # Someone made a typo of `1` instead of `l`.
        .removesuffix("(sln)")  # solid lipid nano particle or rather solution?
        .removesuffix("(ox)")  # oxidized
        .removesuffix("(red)")  # reduced
        .removesuffix("(reduced)")
    )

    # Replace with unicode characters.
    return (
        result
        .replace(r"{\alpha}", "α")
        .replace(r"{\beta}", "β")
        .replace(r"{\gamma}", "γ")
        .replace(r"{\Delta}", "Δ")
        .replace(r"{\omega}", "ω")  # 'o' == chr(111)
        .replace(r"{\οmega}", "ω")  # 'ο' == chr(959)
        .replace(r"{\pm}", "±")
        .strip()
    )
