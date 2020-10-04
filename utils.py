def format_time(dt):
    units = {"ns": 1e-9, "µs": 1e-6, "ms": 1e-3, "s": 1.0}
    for name, u in units.items():
        if dt/u < 1000:
            return f"{dt/u} {name}"
    return f"{dt} sec"