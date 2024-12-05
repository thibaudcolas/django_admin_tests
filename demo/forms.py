from django import forms


class ExampleForm(forms.Form):
    """Demonstration of all Django form fields / widgets"""

    boolean_required = forms.BooleanField(help_text="boolean required field’s help text")
    boolean_optional = forms.BooleanField(help_text="boolean optional field’s help text", required=False)
    boolean_disabled = forms.BooleanField(help_text="boolean disabled field’s help text", disabled=True)

    char_required = forms.CharField(help_text="char required field’s help text", required=True)
    char_optional = forms.CharField(help_text="char optional field’s help text", required=False)
    char_disabled = forms.CharField(help_text="char disabled field’s help text", disabled=True)

    password_required = forms.CharField(
        help_text="field’s help text", required=True, widget=forms.PasswordInput()
    )
    password_optional = forms.CharField(
        help_text="field’s help text", required=False, widget=forms.PasswordInput()
    )
    password_disabled = forms.CharField(
        help_text="field’s help text", disabled=True, widget=forms.PasswordInput()
    )

    char_hidden = forms.CharField(widget=forms.HiddenInput())

    multiline_required = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 40}),
        help_text="field’s help text",
        required=True,
    )
    multiline_optional = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 40}),
        help_text="field’s help text",
        required=False,
    )
    multiline_disabled = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 40}),
        help_text="field’s help text",
        required=False,
    )

    choices = (("one", "One"), ("two", "Two"), ("three", "Three"), ("four", "Four"))

    choice_required = forms.ChoiceField(
        help_text="field’s help text", choices=choices, required=True
    )
    choice_optional = forms.ChoiceField(
        help_text="field’s help text", choices=choices, required=False
    )
    choice_disabled = forms.ChoiceField(
        help_text="field’s help text", choices=choices, disabled=True
    )

    radio_choice_required = forms.ChoiceField(
        help_text="field’s help text", choices=choices, required=True, widget=forms.RadioSelect()
    )
    radio_choice_optional = forms.ChoiceField(
        help_text="field’s help text", choices=choices, required=False, widget=forms.RadioSelect()
    )
    radio_choice_disabled = forms.ChoiceField(
        help_text="field’s help text", choices=choices, disabled=True, widget=forms.RadioSelect()
    )

    date_required = forms.DateField(help_text="date required field’s help text", required=True)
    date_optional = forms.DateField(help_text="date optional field’s help text", required=False)
    date_disabled = forms.DateField(help_text="date disabled field’s help text", disabled=True)

    datetime_required = forms.DateTimeField(help_text="datetime required field’s help text", required=True)
    datetime_optional = forms.DateTimeField(help_text="datetime optional field’s help text", required=False)
    datetime_disabled = forms.DateTimeField(help_text="datetime disabled field’s help text", disabled=True)

    decimal_required = forms.DecimalField(help_text="decimal required field’s help text", required=True)
    decimal_optional = forms.DecimalField(help_text="decimal optional field’s help text", required=False)
    decimal_disabled = forms.DecimalField(help_text="decimal disabled field’s help text", disabled=True)

    duration_required = forms.DurationField(help_text="duration required field’s help text", required=True)
    duration_optional = forms.DurationField(help_text="duration optional field’s help text", required=False)
    duration_disabled = forms.DurationField(help_text="duration disabled field’s help text", disabled=True)

    email_required = forms.EmailField(help_text="email required field’s help text", required=True)
    email_optional = forms.EmailField(help_text="email optional field’s help text", required=False)
    email_disabled = forms.EmailField(help_text="email disabled field’s help text", disabled=True)

    file_required = forms.FileField(help_text="file required field’s help text", required=True)
    file_optional = forms.FileField(help_text="file optional field’s help text", required=False)
    file_disabled = forms.FileField(help_text="file disabled field’s help text", disabled=True)

    # FilePathField

    float_required = forms.FloatField(help_text="float required field’s help text", required=True)
    float_optional = forms.FloatField(help_text="float optional field’s help text", required=False)
    float_disabled = forms.FloatField(help_text="float disabled field’s help text", disabled=True)

    image_required = forms.ImageField(help_text="image required field’s help text", required=True)
    image_optional = forms.ImageField(help_text="image optional field’s help text", required=False)
    image_disabled = forms.ImageField(help_text="image disabled field’s help text", disabled=True)

    integer_required = forms.IntegerField(help_text="integer required field’s help text", required=True)
    integer_optional = forms.IntegerField(help_text="integer optional field’s help text", required=False)
    integer_disabled = forms.IntegerField(help_text="integer disabled field’s help text", disabled=True)

    json_required = forms.JSONField(label="JSON required", help_text="json required field’s help text", required=True)
    json_optional = forms.JSONField(label="JSON optional", help_text="json optional field’s help text", required=False)
    json_disabled = forms.JSONField(label="JSON disabled", help_text="json disabled field’s help text", disabled=True)

    generic_ip_address_required = forms.GenericIPAddressField(help_text="generic ip address required field’s help text", required=True)
    generic_ip_address_optional = forms.GenericIPAddressField(help_text="generic ip address optional field’s help text", required=False)
    generic_ip_address_disabled = forms.GenericIPAddressField(help_text="generic ip address disabled field’s help text", disabled=True)

    select_multiple = forms.MultipleChoiceField(choices=choices)
    checkboxes_multiple = forms.MultipleChoiceField(
        choices=choices, widget=forms.CheckboxSelectMultiple()
    )

    # TypedMultipleChoiceField

    null_boolean_required = forms.NullBooleanField(help_text="null boolean required field’s help text")
    null_boolean_optional = forms.NullBooleanField(help_text="null boolean optional field’s help text", required=False)
    null_boolean_disabled = forms.NullBooleanField(help_text="null boolean disabled field’s help text", disabled=True)

    # SlugField

    regex_required = forms.RegexField(regex="\\w", help_text="regex required field’s help text", required=True)
    regex_optional = forms.RegexField(regex="\\w", help_text="regex optional field’s help text", required=False)
    regex_disabled = forms.RegexField(regex="\\w", help_text="regex disabled field’s help text", disabled=True)

    slug_required = forms.SlugField(help_text="slug required field’s help text", required=True)
    slug_optional = forms.SlugField(help_text="slug optional field’s help text", required=False)
    slug_disabled = forms.SlugField(help_text="slug disabled field’s help text", disabled=True)

    time_required = forms.TimeField(help_text="time required field’s help text", required=True)
    time_optional = forms.TimeField(help_text="time optional field’s help text", required=False)
    time_disabled = forms.TimeField(help_text="time disabled field’s help text", disabled=True)

    url_required = forms.URLField(label="URL required", help_text="url required field’s help text", required=True)
    url_optional = forms.URLField(label="URL optional", help_text="url optional field’s help text", required=False)
    url_disabled = forms.URLField(label="URL disabled", help_text="url disabled field’s help text", disabled=True)

    uuid_required = forms.UUIDField(label="UUID required", help_text="uuid required field’s help text", required=True)
    uuid_optional = forms.UUIDField(label="UUID optional", help_text="uuid optional field’s help text", required=False)
    uuid_disabled = forms.UUIDField(label="UUID disabled", help_text="uuid disabled field’s help text", disabled=True)

    combo_required = forms.ComboField(fields=[forms.CharField(max_length=20), forms.EmailField()], help_text="combo required field’s help text", required=True)
    combo_optional = forms.ComboField(fields=[forms.CharField(max_length=20), forms.EmailField()], help_text="combo optional field’s help text", required=False)
    combo_disabled = forms.ComboField(fields=[forms.CharField(max_length=20), forms.EmailField()], help_text="combo disabled field’s help text", disabled=True)

    # ComboField
    # MultiValueField
    # SplitDateTimeField
    # ModelChoiceField
    # ModelMultipleChoiceField

