from django import forms


class ExampleForm(forms.Form):
    """Demonstration of all Django form fields / widgets"""

    boolean_required = forms.BooleanField(help_text="Help")
    boolean_optional = forms.BooleanField(help_text="Help", required=False)
    boolean_disabled = forms.BooleanField(help_text="Help", disabled=True)

    char_required = forms.CharField(help_text="Help", required=True)
    char_optional = forms.CharField(help_text="Help", required=False)
    char_disabled = forms.CharField(help_text="Help", disabled=True)

    password_required = forms.CharField(
        help_text="Help", required=True, widget=forms.PasswordInput()
    )
    password_optional = forms.CharField(
        help_text="Help", required=False, widget=forms.PasswordInput()
    )
    password_disabled = forms.CharField(
        help_text="Help", disabled=True, widget=forms.PasswordInput()
    )

    char_hidden = forms.CharField(widget=forms.HiddenInput())

    multiline_required = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 40}),
        help_text="Help",
        required=True,
    )
    multiline_optional = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 40}),
        help_text="Help",
        required=False,
    )
    multiline_disabled = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 40}),
        help_text="Help",
        required=False,
    )

    choices = (("one", "One"), ("two", "Two"), ("three", "Three"), ("four", "Four"))

    choice_required = forms.ChoiceField(
        help_text="Help", choices=choices, required=True
    )
    choice_optional = forms.ChoiceField(
        help_text="Help", choices=choices, required=False
    )
    choice_disabled = forms.ChoiceField(
        help_text="Help", choices=choices, disabled=True
    )

    radio_choice_required = forms.ChoiceField(
        help_text="Help", choices=choices, required=True, widget=forms.RadioSelect()
    )
    radio_choice_optional = forms.ChoiceField(
        help_text="Help", choices=choices, required=False, widget=forms.RadioSelect()
    )
    radio_choice_disabled = forms.ChoiceField(
        help_text="Help", choices=choices, disabled=True, widget=forms.RadioSelect()
    )

    date_required = forms.DateField(help_text="Help", required=True)
    date_optional = forms.DateField(help_text="Help", required=False)
    date_disabled = forms.DateField(help_text="Help", disabled=True)

    datetime_required = forms.DateTimeField(help_text="Help", required=True)
    datetime_optional = forms.DateTimeField(help_text="Help", required=False)
    datetime_disabled = forms.DateTimeField(help_text="Help", disabled=True)

    decimal_required = forms.DecimalField(help_text="Help", required=True)
    decimal_optional = forms.DecimalField(help_text="Help", required=False)
    decimal_disabled = forms.DecimalField(help_text="Help", disabled=True)

    duration_required = forms.DurationField(help_text="Help", required=True)
    duration_optional = forms.DurationField(help_text="Help", required=False)
    duration_disabled = forms.DurationField(help_text="Help", disabled=True)

    email_required = forms.EmailField(help_text="Help", required=True)
    email_optional = forms.EmailField(help_text="Help", required=False)
    email_disabled = forms.EmailField(help_text="Help", disabled=True)

    file_required = forms.FileField(help_text="Help", required=True)
    file_optional = forms.FileField(help_text="Help", required=False)
    file_disabled = forms.FileField(help_text="Help", disabled=True)

    # FilePathField

    float_required = forms.FloatField(help_text="Help", required=True)
    float_optional = forms.FloatField(help_text="Help", required=False)
    float_disabled = forms.FloatField(help_text="Help", disabled=True)

    image_required = forms.ImageField(help_text="Help", required=True)
    image_optional = forms.ImageField(help_text="Help", required=False)
    image_disabled = forms.ImageField(help_text="Help", disabled=True)

    integer_required = forms.IntegerField(help_text="Help", required=True)
    integer_optional = forms.IntegerField(help_text="Help", required=False)
    integer_disabled = forms.IntegerField(help_text="Help", disabled=True)

    json_required = forms.JSONField(label="JSON required", help_text="Help", required=True)
    json_optional = forms.JSONField(label="JSON optional", help_text="Help", required=False)
    json_disabled = forms.JSONField(label="JSON disabled", help_text="Help", disabled=True)

    generic_ip_address_required = forms.GenericIPAddressField(help_text="Help", required=True)
    generic_ip_address_optional = forms.GenericIPAddressField(help_text="Help", required=False)
    generic_ip_address_disabled = forms.GenericIPAddressField(help_text="Help", disabled=True)

    select_multiple = forms.MultipleChoiceField(choices=choices)
    checkboxes_multiple = forms.MultipleChoiceField(
        choices=choices, widget=forms.CheckboxSelectMultiple()
    )

    # TypedMultipleChoiceField

    null_boolean_required = forms.NullBooleanField(help_text="Help")
    null_boolean_optional = forms.NullBooleanField(help_text="Help", required=False)
    null_boolean_disabled = forms.NullBooleanField(help_text="Help", disabled=True)

    # SlugField

    regex_required = forms.RegexField(regex="\w", help_text="Help", required=True)
    regex_optional = forms.RegexField(regex="\w", help_text="Help", required=False)
    regex_disabled = forms.RegexField(regex="\w", help_text="Help", disabled=True)

    slug_required = forms.SlugField(help_text="Help", required=True)
    slug_optional = forms.SlugField(help_text="Help", required=False)
    slug_disabled = forms.SlugField(help_text="Help", disabled=True)

    time_required = forms.TimeField(help_text="Help", required=True)
    time_optional = forms.TimeField(help_text="Help", required=False)
    time_disabled = forms.TimeField(help_text="Help", disabled=True)

    url_required = forms.URLField(label="URL required", help_text="Help", required=True)
    url_optional = forms.URLField(label="URL optional", help_text="Help", required=False)
    url_disabled = forms.URLField(label="URL disabled", help_text="Help", disabled=True)

    uuid_required = forms.UUIDField(label="UUID required", help_text="Help", required=True)
    uuid_optional = forms.UUIDField(label="UUID optional", help_text="Help", required=False)
    uuid_disabled = forms.UUIDField(label="UUID disabled", help_text="Help", disabled=True)

    combo_required = forms.ComboField(fields=[forms.CharField(max_length=20), forms.EmailField()], help_text="Help", required=True)
    combo_optional = forms.ComboField(fields=[forms.CharField(max_length=20), forms.EmailField()], help_text="Help", required=False)
    combo_disabled = forms.ComboField(fields=[forms.CharField(max_length=20), forms.EmailField()], help_text="Help", disabled=True)

    # ComboField
    # MultiValueField
    # SplitDateTimeField
    # ModelChoiceField
    # ModelMultipleChoiceField

