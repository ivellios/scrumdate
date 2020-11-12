from pivotal.managers import UpdatesManager

if __name__ == '__main__':
    token = ""  # set your pivotal API access token
    project_id = ""  # set your project id
    initials = ""  # put your initials here - you can check them on pivotl by clicking on them in oyur story

    manager = UpdatesManager(token, project_id)
    print(manager.pull_daily_stories(initials))
