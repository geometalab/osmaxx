from social.pipeline.user import create_user


def create_inactive_user(*args, **kwargs):
    result_dict = create_user(*args, **kwargs)

    if result_dict['is_new']:
        user = result_dict['user']
        user.is_active = False
        user.save()
    return result_dict
