def get_request_data(request):
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()
