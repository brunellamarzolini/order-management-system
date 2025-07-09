class ModelDiffMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_state = None
        if self.pk:  # The item already exists in the database
            check_fields = self._meta.fields
            diff_fields = getattr(self, "diff_fields", None)
            if diff_fields:
                check_fields = [f for f in check_fields if f.name in diff_fields]
            self._original_state = {f.name: getattr(self, f.name) for f in check_fields}

    def get_changed_fields(self):
        if self._original_state is None:
            return []  # is a new object, no changes to track

        changed_fields = []
        for field, original_value in self._original_state.items():
            if original_value != getattr(self, field):
                changed_fields.append(field)
        return changed_fields