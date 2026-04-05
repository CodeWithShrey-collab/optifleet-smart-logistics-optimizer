def fractional_knapsack(capacity, items):
    if capacity <= 0 or not items:
        return [], 0

    normalized_items = []
    for item in items:
        weight = float(item["weight"])
        value = float(item["value"])
        ratio = value / weight if weight > 0 else 0
        normalized_items.append({**item, "weight": weight, "value": value, "ratio": ratio})

    normalized_items.sort(key=lambda entry: (entry["ratio"], entry.get("priority", 0)), reverse=True)

    selected_items = []
    total_value = 0.0
    remaining_capacity = float(capacity)

    for item in normalized_items:
        if remaining_capacity <= 0:
            break

        take_weight = min(item["weight"], remaining_capacity)
        if take_weight <= 0:
            continue

        fraction = round(take_weight / item["weight"], 4)
        earned_value = round(item["value"] * fraction, 2)
        selected_items.append(
            {
                "id": item["id"],
                "package_name": item["package_name"],
                "customer_name": item["customer_name"],
                "destination": item["destination"],
                "selected_weight": round(take_weight, 2),
                "original_weight": item["weight"],
                "fraction": fraction,
                "value_gained": earned_value,
            }
        )
        total_value += earned_value
        remaining_capacity -= take_weight

    return selected_items, round(total_value, 2)
