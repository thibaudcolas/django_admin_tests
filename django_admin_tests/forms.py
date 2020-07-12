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

    # DecimalField
    # DurationField

    email_required = forms.EmailField(help_text="Help", required=True)
    email_optional = forms.EmailField(help_text="Help", required=False)
    email_disabled = forms.EmailField(help_text="Help", disabled=True)

    file_required = forms.FileField(help_text="Help", required=True)
    file_optional = forms.FileField(help_text="Help", required=False)
    file_disabled = forms.FileField(help_text="Help", disabled=True)

    # FilePathField
    # FloatField
    # ImageField

    integer_required = forms.IntegerField(help_text="Help", required=True)
    integer_optional = forms.IntegerField(help_text="Help", required=False)
    integer_disabled = forms.IntegerField(help_text="Help", disabled=True)

    # GenericIPAddressField

    select_multiple = forms.MultipleChoiceField(choices=choices)
    checboxes_multiple = forms.MultipleChoiceField(
        choices=choices, widget=forms.CheckboxSelectMultiple()
    )

    null_boolean_required = forms.NullBooleanField(help_text="Help")
    null_boolean_optional = forms.NullBooleanField(help_text="Help", required=False)
    null_boolean_disabled = forms.NullBooleanField(help_text="Help", disabled=True)

    # RegexField
    # SlugField

    time_required = forms.TimeField(help_text="Help", required=True)
    time_optional = forms.TimeField(help_text="Help", required=False)
    time_disabled = forms.TimeField(help_text="Help", disabled=True)

    url_required = forms.URLField(label="URL", help_text="Help", required=True)
    url_optional = forms.URLField(label="URL", help_text="Help", required=False)
    url_disabled = forms.URLField(label="URL", help_text="Help", disabled=True)

    # UUIDField
    # ComboField
    # MultiValueField
    # SplitDateTimeField
    # ModelChoiceField
    # ModelMultipleChoiceField

