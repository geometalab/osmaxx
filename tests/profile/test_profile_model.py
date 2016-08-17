def test_key_is_always_the_same(valid_profile, unverified_email):
    activation_key = valid_profile.activation_key()
    valid_profile.unverified_email = unverified_email
    valid_profile.save(force_update=True)
    valid_profile.refresh_from_db()
    assert activation_key == valid_profile.activation_key()


def test_key_changes_when_email_changes(valid_profile):
    activation_key = valid_profile.activation_key()
    valid_profile.unverified_email = 'other@example.com'
    valid_profile.save()
    assert activation_key != valid_profile.activation_key()


def test_key_validation_returns_expected_values(valid_profile):
    activation_key = valid_profile.activation_key()
    unsigned_value = valid_profile.validate_key(activation_key)
    assert unsigned_value['username'] == valid_profile.associated_user.username
    assert unsigned_value['email'] == valid_profile.unverified_email


def test_key_validation_returns_none_when_tampered_with_signature(valid_profile):
    activation_key = valid_profile.activation_key() + 'm'
    assert valid_profile.validate_key(activation_key) is None
