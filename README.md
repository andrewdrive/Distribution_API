# test_sending_messages

testTaskProj

## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/andrewdrive/test_sending_messages.git
git branch -M main
git push -uf origin main
```

## Test and Deploy
1) docker-compose up --build
2) Для входа в админ панель Django зайти в контейнер api:
    - docker-compose exec api bash
    - python manage.py createsuperuser
3) Документация Open-Api: http://127.0.0.1:8001/swagger/

Реализованные дополнительные задания:
1) 3. docker-compose для запуска всех сервисов одной командой
2) 5. описание разработанного API



## Installation

