def select_activities(tasks):
    if not tasks:
        return []

    ordered_tasks = sorted(tasks, key=lambda task: task["end"])
    selected = []
    last_end = None

    for task in ordered_tasks:
        if last_end is None or task["start"] >= last_end:
            selected.append(task)
            last_end = task["end"]

    return selected
